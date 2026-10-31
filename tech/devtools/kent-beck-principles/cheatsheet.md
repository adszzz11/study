---
date: 2026-06-18
tags:
  - tech
  - devtools
  - kent-beck
  - cheatsheet
type: tech-tool-study
parent: "[[README]]"
---

# Kent Beck의 지론들 - 치트시트

> [[README|목차로 돌아가기]]

---

## 핵심 문장

| 개념 | 기억할 문장 |
|------|-------------|
| `XP` | 개발은 기술 실천과 인간 관계가 함께 굴러가는 feedback system이다 |
| `TDD` | 모든 테스트를 먼저 쓰는 것이 아니라 한 번에 하나의 runnable failing test를 다룬다 |
| `Spike` | production code가 아니라 모르는 것을 줄이는 timeboxed experiment다 |
| `Tidy First?` | behavior change와 structural change를 분리해 future option을 산다 |
| `3X` | Explore, Expand, Extract 단계마다 좋은 engineering과 metric이 다르다 |
| `Augmented Coding` | AI가 코드를 써도 vision, task breakdown, review, design judgment는 인간 몫이다 |

---

## TDD Loop

```text
test list
  -> one failing test
  -> make it pass
  -> optional refactor
  -> repeat
```

| 체크 | 질문 |
|------|------|
| Test list | 해야 할 behavior를 작은 항목으로 쪼갰는가? |
| Failing test | 지금 딱 하나의 실패를 보고 있는가? |
| Pass | 가장 단순한 코드로 통과시켰는가? |
| Refactor | behavior를 바꾸지 않고 구조만 바꾸는가? |

---

## Spike Ticket Template

```markdown
## Question
- 

## Timebox
- 

## Experiment
- 

## Learned
- 

## Decision
- 

## Remaining Risks
- 
```

| 좋은 spike | 나쁜 spike |
|------------|------------|
| 질문이 좁다 | "이거 한번 알아보기" |
| timebox가 있다 | 끝나는 조건이 없다 |
| runnable proof가 있다 | 글만 있고 실행 결과가 없다 |
| decision이 남는다 | 코드만 남고 판단이 없다 |
| 남은 risk가 보인다 | production readiness처럼 포장한다 |

---

## Tidy First 판단

| 먼저 tidy할 때 | 바로 behavior change할 때 |
|----------------|--------------------------|
| 이름/조건이 헷갈려 change impact를 판단하기 어렵다 | 긴급 bug fix라 시간이 중요하다 |
| test를 쓰기 위한 작은 구조 정리가 필요하다 | tidy scope가 더 커질 위험이 있다 |
| 같은 개념이 여러 곳에 흩어져 있다 | future benefit이 추측뿐이다 |
| review diff를 줄일 수 있다 | 현재 코드도 변경하기 충분히 명확하다 |

### Commit 예시

```text
tidy: extract payment eligibility predicate
test: cover expired payment method branch
fix: reject expired payment method
```

---

## XP Values Review

| Value | 빠른 질문 |
|-------|-----------|
| Communication | 필요한 맥락이 공유됐는가? |
| Simplicity | 지금 필요한 것보다 크게 만들지 않았는가? |
| Feedback | 실패를 얼마나 빨리 알 수 있는가? |
| Courage | 작게 바꾸고 되돌릴 수 있는가? |
| Respect | 사람보다 system을 고치고 있는가? |

---

## 3X Quick Map

| 단계 | 초점 | 대표 작업 | Metric |
|------|------|-----------|--------|
| Explore | 학습 | spike, prototype, customer interview | validated learning |
| Expand | 성장 | feature slice, CI, small releases | cycle time, activation |
| Extract | 효율 | tidying, automation, reliability | cost, defect rate, uptime |

---

## AI Coding Agent 운영 체크리스트

| 체크 | 기준 |
|------|------|
| Task | 작은 단위인가? |
| Context | 필요한 파일/제약만 주었는가? |
| Test | runnable verification이 있는가? |
| Review | behavior/tidy/formatting이 분리됐는가? |
| Rollback | commit 단위로 되돌릴 수 있는가? |
| Decision | spike라면 code보다 decision log가 남았는가? |

---

## Spike vs Feature

| 항목 | Spike | Feature |
|------|-------|---------|
| 목표 | 모르는 것을 줄임 | 사용자 behavior 제공 |
| 산출물 | decision, risk, estimate, proof | production code, test, docs |
| 시간 | timebox | delivery plan |
| 품질 기준 | 학습에 충분한 수준 | production readiness |
| 완료 조건 | 다음 결정을 할 수 있음 | acceptance criteria 충족 |

---

## 관련 노트

- [[study/tech/ai/lazy-codex]] - AI coding task를 작게 쪼개고 검증하기
- [[study/tech/ai/agent-orchestration/cli-agents]] - agent workflow에서 feedback loop 설계
- [[study/tech/ai/mitchellh-ai-adoption-study]] - AI adoption과 engineering judgment 변화
