---
date: 2026-07-30
tags: [tech]
type: tech-tool-study
status: draft
---

# Backstage Deep Dive

> [[../README|목차로 돌아가기]] · [[01-getting-started|이전: Getting Started]] · [[../05-projects|다음: Projects]]

## 1. Catalog ingestion pipeline

Catalog는 원본 YAML을 그대로 조회하는 단순 registry가 아니다.

```text
catalog-info.yaml · SCM discovery · org directory · cloud · custom provider
                              ↓
                     entity ingestion
                              ↓
                processors / validation
                              ↓
             relations + processing results
                              ↓
                         stitching
                              ↓
             materialized entity in PostgreSQL
                              ↓
                   Catalog API / UI / Search
```

### Location, Processor, EntityProvider

| mechanism | 적합한 용도 | 특징 |
|---|---|---|
| Static location | 소수의 명시적 YAML | 단순하지만 대규모 관리에 불리 |
| SCM discovery | repository convention 탐색 | onboarding 자동화, API quota 고려 |
| Processor | entity 해석·검증·relation 생성 | processing pipeline 안에서 동작 |
| EntityProvider | 외부 source가 entity 집합을 공급 | event-driven/full mutation 구현에 적합 |

대규모 환경에서는 provider마다 stable entity reference와 ownership을 명확히 한다. 같은 entity를 여러 source가 주장하거나 source가 사라질 때 orphan/deletion semantics를 설계해야 한다.

### Metadata quality contract

Catalog 신뢰도는 schema보다 운영 계약에서 나온다.

- mandatory: `owner`, `lifecycle`, `type`, source link
- relation: `system`, `dependsOn`, `providesApis`, `consumesApis`
- operational: runbook, dashboard, on-call, repository annotation
- quality: freshness SLO, validation, orphan policy

자동 수집 가능한 값과 사람이 판단해야 하는 값을 구분한다. repository URL은 discovery할 수 있지만 올바른 business owner와 lifecycle은 team의 확인이 필요하다.

## 2. Entity model 설계

```text
Domain
└── System
    ├── Component ──provides──> API
    ├── Component ──consumes──> API
    └── Component ──dependsOn─> Resource

Group ──owns──> Component / API / Resource
```

### 설계 원칙

1. 처음부터 모든 CMDB field를 옮기지 않는다.
2. entity kind와 relation이 실제 developer 질문에 답하도록 한다.
3. `metadata.name`은 stable identifier로 보고 표시명은 `title`로 분리한다.
4. annotation key는 integration contract이므로 namespace와 문서를 관리한다.
5. custom kind는 built-in model로 표현이 불가능하고 지속 소비자가 있을 때만 만든다.

### 흔한 질문

| 질문 | model |
|---|---|
| 누가 운영하는가? | `spec.owner` → `Group` |
| 어떤 제품 영역인가? | `Component` → `System` → `Domain` |
| 어떤 interface를 제공하는가? | `providesApis` |
| database/queue 의존성은? | `dependsOn` → `Resource` |
| production 준비 상태인가? | lifecycle + 별도 scorecard/fact |

## 3. Plugin architecture

### Frontend

Frontend plugin과 extension은 page, route, navigation, entity card와 API reference를 app에 결합한다. 신규 app은 new frontend system을 기본으로 하므로 legacy plugin을 선택할 때 adapter/migration 상태를 확인한다.

### Backend

Backend plugin은 route와 독립 기능을 제공하고, module은 extension point로 plugin을 확장한다. framework shared services는 database, discovery, auth, logger, cache, scheduler 같은 공통 기능을 제공한다.

```text
Backend deployment unit
├── catalog plugin
│   ├── SCM module
│   └── custom processor module
├── scaffolder plugin
│   └── custom action module
└── shared services
    ├── database
    ├── auth
    ├── logger
    └── scheduler
```

plugin을 별도 deployment unit으로 분리할 때는 independent scaling뿐 아니라 service discovery, auth, migrations, startup dependency와 observability 복잡도도 증가한다.

### Plugin 선정 gate

- [ ] current frontend/backend system compatible
- [ ] target Backstage release와 package skew compatible
- [ ] permission framework를 실제 backend에서 enforce
- [ ] maintenance activity와 release process가 신뢰 가능
- [ ] database migration/operational dependency가 문서화됨
- [ ] outbound token scope와 secret handling이 안전함
- [ ] 장애 시 core portal을 함께 망가뜨리지 않음

## 4. Scaffolder를 production workflow로 만들기

```text
Form input
  → schema validation
  → permission decision
  → fetch/render skeleton
  → create repository / PR
  → provision external resource
  → register Catalog entity
  → output links + audit trail
```

### Action 설계 checklist

- input JSON Schema와 server-side validation
- allowlist와 naming policy
- user token vs service token 선택
- 최소 scope, short-lived credential과 secret redaction
- retry해도 중복 resource가 생기지 않는 idempotency key
- timeout, cancellation과 partial failure 상태
- rollback 또는 compensating action
- actor, input, target, result를 남기는 audit
- dry-run에서 검증 가능한 단계 분리

> [!danger] UI validation만 신뢰하지 말 것
> Template form은 UX 계층이다. backend action과 외부 system boundary에서 다시 authorization과 validation을 수행한다.

