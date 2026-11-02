---
date: 2026-11-03
tags: [tech]
type: tech-tool-study
status: draft
---

# BuildIndex.dev — Deep Dive: Catalog 품질과 보안 평가

> [[tech/devtools/buildindex-domain-assessment/README|목차]] · [[tech/devtools/buildindex-domain-assessment/04-learning/01-getting-started|이전: 시작하기]] · [[tech/devtools/buildindex-domain-assessment/05-projects|다음: Projects]]

## 1. catalog의 품질은 freshness에서 시작한다

검색 UI가 좋아도 owner와 runbook이 오래되면 catalog는 신뢰할 수 없다. CI에서 metadata의 최소 요건을 검증하고 변경 사항을 pull request에서 차단한다.

| 필드 | 최소 검증 | 실패 시 영향 |
|---|---|---|
| `owner` | 유효한 group/user 참조 | incident 책임 불명확 |
| `lifecycle` | 허용된 값 | 폐기·실험 서비스 오판 |
| documentation | runbook 또는 docs URL | 대응 시간이 길어짐 |
| repository URL | 접근 가능한 canonical URL | 변경 이력 추적 실패 |
| on-call | rotation 또는 escalation 경로 | 장애 전파 지연 |

## 2. 데이터 수집 경로 모델링

IDP는 Git, Kubernetes, CI/CD, cloud provider에서 metadata를 모을 수 있다. 연결 전에는 어떤 identity가 어떤 API scope로 무엇을 읽고 쓰는지 자료 흐름으로 그린다.

```text
Repository / CI / Kubernetes / Cloud
              │ metadata, source context
              ▼
        Catalog connector ──► IDP storage / search index
              │                         │
              ▼                         ▼
        PR validation              Portal / API / AI enrichment
```

AI enrichment가 있다면 source code와 documentation이 model provider 또는 subprocessor로 전달되는지, retention·training opt-out·region·access log를 확인한다. “AI description” 기능 자체는 데이터 처리 안전성을 보장하지 않는다.

## 3. security review 질문

- SSO, SCIM, RBAC가 최소 권한으로 구성되는가?
- connector token은 read-only scope와 rotation을 지원하는가?
- secret, customer data, private URL이 index 또는 prompt에 유입되지 않는가?
- audit log, export, deletion, incident notification 조건은 무엇인가?
- SaaS 종료 시 metadata와 관계 그래프를 표준 형식으로 export할 수 있는가?

## 4. 검증 결과를 결정으로 연결하기

`buildindex.dev`가 공식 운영 주체를 공개하기 전에는 “reject”가 아니라 “insufficient evidence”로 기록한다. 대안 평가는 동일 샘플·동일 보안 기준에서 수행하고, evidence가 추가될 때만 재개한다.

## Sources

- https://backstage.io/docs/features/software-catalog/
- https://docs.opslevel.com/docs/introducing-opslevel
- https://www.opslevel.com/product/catalog
