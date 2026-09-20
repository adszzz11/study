---
date: 2026-07-20
tags: [tech]
type: tech-tool-study
status: draft
---

# Projects — 실전 적용

> [[04-learning/02-deep-dive|이전: Deep Dive]] · [[README|목차]] · [[cheatsheet|다음: Cheatsheet]]

## Project 1. 한 PR용 Literate Explainer

### 목표

최근의 중간 규모 multi-file PR 하나를 Background→Intuition→Code→Quiz artifact로 바꾼다.

### 산출물

- base/head commit이 명시된 explainer
- control/data flow diagram
- concrete before/after example
- 5문항 quiz와 evidence-backed answer key
- raw diff에서 발견한 explainer 누락 목록

### 완료 기준

- [ ] reviewer가 explainer만 읽은 뒤 change path를 예측한다.
- [ ] 모든 factual claim이 code/spec/test에 연결된다.
- [ ] raw diff review에서 설명과 다른 부분이 명시된다.
- [ ] 다음 design question 하나를 reviewer가 제안한다.

## Project 2. Runtime Micro-world

### 후보

- parser/interpreter evaluation trace
- retry/backoff state machine
- event processing pipeline
- cache invalidation flow
- authorization decision chain

### 단계

1. 한 가지 debugging question을 고른다. 예: “무한 loop는 어느 rule에서 시작하는가?”
2. 최소 `TraceEvent` schema를 정의한다.
3. deterministic example을 기록한다.
4. timeline, state diff, causal link만 있는 작은 UI를 만든다.
5. raw log와 UI 표현을 대조한다.
6. UI로 발견한 bug 또는 잘못된 mental model을 기록한다.

### 완료 기준

- [ ] UI가 product code의 source location으로 연결된다.
- [ ] secret·PII가 trace에 없다.
- [ ] known-good trace로 visualization을 검증했다.
- [ ] UI 없이 log만 볼 때와 진단 시간을 비교했다.

## Project 3. Team Comprehension Gate Pilot

### 범위

2주 동안 한 repository와 한 team에서만 pilot한다. 모든 PR이 아니라 다음 조건 중 하나를 만족하는 change에 적용한다.

- 5개 이상 file 또는 2개 이상 subsystem 변경
- public API/data model 변경
- security/reliability critical path
- agent가 대부분의 implementation을 생성

### PR Template

```markdown
## Intent & constraints
- Problem:
- Invariants:
- Chosen design / why:
- Rejected alternative:

## Comprehension artifact
- Explainer:
- Diagram/trace:
- Quiz result and corrected misunderstanding:

## Verification evidence
- Raw diff reviewed by:
- Tests:
- Remaining risk / unknown:
```

### Retrospective 질문

- explainer가 review 시작 시간을 줄였는가, 늘렸는가?
- quiz가 실제 misunderstanding을 발견했는가?
- 가장 가치 있던 artifact는 무엇이었는가?
- trivial한 change에 과도한 ceremony가 생겼는가?
- rationale이 다음 PR에서 재사용됐는가?

## Project 4. Autonomy Matrix 만들기

팀의 실제 task 유형 10개를 수집해 autonomy policy를 만든다.

| Task | Risk | Clarity | Agent autonomy | Human gate | Artifact |
|---|---:|---:|---|---|---|
| type fix | 낮음 | 높음 | 높음 | spot check | test + summary |
| dependency migration | 중간 | 높음 | 중간~높음 | migration review | plan + CI |
| product behavior | 중간~높음 | 중간 | 낮음 | spec/design review | explainer + quiz |
| auth boundary | 매우 높음 | 낮음~중간 | 매우 낮음 | security expert | threat model + trace |
| data model migration | 높음 | 중간 | 낮음 | architecture/data review | ADR + rollback plan |

Matrix는 고정 규칙이 아니라 incident와 retrospective에 따라 갱신한다.

## Project 5. Cognitive Debt Audit

### Sampling

최근 agent-heavy PR 5개를 골라 다음을 확인한다.

- 최소 한 명이 change의 what/why를 설명할 수 있는가?
- spec, rationale, rejected alternative가 남아 있는가?
- artifact가 current code revision과 맞는가?
- 신규 팀원이 change를 안전하게 확장할 수 있는가?
- 중요한 understanding이 개인 chat에만 있는가?

### Output

```text
PR / change:
Human owner:
Mental-model gap:
Missing intent:
Evidence gap:
Risk if unchanged:
Smallest repair action:
```

audit의 목적은 책임 추궁이 아니라 가장 비싼 cognitive/intent gap을 작은 action으로 줄이는 것이다.

## Recommended Order

1. **Project 1**로 artifact의 최소 형태를 배운다.
2. 복잡한 runtime 문제가 있을 때만 **Project 2**를 수행한다.
3. **Project 3**을 작은 pilot로 운영해 ceremony 비용을 측정한다.
4. 결과를 바탕으로 **Project 4**의 autonomy matrix를 합의한다.
5. 분기별로 **Project 5**를 반복해 drift를 찾는다.

## Sources

- [Understanding is the new bottleneck](https://www.geoffreylitt.com/2026/07/02/understanding-is-the-new-bottleneck.html)
- [공개 `/explain-diff` skill](https://gist.github.com/geoffreylitt/a29df1b5f9865506e8952488eac3d524)
- [AI-generated debugger](https://www.geoffreylitt.com/2024/12/22/making-programming-more-fun-with-an-ai-generated-debugger)
- [Cognitive Debt](https://margaretstorey.com/blog/2026/02/09/cognitive-debt/)

