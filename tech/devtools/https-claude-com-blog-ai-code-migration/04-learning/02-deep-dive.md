---
date: 2026-07-17
tags: [tech]
type: tech-tool-study
status: draft
---

# AI Code Migration — Deep Dive

> [[01-getting-started|이전: Getting Started]] | [[../README|목차로 돌아가기]] | [[../05-projects|다음: Projects]]

## Mental Model: Code가 아니라 Process를 Debug한다

대량 migration에서 개별 defect는 흔히 shared rule의 symptom이다.

```text
failure 발견
  → root cause cluster
  → rulebook / prompt / judge / batching 중 원인 선택
  → process artifact 수정
  → 영향 batch 식별
  → clean context에서 재생성
  → deterministic gate 재실행
```

수동 patch가 필요한 exception은 가능하지만, 왜 일반 rule로 흡수할 수 없는지 gap inventory에 남긴다.

## Artifact 설계

### Rulebook

| 영역 | 필수 질문 | Verification |
|---|---|---|
| Type/nullability | implicit shape와 sentinel을 어떻게 표현할까? | type checker + boundary test |
| Error | exception/status/message contract는 무엇인가? | negative-path parity |
| Resource ownership | allocate/free, `defer`, lifetime을 어떻게 보존할까? | sanitizer, leak/repetition test |
| Concurrency | scheduling, cancellation, ordering 의미는? | race test, stress scenario |
| FFI | ABI, layout, pointer safety boundary는? | integration test, layout assertion |
| Naming/API | public surface를 보존할까, adapter를 둘까? | API snapshot, consumer compile |

Rulebook은 prose만으로 두지 말고 positive/negative example과 자동 check를 연결한다.

### Dependency Map

단순 import graph에 다음 edge를 추가해야 한다.

- build manifest와 feature flag
- generated code와 generator
- shared global state와 initialization order
- C ABI/FFI boundary
- test fixture와 toolchain dependency
- package owner와 approval boundary

Strongly connected component는 같은 batch로 묶거나 adapter를 먼저 만들어 cycle을 끊는다.

### Gap Inventory

```yaml
- id: GAP-017
  source: allocator lifetime escapes request scope
  target_risk: use-after-free or excessive cloning
  affected: [parser, cache]
  owner: runtime-reviewer
  decision: explicit Arc ownership at cache boundary
  verification: [stress-test-12, memory-gate]
  status: accepted
```

## Parallel Translation Loop

| 역할 | Context | Output |
|---|---|---|
| Implementer | 한 batch, rulebook, relevant contracts | patch + uncertainty TODO |
| Reviewer A | patch와 behavior contract | semantic/behavior findings |
| Reviewer B | patch와 target-language idiom/security | independent findings |
| Resolver | 두 review와 evidence | accept/reject/escalate decision |
| Fixer | accepted findings만 | minimal correction |
| Judge | code를 해석하지 않음 | deterministic pass/fail artifacts |

Implementer와 reviewer가 같은 conversation context를 공유하면 초기 가정을 그대로 답습하기 쉽다. independent context와 evidence schema로 역할을 분리한다.

### Resumable Work Queue

```json
{
  "batch": "parser-014",
  "rulebook_version": "r23",
  "depends_on": ["types-003"],
  "workspace": "isolated/parser-014",
  "state": "parity_failed",
  "attempt": 2,
  "artifacts": ["compile.log", "parity.diff"],
  "next": "triage-root-cause"
}
```

queue state는 agent의 기억이 아니라 manifest와 artifact 존재 여부로 판단한다. worktree 또는 sandbox를 batch별로 격리하고, shared Git index에 여러 writer를 두지 않는다.

## Compile → Run → Match Behavior

### Compile Loop

- error를 file, symbol, error code, suspected rule로 구조화한다.
- 동일 error cluster를 한 fixer 또는 rulebook update로 처리한다.
- TypeScript처럼 빠른 compiler는 inner loop에 넣는다.
- 전체 `cargo` build처럼 비싼 작업은 build daemon에 제출한다.

### Smoke Loop

startup crash를 파일별이 아니라 root cause별로 묶는다. initialization order, missing asset, env/config, FFI loading 같은 category가 유용하다.

### Parity Loop

```text
same fixture
  → original result ┐
                     ├→ normalize → semantic diff → gate
  → target result   ┘
```

diff가 있으면 무조건 target 오류로 보지 않는다. 원본 latent bug, intentional change, nondeterminism, harness defect 중 무엇인지 판정하고 contract decision을 기록한다.

## Build Daemon

여러 agent가 비싼 build를 동시에 실행하면 CPU·memory thrash와 stale result가 생긴다. build daemon은 다음을 담당한다.

1. patch 또는 commit hash를 queue에 받는다.
2. compatible patch를 batch한다.
3. build를 직렬화한다.
4. 결과를 exact revision과 연결한다.
5. error cluster를 다시 work queue로 반환한다.

## Phase Gates

| Gate | 최소 조건 | 실패 시 |
|---|---|---|
| Compile | target과 consumer compile | error cluster triage |
| Smoke | startup·핵심 command 무 crash | root cause batch |
| Test | portable contract suite pass | rule 또는 implementation 수정 |
| Parity | 승인되지 않은 semantic diff 0 | contract decision/escalation |
| Security | auth, input, dependency, unsafe boundary 통과 | security owner review |
| Performance | latency·memory·binary budget 충족 | profiling과 explicit waiver |

gate waiver에는 owner, rationale, expiry, follow-up issue를 남긴다.

## 비용과 안전

- 작은 model은 반복적 implementer fan-out, 강한 model은 rule·architecture·adversarial review에 배치한다.
- phase별 token, CI minute, agent count, wall time 상한을 둔다.
- timeout과 retry 횟수를 제한하고 동일 실패의 무한 loop를 막는다.
- filesystem과 Git write 권한은 isolated workspace로 최소화한다.
- merge는 deterministic gate와 human risk approval 뒤에만 수행한다.

## 실패 Pattern과 Process Fix

| 반복 실패 | 의심할 Process Artifact | 수정 |
|---|---|---|
| 같은 error mapping 오류 | Rulebook | mapping과 negative example 추가 후 재생성 |
| 파일 누락 | Dependency Map/queue | generated/conditional edge 추가 |
| test는 pass, scenario는 fail | Portable judge | production fixture와 assertion 강화 |
| reviewer 간 지속 disagreement | Review rubric | evidence schema와 resolver policy 명시 |
| build 결과가 뒤섞임 | Build daemon/workspace | revision pinning과 isolation 강화 |
| 비용 폭주 | Orchestrator | batch 크기, model routing, retry 상한 조정 |

## Sources

- https://claude.com/blog/ai-code-migration
- https://github.com/anthropics/code-migration-kit-with-claude-code
- https://bun.com/blog/bun-in-rust
- https://claude.com/blog/introducing-dynamic-workflows-in-claude-code
