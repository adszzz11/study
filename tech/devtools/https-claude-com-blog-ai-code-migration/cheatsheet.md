---
date: 2026-07-17
tags: [tech]
type: tech-tool-study
status: draft
---

# AI Code Migration — Cheatsheet

> [[05-projects|이전: Projects]] | [[README|목차로 돌아가기]]

## 핵심 공식

```text
Reliable migration
= explicit Rulebook
+ dependency-aware parallelism
+ portable deterministic Judge
+ independent review
+ bounded iterative loop
```

> 반복 오류는 파일이 아니라 그 오류를 만든 process loop를 수정한다.

## 실행 순서

```text
Feasibility
→ Portable Judge
→ Rulebook + Dependency Map + Gap Inventory
→ Disposable Stress Test
→ Parallel Implement / Independent Review / Resolve
→ Compile / Smoke / Parity / Security / Performance
→ Rule Update / Affected Batch Regeneration
```

## Artifact 빠른 참조

| Artifact | 반드시 담을 것 |
|---|---|
| Feasibility report | reason, port/redesign, costs, decision, non-goals |
| Rulebook | rule id, rationale, examples, verification |
| Dependency Map | imports, manifest, generated code, global state, FFI |
| Gap Inventory | semantic risk, owner, decision, affected scope, test |
| Work queue | batch, rule version, dependencies, revision, state, artifacts |
| Judge | contract tests, scenarios, normalization, mutation evidence |
| Gate report | revision별 compile/smoke/parity/security/performance 결과 |

## Judge Checklist

- [ ] original과 target에 같은 input·environment를 사용한다.
- [ ] external observable test와 implementation-detail test를 분류했다.
- [ ] original baseline이 통과한다.
- [ ] intentionally broken implementation이 실패한다.
- [ ] stdout, exit code, files, response, state 중 필요한 것을 diff한다.
- [ ] nondeterminism normalization이 실제 bug를 숨기지 않는다.
- [ ] 기능 parity와 performance/security threshold를 분리한다.

## Agent 역할

| 역할 | 원칙 |
|---|---|
| Implementer | 작은 batch, rulebook 준수, 불확실성은 `TODO(port): reason` |
| Reviewer A | behavior와 source semantic 중심 |
| Reviewer B | target idiom, security, performance 중심 |
| Resolver | disagreement를 evidence로 판정 |
| Judge | deterministic artifact만으로 pass/fail |
| Orchestrator | queue, budget, concurrency, retry, phase gate |

## 실패 대응

| 현상 | 먼저 볼 곳 | Action |
|---|---|---|
| 같은 변환 오류 반복 | Rulebook | rule 수정 후 영향 batch 재생성 |
| 누락 파일/순서 오류 | Dependency Map | edge와 queue 갱신 |
| test pass, 실제 output fail | Portable Judge | scenario/contract 강화 |
| reviewer가 같은 오류 누락 | 역할/context | independent adversarial review |
| build 중복·stale result | Build daemon | 직렬화, revision pinning |
| token·CI 폭주 | Orchestration | scope, concurrency, retry 상한 축소 |

## Stop / Go 기준

| Go | Stop 또는 재검토 |
|---|---|
| portable judge가 known mutation을 잡음 | original만 pass하고 mutation은 놓침 |
| batch dependency와 owner가 명확 | shared global state와 cycle이 미해결 |
| port와 redesign이 분리됨 | acceptance criteria가 계속 변함 |
| 비용·권한·timeout 상한이 있음 | 무제한 fan-out과 shared Git index |
| post-merge canary/rollback이 있음 | compile 또는 CI pass만 성공 기준 |

## Language Gap 예시

```text
Zig → Rust
allocator lifetime / defer / raw pointer / C ABI
→ ownership / Drop / borrow checker / explicit unsafe boundary

Python → TypeScript
duck typing / sync-async ambiguity / implicit None
→ interface / generic / Promise contract / explicit nullability

COBOL → Java
data layout / transaction boundary / embedded business rule
→ 먼저 rule extraction, 그 다음 representation mapping
```

## 운영 Guardrail

- cost ceiling, concurrency, timeout, retry를 phase별로 명시한다.
- batch마다 isolated worktree/sandbox를 사용한다.
- 비싼 전체 build는 build daemon이 직렬화한다.
- merge에는 deterministic gate와 human risk approval을 모두 요구한다.
- vendor 성공 사례 수치를 자신의 repository estimate로 그대로 쓰지 않는다.
- `Don't migrate`를 정상적인 최종 결론으로 허용한다.

## Sources

- https://claude.com/blog/ai-code-migration
- https://github.com/anthropics/code-migration-kit-with-claude-code
- https://bun.com/blog/bun-in-rust
- https://aclanthology.org/2025.findings-acl.140/
- https://claude.com/blog/introducing-dynamic-workflows-in-claude-code