## 5. TechDocs production path

권장 흐름은 repository CI에서 generate하고 object storage에 publish한 뒤 Backstage가 serve하는 방식이다.

```text
Git push
  → docs CI job
  → techdocs-cli/MkDocs build
  → S3/GCS/Azure Blob publish
  → techdocs-backend fetch
  → TechDocs Reader render
```

운영 시 확인한다.

- builder/publisher 설정과 storage credential
- entity reference에서 storage key로 가는 naming
- stale docs와 failed build visibility
- MkDocs plugin dependency pinning
- generated HTML sanitization과 untrusted content
- cache/CDN, retention과 storage lifecycle
- repository access와 private docs authorization

## 6. Search architecture

Search는 plugin content를 collator가 document로 만들고 index한 뒤 query하는 구조다.

```text
Catalog / TechDocs / custom plugin
          ↓ collators
       scheduler
          ↓
  search engine index
          ↓
 backend API → Search UI
```

공식 architecture의 현재 non-goal에는 event-driven/incremental index management가 포함된다. 따라서 schedule interval, full index 비용과 freshness expectation을 명시한다.

engine 선택 기준:

- corpus size와 update frequency
- 한국어/영어 tokenizer와 relevance
- filter/facet, ranking customization
- high availability와 backup
- 별도 search cluster 운영 능력

## 7. Security와 permissions

### Trust boundary

| boundary | 주요 위험 | control |
|---|---|---|
| Browser → backend | impersonation, unauthorized action | auth/session, permission |
| Backend → SCM/cloud | over-privileged token | least privilege, broker/short-lived token |
| Scaffolder → external systems | destructive/duplicate operation | validation, idempotency, audit |
| Catalog ingestion | untrusted metadata/URL | rules, allowlist, processor validation |
| TechDocs content | unsafe generated content | supported generator, sanitization |
| Plugin supply chain | vulnerable/malicious package | pinning, review, SBOM/scanning |

Authentication과 permission은 다른 문제다. plugin author가 permission을 선언하고 backend가 decision을 요청·enforce해야 하며, integrator는 조직 policy를 구현한다. UI에서 button을 숨기는 것만으로 authorization이 되지 않는다.

## 8. PostgreSQL과 deployment

production은 persistent PostgreSQL을 권장한다. plugin별 schema/migration, connection pool, backup/restore와 upgrade 순서를 운영 대상으로 본다.

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

deployment checklist:

- [ ] immutable Docker image와 pinned runtime
- [ ] readiness/liveness와 graceful shutdown
- [ ] multiple replicas에서 scheduler/task 동작 검증
- [ ] PostgreSQL backup/restore drill
- [ ] object storage와 external service connectivity
- [ ] structured log, metrics, trace와 SLO
- [ ] config/secret 분리와 rotation
- [ ] migration이 포함된 rollout/rollback procedure

## 9. Upgrade 전략

umbrella minor release에 breaking change가 포함될 수 있으므로 “minor 자동 병합”은 위험하다.

1. stable target release와 support matrix를 고른다.
2. Upgrade Helper로 generated app diff를 확인한다.
3. release notes와 package changelog의 `BREAKING`을 분류한다.
4. core packages와 paired frontend/backend plugin skew를 점검한다.
5. build, typecheck, unit/integration test를 실행한다.
6. Catalog processing, auth, search, TechDocs, template smoke test를 한다.
7. staging에서 DB migration과 rollback 가능성을 검증한다.
8. backend를 frontend보다 먼저 또는 함께 배포한다.
9. error rate, task failure와 entity processing을 관찰한다.

`next` line은 weekly preview이며 breaking change 보장이 더 약하다. production 기본값으로 삼기보다 compatibility test와 조기 검증에 사용한다.

## 10. 성공 metric

| 영역 | metric 예 |
|---|---|
| Catalog | owner가 resolve된 entity 비율, metadata freshness |
| Discovery | owner/runbook/dashboard를 찾는 median time |
| Templates | task success rate, completion time, failure reason |
| TechDocs | build success, freshness, search click-through |
| Reliability | availability, backend error, processing delay |
| Adoption | target team coverage, repeat users, golden path reuse |
| Outcome | onboarding time, standard-compliant service 비율 |

page view는 adoption signal일 뿐 outcome 전체가 아니다. 처음 정의한 user journey가 실제로 빨라지고 안전해졌는지 측정한다.

## Sources

- [Catalog Overview](https://backstage.io/docs/features/software-catalog/)
- [Catalog API](https://backstage.io/docs/features/software-catalog/software-catalog-api/)
- [External Integrations](https://backstage.io/docs/integrations/)
- [Backend System](https://backstage.io/docs/backend-system/)
- [Frontend System](https://backstage.io/docs/frontend-system/)
- [Software Templates](https://backstage.io/docs/features/software-templates/)
- [TechDocs Architecture](https://backstage.io/docs/features/techdocs/architecture/)
- [Search Architecture](https://backstage.io/docs/features/search/architecture/)
- [Permissions Overview](https://backstage.io/docs/permissions/overview/)
- [Deploying Backstage to Production](https://backstage.io/docs/golden-path/deployment/)
- [Release & Versioning Policy](https://backstage.io/docs/overview/versioning-policy/)

