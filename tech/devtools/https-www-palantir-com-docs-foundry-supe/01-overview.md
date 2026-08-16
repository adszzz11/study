---
date: 2026-08-17
tags: [tech]
type: tech-tool-study
status: draft
---

# Palantir SuperRepo — What, Why, 특징

> [[README|목차로 돌아가기]] · [[02-ecosystem|다음: Ecosystem]]

## What

SuperRepo는 Foundry full-stack application의 data pipeline, Ontology primitives, Functions, Actions, Agents, frontend를 한 Git monorepo에서 정의하고 개발하는 Foundry-native 환경이다.

```text
SuperRepo
├── data pipelines / transforms
├── ontology
│   ├── object types / link types
│   ├── schema / properties
│   └── action types
├── functions
│   ├── Python
│   └── TypeScript
├── agents
└── frontend
    └── React + OSDK
```

여기서 Ontology는 database ORM schema와 다르다. Foundry는 실제 entity와 event를 **Object Type**, 관계를 **Link Type**, 사용자가 실행할 수 있는 변경 operation을 **Action Type**으로 모델링한다. 이 model이 application layer의 공통 contract가 된다.

## Why

### 기존 pro-code workflow의 분산

| 관심사 | 주로 위치하던 개발 표면 |
|---|---|
| Data transform | Python/Java/SQL Code Repository |
| Business semantic model | Ontology Manager |
| Operational logic | Functions, Actions |
| UI | Workshop 또는 OSDK React application |
| Agent | agent-template repository |

각 표면은 자체 build, release/tag, import, deployment lifecycle을 가질 수 있다. 독립 배포에는 유리하지만 하나의 기능이 여러 표면을 관통하면 coordination cost가 커진다.

### 해결하려는 문제

- 연결된 변경이 여러 repository와 application에 흩어진다.
- artifact version, import order, compatibility를 사람이 조정해야 한다.
- frontend OSDK type과 실제 Ontology schema 사이에 drift가 생길 수 있다.
- 전체 workflow 검증을 위해 remote CI/build/deployment를 반복하게 된다.
- coding agent가 여러 UI와 repository의 context를 오가야 한다.

SuperRepo는 이를 **단일 source of truth**, **한 변경 단위**, **짧은 local feedback loop**로 바꾸려는 접근이다.

## 핵심 특징

### 1. Full-stack, Ontology-first monorepo

repository의 중심 계약은 Ontology다. pipeline이 object에 공급할 data를 만들고, Functions/Actions가 object를 읽거나 수정하며, React와 Agent가 같은 domain model을 사용한다.

### 2. Vertical slice를 하나의 변경으로 표현

```text
Incident.severity property 추가
  → triage Function 갱신
  → Action parameter 추가
  → Agent tool/prompt 갱신
  → React form·alert UI 갱신
```

같은 branch에서 계약과 consumer를 함께 수정하면 review가 feature의 end-to-end 의미를 볼 수 있다. 다만 “같은 repository”가 곧 “production에서 완전히 atomic한 배포”를 뜻하지는 않는다.

### 3. Local embedded Ontology

- remote Foundry deployment 전 Object/Link/Action semantics를 로컬에서 실행한다.
- schema와 generated type binding을 빠르게 검증한다.
- Function, Agent, frontend가 같은 local model을 대상으로 동작하게 한다.
- 매 변경마다 전체 remote CI/deployment를 기다리는 횟수를 줄인다.

기존 embedded Ontology application 문서에는 `@palantir/lohi-ts`, Vite plugin, WebAssembly 기반 local/offline client와 sync pattern이 나온다. SuperRepo가 같은 package와 설정을 그대로 노출하는지는 공개 근거만으로 확정할 수 없다.

### 4. Generated, type-safe contract

| Consumer | Ontology contract 활용 |
|---|---|
| Functions | Object/Object Set parameter, search, Ontology edit |
| React + OSDK | object query, aggregation, Action 호출 |
| Agent | scoped OSDK 또는 Ontology/MCP tool을 통한 interaction |

schema 변경은 generated binding을 통해 consumer의 compile/test 단계에 드러날 수 있다. 즉 runtime drift 일부를 더 이른 feedback으로 바꾸는 구조다.

### 5. Agent-native development

pro-code Agent의 prompt, tools, OSDK client, MCP configuration을 application code와 가까이 둔다. Agent가 publish되면 Ontology binding과 API name을 통해 Workshop, OSDK, Actions, Automate 등에서 호출할 수 있다. SuperRepo에서는 Agent 정의와 그 도구가 의존하는 schema·Functions·UI를 한 context에서 추적할 수 있다.

### 6. Foundry-native deployment와 governance

SuperRepo는 generic build orchestrator가 아니라 Foundry resource를 함께 정의·배포하는 developer platform에 가깝다. Foundry의 security와 governance context 안에서 artifact 관계를 다루는 것이 범용 monorepo 도구와의 핵심 차이다.

## 공개 정보로 확정하지 않는 항목

- deployment atomicity와 rollback의 정확한 범위
- partial/affected deployment 지원 여부
- branch별 ephemeral Ontology 생성 방식
- production promotion과 environment overlay 문법
- repository size 또는 artifact 수 제한
- Nx/Turborepo 같은 remote build cache 제공 여부

## Sources

- https://www.palantir.com/docs/foundry/superrepo/overview
- https://www.palantir.com/devcon5/
- https://www.palantir.com/devcon/
- https://www.palantir.com/docs/foundry/ontology/core-concepts
- https://www.palantir.com/docs/foundry/developer-console/create-embedded-ontology-application
- https://www.palantir.com/docs/foundry/functions/functions-on-objects
- https://www.palantir.com/docs/foundry/agents/overview
