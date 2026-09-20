---
date: 2026-07-30
tags: [tech]
type: tech-tool-study
status: draft
---

# Backstage: What, Why, 특징

> [[README|목차로 돌아가기]] · [[02-ecosystem|다음: Ecosystem 비교]]

## What

Backstage는 조직이 자신만의 Internal Developer Portal(IDP)을 만들기 위한 Apache-2.0 open-source TypeScript framework다. 중앙의 Software Catalog와 composable plugin architecture를 토대로 documentation, software creation, search, infrastructure visibility를 일관된 UX에 결합한다.

Backstage의 위치를 정확히 잡는 것이 중요하다.

| Backstage가 하는 일 | Backstage가 아닌 것 |
|---|---|
| 기존 도구의 metadata와 링크를 entity 중심으로 통합 | CI/CD engine |
| owner, dependency, lifecycle의 discoverability 제공 | Kubernetes control plane |
| golden path를 form과 workflow로 제공 | 범용 workflow engine의 완전한 대체 |
| 조직별 plugin과 policy를 담는 portal framework | 설치 즉시 완성되는 SaaS 제품 |

Spotify에서 microservice 증가와 tooling fragmentation을 해결하기 위해 시작됐다. 2019년 첫 commit 이후 2020년 CNCF에 기부되었고, 2020-09-08 CNCF에 합류해 2022-03-15부터 조사 기준일 현재까지 Incubating 단계다.

## Why

### 규모가 커질 때 반복되는 문제

- 어느 team이 어떤 service, API, database를 소유하는지 불명확해진다.
- GitHub, CI/CD, Kubernetes, observability, incident, security UI가 분산된다.
- 새 project마다 repository, pipeline, IaC와 monitoring을 다시 조립한다.
- architecture와 runbook이 wiki, repository와 개인 기억에 흩어진다.
- 문서로 배포한 표준은 실제 생성 과정에서 빠지기 쉽다.
- 장애 시 dependency, owner, dashboard와 runbook을 찾는 시간이 길어진다.

### Backstage의 해결 방식

1. SCM, 조직 directory, cloud와 custom provider에서 metadata를 수집한다.
2. 모든 대상을 표준화된 entity와 relation으로 표현한다.
3. entity page에 문서, 배포 상태, dashboard와 action을 모은다.
4. Software Template에 조직 표준을 실행 가능한 golden path로 넣는다.
5. Search와 plugin으로 portal의 탐색 범위를 확장한다.

### 기대 가치

| 가치 | 구체적 결과 |
|---|---|
| Discoverability | service, API, owner, dependency를 한곳에서 탐색 |
| Reduced cognitive load | 여러 운영 도구의 정보를 entity page에 결합 |
| Standardization | security, CI/CD, IaC 기본값을 template에 내장 |
| Self-service | repository 생성과 Catalog 등록을 승인된 workflow로 제공 |
| Documentation | code와 함께 versioning되는 docs-like-code |
| Extensibility | 사내 시스템도 custom plugin/action/provider로 연결 |

## 핵심 특징

### 1. Software Catalog와 entity graph

Catalog는 `Component`만이 아니라 `API`, `Resource`, `System`, `Domain`, `Group`, `User`, `Template`, `Location` 등을 entity로 표현한다. 식별자는 `kind:namespace/name`이며 namespace의 기본값은 `default`다.

```yaml
apiVersion: backstage.io/v1alpha1
kind: Component
metadata:
  name: payments-api
  description: Payment authorization service
  annotations:
    github.com/project-slug: acme/payments-api
    backstage.io/techdocs-ref: dir:.
spec:
  type: service
  lifecycle: production
  owner: group:default/payments
  system: checkout
  providesApis:
    - payments
  dependsOn:
    - resource:default/payments-db
```

`owner`, `partOf`, `dependsOn`, `providesApi`, `consumesApi` 같은 relation을 통해 목록이 software graph가 된다. repository의 `catalog-info.yaml`을 source of truth로 둘 수 있어 team은 일반 Git workflow로 metadata를 관리한다.

### 2. Composable plugin architecture

| 층 | 역할 |
|---|---|
| Frontend | React SPA, pages/cards/routes, frontend plugins와 extensions |
| Backend | Node.js backend plugins, modules, extension points, shared services |
| Data | plugin별 schema를 사용하는 PostgreSQL 중심 persistent storage |

Backend plugin은 독립 기능 단위이고 module은 extension point를 통해 기존 plugin을 확장한다. 규모와 장애 격리가 필요하면 backend plugins를 여러 deployment unit으로 나눌 수 있다.

