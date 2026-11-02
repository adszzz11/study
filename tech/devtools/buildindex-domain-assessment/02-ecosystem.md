---
date: 2026-11-03
tags: [tech]
type: tech-tool-study
status: draft
---

# BuildIndex.dev — Ecosystem 및 비교

> [[tech/devtools/buildindex-domain-assessment/README|목차]] · [[tech/devtools/buildindex-domain-assessment/01-overview|이전: Overview]] · [[tech/devtools/buildindex-domain-assessment/04-learning/01-getting-started|다음: 시작하기]]

## 비교 기준

`buildindex.dev`에 대한 제품 정보는 검증되지 않았다. 아래 비교는 이를 경쟁 제품으로 전제하지 않고, “조직 내 서비스 발견”이라는 가능한 문제에 대한 검증 가능한 선택지를 보여준다.

| 제품/접근 | 유형 | 검증 가능한 특징 | BuildIndex.dev 대비 판단 |
|---|---|---|---|
| BuildIndex.dev | 미확인 | 공개 제품 정보 없음 | PoC·도입 판단 불가 |
| Backstage | Open Source IDP | Git YAML metadata를 수집하고 entity/relationship 표시 | 자체 호스팅·확장성이 필요할 때 기준선 |
| OpsLevel | SaaS IDP | Git, Kubernetes, CI/CD, cloud provider에서 catalog 발견·보강; AI description 제공 | 빠른 운영 도입과 scorecard/automation이 필요할 때 |
| Cortex | SaaS IDP | Developer Portal과 API 문서 제공 | 상용 catalog/portal 평가 후보 |
| Build Index Australia | Proptech | NSW builder 비교·compliance 정보 집계 | 이름만 유사하며 developer-tool 대안이 아님 |

## 대안 선택의 관점

### Backstage

Backstage Software Catalog는 소스 제어의 metadata YAML을 source of truth로 두고 service, website, library, data pipeline의 ownership과 메타데이터를 중앙화한다. 조직이 schema·plugin·hosting을 직접 통제해야 한다면 명확한 기준선이다. 자세한 학습은 [[tech/devtools/backstage-io/README|Backstage.io]]를 참고한다.

### OpsLevel과 Cortex

SaaS IDP는 초기 통합과 운영 부담을 줄일 수 있지만, catalog discovery와 AI enrichment가 읽거나 외부로 전송하는 데이터 범위를 계약·보안 검토에 포함해야 한다. 제품 선택 전에 SSO/RBAC, retention, model-provider, data residency, export/exit 조건을 확인한다.

## 평가 표준화

같은 10개 서비스 샘플과 동일 보안 요건으로 비교한다.

| 기준 | 확인 질문 |
|---|---|
| Discovery accuracy | 실제 repository/runtime를 올바른 service와 owner로 연결하는가? |
| Relationship graph | System, dependency, API, on-call 관계를 탐색할 수 있는가? |
| Setup effort | 초기 metadata 작성·연동·운영에 드는 시간이 얼마인가? |
| Access control | SSO, RBAC, audit log, least privilege가 충분한가? |
| Data egress | source/documentation이 어디로 전송·보관되는가? |
| Total cost | license, hosting, integration, maintenance 비용은 무엇인가? |

## Sources

- https://backstage.io/docs/features/software-catalog/
- https://backstage.io/docs/overview/technical-overview/
- https://docs.opslevel.com/docs/introducing-opslevel
- https://www.opslevel.com/product/catalog
- https://developer.cortextech.io/
- https://www.linkedin.com/company/build-index
