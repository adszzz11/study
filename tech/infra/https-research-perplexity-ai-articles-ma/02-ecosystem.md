---
date: 2026-07-20
tags: [tech]
type: tech-tool-study
status: draft
---

# SPACE Ecosystem

> [[01-overview|이전: Overview]] · [[README|목차]] · [[03-references|다음: References]]

## 먼저 계층을 구분한다

SPACE와 LangGraph/Temporal을 한 표에서 “경쟁 제품”으로만 비교하면 category error가 생긴다.

```text
Agent application / orchestrator
        │
        ├─ Durable workflow state: Temporal, LangGraph, Prefect
        │
        └─ Execution sandbox: SPACE, E2B, Daytona, Kubernetes Agent Sandbox
                     │
                     └─ Isolation primitive: VM/microVM, Kata, gVisor, container
```

- **Workflow runtime**은 step, event, retry, approval 같은 logical state를 보존한다.
- **Sandbox runtime**은 code가 실제로 실행되는 filesystem, process, memory와 security boundary를 제공한다.
- **Isolation primitive**는 sandbox runtime이 사용하는 kernel/hypervisor 경계다.

실전에서는 대안 관계보다 조합 관계인 경우가 많다. 예를 들어 Temporal workflow가 approval을 기다리고, 재개 후 E2B/Daytona 같은 sandbox에 command를 보내는 구조가 가능하다.

## Sandbox Platform 비교

| 대상 | 위치/격리 | Stateful 기능 | 강점 | 주의 |
|---|---|---|---|---|
| **SPACE** | per-sandbox VM + host process isolation | disk/full snapshot, pause/resume, suspend/restore, rollback/fork | credential을 guest 밖에서 중개하고 cross-node recovery까지 통합한 production architecture | Perplexity 내부 platform이며 public API/구현 세부가 공개되지 않음 |
| **E2B** | hosted secure cloud sandbox | filesystem+memory pause/resume, snapshot에서 one-to-many fork | 공개 SDK/API로 agent sandbox를 빠르게 도입 가능 | hosted service의 limits, pricing, network/credential model을 실제 요구사항과 검토해야 함 |
| **Daytona** | container 및 Linux/Windows VM sandbox | container는 filesystem snapshot, VM은 memory 포함 hot snapshot과 pause/resume | 여러 언어 SDK, container/VM class, snapshot lifecycle | sandbox class마다 보존 상태와 pause/archive 지원이 다름 |
| **Kubernetes Agent Sandbox** | Kubernetes CRD + 선택 runtime(gVisor/Kata 등) | scale-to-zero/resume, stable identity, warm pool extension | 기존 Kubernetes 운영 모델과 declarative API를 재사용 | 2026-07 기준 개발 중인 SIG Apps project; backend별 실제 isolation/state semantics 확인 필요 |
| **직접 구축** | VM/microVM + 자체 control plane | 요구에 맞춰 구현 | policy와 data plane을 완전히 통제 | snapshot correctness, scheduler, patching, KMS, egress, multi-tenancy의 운영 비용이 매우 큼 |

## Isolation Primitive 비교

| 방식 | Kernel 경계 | 장점 | 한계/적합성 |
|---|---|---|---|
| Linux container | host kernel 공유 | 빠른 시작, 높은 밀도, 성숙한 tooling | hostile multi-tenant code에서는 host kernel이 공통 공격면 |
| gVisor | per-sandbox userspace application kernel + host kernel | OCI/Kubernetes 통합, syscall interception으로 host kernel 노출 축소 | 완전한 VM과 semantics/performance가 다르며 workload compatibility 검증 필요 |
| Kata Containers/VM | workload별 guest kernel/hardware virtualization | 강한 kernel boundary와 container workflow의 결합 | VM resource overhead와 image/snapshot 운영 필요 |
| Firecracker류 microVM | 경량 VMM + guest kernel | 작은 device model, 빠른 microVM 지향 | VMM은 primitive일 뿐 lifecycle, credential mediation, durable state는 별도 구축 |
| SPACE의 공개 설계 | per-sandbox VM + host process isolation | 격리 경계를 state checkpoint boundary로도 활용 | 구체 hypervisor와 attestation model은 비공개 |

## Workflow Runtime과의 비교

| 질문 | SPACE / sandbox runtime | Temporal/LangGraph/Prefect류 |
|---|---|---|
| 무엇을 checkpoint하는가? | VM memory/process/filesystem 또는 disk | workflow variables, event history, graph state |
| untrusted code를 격리하는가? | 핵심 책임 | 일반적으로 별도 worker/sandbox 책임 |
| human-in-the-loop 대기 | compute pause/suspend | workflow wait/signal/interrupt |
| retry 단위 | lifecycle operation, process command, VM restore | activity/node/task |
| fork/rollback 의미 | machine state에서 branch/restore | logical workflow checkpoint에서 branch/replay |
| credential 처리 | egress/network/browser injection을 포함할 수 있음 | secret reference와 worker auth가 중심; guest 격리는 별도 |

두 계층을 함께 쓰면 logical durability와 compute durability를 분리할 수 있다.

```text
Temporal/LangGraph checkpoint
  task_id, approval event, next action, sandbox_id
                         │
                         ▼
Sandbox checkpoint
  files, processes, memory, network policy, template identity
```

## 선택 기준

| 상황 | 권장 출발점 |
|---|---|
| 몇 분짜리 disposable code execution | hosted sandbox 또는 hardened container부터 검토 |
| memory/process까지 이어지는 interactive session | VM pause/resume과 full snapshot을 지원하는 platform |
| Kubernetes가 표준 platform이고 CRD 운영 역량이 있음 | Kubernetes Agent Sandbox + isolation runtime 평가 |
| 승인·timer·business retry가 핵심이고 code는 trusted | durable workflow runtime 우선 |
| untrusted code와 장기 workflow가 모두 핵심 | workflow runtime + sandbox runtime 조합 |
| customer-managed KMS, egress, audit가 필수 | 제품별 실제 enterprise control을 검증하거나 자체 platform 설계 |

## Evaluation Checklist

- [ ] sandbox마다 독립 kernel boundary가 필요한 threat model인가?
- [ ] disk만 보존하면 되는가, memory/process까지 보존해야 하는가?
- [ ] snapshot은 one-to-one resume인가, one-to-many fork도 가능한가?
- [ ] node/zone failure 뒤 다른 node에서 restore되는가?
- [ ] secret이 guest의 env/file/`/proc`에 나타나는가?
- [ ] egress policy가 DNS, redirect, private IP, browser traffic에도 적용되는가?
- [ ] snapshot encryption, integrity, retention, deletion이 audit 가능한가?
- [ ] cold/warm create latency와 restore latency를 내 workload로 측정했는가?
- [ ] public benchmark의 workload/region/size/cold ratio가 비교 가능한가?
- [ ] workflow checkpoint와 machine checkpoint의 source of truth를 정했는가?

## Sources

- https://research.perplexity.ai/articles/making-space-secure-and-efficient-runtimes-for-long-running-agents
- https://kubernetes.io/blog/2026/03/20/running-agents-on-kubernetes-with-agent-sandbox/
- https://e2b.dev/docs/sandbox/persistence
- https://e2b.dev/docs/sandbox/snapshots
- https://www.daytona.io/docs/en/sandboxes/
- https://www.daytona.io/docs/en/snapshots/
- https://gvisor.dev/docs/architecture_guide/intro/
- https://firecracker-microvm.github.io/
- https://docs.temporal.io/

