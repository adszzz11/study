---
date: 2026-08-17
tags: [tech]
type: tech-tool-study
status: draft
---

# Palantir SuperRepo

> **한 줄 정의**: Palantir SuperRepo는 data pipeline, Ontology schema·Actions, Python/TypeScript Functions, React frontend와 pro-code Agent를 하나의 Git monorepo에서 로컬 개발하고 일관되게 배포하는 Foundry-native full-stack DevOps 환경이다.

## Overview

SuperRepo는 Foundry의 여러 개발 표면에 흩어지기 쉬운 data, semantic model, operational logic, UI, Agent를 하나의 source of truth로 묶는다. 핵심은 단순한 monorepo 폴더 구조가 아니라 다음 세 요소의 결합이다.

- **Ontology-first contract**: Object Type, Link Type, Action Type이 Functions, OSDK frontend, Agent를 잇는 도메인 계약이 된다.
- **vertical slice change**: schema부터 UI까지 연결된 변경을 같은 branch와 commit에서 다룬다.
- **local embedded Ontology**: remote deployment 전에 로컬에서 Ontology semantics와 consumer code를 함께 검증해 feedback loop를 줄인다.

```text
data pipeline → Ontology → Functions / Actions → Agent → React + OSDK
       └──────────── 하나의 repository와 변경 단위 ────────────┘
```

> [!warning] 조사 범위
> 조사 기준은 2026-08-17이다. 지정된 overview 페이지의 본문을 공개 검색에서 직접 확인하지 못했으므로 DevCon 5·6 발표와 관련 Foundry 공식 문서를 교차 검증했다. CLI, manifest schema, atomic deployment/rollback 보장은 이 노트에서 추정하지 않는다.

## Learning Path

- [ ] [[01-overview|1. Overview]] — What/Why와 핵심 특징 이해
- [ ] [[02-ecosystem|2. Ecosystem]] — 기존 Foundry 개발 방식과 범용 monorepo/DataOps 대안 비교
- [ ] [[03-references|3. References]] — 근거 수준별 공식 자료 읽기
- [ ] [[04-learning/01-getting-started|4. Getting Started]] — 접근 권한과 첫 vertical slice 계획
- [ ] [[04-learning/02-deep-dive|5. Deep Dive]] — contract propagation, local validation, deployment 경계 분석
- [ ] [[05-projects|6. Projects]] — incident triage 예제로 학습 산출물 만들기
- [ ] [[cheatsheet|7. Cheatsheet]] — 개념, 검증 질문, 의사결정 빠른 참조

## When To Use

- Foundry 위에서 pipeline, Ontology, Functions/Actions, Agent, React application을 함께 개발할 때
- Object/Action schema 변경이 여러 consumer에 연쇄 영향을 주는 operational application을 만들 때
- 중간 remote build/deployment를 반복하기 전에 end-to-end 동작을 로컬에서 확인하고 싶을 때
- AI coding agent가 전체 dependency context를 한 codebase에서 탐색해야 할 때
- 여러 artifact의 version/import 순서를 사람이 조율하는 비용이 커졌을 때

## When Not To Use

- 독립적인 transform이나 Function package 하나만 관리하면 충분할 때
- Foundry Ontology나 Foundry deployment semantics를 사용하지 않는 범용 monorepo일 때
- 조직의 repository ownership, access boundary, release cadence가 의도적으로 분리되어야 할 때
- local embedded Ontology가 실제 production data volume, 권한, integration을 완전히 재현한다고 가정해야만 테스트가 성립할 때
- 공개 문서로 확인되지 않은 rollback, affected build, environment overlay 기능이 필수 요구사항일 때

## Related Notes

- [[MOCs/Index]]
- [[MOCs/Devtools]]
- [[tech/devtools/ripgrep/README|ripgrep]] — monorepo에서 schema와 consumer 사용처를 추적하는 lexical search 도구

## Sources

- https://www.palantir.com/docs/foundry/superrepo/overview
- https://www.palantir.com/devcon5/
- https://www.palantir.com/devcon/
- https://www.palantir.com/docs/foundry/code-repositories/overview/index.html
- https://www.palantir.com/docs/foundry/ontology/core-concepts
- https://www.palantir.com/docs/foundry/developer-console/create-embedded-ontology-application
- https://www.palantir.com/docs/foundry/functions/functions-on-objects
- https://www.palantir.com/docs/foundry/agents/overview
