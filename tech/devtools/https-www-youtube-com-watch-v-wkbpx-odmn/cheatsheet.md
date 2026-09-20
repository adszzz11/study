---
date: 2026-07-20
tags: [tech]
type: tech-tool-study
status: draft
---

# Cheatsheet — Understanding-centered AI Coding

> [[05-projects|이전: Projects]] · [[README|목차]]

## 핵심 구분

| Mode | 질문 | 충분한 상태 |
|---|---|---|
| **Understand to verify** | 맞고 안전한가? | spec, bug, security, architecture를 검토해 승인/거절 가능 |
| **Understand to participate** | 다음에 무엇을 어떻게 만들까? | concept, constraint, trade-off를 바탕으로 새 design 제안 가능 |

## Comprehension Loop

```text
Spec/Intent + Repo + Diff + Tests/Trace
                ↓
Background → Intuition → Code walkthrough → Quiz
                ↓
      Human teach-back / prediction
                ↓
Raw diff + tests → Shared rationale → Next loop
```

## Autonomy Slider

| Change | Autonomy | Gate |
|---|---:|---|
| typo, type fix, formatting | 높음 | CI + spot check |
| mechanical migration, docs, tests | 중간~높음 | plan + diff review |
| product behavior, public API | 낮음 | spec + explainer + quiz |
| security, data model, architecture | 매우 낮음 | expert design review + strong evidence |

## Explainer Template

```markdown
## Background
- 변경 전 components/contracts/invariants

## Intuition
- goal, principle, concrete before/after

## Code walkthrough
- dependency/control/data flow 순서
- failure/rollback path
- file/function/test evidence

## Quiz
- causality
- invariant
- edge case
- trade-off
- counterfactual

## Unknowns
- 확인하지 못한 사실과 inference
```

## Agent Prompt

```text
Reviewer가 다음 설계에 참여할 수 있을 정도로 change를 설명하라.
Background → Intuition → Code → Quiz 순서를 사용하라.
file 순서 대신 dependency와 control/data flow 순서로 설명하라.
모든 주장에 spec/code/test/trace 근거를 붙여라.
근거 없는 rationale은 inference, 확인 불가는 unknown으로 표시하라.
raw diff를 대체하지 말라.
```

## Quiz Checklist

- [ ] 명칭 recall이 아니라 causality/prediction을 묻는다.
- [ ] invariant와 edge case를 포함한다.
- [ ] failure 또는 rollback path를 묻는다.
- [ ] design trade-off와 rejected alternative를 묻는다.
- [ ] 정답 위치·길이 bias가 없다.
- [ ] answer key를 code·test·spec으로 검증했다.
- [ ] 최소 하나는 free-response “what if” 질문이다.

## Merge 전에 묻기

- [ ] 최소 한 명이 what과 why를 자기 말로 설명할 수 있는가?
- [ ] 이 change가 깨뜨릴 수 있는 invariant는 무엇인가?
- [ ] input에서 external effect까지의 실제 path는 무엇인가?
- [ ] 설명과 raw diff가 일치하는가?
- [ ] test가 acceptance criteria와 negative case를 다루는가?
- [ ] rationale, unknown, remaining risk가 shared space에 남았는가?
- [ ] explainer가 현재 head revision을 가리키는가?

## Red Flags

- “test가 통과하므로 이해했다”
- “agent가 설명했으므로 사실이다”
- “quiz 점수가 높으므로 설계에 참여할 수 있다”
- explainer가 raw diff review를 대체함
- code에 없는 rationale을 단정함
- 개인 chat만이 decision history를 보유함
- trivial PR까지 동일한 긴 ceremony를 강제함
- trace에 secret·PII가 포함됨

## Debt 빠른 진단

| 징후 | Debt | 첫 조치 |
|---|---|---|
| code가 복잡하고 변경하기 어려움 | Technical | refactor/test |
| 누구도 behavior를 예측하지 못함 | Cognitive | walkthrough/quiz/trace |
| 선택 이유와 requirement가 없음 | Intent | spec/ADR/rationale 기록 |

## Micro-world 최소 기능

- step forward/backward
- timeline scrub
- state before/after diff
- causal parent/child
- repeated state/loop 강조
- source location link
- annotation export
- secret redaction

## Sources

- [발표 영상](https://www.youtube.com/watch?v=WkBPX-oDMnA)
- [발표 원문](https://www.geoffreylitt.com/2026/07/02/understanding-is-the-new-bottleneck.html)
- [공개 `/explain-diff` skill](https://gist.github.com/geoffreylitt/a29df1b5f9865506e8952488eac3d524)
- [Cognitive Debt](https://margaretstorey.com/blog/2026/02/09/cognitive-debt/)

