---
date: 2026-08-17
tags: [tech]
type: tech-tool-study
status: draft
---

# Palantir SuperRepo — References

> [[02-ecosystem|이전: Ecosystem]] · [[README|목차로 돌아가기]] · [[04-learning/01-getting-started|다음: Getting Started]]

## 근거 읽는 법

| 등급 | 의미 | 이 노트에서의 사용 |
|---|---|---|
| A | SuperRepo를 직접 다루는 공식 문서·발표 | 제품 범위와 의도 설명 |
| B | 관련 Foundry component의 공식 문서 | Ontology, Functions, Agents의 확인된 동작 설명 |
| C | 공식 경쟁 제품 문서 | ecosystem 비교 |
| 미확인 | 공개 본문이나 schema로 검증되지 않음 | 질문 목록으로만 유지 |

## A — SuperRepo 직접 자료

- [SuperRepo overview](https://www.palantir.com/docs/foundry/superrepo/overview) — 지정된 진입점. 조사 시점에는 공개 검색에서 본문을 직접 확인하지 못했다.
- [Palantir DevCon 5](https://www.palantir.com/devcon5/) — data pipelines, Ontology primitives, application artifacts를 포함하는 end-to-end pro-code monorepo 공개 맥락.
- [Palantir DevCon](https://www.palantir.com/devcon/) — DevCon 6 SuperRepo와 local embedded Ontology 시연 맥락.

## B — Foundry 구성요소

- [Code Repositories overview](https://www.palantir.com/docs/foundry/code-repositories/overview/index.html) — Git, branch, PR, preview, build, release와 repository type의 기준선.
- [Ontology core concepts](https://www.palantir.com/docs/foundry/ontology/core-concepts) — Object Type, Link Type, Action Type 개념.
- [Create an embedded Ontology application](https://www.palantir.com/docs/foundry/developer-console/create-embedded-ontology-application) — `lohi-ts`, WebAssembly, offline/local sync pattern.
- [Functions on Objects](https://www.palantir.com/docs/foundry/functions/functions-on-objects) — Ontology object 검색, parameter, edit 관련 Function model.
- [Foundry Agents overview](https://www.palantir.com/docs/foundry/agents/overview) — pro-code Agent, tool, Ontology binding과 호출 모델.

## C — 비교 제품

- [Databricks Declarative Automation Bundles](https://docs.databricks.com/aws/en/dev-tools/bundles/) — source와 workspace resource를 묶는 DataOps/MLOps IaC.
- [Nx Project Graph](https://nx.dev/features/explore-graph) / [Remote Cache](https://nx.dev/ci/features/remote-cache) — 범용 monorepo dependency와 cache 비교.
- [Turborepo Internal Packages](https://turborepo.com/docs/core-concepts/internal-packages) / [Remote Caching](https://turborepo.com/docs/core-concepts/remote-caching) — JS/TS workspace와 task cache 비교.

## 공개 확인이 필요한 질문

- [ ] 지원되는 repository bootstrap 절차와 prerequisite는 무엇인가?
- [ ] 공식 directory layout과 manifest schema는 무엇인가?
- [ ] local embedded Ontology가 지원하는 Object/Link/Action capability와 제한은 무엇인가?
- [ ] local test data, remote sync, credential은 어떻게 분리하는가?
- [ ] generated binding은 언제, 어떤 명령 또는 build 단계에서 갱신되는가?
- [ ] deploy가 resource 전체에 atomic한가, resource별로 순차적인가?
- [ ] rollback과 failed partial deployment의 보장은 무엇인가?
- [ ] branch/preview environment 및 production promotion model은 무엇인가?
- [ ] affected deployment나 remote build cache가 있는가?
- [ ] repository/artifact size 및 language/version 제한은 무엇인가?

## 권장 읽기 순서

1. DevCon 발표로 SuperRepo가 해결하려는 workflow를 본다.
2. Ontology core concepts로 중심 contract를 이해한다.
3. Functions와 Agents 문서로 consumer model을 확인한다.
4. embedded Ontology 문서로 local/offline pattern과 제한을 읽는다.
5. Code Repositories를 기준선으로 두고 migration cost를 비교한다.
6. SuperRepo overview 본문에 접근할 수 있을 때 미확인 질문을 하나씩 닫는다.

## Sources

- https://www.palantir.com/docs/foundry/superrepo/overview
- https://www.palantir.com/devcon5/
- https://www.palantir.com/devcon/
- https://www.palantir.com/docs/foundry/code-repositories/overview/index.html
- https://www.palantir.com/docs/foundry/ontology/core-concepts
- https://www.palantir.com/docs/foundry/developer-console/create-embedded-ontology-application
- https://www.palantir.com/docs/foundry/functions/functions-on-objects
- https://www.palantir.com/docs/foundry/agents/overview
- https://docs.databricks.com/aws/en/dev-tools/bundles/
- https://nx.dev/
- https://turborepo.com/docs
