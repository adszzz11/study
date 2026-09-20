---
date: 2026-07-20
tags: [tech]
type: tech-tool-study
status: draft
---

# SPACE Overview

> [[README|목차]] · [[02-ecosystem|다음: Ecosystem]]

## What

SPACE는 long-running agent가 사용하는 execution environment의 control plane, node runtime, isolated VM을 함께 설계한 Perplexity의 sandbox platform이다. 각 sandbox에는 독립 guest kernel과 writable btrfs CoW filesystem이 있고, guest 내부의 `space` daemon이 process, filesystem operation, readiness와 activity/idle state를 중개한다.

```text
Client / Agent Orchestrator
          │
          ▼
┌────────────────────────────────────────┐
│ Stateless Control Plane                │
│ API gateway · AuthN/AuthZ · scheduler  │
│ desired state · shared database        │
└──────────────────┬─────────────────────┘
                   │ reconcile / idempotent operation
                   ▼
┌────────────────────────────────────────┐
│ Node-local Services                    │
│ unprivileged sandbox manager           │
│ root node manager · volume · gateway   │
└──────────────────┬─────────────────────┘
                   │ private in-VM channel
                   ▼
┌────────────────────────────────────────┐
│ Per-sandbox VM                         │
│ guest kernel · workload · space daemon │
│ writable btrfs CoW filesystem          │
└────────────────────────────────────────┘
```

## Why

Agent workload는 일반 web service나 one-shot job과 다르다.

| 요구사항 | 문제 | SPACE의 답 |
|---|---|---|
| Security | generated code와 tool output은 untrusted이며 prompt injection이 shell과 network로 이어질 수 있다. | per-sandbox VM, host process isolation, forced egress, 외부 credential store |
| Functionality | 작업 중 files/process/memory가 쌓이고 승인 대기, 실패 복구, 분기가 필요하다. | explicit lifecycle와 disk/full snapshot |
| Efficiency | session은 오래 존재하지만 대부분 idle이다. | pause/suspend, warm pool, btrfs reflink/delta |

일반 container는 host kernel을 공유한다. namespace, cgroup, seccomp는 중요한 경계지만 multi-tenant hostile workload에서 host kernel exploit의 blast radius를 없애지는 못한다. 반대로 VM만 붙인다고 lifecycle, credential mediation, durable recovery가 자동으로 생기지는 않는다. SPACE의 핵심은 이 기능을 **통합된 stateful compute substrate**로 만든 데 있다.

## 3계층과 책임

### Control plane

- request를 authenticate/authorize한 뒤 **desired state**를 shared database에 기록한다.
- observed state와 desired state를 계속 reconcile한다.
- operation을 idempotent하게 만들어 crash, retry, partial failure를 흡수한다.
- sandbox placement와 durable backup 여부 같은 cluster-level metadata를 관리한다.

### Node-local services

- template 준비, VM 시작, network wiring, local snapshot을 담당한다.
- sandbox manager는 unprivileged로 실행한다.
- privileged operation은 하나의 root node manager로 좁혀 broker한다.
- credential manager와 network gateway가 guest의 외부 접근을 통제한다.

### Sandbox VM

- workload마다 독립 guest kernel을 할당한다.
- `space` daemon만 trusted platform과 guest 사이의 sanctioned channel로 둔다.
- guest는 자유롭게 code와 package를 실행하되 platform boundary는 직접 다루지 못한다.

## Defense in Depth

```text
untrusted workload
  └─ guest process boundary
      └─ guest kernel / VM boundary
          └─ host process isolation
              └─ private control channel
                  └─ forced egress gateway
                      └─ external credential store / KMS
```

- **이중 격리**: cross-sandbox 접근에는 VM과 host-level process isolation을 모두 넘어야 한다.
- **Controlled channel**: guest-host interaction을 private channel과 `space` daemon에 제한한다.
- **Forced egress**: outbound traffic을 중앙 gateway로 보내 domain/service policy를 적용한다.
- **Credential outside sandbox**: secret을 environment variable이나 file로 guest에 두지 않고 network layer 또는 browser autofill 시점에 주입한다.
- **BYOK**: externally stored data용 key는 customer KMS에서 가져오며 sandbox에 넣지 않는다. revoke 시 data를 읽을 수 없게 한다.

