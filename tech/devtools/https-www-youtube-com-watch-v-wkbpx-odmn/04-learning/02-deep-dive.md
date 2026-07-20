---
date: 2026-07-20
tags: [tech]
type: tech-tool-study
status: draft
---

# Deep Dive — Comprehension Pipeline 설계

> [[01-getting-started|이전: Getting Started]] · [[README|목차]] · [[../05-projects|다음: Projects]]

## Mental Model을 측정 가능한 행동으로 바꾸기

“이해했다”를 binary self-report로 두면 illusion of explanatory depth를 잡기 어렵다. 대신 사람이 수행할 수 있는 행동으로 operationalize한다.

| Level | 가능한 행동 | 확인 방법 |
|---|---|---|
| 1. Locate | 관련 component와 entry point를 찾는다 | code map에서 경로 지목 |
| 2. Explain | control/data flow와 rationale을 설명한다 | walkthrough, teach-back |
| 3. Predict | input/condition 변화의 결과를 예측한다 | quiz, counterfactual |
| 4. Diagnose | failure 원인과 관찰 지점을 좁힌다 | trace/debug task |
| 5. Modify | invariant를 지키며 변경점을 설계한다 | small extension task |
| 6. Participate | alternative와 trade-off를 제안한다 | design discussion |

Verify에는 주로 1~4가 필요하지만 participate에는 5~6이 중요하다.

## Context Reconstruction

Diff만으로 설명을 생성하지 않는다. 설명 context를 여러 source에서 재구성한다.

```text
Intent plane:   issue ─ spec ─ ADR ─ discussion
Code plane:     repository ─ dependency ─ diff
Behavior plane: tests ─ logs ─ runtime trace ─ metrics
Human plane:    reviewer questions ─ quiz ─ annotations
```

충돌 시 자동으로 매끈한 narrative를 만들지 말고 contradiction을 드러낸다.

- spec과 test가 다르면 expected behavior를 확정한다.
- comment와 code가 다르면 drift 후보로 표시한다.
- implementation rationale의 근거가 없으면 inference로 기록한다.
- test가 green이어도 relevant negative case가 없으면 evidence gap으로 남긴다.

## Literate Diff Architecture

좋은 explainer는 요약문이 아니라 **navigation layer**다.

```text
Background
  ├─ vocabulary
  ├─ pre-change contracts
  └─ affected boundaries
Intuition
  ├─ concrete input/output
  ├─ design principle
  └─ before/after
Code walkthrough
  ├─ entry point
  ├─ transformations
  ├─ persistence/external effect
  └─ failure/rollback
Quiz
  ├─ causality
  ├─ invariant
  ├─ edge case
  └─ trade-off
```

각 section은 raw evidence로 jump할 수 있어야 한다. self-contained HTML이나 Notion page를 쓰더라도 base/head revision을 고정해 stale artifact임을 판별할 수 있게 한다.

## Quiz Quality

### 좋은 문항

- 단순 명칭 recall보다 **prediction**을 요구한다.
- code의 happy path뿐 아니라 failure/rollback을 묻는다.
- architecture decision의 rejected alternative를 묻는다.
- correct answer의 길이와 위치로 답을 추측하기 어렵다.
- answer에 source location과 reasoning을 포함한다.

### 나쁜 문항

```text
Q. 이 PR은 무엇을 개선합니까?
A. 성능
B. 이 PR은 새로운 batching architecture를 도입하여 매우 크게 성능을 개선합니다. ✅
C. 색상
D. 문서
```

정답이 외형으로 드러나며 causality나 invariant를 확인하지 않는다.

### 문항 검증 절차

1. 정답을 code/test/spec에서 독립적으로 확인한다.
2. 질문이 ambiguous하면 implementation ambiguity인지 wording 문제인지 분리한다.
3. 정답 위치와 길이를 섞는다.
4. free-response와 “what if” question을 포함한다.
5. 틀린 답을 학습 signal로 기록하되 개인 평가 점수로 단순화하지 않는다.

## Interactive Micro-world 설계

복잡한 state machine, interpreter, concurrency, caching에서 다음 구조가 유용하다.

