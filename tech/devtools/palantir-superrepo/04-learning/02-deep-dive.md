---
date: 2026-08-17
tags: [tech]
type: tech-tool-study
status: draft
---

# Palantir SuperRepo — Deep Dive

> [[01-getting-started|이전: Getting Started]] · [[../README|목차로 돌아가기]] · [[../05-projects|다음: Projects]]

## 1. Ontology가 dependency graph의 중심인 이유

일반 monorepo의 graph는 package import와 build task를 중심으로 계산된다. SuperRepo에서는 여기에 operational semantics가 추가된다.

```text
dataset / transform
        ↓ supplies
   Object Type ← Link Type → Object Type
        ↓ read/edit
 Function ── Action ── Agent tool
        ↓                  ↓
       OSDK React application
```

| 변경 | 잠재 consumer | 대표 위험 |
|---|---|---|
| property type 변경 | Function, UI, Agent tool | compile error 또는 runtime validation failure |
| Object API name 변경 | generated binding 전체 | import/query breakage |
| Link cardinality 변경 | query와 UI state | 단일 object/list 가정 불일치 |
| Action parameter 변경 | UI form, Agent tool | 호출 contract 불일치 |
| permission 변경 | Function/Action/Agent runtime | local success와 remote denial 차이 |

## 2. Generated binding의 역할과 한계

Generated, type-safe binding은 schema와 consumer 사이의 drift를 compile/test 단계로 당긴다. 그러나 모든 의미 오류를 막지는 못한다.

- type system이 찾기 쉬움: property 삭제, type/API name 변경, Action signature 변경
- 별도 test가 필요함: enum의 업무 의미, permission, data quality, prompt behavior, network integration
- production 검증이 필요함: 실제 data volume, indexing latency, governance policy, external system side effect

> [!important]
> type-safe는 “올바른 업무 결정”을 보장하지 않는다. contract consistency와 semantic correctness를 분리해서 테스트한다.

## 3. Local embedded Ontology의 feedback boundary

### 로컬에서 얻고 싶은 feedback

- Object/Link/Action model이 application logic과 맞는가?
- generated type이 Function과 frontend를 일관되게 연결하는가?
- Agent가 허용된 tool을 올바른 parameter로 선택하는가?
- UI가 query, loading, empty, error, Action confirmation state를 처리하는가?

### remote에서 다시 확인해야 할 것

- 실제 authorization과 marking/organization policy
- production-scale data와 indexing behavior
- external connection, secret, network policy
- publish/import/deploy ordering과 rollback
- observability, audit, operational support process

기존 embedded Ontology 문서의 `lohi-ts`와 WebAssembly 기반 pattern은 기술적 배경을 설명하지만, 그것이 SuperRepo 내부 구현과 1:1로 동일하다고 단정하지 않는다.

## 4. Change propagation 분석

예: `Incident.escalationReason`을 추가한다.

```text
1. Ontology schema
   └── property/API contract 추가
2. Generated bindings
   ├── Function type
   └── OSDK client type
3. Operational logic
   ├── triage Function
   └── escalate Action validation
4. Agent
   ├── prompt에 판단 기준 추가
   └── Action tool argument 추가
5. Frontend
   ├── form field
   └── alert/detail rendering
6. Tests
   ├── contract + unit
   ├── Agent tool selection
   └── end-to-end scenario
```

좋은 review는 파일 수보다 이 propagation chain의 누락을 찾는다.

## 5. Agent safety를 별도 축으로 보기

Agent가 Ontology Action을 호출할 수 있다면 correctness 외에 authority가 중요하다.

| Control | 질문 |
|---|---|
| Tool scope | 필요한 Object/Action만 노출했는가? |
| Read/write 분리 | 추천과 실행이 구분되는가? |
| Confirmation | irreversible/high-impact Action 전에 사람 확인이 있는가? |
| Validation | prompt가 아니라 Action/Function layer에서도 검증하는가? |
| Audit | 누가 어떤 input으로 Action을 실행했는지 추적 가능한가? |
| Failure | timeout, partial failure, duplicate call을 안전하게 처리하는가? |

## 6. Deployment를 해석할 때의 주의

“defined and deployed together”는 관련 artifact가 하나의 developer workflow에 포함된다는 뜻으로 읽는 것이 안전하다. 다음은 별도 공식 보장이 필요하다.

- 모든 resource가 단일 transaction으로 배포되는가?
- 중간 실패 시 이미 적용된 resource는 되돌아가는가?
- affected resource만 배포할 수 있는가?
- environment별 config와 secret overlay는 어떻게 표현되는가?
- branch preview와 production promotion이 같은 artifact identity를 유지하는가?

## 7. Architecture review 질문

- Ontology가 stable domain contract인가, UI 편의를 위해 과도하게 흔들리는가?
- pipeline output과 Object Type 사이 data quality contract가 있는가?
- Action이 업무 불변식과 permission을 중앙에서 강제하는가?
- Agent 없이도 Function/Action을 deterministic하게 테스트할 수 있는가?
- local model과 remote integration test의 책임이 명확한가?
- repository 통합이 팀 ownership과 blast radius를 불필요하게 키우지 않는가?

## Sources

- https://www.palantir.com/devcon/
- https://www.palantir.com/docs/foundry/superrepo/overview
- https://www.palantir.com/docs/foundry/ontology/core-concepts
- https://www.palantir.com/docs/foundry/developer-console/create-embedded-ontology-application
- https://www.palantir.com/docs/foundry/functions/functions-on-objects
- https://www.palantir.com/docs/foundry/agents/overview
