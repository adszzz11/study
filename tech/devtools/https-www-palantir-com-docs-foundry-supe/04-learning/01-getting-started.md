---
date: 2026-08-17
tags: [tech]
type: tech-tool-study
status: draft
---

# Palantir SuperRepo — Getting Started

> [[../03-references|이전: References]] · [[../README|목차로 돌아가기]] · [[02-deep-dive|다음: Deep Dive]]

## 시작 전 전제

SuperRepo의 공개 CLI와 manifest를 확인하지 못했으므로 아래는 실행 명령이 아니라 **안전한 학습 절차**다. 실제 enrollment에서 보이는 공식 template/guide를 우선하고 임의의 command나 schema를 만들지 않는다.

## 1. 접근성과 범위 확인

- [ ] 조직의 Foundry enrollment에서 SuperRepo 기능이 활성화되어 있는가?
- [ ] repository 생성, Ontology edit, Function/Agent publish, application deploy 권한이 있는가?
- [ ] development Ontology와 production Ontology의 boundary가 분리되어 있는가?
- [ ] 사용할 language/runtime version이 공식 지원 범위인가?
- [ ] local embedded Ontology에서 사용할 test data에 민감 정보가 포함되지 않는가?

## 2. 작은 vertical slice 선택

처음부터 대형 application을 옮기기보다 한 Object Type과 한 use case를 고른다.

```text
Incident object 읽기
  → severity 기반 triage Function
  → Assign action
  → Agent가 추천 담당자 제안
  → React 화면에서 검토·실행
```

### 완료 조건

| Layer | 최소 산출물 | 확인할 것 |
|---|---|---|
| Data | 작은 synthetic Incident fixture | key, nullability, freshness |
| Ontology | Incident Object Type과 필요한 Link | API name, property type, relation |
| Logic | side effect가 제한된 triage Function | input/output와 error behavior |
| Action | 명시적인 assignment operation | parameter, permission, validation |
| Agent | 좁은 tool scope와 prompt | tool selection, unsafe action 방지 |
| UI | object 조회와 Action 확인 화면 | generated type, loading/error state |

## 3. Contract를 먼저 그리기

```text
Incident
├── id: primary key
├── severity: enum/string
├── status: lifecycle state
├── assignedTo → Person
└── action: assignIncident(person, reason)
```

- schema field의 의미와 owner를 적는다.
- write operation은 Action으로 명시하고 validation과 permission을 기록한다.
- Function, Agent, UI가 어떤 property와 Action에 의존하는지 표로 만든다.
- API name 변경은 source rename보다 넓은 breaking change로 취급한다.

## 4. Local validation loop 설계

```text
schema edit
  → binding 갱신
  → Function test
  → Agent tool test
  → React interaction test
  → integration check
  → remote preview/deploy
```

구체 명령은 실제 SuperRepo template의 README와 generated scripts에서 확인한다. 이 순서의 목적은 schema change가 모든 consumer에 전파되는지 remote deploy 전에 찾는 것이다.

## 5. Test scenario

| Scenario | 기대 결과 |
|---|---|
| severity가 `critical` | triage 결과가 urgent이며 UI alert가 보임 |
| 담당자 없음 | Agent는 후보를 제안하되 Action을 무단 실행하지 않음 |
| Action permission 없음 | UI와 Agent 모두 명확한 failure를 표시 |
| schema property rename | stale binding/consumer가 compile 또는 test에서 탐지됨 |
| remote service unavailable | local model의 가능 범위와 실제 integration 실패가 구분됨 |

## 6. 첫 review 체크리스트

- [ ] diff가 schema → logic → Agent → UI의 연결을 보여주는가?
- [ ] generated file을 수동 편집하지 않았는가?
- [ ] Agent tool scope가 최소 권한인가?
- [ ] synthetic/local data와 production data를 혼동하지 않는가?
- [ ] local success를 production integration 성공으로 과장하지 않는가?
- [ ] deployment와 rollback 절차를 실제 enrollment 문서로 확인했는가?

## 막히면 확인할 곳

- feature availability와 bootstrap: SuperRepo overview 또는 Palantir support/admin
- domain modeling: Ontology core concepts
- Object edit: Functions on Objects
- Agent publish/invocation: Foundry Agents overview
- offline/local sync: embedded Ontology application guide

## Sources

- https://www.palantir.com/docs/foundry/superrepo/overview
- https://www.palantir.com/docs/foundry/ontology/core-concepts
- https://www.palantir.com/docs/foundry/functions/functions-on-objects
- https://www.palantir.com/docs/foundry/agents/overview
- https://www.palantir.com/docs/foundry/developer-console/create-embedded-ontology-application
