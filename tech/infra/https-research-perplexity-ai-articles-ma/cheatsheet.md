---
date: 2026-07-20
tags: [tech]
type: tech-tool-study
status: draft
---

# SPACE Cheatsheet

> [[05-projects|이전: Projects]] · [[README|목차]]

## 한눈에 보기

```text
SPACE = strong isolation
      + explicit lifecycle
      + disk/full snapshots
      + credential mediation
      + CoW/warm-pool efficiency
```

| 구분 | 핵심 |
|---|---|
| Workload | isolated, stateful, singleton, mostly idle agent session |
| Isolation | per-sandbox VM + host process isolation |
| Control | stateless control plane + shared DB + desired/observed reconciliation |
| Node | unprivileged sandbox manager + single privileged node manager |
| Guest channel | private channel + `space` daemon |
| Network | forced egress gateway |
| Secret | guest 밖 credential store, network/browser 시점 injection |
| Storage | btrfs CoW, reflink, atomic filesystem snapshot, delta |
| Performance | matching template warm pool + concurrent image download coalescing |

## Lifecycle

```text
create -> running <-> pause/resume
             |
             +-> suspend -> durable/restorable -> restore -> running
             |
             +-> stop
```

- **pause**: live execution을 멈추되 빠른 재개용 state 유지
- **suspend**: full snapshot을 durable object storage에 올려 node resource/state 의존성 해제
- **restore**: 다른 node도 artifact로 runtime 재구성 가능
- **stop**: session 종료; 구체 retention/delete semantics는 구현별 확인

## Snapshot 선택

| 필요 | 선택 |
|---|---|
| 파일 rollback만 필요 | Disk snapshot |
| process/memory 이어서 실행 | Full snapshot |
| node failure는 고려하지 않음 | Node-local snapshot 가능 |
| cross-node/zone recovery | Durable object storage upload 필요 |
| 여러 branch 생성 | Snapshot에서 one-to-many fork semantics 확인 |

```text
Never mark RESTORABLE
until every artifact is uploaded and verified.
```

## 핵심 Invariant

- operation retry는 idempotent하다.
- sandbox identity당 active VM은 최대 하나다.
- stale generation/node report는 현재 placement를 덮지 않는다.
- incomplete/corrupt snapshot은 restore 대상이 아니다.
- raw long-lived credential은 guest env/file/`/proc`에 없다.
- 모든 egress path는 policy gateway를 통과한다.
- restore 후 external connection, token, lock, side effect를 재검증한다.

## Threat Model Quick Check

- [ ] guest code와 tool output을 untrusted로 보는가?
- [ ] cross-tenant kernel boundary가 있는가?
- [ ] guest-host 통신 channel이 allowlist인가?
- [ ] egress가 DNS/redirect/private IP 우회를 막는가?
- [ ] credential에 scope, expiry, rate limit, audit가 있는가?
- [ ] snapshot이 encrypted/integrity-checked 되는가?
- [ ] customer key revoke가 모든 stored artifact에 적용되는가?
- [ ] sandbox 내부 피해와 외부 side effect도 별도 제한하는가?

## Benchmark Quick Check

```yaml
report:
  paths: [warm-create, cold-create, local-restore, cross-node-restore]
  percentiles: [p50, p90, p99]
  disclose:
    - region
    - VM_size
    - template_size
    - warm_hit_ratio
    - memory_dirty_ratio
    - filesystem_delta
    - concurrency
```

Perplexity 공개 결과:

| Metric | Previous | SPACE | Claimed improvement |
|---|---:|---:|---:|
| create p50 | 185 ms | 60 ms | 3.1× |
| create p90 | 447 ms | 89 ms | 5.0× |

> Vendor 내부 production 측정값이며 외부 provider와 직접 비교할 독립 benchmark가 아니다.

## Category 구분

```text
Workflow runtime (Temporal/LangGraph)
  = logical state, event, retry, approval

Sandbox runtime (SPACE/E2B/Daytona)
  = code, files, process, memory, isolation

Isolation primitive (VM/gVisor/Kata)
  = kernel/hypervisor security boundary
```

## 공개 정보의 한계

SPACE 원문만으로 알 수 없는 것:

- hypervisor, attestation, guest image signing
- vulnerability response와 patch cadence
- egress policy의 정확한 표현력
- snapshot encryption/integrity/deletion 세부
- public API, pricing, self-hosting

## Sources

- https://research.perplexity.ai/articles/making-space-secure-and-efficient-runtimes-for-long-running-agents
- https://kubernetes.io/blog/2026/03/20/running-agents-on-kubernetes-with-agent-sandbox/
- https://e2b.dev/docs/sandbox/persistence
- https://www.daytona.io/docs/en/sandboxes/
