---
date: 2026-06-18
tags:
  - tech
  - devtools
  - kent-beck
  - overview
type: tech-tool-study
parent: "[[README]]"
---

# Kent Beck의 지론들 - 개요

> [[README|목차로 돌아가기]] | [[02-ecosystem|다음: 생태계]]

---

## 1. What - 무엇인가?

Kent Beck의 지론은 특정 tool 하나가 아니라 software development를 다루는 실천 체계다. 중심에는 `short feedback loop`, `working software`, `human relationships`, `simple design`, `TDD`, `XP`, `spike`, `tidying`, `optionality`가 있다.

```text
불확실성
  -> 작은 실험(spike)
  -> 빠른 피드백(short feedback loop)
  -> 동작하는 코드(working software)
  -> 작은 정리(tidying)
  -> 다음 선택지(optionality)
```

Kent Beck은 XP, TDD, JUnit/xUnit, Agile Manifesto, Tidy First?, Augmented Coding 논의로 이어지는 인물이다. 그의 관점에서 좋은 개발은 "큰 계획을 완벽히 실행하는 일"보다 "작게 배우고, 작게 고치고, 사람 사이의 피드백을 유지하는 일"에 가깝다.

### 주요 용어

| 용어 | English | 설명 |
|------|---------|------|
| 짧은 피드백 루프 | `short feedback loop` | 작성, 실행, 검토, 배포, 사용자 반응을 가능한 한 짧게 돌리는 방식 |
| 동작하는 소프트웨어 | `working software` | 문서나 의도보다 실제로 실행되고 검증되는 결과물 |
| 단순 설계 | `simple design` | 현재 요구를 통과하는 가장 단순한 설계. 나중의 선택지를 막지 않는 설계 |
| 테스트 주도 개발 | `TDD` | test list에서 시작해 한 번에 하나의 failing test를 통과시키는 workflow |
| 익스트림 프로그래밍 | `XP` | communication, simplicity, feedback, courage, respect를 중심에 둔 agile engineering discipline |
| 스파이크 | `spike` | 모르는 것을 줄이기 위한 짧은 timebox 실험. 산출물은 production code보다 decision이다 |
| 코드 정리 | `tidying` | behavior change와 분리된 작은 structural change |
| 선택 가능성 | `optionality` | 미래에 더 싸게 바꿀 수 있는 선택지를 확보하는 경제적 가치 |

---

## 2. Why - 왜 중요한가?

소프트웨어 일은 대개 다음 불확실성을 포함한다.

- 사용자가 실제로 원하는지 모른다.
- 지금 설계가 나중 요구를 견딜지 모른다.
- 새 library/API가 팀의 제약에 맞을지 모른다.
- AI coding agent가 만든 결과가 실제 production 품질인지 모른다.
- 팀 안에서 기대, 책임, 품질 기준이 충분히 공유됐는지 모른다.

Beck식 접근은 이 불확실성을 큰 결심으로 해결하지 않는다. 대신 `batch size`를 줄이고, 확인 가능한 결과를 만들고, 설계 변경과 행동 변경을 분리해 실패 비용을 낮춘다.

### 문제를 다루는 방식

| 문제 | 흔한 대응 | Beck식 대응 |
|------|----------|-------------|
| 기술을 모름 | 바로 feature 구현 시작 | `spike`로 risk와 option을 먼저 확인 |
| 요구사항이 모호함 | 큰 설계 문서 작성 | working software로 고객 피드백 확보 |
| 코드가 지저분함 | 대규모 refactor 계획 | 작은 `tidying`을 먼저 수행 |
| 회귀가 두려움 | 수동 QA에 의존 | TDD와 자동화 테스트로 feedback loop 단축 |
| 팀 소통이 깨짐 | process ceremony 추가 | XP values로 communication/respect 복구 |
| AI가 코드를 많이 만듦 | 생성량을 성과로 봄 | 작은 task, test-first, review rhythm으로 통제 |

---

## 3. 핵심 특징

### XP Values