> [!important] Sandbox는 agent를 안전하게 만들지 않는다
> sandbox 안의 data 파괴, 허용된 endpoint를 통한 오용, 과도한 비용, 잘못된 사용자 승인까지 막아 주지는 않는다. least privilege, policy, audit, budget, application-level validation이 별도로 필요하다.

## Stateful Lifecycle

```text
create -> running <-> pause
             │          │
             │          └─ CPU 해제, node-local state 유지
             ▼
          suspend -> restorable -> restore -> running
             │
             └─ full snapshot을 object storage에 완전히 올린 뒤 전환

running/paused/suspended -> stop
```

공개 글은 `create`, `running`, `pause`, `resume`, `suspend`, `restore`, `stop` 중심의 state machine을 설명한다. transition을 명시하면 retry 가능한 command와 실제 state를 분리할 수 있다.

주요 use case:

- human approval 대기 중 pause/suspend
- 위험한 명령 전 disk checkpoint와 rollback
- 같은 checkpoint에서 여러 branch를 만드는 fork
- node failure 후 다른 node에서 recovery
- 오래 idle인 session의 durable suspend/resume

## 이중 Snapshot

| Snapshot | 포함 상태 | 생성 특성 | 주요 용도 |
|---|---|---|---|
| Disk snapshot | filesystem point-in-time state | 자주, node-local, VM pause 불필요 | destructive change rollback, 파일 복구 |
| Full snapshot | paused VM의 memory/process/filesystem checkpoint | 상대적으로 드물고 무거움 | crash recovery, suspend/resume, migration |

Suspend의 commit protocol은 중요하다.

```text
pause VM
  -> create full snapshot
  -> upload every artifact to object storage
  -> verify completion
  -> mark DB record as restorable
```

DB를 먼저 `restorable`로 바꾸면 partial upload를 정상 checkpoint로 오인할 수 있다. SPACE는 모든 artifact가 도착한 뒤에만 상태를 전환한다. Restore에서는 scheduler가 새 node를 선택하고 base template과 filesystem delta를 받은 뒤 captured VM state를 재구성한다.

## btrfs와 Warm Pool

- **Reflink clone**: data extent를 공유하고 metadata만 복제한다.
- **Atomic snapshot**: 새 filesystem root를 만들어 빠른 point-in-time snapshot을 얻는다.
- **Delta storage**: base image 전체가 아니라 changed block만 저장한다.
- **Rolling disk checkpoint**: VM을 멈추지 않고 filesystem snapshot을 만든다.
- **Warm pool**: common template이 materialize된 pod에 sandbox를 bind한다.
- **Request coalescing**: 동일 image의 concurrent download를 하나로 합친다.

## 공개 성능과 해석

Perplexity가 이전 provider와 같은 production traffic에서 측정했다고 밝힌 결과다.

| 지표 | 기존 | SPACE | 개선 |
|---|---:|---:|---:|
| Median create latency | 185 ms | 60 ms | 3.1× |
| p90 create latency | 447 ms | 89 ms | 5.0× |

이 수치는 warm pool과 btrfs reflink 설계의 production 효과를 보여 주는 내부 evidence다. 그러나 workload, region, VM size, cold/warm ratio, 이전 provider가 공개되지 않았으므로 외부 provider와 apples-to-apples benchmark로 사용하면 안 된다. 출시 주간의 수백만 sandbox creation, 수천만 reconnect 및 Computer session 100% 전환도 Perplexity가 공개한 자체 운영 수치다.

## 공개되지 않은 것

- hypervisor/microVM implementation과 hardware virtualization 세부
- attestation, measured boot, guest image signing
- patch cadence와 vulnerability response process
- egress policy language와 DNS rebinding/IP literal 처리
- snapshot encryption, integrity manifest, deletion/retention의 구체적 규칙
- public API, pricing, self-hosting 또는 open-source 계획

이 빈칸은 “구현되어 있지 않다”는 뜻이 아니라 **공개 글만으로 판단할 수 없다**는 뜻이다.

## Sources

- https://research.perplexity.ai/articles/making-space-secure-and-efficient-runtimes-for-long-running-agents
- https://kubernetes.io/blog/2026/03/20/running-agents-on-kubernetes-with-agent-sandbox/

