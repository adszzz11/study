---
date: 2026-07-30
tags: [tech]
type: tech-tool-study
status: draft
---

# Backstage Cheatsheet

> [[README|목차로 돌아가기]] · [[05-projects|이전: Projects]]

## 핵심 용어

| 용어 | 의미 |
|---|---|
| IDP | Internal Developer Portal |
| Entity | Catalog가 관리하는 metadata object |
| Entity ref | `kind:namespace/name` |
| Component | service, website, library 등 software unit |
| System | 함께 기능을 제공하는 component/resource 집합 |
| Domain | 여러 system을 묶는 business 영역 |
| Resource | database, queue, bucket 같은 infrastructure |
| Template | Scaffolder가 실행하는 self-service workflow entity |
| Processor | ingestion 중 entity를 처리하고 relation을 생성 |
| EntityProvider | 외부 source에서 entity 집합을 공급 |
| Module | extension point로 backend plugin을 확장 |
| Golden Path | 조직의 권장 기본값을 내장한 쉬운 workflow |

## Version snapshot

```text
조사일:        2026-07-30
stable:        v1.53.1 (2026-07-29)
next:          v1.54.0-next.*
main cadence:  monthly
next cadence:  weekly
주의:          umbrella minor release에도 breaking change 가능
```

## 기본 명령

```bash
# 새 app 생성
npx @backstage/create-app@latest

# generated app 실행
cd my-backstage-app
yarn start

# 일반적인 품질 검사: 실제 script는 generated package.json 확인
yarn lint
yarn test
yarn tsc
yarn build:backend
```

재현 가능한 환경에서는 `@latest` 대신 검증한 version과 lockfile을 사용한다.

## Entity reference

```text
canonical:          component:default/payments-api
namespace 생략:     component:payments-api
문맥상 kind 생략:   default/payments-api
둘 다 생략:         payments-api
owner 권장 표기:    group:default/payments
resource 표기:      resource:default/payments-db
```

## Component YAML

```yaml
apiVersion: backstage.io/v1alpha1
kind: Component
metadata:
  name: payments-api
  title: Payments API
  description: Payment authorization service
  tags: [typescript, payments]
  links:
    - url: https://grafana.example.com/d/payments
      title: Dashboard
  annotations:
    github.com/project-slug: acme/payments-api
    backstage.io/techdocs-ref: dir:.
spec:
  type: service
  lifecycle: production
  owner: group:default/payments
  system: checkout
  providesApis: [payments]
  dependsOn:
    - resource:default/payments-db
```

## 주요 kind와 relation

| kind | 주요 관계/field |
|---|---|
| `Domain` | `spec.owner` |
| `System` | `spec.domain`, `spec.owner` |
| `Component` | `owner`, `system`, `subcomponentOf`, `providesApis`, `consumesApis`, `dependsOn` |
| `API` | `owner`, `system`, `definition` |
| `Resource` | `owner`, `system`, `dependsOn`, `dependencyOf` |
| `Group` | `parent`, `children`, `members` |
| `User` | `memberOf` |
| `Template` | `owner`, `type`, `parameters`, `steps` |
| `Location` | entity descriptor target |

## Config snippets

### Catalog location

```yaml
catalog:
  locations:
    - type: url
      target: https://github.com/acme/service/blob/main/catalog-info.yaml
```

### GitHub integration

```yaml
integrations:
  github:
    - host: github.com
      token: ${GITHUB_TOKEN}
```

### PostgreSQL

```yaml
backend:
  database:
    client: pg
    connection:
      host: ${POSTGRES_HOST}
      port: ${POSTGRES_PORT}
      user: ${POSTGRES_USER}
      password: ${POSTGRES_PASSWORD}
```

### TechDocs annotation

```yaml
metadata:
  annotations:
    backstage.io/techdocs-ref: dir:.
```

## Template skeleton

```yaml
apiVersion: scaffolder.backstage.io/v1beta3
kind: Template
metadata:
  name: create-service
  title: Create Service
spec:
  owner: group:default/platform
  type: service
  parameters:
    - title: Metadata
      required: [name, owner]
      properties:
        name:
          type: string
          pattern: '^[a-z0-9-]+$'
        owner:
          type: string
  steps:
    - id: fetch
      name: Fetch skeleton
      action: fetch:template
      input:
        url: ./skeleton
        values:
          name: ${{ parameters.name }}
  output:
    text:
      - title: Result
        content: Created `${{ parameters.name }}`
```

custom action ID에는 camelCase를 사용한다. hyphen이 있는 step/action reference는 expression에서 subtraction으로 해석될 수 있다.

## Production checklist

### Catalog

- [ ] stable naming과 source-of-truth 정의
- [ ] owner/lifecycle/type validation
- [ ] discovery/provider quota와 deletion semantics
- [ ] orphan, processing error와 freshness monitoring

### Security

- [ ] production auth provider와 sign-in resolver
- [ ] backend-enforced permission policy
- [ ] service-to-service auth
- [ ] short-lived/least-privilege token
- [ ] template validation, idempotency와 audit

### Data와 runtime

- [ ] PostgreSQL backup/restore
- [ ] migration-aware deployment
- [ ] health check, replicas와 graceful shutdown
- [ ] structured log, metrics, traces와 SLO

### TechDocs와 Search

- [ ] CI generate + object storage publish
- [ ] docs build failure와 freshness alert
- [ ] search index schedule와 relevance test
- [ ] private content authorization

### Upgrade

- [ ] Releases/Versioning Policy 확인
- [ ] Upgrade Helper diff 적용
- [ ] core/community plugin compatibility
- [ ] `BREAKING` changelog와 support window
- [ ] auth, Catalog, TechDocs, Search, Scaffolder smoke test
- [ ] backend를 frontend보다 먼저 또는 함께 배포

## 빠른 troubleshooting

| 증상 | 먼저 볼 곳 |
|---|---|
| entity가 보이지 않음 | location URL, integration credential, Catalog processing error |
| owner가 unresolved | `Group` ingestion, namespace/kind reference |
| relation이 없음 | field 이름, target entity 존재, processor output |
| TechDocs가 안 열림 | annotation, `mkdocs.yml`, generator/publisher log |
| Template가 실패 | installed action, input schema, task log, credential/permission |
| Search 결과가 오래됨 | collator schedule, indexer log, engine connectivity |
| plugin upgrade 후 오류 | release skew, migrations, package changelog |
| local에서는 되고 prod에서 실패 | config merge, secret, network, database/storage permission |

## Sources

- [Standalone Installation](https://backstage.io/docs/getting-started/)
- [Descriptor Format](https://backstage.io/docs/features/software-catalog/descriptor-format/)
- [Entity References](https://backstage.io/docs/features/software-catalog/references/)
- [Writing Templates](https://backstage.io/docs/features/software-templates/writing-templates/)
- [TechDocs Architecture](https://backstage.io/docs/features/techdocs/architecture/)
- [Permissions Overview](https://backstage.io/docs/permissions/overview/)
- [Release & Versioning Policy](https://backstage.io/docs/overview/versioning-policy/)

