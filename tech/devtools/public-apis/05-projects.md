---
date: 2026-10-18
tags: [tech]
type: tech-tool-study
status: draft
---

# Projects

## 1. API Discovery Dashboard

여러 directory의 후보를 수집해 auth, CORS, pricing, health, OpenAPI 유무를 정규화하고 검색하는 internal portal을 만든다.

- 데이터 모델: provider, endpoint, auth, plan, quota, contract URL, checkedAt
- 검증: source link와 official docs link를 분리하고 health는 시점 데이터로 표시

## 2. Weather / Geo BFF

weather·geocoding provider를 server-side에서 통합하고 frontend-safe endpoint를 제공한다.

- cache TTL, request coalescing, per-user rate limit
- timeout과 fallback provider
- provider key는 secret manager에만 보관

## 3. Open Data Monitor

정부·공공 API의 dataset 변경, schema drift, 실패율, quota 소진을 감시하고 Slack/Email alert를 보낸다.

## 4. Developer API Sandbox

Postman collection, OpenAPI mock server, 예제 response로 팀원이 credential 없이 contract를 학습하게 한다.

## 5. LLM Tool Gateway

검증된 API만 OpenAPI 기반 tool로 등록한다. allowlist, parameter validation, egress 제한, cost/rate-limit guardrail, audit log를 포함한다.

## 공통 평가 기준

| 영역 | 질문 |
|---|---|
| Reliability | timeout, retry, fallback이 있는가? |
| Security | secret과 user input이 경계를 넘을 때 검증되는가? |
| Cost | quota/overage를 관찰하고 제한하는가? |
| Change | version과 schema drift를 감시하는가? |

## Sources

- https://spec.openapis.org/oas/
- https://learning.postman.com/latest-v-12/docs/postman-api-network/overview
- https://docs.rapidapi.com/v2.0/