```typescript
type TraceEvent = {
  seq: number
  timestamp: number
  component: string
  rule: string
  input: unknown
  stateBefore: unknown
  stateAfter: unknown
  output?: unknown
  parentSeq?: number
}
```

UI는 최소한 다음을 제공한다.

- step forward/backward와 timeline scrub
- component/rule/filter
- state before/after diff
- causal parent/child 연결
- loop 또는 repeated state 강조
- source code location link
- annotation export

주의할 점:

- instrumentation이 behavior를 바꾸지 않는지 확인한다.
- secret과 PII를 trace에서 redact한다.
- agent-generated visualization과 raw trace를 대조한다.
- disposable tool이라도 실행법과 scope를 짧게 기록한다.

## Shared Workspace와 Intent 보존

chat transcript 전체를 저장하는 것만으로는 shared understanding이 되지 않는다. team artifact에는 다음이 필요하다.

| 항목 | 답해야 할 질문 |
|---|---|
| Intent | 어떤 user/system problem을 해결하는가? |
| Constraints | 절대 깨뜨리면 안 되는 것은 무엇인가? |
| Rationale | 왜 이 option을 선택했는가? |
| Alternatives | 무엇을 왜 거절했는가? |
| Evidence | 어떤 test/trace가 주장을 뒷받침하는가? |
| Unknowns | 아직 모르는 것과 follow-up owner는 누구인가? |
| Revision | 어느 commit/diff에 대한 artifact인가? |

## Risk-based Autonomy Policy

점수는 정밀 측정이 아니라 discussion aid다.

```text
Risk score = blast radius + irreversibility + novelty
           + security/data sensitivity + review difficulty

Clarity score = spec quality + testability + precedent
              + repository familiarity
```

- **Low risk + high clarity**: agent가 구현·test·summary까지 수행, human spot check
- **Medium risk/clarity**: plan 승인 후 구현, explainer+quiz+full diff review
- **High risk 또는 low clarity**: human이 design과 boundary를 먼저 확정, agent는 research·prototype·instrumentation 보조

## Failure Modes and Guardrails

| Failure mode | 징후 | Guardrail |
|---|---|---|
| Explanation hallucination | code에 없는 rationale을 단정 | evidence link, inference label |
| Comprehension theater | 긴 문서와 quiz 점수만 남음 | teach-back, prediction, modification task |
| Stale artifact | explainer revision과 PR head 불일치 | commit SHA 고정, regenerate flag |
| Quiz bias | 정답 위치·길이가 반복 | free-response, option balancing, human validation |
| Review automation trap | explainer가 raw diff review를 대체 | 독립 review checklist |
| Ceremony overload | trivial PR에도 긴 문서 강제 | risk-based threshold |
| Private understanding | 중요한 rationale이 개인 chat에만 존재 | shared plan/PR/ADR에 요약 |
| Trace leakage | secret/PII가 visualization에 노출 | allowlist schema, redaction, local-only mode |

## Team Metrics

단순한 document 수보다 다음 signal을 함께 본다.

- reviewer가 change causality를 설명하거나 예측하는 데 걸린 시간
- merge 후 “왜?” 질문과 rollback/rework 빈도
- onboarding engineer가 독립적으로 첫 safe change를 만들기까지의 시간
- explainer에서 발견한 code/spec/test contradiction 수
- stale artifact 비율
- task lead time과 comprehension activity의 균형

Metric이 target이 되면 quiz 암기나 document 양산으로 왜곡될 수 있다. 정량 signal은 interview, retrospective, design quality와 함께 해석한다.

## Sources

- [Understanding is the new bottleneck](https://www.geoffreylitt.com/2026/07/02/understanding-is-the-new-bottleneck.html)
- [공개 `/explain-diff` skill](https://gist.github.com/geoffreylitt/a29df1b5f9865506e8952488eac3d524)
- [AI-generated debugger](https://www.geoffreylitt.com/2024/12/22/making-programming-more-fun-with-an-ai-generated-debugger)
- [Cognitive Debt 논문](https://arxiv.org/abs/2603.22106)
- [DORA 2025](https://research.google/pubs/dora-2025-state-of-ai-assisted-software-development-report/)

