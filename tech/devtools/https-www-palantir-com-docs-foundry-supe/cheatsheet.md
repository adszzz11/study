---
date: 2026-08-17
tags: [tech]
type: tech-tool-study
status: draft
---

# Palantir SuperRepo — Cheatsheet

> [[05-projects|이전: Projects]] · [[README|목차로 돌아가기]]

## 한눈에 보기

| 항목 | 요약 |
|---|---|
| 정체 | Foundry-native full-stack pro-code monorepo |
| 중심 계약 | Ontology Object/Link/Action Type |
| 포함 범위 | pipeline, Ontology, Python/TypeScript Functions, Actions, Agents, React + OSDK |
| 변경 단위 | schema부터 UI까지의 vertical slice |
| local loop | embedded Ontology를 이용한 contract/application 검증 |
| 배포 | Foundry resource를 함께 정의·배포하는 workflow |
| 비교 대상 | Code Repositories, Databricks Bundles, Nx, Turborepo, multi-repo CI/CD |

## 핵심 흐름

```text
pipeline
  ↓
Ontology contract
  ├── Function / Action
  ├── Agent tool
  └── React + OSDK
          ↓
local validation → remote preview/deploy → production verification
```

## Change checklist

### Schema

- [ ] Object/Link/Action의 API name과 의미가 안정적인가?
- [ ] nullability, cardinality, enum/lifecycle이 명시적인가?
- [ ] generated binding을 공식 workflow로 갱신했는가?

### Consumers

- [ ] Function input/output와 Ontology edit를 갱신했는가?
- [ ] Action parameter, validation, permission을 갱신했는가?
- [ ] Agent prompt/tool schema와 authority를 갱신했는가?
- [ ] OSDK query/call site와 UI state를 갱신했는가?

### Tests

- [ ] contract/compile test
- [ ] Function unit test
- [ ] Agent tool-selection 및 safety test
- [ ] UI interaction test
- [ ] local end-to-end scenario
- [ ] remote permission/integration test

## Local vs Remote

| Local에서 우선 확인 | Remote에서 반드시 재확인 |
|---|---|
| schema-consumer 일관성 | 실제 permission/marking |
| generated type 오류 | production data volume/index |
| Function/Agent/UI 연결 | external connection/network |
| synthetic scenario | publish/deploy/rollback behavior |

## Go / No-Go

| 질문 | Yes라면 |
|---|---|
| 하나의 feature가 3개 이상의 Foundry layer를 함께 바꾸는가? | SuperRepo 검토 |
| Ontology drift가 반복되는가? | SuperRepo 검토 |
| 독립 release/ownership이 더 중요한가? | multi-repo 유지 검토 |
| 핵심이 generic build cache/affected task인가? | Nx/Turborepo 검토 |
| 핵심이 Databricks workspace DataOps/MLOps인가? | Bundles 검토 |

## 주장 강도

### 공개 근거로 말할 수 있음

- end-to-end pro-code monorepo를 지향한다.
- data pipeline, Ontology primitives, application artifact를 함께 다룬다.
- DevCon 6에서 local embedded Ontology와 schema/logic/frontend/Agent 연속 변경을 시연했다.
- Ontology binding은 Functions와 OSDK consumer의 type-safe contract 역할을 한다.

### 아직 단정하지 않음

- 공식 CLI command와 manifest schema
- atomic deploy/rollback 보장
- affected/partial deployment
- branch별 ephemeral Ontology
- environment overlay syntax
- remote build cache와 repository limit

## 공식 문서 바로가기

- [SuperRepo overview](https://www.palantir.com/docs/foundry/superrepo/overview)
- [DevCon](https://www.palantir.com/devcon/)
- [Ontology core concepts](https://www.palantir.com/docs/foundry/ontology/core-concepts)
- [Functions on Objects](https://www.palantir.com/docs/foundry/functions/functions-on-objects)
- [Foundry Agents](https://www.palantir.com/docs/foundry/agents/overview)
- [Embedded Ontology application](https://www.palantir.com/docs/foundry/developer-console/create-embedded-ontology-application)

## Sources

- https://www.palantir.com/docs/foundry/superrepo/overview
- https://www.palantir.com/devcon5/
- https://www.palantir.com/devcon/
- https://www.palantir.com/docs/foundry/ontology/core-concepts
- https://www.palantir.com/docs/foundry/functions/functions-on-objects
- https://www.palantir.com/docs/foundry/agents/overview
