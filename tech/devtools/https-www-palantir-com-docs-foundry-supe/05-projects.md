---
date: 2026-08-17
tags: [tech]
type: tech-tool-study
status: draft
---

# Palantir SuperRepo — Projects

> [[04-learning/02-deep-dive|이전: Deep Dive]] · [[README|목차로 돌아가기]] · [[cheatsheet|다음: Cheatsheet]]

## Project 1. Incident Triage Vertical Slice

### 목표

한 Incident workflow를 통해 schema, Function, Action, Agent, React UI가 하나의 contract로 움직이는지 검증한다.

### 범위

```text
synthetic incidents
  → Incident Object Type
  → triage Function
  → assign/escalate Action
  → triage Agent
  → operator React UI
```

### Milestone

- [ ] `Incident`, `Person` Object Type과 assignment Link 정의
- [ ] severity/status/assignment 업무 규칙 문서화
- [ ] deterministic triage Function과 unit scenario 작성
- [ ] assign/escalate Action에 validation과 permission 적용
- [ ] Agent는 추천만 하고 write는 사람 확인 후 실행하도록 구성
- [ ] React UI에서 추천 근거, Action preview, failure state 표시
- [ ] local contract test 후 remote permission/integration 확인

### Acceptance scenario

| 입력 | 기대 결과 |
|---|---|
| Critical incident, 미할당 | urgent 분류와 담당자 후보 제시 |
| 유효하지 않은 담당자 | Action layer가 거부 |
| 권한 없는 operator | write 금지와 설명 가능한 error |
| Agent timeout | UI는 수동 triage path 유지 |
| 같은 Action 재시도 | 중복 side effect 방지 여부 검증 |

## Project 2. Schema Change Impact Map

### 목표

Ontology 변경 하나가 어떤 consumer에 전파되는지 review artifact로 만든다.

```text
Action parameter change
├── Function implementation
├── Agent tool definition/prompt
├── OSDK call site
├── React form
└── unit/integration/e2e tests
```

### 산출물

- dependency matrix
- breaking/non-breaking change 분류
- generated binding refresh 확인 결과
- local/remote test 책임표
- deployment와 rollback의 미확인 가정 목록

## Project 3. 기존 분산 application의 Migration Spike

### 목표

전체 migration 전에 한 vertical slice만 옮겨 SuperRepo의 가치와 비용을 측정한다.

### 비교 지표

| 지표 | 기존 방식 | Spike 후 |
|---|---:|---:|
| 관련 repository 수 | 기록 | 기록 |
| schema-to-UI feedback time | 기록 | 기록 |
| manual import/version step | 기록 | 기록 |
| local에서 잡힌 contract defect | 기록 | 기록 |
| remote-only defect | 기록 | 기록 |
| review에 필요한 context switch | 기록 | 기록 |

### 중단 기준

- required resource type이 SuperRepo에서 지원되지 않는다.
- team access boundary를 한 repository에 표현할 수 없다.
- local model이 핵심 integration을 충분히 대표하지 못한다.
- migration cost가 coordination reduction보다 크다.

## Project 4. Agent Governance Test Harness

### 목표

Agent prompt 품질만이 아니라 tool authority와 Action safety를 검증한다.

- [ ] read-only 질문은 write tool을 선택하지 않는다.
- [ ] write 요청은 대상, parameter, 영향 범위를 확인한다.
- [ ] high-impact Action은 confirmation 없이는 실행하지 않는다.
- [ ] Function/Action layer가 prompt와 독립적으로 업무 규칙을 강제한다.
- [ ] permission denial, timeout, duplicate request를 테스트한다.
- [ ] audit에 필요한 actor, input, result를 남긴다.

## 회고 질문

- repository 통합이 실제 lead time을 줄였는가?
- compile/test feedback으로 이동한 defect는 무엇인가?
- 여전히 remote에서만 발견되는 failure는 무엇인가?
- Ontology contract owner와 application owner의 review 책임이 명확한가?
- production promotion/rollback에 남은 불확실성은 무엇인가?

## Sources

- https://www.palantir.com/devcon/
- https://www.palantir.com/docs/foundry/superrepo/overview
- https://www.palantir.com/docs/foundry/ontology/core-concepts
- https://www.palantir.com/docs/foundry/functions/functions-on-objects
- https://www.palantir.com/docs/foundry/agents/overview
