---
date: 2026-07-30
tags: [tech]
type: tech-tool-study
status: draft
---

# Backstage 실전 Projects

> [[README|목차로 돌아가기]] · [[04-learning/02-deep-dive|이전: Deep Dive]] · [[cheatsheet|다음: Cheatsheet]]

## Project 1. Catalog pilot

### 목표

대표 team 2–3개, service 20–50개를 대상으로 “owner, repository, runbook, dashboard를 2분 안에 찾는다”는 user journey를 검증한다.

### 범위

- `Component`, `API`, `Resource`, `System`, `Group`
- GitHub/GitLab discovery 또는 제한된 locations
- mandatory metadata: owner, lifecycle, type, source
- entity page에 source, CI, dashboard, on-call link

### 단계

1. 실제 developer 질문 5개를 interview로 수집한다.
2. 최소 entity model과 naming convention을 정한다.
3. repository별 `catalog-info.yaml`을 추가한다.
4. 조직 Group ingestion과 owner resolution을 연결한다.
5. validation report와 freshness dashboard를 만든다.
6. pilot 전후 탐색 시간을 비교한다.

### 완료 기준

- [ ] pilot entity의 95% 이상에서 owner가 resolve된다.
- [ ] source/runbook/dashboard link의 90% 이상이 유효하다.
- [ ] 대표 탐색 task의 median time이 목표 안에 든다.
- [ ] stale metadata의 수정 owner와 process가 정해져 있다.

## Project 2. Production TechDocs

### 목표

local backend build/storage를 벗어나 CI build + object storage 구조로 안정적인 docs-like-code를 제공한다.

```text
Repository → CI build → Object Storage → Backstage Reader
```

### 구현 항목

- 공통 `mkdocs.yml` baseline과 dependency pinning
- CI에서 `techdocs-cli generate`와 publish
- S3/GCS/Azure Blob bucket, retention과 credential
- build failure notification
- private repository/document authorization 검증
- docs freshness와 broken link metric

### 완료 기준

- [ ] Backstage replica를 교체해도 docs가 유지된다.
- [ ] docs change가 정해진 SLO 안에 반영된다.
- [ ] CI 실패 원인과 담당자가 보인다.
- [ ] storage credential이 runtime/build role로 분리된다.

## Project 3. Golden Path: 새 service 생성

### 목표

repository, CI, Catalog, baseline documentation까지 일관되게 생성하는 self-service template을 만든다.

### Input

| field | validation |
|---|---|
| service name | naming regex, uniqueness |
| owner | Catalog `Group` picker |
| system/domain | 허용된 entity reference |
| runtime | 지원하는 option enum |
| visibility | 조직 policy와 repository rule |
| data classification | security control 분기 |

### Workflow

```text
Validate input
  → Render skeleton
  → Create repository
  → Configure branch protection/CI
  → Create catalog-info.yaml + docs
  → Open PR or publish
  → Register entity
  → Return links
```

### 실패 설계

- repository 생성 후 Catalog 등록 실패 시 재시도 가능해야 한다.
- 동일 request의 retry가 duplicate repository를 만들지 않아야 한다.
- irreversible step 전 permission과 target을 다시 확인한다.
- actor, parameters, external resource ID와 결과를 audit log에 남긴다.

### 완료 기준

- [ ] happy path와 주요 failure path test가 있다.
- [ ] secret이 task log와 generated repository에 노출되지 않는다.
- [ ] 생성 결과가 조직 security/CI/docs baseline을 만족한다.
- [ ] 기존 수동 절차 대비 lead time을 측정했다.

## Project 4. Catalog health와 scorecard

### 목표

metadata를 처벌 수단이 아니라 actionable improvement system으로 운영한다.

### 검사 예

- owner entity가 resolve되는가?
- production service에 runbook과 on-call link가 있는가?
- TechDocs build가 최근 성공했는가?
- repository에 required CI workflow가 있는가?
- dependency와 API relation이 최소 기준을 만족하는가?

각 실패 항목에서 문서 링크만 보여 주지 말고 가능한 경우 fix action 또는 golden path로 연결한다.

### Guardrail

- 자동 검증 가능한 fact만 점수화한다.
- team 간 성격이 다른 component를 같은 기준으로 비교하지 않는다.
- 점수의 목적, 예외와 appeal process를 공개한다.
- metric gaming과 stale external data를 정기 검토한다.

## Project 5. Production readiness

### Architecture Decision Records

- Catalog source of truth와 deletion semantics
- auth provider, sign-in resolver와 group mapping
- permission model: RBAC/ABAC/custom
- PostgreSQL topology와 disaster recovery
- TechDocs builder/publisher/storage
- search engine과 indexing interval
- deployment topology와 plugin separation
- release cadence와 community plugin policy

### Game day

다음 failure를 staging에서 연습한다.

- PostgreSQL unavailable/restore
- SCM API rate limit 또는 credential expiration
- object storage unavailable
- invalid entity가 대량 ingestion
- Scaffolder external API timeout
- plugin upgrade 후 migration 실패

### 완료 기준

- [ ] SLO/SLI와 alert owner가 있다.
- [ ] backup restore를 실제로 검증했다.
- [ ] release rollback/runbook이 있다.
- [ ] least privilege와 secret rotation을 검증했다.
- [ ] Platform Team의 support/on-call model이 정해졌다.

## 90-day rollout 예시

| 기간 | 결과물 | 판단 gate |
|---|---|---|
| 1–30일 | user research, Catalog pilot, baseline metric | 실제 탐색 시간이 줄었는가? |
| 31–60일 | TechDocs production path, 첫 golden path | 반복 사용과 task success가 있는가? |
| 61–90일 | permissions, observability, upgrade/runbook | 운영 가능성과 확장 가치가 있는가? |

범위를 넓히는 조건은 “기능이 구현됨”이 아니라 target journey의 outcome이 개선되었다는 증거다.

## Project retrospective 질문

- portal이 어떤 context switch를 실제로 제거했는가?
- source metadata를 누가, 어떤 workflow로 고치는가?
- 실패한 template task를 사용자가 복구할 수 있는가?
- 가장 유지비가 큰 plugin은 어떤 가치에 기여하는가?
- Backstage가 없어져도 유지되어야 할 source of truth는 어디인가?
- 다음 분기에 제거할 기능과 강화할 journey는 무엇인가?

## Sources

- [Software Catalog](https://backstage.io/docs/features/software-catalog/)
- [Software Templates](https://backstage.io/docs/features/software-templates/)
- [Writing Templates](https://backstage.io/docs/features/software-templates/writing-templates/)
- [TechDocs Architecture](https://backstage.io/docs/features/techdocs/architecture/)
- [Permissions Overview](https://backstage.io/docs/permissions/overview/)
- [Deploying Backstage to Production](https://backstage.io/docs/golden-path/deployment/)
- [Observability](https://backstage.io/docs/observability/)

