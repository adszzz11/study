---
date: 2026-07-20
tags: [tech]
type: tech-tool-study
status: draft
---

# SPACE Getting Started: State Machine부터 설계하기

> [[../03-references|이전: References]] · [[../README|목차]] · [[02-deep-dive|다음: Deep Dive]]

## 목표

SPACE는 공개 설치형 tool이 아니므로 첫 실습은 SDK 호출이 아니라 **sandbox lifecycle model과 safety invariant**를 작성하는 것이다. 이 산출물은 E2B, Daytona, Kubernetes Agent Sandbox 또는 자체 runtime을 평가할 때 그대로 사용할 수 있다.

## 1. Workload를 명세한다

아래 질문에 답한다.

```yaml
workload:
  trust: untrusted-generated-code
  lifetime: days
  idle_ratio: 0.95
  required_state:
    filesystem: true
    memory: true
    processes: true
  operations:
    - rollback
    - fork
    - cross_node_restore
  external_access:
    - github.com
    - api.example.com
  credentials:
    - github_installation_token
  recovery_point_objective: 5m
  recovery_time_objective: 30s
```

`required_state`가 filesystem뿐이면 disk snapshot으로 충분할 수 있다. memory/process가 필요하면 full VM checkpoint나 application-level reconstruction을 검토한다.

## 2. State와 Transition을 정의한다

```text
NEW --create--> RUNNING
RUNNING --pause--> PAUSED --resume--> RUNNING
RUNNING --suspend--> SUSPENDING --commit--> RESTORABLE
RESTORABLE --restore--> RESTORING --ready--> RUNNING
RUNNING --stop--> STOPPED
PAUSED --stop--> STOPPED
RESTORABLE --stop--> STOPPED
```

각 transition은 다음 schema를 가진 idempotent command로 생각한다.

```json
{
  "operation_id": "op-01HV...",
  "sandbox_id": "sbx-42",
  "expected_generation": 7,
  "desired_state": "RESTORABLE",
  "reason": "idle-timeout",
  "requested_at": "2026-07-20T10:00:00Z"
}
```

### 최소 invariant

- 같은 `operation_id`를 재시도해도 artifact나 VM이 중복 생성되지 않는다.
- observed state를 확인하지 않고 성공으로 간주하지 않는다.
- 허용되지 않은 transition은 reject한다.
- 오래 걸리는 중간 상태(`SUSPENDING`)는 timeout과 recovery path를 가진다.
- state row의 generation/version으로 stale writer를 막는다.

## 3. Snapshot Policy를 작성한다

```yaml
snapshot_policy:
  disk:
    interval: 60s
    retention: [5m, 1h, 24h]
    pause_required: false
  full:
    interval: 15m
    on_events: [before_high_risk_command, idle_suspend]
    retention: [1h, 24h]
  durable_upload:
    required_before_restorable: true
    integrity_manifest: true
    encryption: customer_key
```

| Decision | Trade-off |
|---|---|
| disk snapshot을 자주 생성 | 낮은 filesystem RPO, memory/process는 복원하지 못함 |
| full snapshot을 자주 생성 | 낮은 full-state RPO, pause/CPU/storage/network 비용 증가 |
| node-local retention | 빠른 rollback, node failure에는 취약 |
| object storage upload | cross-node recovery, upload/restore latency와 비용 증가 |

## 4. Suspend를 Transaction으로 모델링한다

```pseudo
function suspend(sandbox, operation_id):
    if durable_snapshot_for(operation_id).is_restorable:
        return success

    pause_vm(sandbox)
    artifacts = create_full_snapshot(sandbox)
    manifest = hash_and_list(artifacts)
    upload_all(artifacts, manifest)
    verify_all_objects(manifest)

    compare_and_swap(
        sandbox.state,
        from = SUSPENDING,
        to = RESTORABLE,
        snapshot = manifest.id
    )
```

실패를 주입해 본다.

| 실패 지점 | 기대 동작 |
|---|---|
| VM pause 뒤 manager crash | reconcile이 paused VM/operation을 발견하고 재개 또는 안전 rollback |
| artifact 3개 중 2개 upload | `RESTORABLE` 금지, incomplete artifact 정리 가능 |
| upload 완료 뒤 DB timeout | manifest로 idempotent commit 재시도 |
| original node 소실 | durable manifest가 있으면 다른 node restore |
| restore 중 client reconnect | stable sandbox identity로 상태 조회, 중복 restore 방지 |

## 5. Security Boundary를 그린다

```text
[Guest: untrusted]
  agent, shell, packages, /proc, browser
       │ only approved RPC / egress
-------┼---------------- trust boundary ----------------
       ▼
[Platform: trusted]
  space-like daemon endpoint
  egress gateway
  credential broker
  snapshot service
  audit log
       │
       ▼
[External]
  scoped credential store / customer KMS / allowed services
```

검증 질문:

- guest에서 `env`, `/proc/*/environ`, shell history를 읽어도 long-lived secret이 없는가?
- redirect와 DNS rebinding 뒤에도 egress policy가 유지되는가?
- browser autofill된 secret을 page script나 screenshot이 읽을 수 있는가?
- credential scope, expiry, rate limit, audit event가 service별로 분리되는가?

## 6. SLO를 정한다

```yaml
slo:
  create_latency_ms:
    p50: 100
    p90: 250
  restore_latency_ms:
    p90: 5000
  snapshot_success_rate: 0.999
  false_restorable_records: 0
  cross_tenant_access: 0
  credential_exposure_in_guest: 0
```

create latency만 보면 안 된다. cold/warm ratio, restore size, checkpoint age, reconnect success, orphan VM/artifact, egress deny rate도 함께 측정한다.

## 완료 조건

- [ ] threat model과 required state를 적었다.
- [ ] state/transition table과 invalid transition을 정의했다.
- [ ] disk/full snapshot의 RPO와 retention을 정했다.
- [ ] partial upload가 `RESTORABLE`이 되지 않는 invariant를 만들었다.
- [ ] guest 밖 credential flow를 그렸다.
- [ ] 내 workload 기준 cold/warm/create/restore SLO를 정했다.

## Sources

- https://research.perplexity.ai/articles/making-space-secure-and-efficient-runtimes-for-long-running-agents
- https://e2b.dev/docs/sandbox/persistence
- https://www.daytona.io/docs/en/sandboxes/

