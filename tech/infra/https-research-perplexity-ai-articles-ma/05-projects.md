---
date: 2026-07-20
tags: [tech]
type: tech-tool-study
status: draft
---

# SPACE Projects

> [[04-learning/02-deep-dive|이전: Deep Dive]] · [[README|목차]] · [[cheatsheet|다음: Cheatsheet]]

SPACE 자체 public API가 없으므로 아래 프로젝트는 설계 원리를 작은 local prototype이나 선택한 sandbox provider/Kubernetes 환경에 적용한다.

## Project 1 — Lifecycle Simulator

**난이도:** 초급 · **목표:** explicit state machine과 idempotency 이해

JSON/SQLite에 desired/observed state를 저장하고 `create`, `pause`, `resume`, `suspend`, `restore`, `stop` command를 처리하는 simulator를 만든다.

```text
simulator/
├── state_machine.*
├── reconciler.*
├── fault_injection.*
└── tests/
```

필수 test:

- 같은 operation을 10회 재전송해도 resource는 하나
- invalid transition reject
- process restart 뒤 reconciliation 재개
- stale generation update reject

완료 기준:

- [ ] transition table이 code와 test에서 일치한다.
- [ ] 중간 상태 crash test가 있다.
- [ ] event log로 최종 state를 설명할 수 있다.

## Project 2 — Dual Snapshot Lab

**난이도:** 중급 · **목표:** filesystem checkpoint와 application state 차이 관찰

local btrfs 가능 환경 또는 snapshot을 지원하는 sandbox provider에서 다음을 비교한다.

1. process가 file에 buffered write를 수행한다.
2. flush 전/후 disk snapshot을 만든다.
3. memory counter와 background process를 함께 실행한다.
4. disk-only restore와 full-state restore 결과를 비교한다.

측정표:

| Run | Snapshot type | Pause time | Restore time | File state | Process state |
|---|---|---:|---:|---|---|
| A | disk, pre-flush |  |  |  | lost |
| B | disk, post-fsync |  |  |  | lost |
| C | full VM |  |  |  |  |

> [!warning] 환경 제한
> macOS 기본 filesystem에서 btrfs semantics를 흉내 내지 말고 Linux VM/test host를 사용한다. provider마다 “snapshot”에 memory가 포함되는지 반드시 문서로 확인한다.

## Project 3 — Credential Mediation Proxy

**난이도:** 중급 · **목표:** guest 밖 secret injection prototype

fake external API와 egress proxy를 만든다. sandbox는 credential 없이 proxy에 request하고, proxy가 sandbox identity와 policy를 확인해 short-lived token을 붙인다.

```text
sandbox(no secret)
  -> authenticated proxy
      -> policy check
      -> short-lived token injection
      -> fake API
      -> redacted audit event
```

공격 test:

- guest의 `env`와 filesystem scan
- 허용되지 않은 method/path
- redirect to private IP
- expired sandbox identity
- rate-limit 초과
- audit log secret leakage

완료 기준:

- [ ] raw token이 guest와 log에 나타나지 않는다.
- [ ] deny case는 fail closed다.
- [ ] subject/service/scope별 audit trail이 있다.

## Project 4 — Suspend/Restore Fault Harness

**난이도:** 고급 · **목표:** partial failure correctness 검증

snapshot을 여러 artifact로 나눠 object storage emulator에 올리고 manifest commit을 구현한다.

```json
{
  "snapshot_id": "snap-007",
  "state": "UPLOADING",
  "artifacts": [
    {"key": "memory", "sha256": "...", "complete": true},
    {"key": "disk-delta", "sha256": "...", "complete": false},
    {"key": "vm-state", "sha256": "...", "complete": true}
  ]
}
```

다음 지점마다 process를 kill한다.

- pause 직후
- 첫 artifact upload 뒤
- 모든 upload 뒤, DB commit 전
- DB commit 뒤 acknowledgement 전
- restore download 중

불변식: **모든 artifact가 존재하고 hash가 일치하기 전 `RESTORABLE`은 0건**이어야 한다.

## Project 5 — Build vs Buy Evaluation

**난이도:** 고급 · **목표:** SPACE design을 evaluation rubric으로 전환

E2B, Daytona, Kubernetes Agent Sandbox 또는 내부 후보 2개 이상을 동일 workload로 평가한다.

| Dimension | Weight | Candidate A | Candidate B |
|---|---:|---:|---:|
| isolation/threat model | 25 |  |  |
| disk+memory lifecycle | 20 |  |  |
| credential/egress control | 20 |  |  |
| cross-node recovery | 15 |  |  |
| warm/cold latency | 10 |  |  |
| operability/cost | 10 |  |  |

Deliverables:

- architecture decision record(ADR)
- threat model과 trust boundary diagram
- warm/cold/create/restore benchmark raw data
- failure injection report
- unanswered security questionnaire

## Project 6 — Workflow + Sandbox Composition

**난이도:** 고급 · **목표:** logical state와 machine state 분리

Temporal/LangGraph/Prefect 중 하나로 approval workflow를 만들고, compute는 sandbox에 둔다.

```text
Workflow: PLAN -> RUN -> WAIT_APPROVAL -> APPLY -> VERIFY
                    │          │
Sandbox:          running -> suspend -> restore -> running
```

정해야 할 ownership:

- workflow가 저장할 것: task ID, approval, next step, sandbox ID, snapshot ID
- sandbox가 저장할 것: files, process/memory, execution artifacts
- 양쪽에 중복 저장하지 않을 것: authoritative transition state
- restore 뒤 재검증할 것: credential expiry, network session, external side effects

## Sources

- https://research.perplexity.ai/articles/making-space-secure-and-efficient-runtimes-for-long-running-agents
- https://e2b.dev/docs/sandbox/snapshots
- https://www.daytona.io/docs/en/snapshots/
- https://kubernetes.io/blog/2026/03/20/running-agents-on-kubernetes-with-agent-sandbox/