`XP values`는 communication, simplicity, feedback, courage, respect다. 이는 단순한 구호가 아니라 팀이 빨리 배우고, 작게 배포하고, 서로의 일을 망치지 않게 만드는 사회적 규율이다.

| Value | 실무 질문 |
|-------|-----------|
| Communication | 필요한 맥락이 pair, PR, issue, test에 드러나는가? |
| Simplicity | 지금 필요하지 않은 일반화를 만들고 있지 않은가? |
| Feedback | 실패를 몇 분, 몇 시간, 며칠 뒤에 알게 되는가? |
| Courage | 작은 변경을 자주 할 수 있는 용기가 있는가? |
| Respect | 사람을 탓하지 않고 system과 feedback loop를 고치는가? |

### TDD

Beck은 2023년 `Canon TDD`에서 TDD를 "모든 테스트를 미리 쓰는 것"이 아니라 한 번에 하나의 runnable test를 다루는 workflow로 정리했다.

```text
test list
  -> one failing test
  -> make it pass
  -> optional refactor
  -> repeat
```

### Spike

`Spike`는 "정답 구현"이 아니라 "모르는 것을 줄이는 코드/프로토타입"이다.

| 항목 | 기준 |
|------|------|
| 목적 | 기술, 설계, 요구사항 risk를 줄인다 |
| 시간 | 짧은 `timebox`를 둔다 |
| 산출물 | decision, risk reduction, estimate, design option |
| 주의 | production code처럼 유지하려 들지 않는다 |

### Tidy First?

`Tidy First?`는 behavioral change와 structural change를 분리한다. 코드 정리는 "예쁘게 만들기"가 아니라 future option을 사는 경제적 행위다.

| 변경 종류 | 의미 | 예 |
|-----------|------|----|
| Behavioral change | observable behavior가 바뀜 | 새 기능, bug fix |
| Structural change | behavior는 같고 구조만 바뀜 | guard clause, dead code removal, extract helper |

### 3X

`3X`는 Explore, Expand, Extract로 제품/조직 단계를 나눈다. 단계에 따라 좋은 engineering 방식과 metric이 달라진다.

| 단계 | 초점 | 좋은 metric |
|------|------|-------------|
| Explore | 무엇이 맞는지 찾기 | learning rate, experiment count, validated insight |
| Expand | 맞는 것을 키우기 | growth, throughput, customer feedback |
| Extract | 효율과 안정성 추출 | cost, reliability, defect rate, cycle time |

### Augmented Coding

2025-2026 AI coding agents 맥락에서 Beck의 관점은 AI를 코드 작성 대체자라기보다 `augmented coding`의 협업 대상, 일종의 "genie"로 보는 쪽에 가깝다. 그래서 더 중요한 능력은 언어 문법 지식보다 `vision`, `milestone`, `task breakdown`, `feedback loop`, `design judgment`다.

---

## 4. 사용 사례

| 사용 사례 | 적용 방식 |
|----------|-----------|
| 새 library 도입 | 1일 spike로 API surface, failure mode, security note 확인 |
| 레거시 수정 | behavior change 전 작은 tidying commit 분리 |
| 기능 개발 | TDD test list로 scope를 작게 나누고 한 번에 하나씩 통과 |
| PR 리뷰 | formatting/refactor/behavior change가 섞였는지 확인 |
| AI agent 작업 | 작은 task, 좁은 context, test-first, human review, rollback 가능한 commit 단위 |

---

## 관련 노트

- [[study/tech/ai/lazy-codex]] - AI coding agent에게 작은 task와 검증 기준을 주는 방식
- [[study/tech/ai/agent-orchestration/cli-agents]] - CLI agent 작업을 spike와 feedback loop로 운영하기
- [[study/tech/ai/mitchellh-ai-adoption-study]] - AI adoption에서 개발자 역할 변화 비교

---

## References

- [Kent Beck 공식 사이트](https://kentbeck.com/)
- [Software Design: Tidy First? newsletter](https://newsletter.kentbeck.com/)
- [Canon TDD by Kent Beck](https://newsletter.kentbeck.com/p/canon-tdd)
- [Agile Manifesto](https://agilemanifesto.org/)
