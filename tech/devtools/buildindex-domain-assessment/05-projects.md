---
date: 2026-11-03
tags: [tech]
type: tech-tool-study
status: draft
---

# BuildIndex.dev — Projects

> [[tech/devtools/buildindex-domain-assessment/README|목차]] · [[tech/devtools/buildindex-domain-assessment/04-learning/02-deep-dive|이전: Deep Dive]] · [[tech/devtools/buildindex-domain-assessment/cheatsheet|다음: Cheatsheet]]

## 1. Domain due-diligence project

공식 운영 주체가 확인되기 전까지 구매·credential 입력 없이 domain, DNS, TLS, 법인, GitHub 증거를 수집하는 체크리스트를 운영한다.

**완료 기준**

- evidence log에 관찰 시각과 원문 URL이 있다.
- domain, certificate, legal document, GitHub가 동일 운영 주체를 가리킨다.
- 충돌·미확인 항목과 다음 재확인 날짜가 명시된다.

## 2. Service catalog MVP

10개 서비스에 `owner`, `repo`, `runtime`, `tier`, `documentation`, `on-call`을 Backstage YAML로 등록한다. 검색 결과보다 ownership 공백과 누락 metadata 수를 먼저 측정한다.

**지표 예시**

| 지표 | 계산 |
|---|---|
| Owner coverage | owner가 있는 서비스 / 전체 서비스 |
| Docs coverage | 유효한 runbook 또는 docs가 있는 서비스 / 전체 서비스 |
| On-call coverage | escalation 경로가 있는 production 서비스 / production 서비스 |
| Freshness | 최근 검증 기준을 통과한 entity / 전체 entity |

## 3. Catalog freshness pipeline

GitHub, CI/CD, Kubernetes의 metadata를 catalog와 동기화하고 owner·문서·runbook 누락을 PR check로 차단한다. 자동 추론값과 사람이 승인한 값은 provenance를 구분한다.

## 4. Alternative evaluation

Backstage와 OpsLevel을 같은 서비스 샘플과 보안 요구사항으로 비교한다.

- discovery accuracy와 relationship graph
- setup effort와 유지보수 부담
- SSO/RBAC, audit log, data egress
- AI enrichment의 retention 및 model-provider 정책
- total cost와 exit/export 가능성

## Sources

- https://backstage.io/docs/features/software-catalog/
- https://docs.opslevel.com/docs/introducing-opslevel
