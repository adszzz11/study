---
date: 2026-07-20
tags: [tech]
type: tech-tool-study
status: draft
---

# SPACE Deep Dive: Correctness, Security, Efficiency

> [[01-getting-started|이전: Getting Started]] · [[../README|목차]] · [[../05-projects|다음: Projects]]

## 1. Desired State Reconciliation

Control plane이 stateless하고 durable state를 shared DB에 둔다는 것은 모든 request를 즉시 성공시키는 것이 아니라 **의도를 기록하고 실제 상태를 수렴시키는 것**에 가깝다.

```pseudo
loop reconcile(sandbox_id):
    desired = db.get_desired_state(sandbox_id)
    observed = node.query_observed_state(sandbox_id)

    if desired == RUNNING and observed == ABSENT:
        ensure_template()
        ensure_vm_started()
    elif desired == RESTORABLE and observed == PAUSED_LOCAL:
        ensure_full_snapshot_uploaded()
        commit_restorable_if_complete()
    elif desired == STOPPED:
        ensure_runtime_removed()
```

### Correctness invariant

| 대상 | Invariant |
|---|---|
| identity | sandbox ID 하나에 active VM은 최대 하나 |
| generation | 이전 generation의 node report가 새 placement를 덮지 않음 |
| snapshot | manifest의 모든 artifact가 검증돼야 restorable |
| command | retry가 side effect를 중복 생성하지 않음 |
| credential | guest가 raw long-lived secret을 보유하지 않음 |

Split-brain을 피하려면 DB generation, node lease/fencing token, snapshot manifest를 함께 고려해야 한다. 원문은 reconcile과 idempotency를 설명하지만 구체 consensus/fencing 방식은 공개하지 않는다.

## 2. Disk Snapshot과 Full Snapshot의 Consistency

### Disk snapshot

btrfs snapshot은 filesystem root를 빠르게 고정하지만 다음 상태는 별개다.

- application userspace buffer
- database page cache와 WAL ordering
- memory-only queue
- 외부 API에 이미 보낸 side effect

따라서 rolling disk snapshot은 보통 **crash-consistent filesystem checkpoint**로 해석해야 한다. application-consistent checkpoint가 필요하면 freeze hook, `fsync`, database checkpoint 또는 agent-level barrier를 추가한다.

```text
Agent barrier
  -> stop new writes
  -> flush/fsync application state
  -> create disk snapshot
  -> record external side-effect cursor
  -> resume writes
```

### Full snapshot

paused VM의 memory/process를 포함해도 network connection의 상대 endpoint까지 과거로 돌아가지는 않는다. restore 후에는 다음을 재수립해야 한다.

- TCP/WebSocket/PTY connection
- expired token과 lease
- wall clock 기반 timer
- external lock와 queue visibility timeout
- already-committed API side effect

즉 full snapshot은 distributed system 전체의 time travel이 아니다.

## 3. Credential Mediation

SPACE의 중요한 아이디어는 secret을 guest에 넣지 않고 필요한 순간 platform boundary에서 중개하는 것이다.

```text
Guest request
  GET https://api.example.com/data
       │ no raw credential
       ▼
Egress gateway
  1. authenticate sandbox identity
  2. authorize service + method + scope
  3. fetch short-lived credential
  4. inject/sign request
  5. rate-limit and audit
       ▼
External service
```

### 정책 예시

```yaml
credential_policy:
  subject: sandbox:sbx-42
  service: api.example.com
  methods: [GET]
  path_prefixes: [/v1/read-only/]
  scope: dataset:customer-7
  expires_in: 5m
  rate_limit: 60/min
  deny_private_ip_redirects: true
  audit: required
```

### 남는 공격면

- 허용된 endpoint가 data exfiltration channel이 되는 confused deputy
- response/tool output이 다시 prompt injection을 전달
- browser DOM 또는 page script가 autofill value를 탈취
- DNS rebinding, redirect, IPv6/private range 우회
- audit log에 secret이나 sensitive payload가 남음