2026년 신규 app은 new frontend system을 기본으로 생성한다. 일부 community plugin은 legacy frontend API에 머물러 있으므로 package version뿐 아니라 frontend system 호환성도 확인한다.

### 3. Software Templates / Scaffolder

`Template` entity는 JSON Schema 기반 input form과 실행 `steps`를 선언한다.

- code skeleton fetch와 variable rendering
- GitHub/GitLab repository 생성
- pull/merge request 발행
- Catalog 자동 등록
- Terraform, CI/CD, ticket, cloud API를 호출하는 custom action
- dry-run, task log, cancellation과 permission

Template action은 외부 시스템을 변경한다. 따라서 input validation, least privilege, secret scope, idempotency, audit log와 실패 시 보상/rollback 전략이 필요하다.

### 4. TechDocs

TechDocs는 Markdown과 MkDocs에 기반한 docs-like-code다. 개발 기본 설정은 backend local filesystem을 사용하지만 production 권장 구조는 build와 serve를 분리한다.

```text
Repository Markdown
        ↓ CI: techdocs-cli / MkDocs
Generated static site
        ↓
S3 / GCS / Azure Blob
        ↓
techdocs-backend → TechDocs Reader
```

CI build + object storage 방식은 horizontal scaling, persistence와 page load 측면에서 유리하다.

### 5. Search

Search는 Catalog entity와 TechDocs를 포함해 plugin이 제공하는 content를 통합 검색하는 extensible platform이다. 각 collator가 content를 수집하고 scheduler가 index를 갱신하며, query는 configured search engine을 통한다.

기본 환경과 production 요구사항은 다르다. 검색 corpus, ranking, 언어 분석, latency와 운영 역량을 기준으로 PostgreSQL 기반 engine 또는 별도 search backend를 선택한다.

### 6. Authentication과 Authorization

- Authentication: 사용자가 누구인지 확인하고 third-party provider access를 연결한다.
- Authorization: permission policy가 특정 action/resource의 허용 여부를 결정한다.

기본 endpoint가 자동으로 모두 안전해진다고 가정하면 안 된다. sign-in resolver, service-to-service authentication, permission integration과 plugin 자체의 enforcement를 함께 검토한다.

## 운영 모델

Backstage의 성공은 설치보다 ownership model에 좌우된다.

| 역할 | 책임 |
|---|---|
| Platform product owner | 사용자 문제, roadmap, adoption metric, UX 우선순위 |
| Backstage maintainers | core app, plugins, upgrades, reliability, security |
| Domain/service owners | entity metadata, docs, runbook 품질과 freshness |
| Security/governance | permission, secret, template action, audit 기준 |
| Developer users | feedback, golden path 사용, metadata 개선 |

좋은 rollout은 “모든 integration을 먼저 구축”하지 않는다. 대표 user journey 하나를 정하고 Catalog completeness와 task success를 측정한 뒤 확장한다.

## Release 해석

조사 기준 2026-07-30:

- 최신 stable: `v1.53.1` (2026-07-29)
- preview: `v1.54.0-next.*`
- main line: 월간
- `next` line: 주간

Backstage umbrella version은 함께 검증된 package 집합이지만 strict SemVer가 아니다. minor release에도 breaking change가 있을 수 있다. 개별 package는 SemVer를 따르므로 upgrade 시 다음을 함께 본다.

1. target Backstage release의 upgrade helper/changelog
2. 설치한 core/community plugin compatibility
3. `**BREAKING**`과 migration guide
4. frontend/backend counterpart의 release skew
5. Node.js, TypeScript, PostgreSQL support window

## Sources

- [What is Backstage?](https://backstage.io/docs/overview/what-is-backstage/)
- [Technical Overview](https://backstage.io/docs/overview/technical-overview/)
- [Architecture Overview](https://backstage.io/docs/overview/architecture-overview/)
- [CNCF Backstage Project Page](https://www.cncf.io/projects/backstage/)
- [Software Catalog System Model](https://backstage.io/docs/features/software-catalog/system-model/)
- [Entity References](https://backstage.io/docs/features/software-catalog/references/)
- [Backend System](https://backstage.io/docs/backend-system/)
- [Plugin Configuration](https://backstage.io/docs/getting-started/configure-app-with-plugins/)
- [Permission Framework Overview](https://backstage.io/docs/permissions/overview/)
- [Release & Versioning Policy](https://backstage.io/docs/overview/versioning-policy/)

