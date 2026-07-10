---
date: 2026-06-18
tags:
  - tech
  - devtools
  - kent-beck
  - learning
type: tech-tool-study
parent: "[[../README]]"
---

# Kent Beck의 지론들 - 시작하기

> [[../README|목차로 돌아가기]] | [[02-deep-dive|다음: 심화]]

---

## 1. 목표

처음에는 개념을 많이 읽는 것보다 작은 실습 3개로 감각을 잡는다.

- `TDD kata`: test list에서 시작해 한 번에 하나의 failing test만 통과시킨다.
- `Spike ticket`: 모르는 기술을 feature 구현이 아니라 timeboxed learning으로 다룬다.
- `Tidy First?`: behavior change와 structural change commit을 분리한다.

---

## 2. TDD Kata

### 흐름

```text
1. test list를 작성한다.
2. 가장 작은 failing test 하나를 고른다.
3. test가 실패하는 것을 확인한다.
4. 가장 단순한 코드로 통과시킨다.
5. 필요한 경우 refactor한다.
6. 다음 test로 반복한다.
```

### 예시: String Calculator kata

```markdown
## Test list
- [ ] empty string returns 0
- [ ] single number returns that number
- [ ] two comma-separated numbers return sum
- [ ] multiple numbers return sum
- [ ] newline can separate numbers
- [ ] negative number raises error
```

| 단계 | 질문 |
|------|------|
| Failing test | 지금 딱 하나의 실패만 보고 있는가? |
| Pass | 이 test를 통과시키는 가장 단순한 구현인가? |
| Refactor | behavior를 바꾸지 않고 구조만 바꾸는가? |
| Repeat | test list에서 다음으로 가장 작은 항목은 무엇인가? |

---

## 3. Spike Ticket 작성

`Spike`는 production code를 만드는 ticket이 아니다. 모르는 것을 줄이고 다음 결정을 가능하게 만드는 ticket이다.

### Template

```markdown
## Question
- 우리가 모르는 것은 무엇인가?

## Timebox
- 예: 4시간 / 1일 / 2일

## Experiment
- 어떤 가장 작은 runnable proof로 확인할 것인가?

## Findings
- 배운 점:
- 실패한 점:
- 예상과 달랐던 점:

## Decision
- 채택 / 보류 / 폐기:
- 이유:

## Remaining Risks
- 남은 리스크:
- 다음 spike 또는 feature ticket:
```

### 좋은 spike의 기준

| 기준 | 설명 |
|------|------|
| 질문이 좁다 | "이 기술 좋은가?"보다 "우리 auth flow에서 token refresh가 되는가?" |
| timebox가 있다 | 끝나는 시간이 있어야 학습 산출물이 나온다 |
| runnable proof가 있다 | 말보다 실행 가능한 작은 증거가 있다 |
| decision이 남는다 | 코드를 버려도 판단 근거가 남는다 |
| production code와 구분한다 | spike code를 무심코 제품 코드로 승격하지 않는다 |

---

## 4. Tidy First? 실습

기능 변경 전에 작은 `tidying`을 먼저 해본다. 단, behavior change와 섞지 않는다.

| Tidying | 예 |
|---------|----|
| Guard clauses | 깊은 nested conditional을 빠른 return으로 정리 |
| Dead code removal | 사용되지 않는 branch/function 제거 |
| Explaining variables | 복잡한 expression에 의도를 드러내는 변수 부여 |
| Extract helper | 반복되거나 의미 단위가 분명한 코드를 helper로 추출 |
| Normalize names | 같은 개념에 같은 이름 사용 |

### Commit 분리 예시

```text
commit 1: tidy: extract invoice status predicate
commit 2: test: cover overdue invoice notification
commit 3: feat: send overdue invoice notification
```

| 하지 말 것 | 이유 |
|------------|------|
| refactor와 기능을 한 commit에 섞기 | review와 rollback이 어려워짐 |
| 큰 rename을 기능 변경 중에 수행 | diff가 noisy해지고 risk가 커짐 |
| "나중을 위해" 대규모 abstraction 추가 | optionality가 아니라 premature generalization일 수 있음 |

---

## 5. XP Values 회고

작은 팀 회고에서 다음 질문을 체크한다.

| Value | 회고 질문 |
|-------|-----------|
| Communication | 필요한 맥락이 issue, test, PR에 충분히 남았는가? |
| Simplicity | 현재 문제보다 큰 설계를 만들지 않았는가? |
| Feedback | 실패를 너무 늦게 알게 된 지점은 어디인가? |
| Courage | 작게 바꾸고 자주 배포할 용기를 방해한 것은 무엇인가? |
| Respect | 사람 탓이 아니라 system과 loop를 고쳤는가? |

---

## 실습 체크리스트

- [ ] TDD kata test list 작성
- [ ] 한 번에 하나의 failing test만 구현
- [ ] refactor commit과 behavior commit 분리
- [ ] spike ticket template으로 모르는 기술 하나 조사
- [ ] spike 산출물을 decision log로 남김
- [ ] XP values 회고 질문 5개를 팀/개인 작업에 적용

---

## 관련 노트

- [[study/tech/ai/lazy-codex]] - AI agent에게도 test list와 done criteria를 주기
- [[study/tech/ai/model-context-protocol-mcp]] - MCP 같은 새 protocol을 spike ticket으로 조사하기
- [[study/tech/ai/agent-orchestration/cli-agents]] - agent 작업 단위를 작게 쪼개 feedback loop 만들기