그래서 “secret이 guest 밖에 있다”와 “권한 오용이 불가능하다”는 같은 말이 아니다.

## 4. btrfs CoW의 비용 모델

Reflink는 initial clone을 싸게 만들지만 changed block은 결국 새 extent를 차지한다.

```text
base template extents: A B C D
sandbox 1:             A B C D + E1
sandbox 2:             A B C D + E2 E3
snapshot s2-1:         shared roots + changed metadata/extents
```

관찰할 metric:

- logical bytes vs exclusive/physical bytes
- snapshot depth와 metadata growth
- random overwrite workload의 CoW amplification
- deletion 뒤 delayed space reclamation
- template cache hit ratio
- request coalescing wait time
- full checkpoint upload bytes와 restore read bytes

Warm pool은 p50/p90 create latency를 줄이지만 인기 없는 template의 cold path와 pool memory/disk 비용을 숨길 수 있다. benchmark에는 반드시 template popularity와 warm-hit ratio를 포함한다.

## 5. Failure Injection Matrix

| Scenario | 주입 방법 | 성공 기준 |
|---|---|---|
| control-plane restart | transition 중 API/control process 종료 | 재시도 후 desired state 수렴, duplicate 없음 |
| node-manager crash | snapshot 도중 privileged broker 종료 | incomplete snapshot 비가시화, node reconcile |
| node loss | running/paused node 강제 단절 | RPO 내 durable checkpoint로 다른 node restore |
| object partial upload | N번째 artifact write 실패 | DB가 절대 restorable로 전환되지 않음 |
| stale node report | placement generation을 늦게 전달 | 새 VM/placement를 덮지 않음 |
| credential store outage | egress signing 시 timeout | fail closed, raw secret fallback 금지 |
| gateway bypass | direct IP/DNS/redirect 시도 | 모든 outbound path가 policy를 통과 |
| snapshot corruption | artifact byte 변경 | manifest/integrity check로 restore 차단 |

## 6. Benchmark Design

```yaml
benchmark_dimensions:
  path: [warm-create, cold-create, local-restore, cross-node-restore]
  template_size_gb: [0.5, 5, 20]
  memory_gb: [1, 4, 16]
  dirty_memory_ratio: [0.1, 0.5, 0.9]
  filesystem_delta_gb: [0, 1, 10]
  concurrency: [1, 100, 1000]
metrics:
  - p50_p90_p99_latency
  - reconnect_success_rate
  - bytes_read_written
  - node_cpu_memory_disk
  - orphan_artifact_count
```

Perplexity의 60 ms median/89 ms p90은 같은 production traffic에서 이전 provider보다 빨랐다는 first-party result다. 위 dimension이 공개되지 않았으므로 이 숫자를 capacity planning input으로 직접 사용하지 않는다.

## 7. Design Review 질문

- control plane DB가 unavailable일 때 running sandbox는 계속 동작하는가?
- node의 source of truth와 DB desired state가 충돌하면 누가 이기는가?
- fencing 없이 cross-node restore가 중복 VM을 만들 수 있는가?
- snapshot에 credential, browser cookie, decrypted customer data가 포함되는가?
- BYOK revoke가 cache, local snapshot, backup 모두에 언제 반영되는가?
- stop, suspend, delete의 storage/retention semantics가 각각 무엇인가?
- guest image CVE가 발견되면 기존 full snapshot은 어떻게 처리하는가?
- restore된 process가 stale network/session state를 어떻게 감지하는가?

## Sources

- https://research.perplexity.ai/articles/making-space-secure-and-efficient-runtimes-for-long-running-agents
- https://btrfs.readthedocs.io/en/latest/Reflink.html
- https://btrfs.readthedocs.io/en/latest/Subvolumes.html
- https://gvisor.dev/docs/architecture_guide/security/

