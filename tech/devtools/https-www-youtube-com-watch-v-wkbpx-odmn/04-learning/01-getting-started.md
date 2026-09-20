---
date: 2026-07-20
tags: [tech]
type: tech-tool-study
status: draft
---

# Getting Started — 첫 Comprehension Loop

> [[03-references|이전: References]] · [[README|목차]] · [[02-deep-dive|다음: Deep Dive]]

## Goal

작은 multi-file PR 하나에 **evidence 수집 → explainer → quiz → raw review → shared 기록** loop를 적용한다. 특정 agent나 platform에 종속되지 않는 최소 workflow다.

## 0. Change 분류

먼저 autonomy를 결정한다.

| 질문 | Yes라면 |
|---|---|
| public API, security boundary, data model, architecture가 바뀌는가? | autonomy를 낮추고 human design review 추가 |
| rollback이 어렵거나 blast radius가 큰가? | spec·ADR·runtime evidence 추가 |
| 여러 subsystem의 control/data flow를 건드리는가? | literate explainer와 diagram 추가 |
| state transition이 핵심인가? | trace 또는 micro-world 고려 |
| 단순하고 reversible한 mechanical change인가? | concise summary + test + diff로 축소 가능 |

## 1. Evidence Pack 만들기

Agent에 설명을 요청하기 전에 사실의 기준을 모은다.

```text
evidence/
├── spec-or-issue.md      # expected behavior와 acceptance criteria
├── diff.patch            # 실제 변경
├── tests.txt             # 실행 명령과 결과
├── trace.json            # 필요한 경우 runtime evidence
└── decisions.md          # constraints와 rationale
```

실제 repository에 이 구조를 반드시 commit할 필요는 없다. 중요한 것은 설명이 다음 입력을 참조하도록 하는 것이다.

- base revision과 target revision
- 관련 spec/issue/ADR
- test command와 실제 결과
- known limitation과 rejected alternative
- runtime trace 또는 reproducible example

## 2. Explainer 요청

다음 prompt를 project context에 맞게 사용한다.

```text
이 change를 reviewer가 다음 설계에 참여할 수 있을 정도로 설명하라.

근거 우선순위:
1. specification / ADR
2. code와 raw diff
3. tests와 runtime trace
4. 추론

구조:
1. Background: 변경 전 component, contract, invariant
2. Intuition: 목표, 핵심 원리, 작은 concrete example
3. Code: file 순서가 아니라 dependency와 control/data flow 순서
4. Quiz: causality, invariant, edge case, trade-off를 묻는 5문항

각 주장에 file/function/test 근거를 붙이고, 확인하지 못한 내용은
"unknown" 또는 "inference"로 표시하라. raw diff를 생략하지 말라.
```

## 3. Explainer 검증

문장이 유창한지보다 evidence와 맞는지 확인한다.

- Background의 contract가 code와 test에 존재하는가?
- “왜”에 대한 설명이 spec/ADR인지 agent 추론인지 표시됐는가?
- walkthrough가 실제 control/data flow를 따르는가?
- before/after example이 실행 가능한 input/output과 일치하는가?
- failure path, fallback, rollback이 누락되지 않았는가?
- diagram이 실제 dependency direction을 뒤집지 않았는가?

오류가 있으면 explainer만 고칠지, code/test/spec 자체의 ambiguity를 고칠지 구분한다.

## 4. Quiz 통과

답을 보지 않고 작성자 또는 reviewer가 구두/서면으로 설명한다.

```text
1. 이 변경이 없을 때 input X는 어느 경로에서 실패하는가?
2. 변경 후에도 반드시 유지되는 invariant 두 개는 무엇인가?
3. component A의 output이 component C까지 전달되는 순서는?
4. edge case Y에서 fallback이 발동하는 조건은?
5. alternative B 대신 현재 design을 택한 trade-off는?
```

통과 기준 예시:

- 정답 개수만 보지 않고 설명에 code/test 근거가 있는지 본다.
- 틀린 답은 사람의 주의 부족, explainer 결함, implementation ambiguity로 분류한다.
- high-risk change에서 핵심 invariant나 security question을 틀리면 merge를 보류한다.

## 5. Raw Diff와 Test 검토

Explainer를 읽었어도 다음은 별도로 수행한다.

```bash
git diff --stat <base>...<head>
git diff <base>...<head>
# project-specific lint, typecheck, unit/integration test 실행
```

- 설명에서 언급하지 않은 file/change가 있는가?
- test가 실제 acceptance criteria를 검증하는가?
- generated code, migration, config에 hidden blast radius가 있는가?
- security, performance, concurrency failure가 happy path 뒤에 숨지 않았는가?

## 6. Shared Artifact 남기기

PR 또는 collaborative document에 짧게 고정한다.

```markdown
## Intent
- 해결하려는 문제:
- 유지해야 할 invariants:
- 선택한 design과 이유:
- 거절한 alternative:

## Evidence
- Tests:
- Runtime trace:
- Explainer/diagram:

## Comprehension check
- Reviewer:
- 확인한 causality/edge case:
- 남은 unknown:
```

## Done Criteria

- [ ] 최소 한 명이 “무엇”과 “왜”를 자신의 말로 설명한다.
- [ ] 중요한 주장에 code, spec, test, trace 근거가 있다.
- [ ] raw diff와 test를 explainer와 독립적으로 확인했다.
- [ ] unknown과 inference가 표시됐다.
- [ ] rationale과 남은 risk가 shared space에 보존됐다.
- [ ] 다음 design loop에서 사용할 vocabulary와 constraint가 남았다.

## Sources

- [공개 `/explain-diff` skill](https://gist.github.com/geoffreylitt/a29df1b5f9865506e8952488eac3d524)
- [Understanding is the new bottleneck](https://www.geoffreylitt.com/2026/07/02/understanding-is-the-new-bottleneck.html)
- [Cognitive Debt](https://margaretstorey.com/blog/2026/02/09/cognitive-debt/)

