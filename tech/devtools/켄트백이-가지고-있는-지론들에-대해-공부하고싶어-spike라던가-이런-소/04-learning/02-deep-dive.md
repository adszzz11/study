---
date: 2026-06-18
tags:
  - tech
  - devtools
  - kent-beck
  - deep-dive
type: tech-tool-study
parent: "[[../README]]"
---

# Kent Beck의 지론들 - 심화

> [[01-getting-started|이전: 시작하기]] | [[../README|목차로 돌아가기]] | [[../05-projects|다음: 프로젝트]]

---

## 1. Optionality를 경제적으로 보기

`Tidy First?`에서 중요한 점은 정리가 미학이 아니라 경제성이라는 것이다. 작은 structural change는 미래의 선택지를 산다.

| 질문 | 의미 |
|------|------|
| 이 정리가 다음 behavior change를 더 싸게 만드는가? | option value가 있음 |
| 지금 하지 않으면 나중에 변경 비용이 커지는가? | 먼저 tidy할 이유가 있음 |
| behavior change와 섞이면 review가 어려워지는가? | commit 분리가 필요함 |
| 단지 보기 좋아지는 정도인가? | 지금 할 이유가 약할 수 있음 |

### 판단 예시

```text
When tidy first:
  - 같은 condition을 여러 곳에서 바꿔야 한다.
  - test를 쓰기 전에 seam/helper가 필요하다.
  - 이름이 헷갈려 change impact를 판단하기 어렵다.

When not tidy first:
  - production incident fix가 급하다.
  - tidy scope가 behavior change보다 커진다.
  - future use case가 아직 추측뿐이다.
```

---

## 2. 3X - Explore, Expand, Extract

`3X`는 같은 engineering practice도 제품/조직 단계에 따라 다르게 써야 한다는 관점이다.

| 단계 | 목표 | 위험 | 좋은 행동 |
|------|------|------|-----------|
| Explore | 맞는 문제/해결책 찾기 | 너무 빨리 optimize | spike, prototype, customer feedback |
| Expand | 검증된 것을 키우기 | 품질과 속도 충돌 | TDD, CI, small releases, observability |
| Extract | 효율과 안정성 추출 | 변화 대응력 상실 | tidying, automation, cost/reliability tuning |

### Metric 재설계

| 단계 | 피해야 할 metric | 더 나은 metric |
|------|------------------|----------------|
| Explore | output line count, feature count | validated learning, decision quality |
| Expand | 회의 횟수, story point 소모량 | cycle time, activation, defect escape |
| Extract | 무조건적인 velocity | cost per transaction, reliability, maintainability |

---

## 3. Thinkies - 사고 패턴

`Thinkies`는 막혔을 때 문제를 재구성하는 사고 도구다. 예를 들어 "We can't X because Y"를 "When not Y, then we can X"로 바꾼다.

| 기존 문장 | 재구성 |
|-----------|--------|
| We can't ship because tests are flaky. | When tests are stable, then we can ship. |
| We can't refactor because code has no tests. | When characterization tests cover the behavior, then we can refactor. |
| We can't choose this library because security is unknown. | When a spike verifies auth, license, and failure modes, then we can decide. |
| We can't trust AI output because it changes too much. | When tasks are small and tests are runnable, then AI output can be reviewed. |

### 실무 사용법

```markdown
## Blocker
We can't X because Y.

## Reframe
When not Y, then we can X.

## Smallest Next Step
- 

## Feedback Signal
- 어떤 결과가 나오면 unblock으로 볼 것인가?
```

---

## 4. Augmented Coding 운영

AI coding agent를 쓸수록 Beck식 discipline이 더 중요해진다. agent는 implementation cost를 낮추지만, context와 judgment를 자동으로 보장하지 않는다.

| 영역 | 운영 원칙 |
|------|-----------|
| Vision | agent에게 목표와 non-goal을 분리해 준다 |
| Milestone | 큰 feature를 runnable milestone으로 쪼갠다 |
| Task breakdown | agent task는 작고 검증 가능해야 한다 |
| Feedback loop | test, lint, screenshot, smoke test를 즉시 돌린다 |
| Design judgment | generated code가 future option을 막는지 사람이 본다 |
| Review rhythm | behavior change, tidy, formatting을 분리해 review한다 |

### AI-assisted spike 산출물

```markdown
## AI-assisted Spike Result
- Question:
- Timebox:
- Agent prompt:
- Runnable proof:
- Failure cases:
- Security note:
- Decision:
- Remaining risks:
- Next ticket:
```

---

## 5. Spike와 Production Code의 경계

Spike code를 그대로 production code로 쓰면 숨은 risk가 남기 쉽다.

| 구분 | Spike code | Production code |
|------|------------|-----------------|
| 목적 | 학습과 결정 | 사용자 가치 전달 |
| 품질 기준 | 빠른 실험, 좁은 proof | test, observability, security, maintainability |
| 수명 | 버릴 수 있음 | 유지해야 함 |
| 리뷰 | decision 중심 | behavior, design, regression 중심 |
| 산출물 | decision log | merged implementation |

### 승격할 때 필요한 것

- [ ] spike question과 decision이 문서화됐다.
- [ ] spike code 중 버릴 부분과 재사용할 부분을 구분했다.
- [ ] production acceptance criteria를 새로 썼다.
- [ ] test list를 만들었다.
- [ ] security, error handling, rollback plan을 확인했다.

---

## 6. Deep-dive 실습 과제

| 과제 | 목표 |
|------|------|
| 3X 진단 | 현재 제품/팀을 Explore, Expand, Extract 중 하나로 분류 |
| Optionality review | 최근 PR 하나에서 future option을 산 정리와 단순 미화를 구분 |
| Thinkies exercise | 막힌 ticket 3개를 "When not Y..." 형식으로 재구성 |
| AI-assisted spike | 새 library/API를 agent로 조사하고 decision record만 남김 |
| Tidy First review | behavior/refactor/formatting이 섞인 PR을 분해해 다시 구성 |

---

## 관련 노트

- [[study/tech/ai/lazy-codex]] - agent 작업 완료를 검증 가능한 loop로 닫기
- [[study/tech/ai/mitchellh-ai-adoption-study]] - AI adoption과 개발자 judgment의 이동
- [[study/tech/ai/agent-garden]] - agent를 협업 대상으로 볼 때의 workflow 관점
