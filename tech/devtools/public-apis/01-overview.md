---
date: 2026-10-18
tags: [tech]
type: tech-tool-study
status: draft
---

# public-apis 개요

## What

`public-apis/public-apis`는 API 이름, 설명, 인증 여부, CORS 상태를 category별 Markdown 목록으로 정리한 오픈소스 directory다. “public”은 일반적으로 self-service 접근과 문서 공개를 뜻하며 **무료**를 뜻하지 않는다. API key, OAuth, 유료 quota가 있을 수 있다.

## Why

외부 데이터·지도·결제·AI·정부 서비스를 직접 구축하지 않고 product에 연결하려면 후보 discovery가 필요하다. directory는 탐색 비용을 낮추지만, 호출 contract와 운영 조건은 실제 provider가 소유한다.

## 특징과 책임 경계

| 계층 | 역할 | 확인할 것 |
|---|---|---|
| Catalog | 후보를 발견하고 분류 | listing의 최신성, 문서 링크 |
| Provider API | endpoint와 data 제공 | SLA, pricing, quota, ToS, version |
| Contract | REST/GraphQL/gRPC 호출 정의 | OpenAPI, schema, collection |
| Access control | API key, OAuth, service token | 최소 권한, secret 저장 위치 |
| Runtime | 호출과 오류 처리 | timeout, pagination, retry, `429` |
| Browser | Fetch와 Origin 제약 | CORS, BFF 필요 여부 |

## 안전한 채택 흐름

1. directory에서 domain 후보를 모은다.
2. provider 공식 docs에서 auth, 요금, quota, deprecation, ToS를 확인한다.
3. `curl`/Postman으로 정상·인증 실패·rate limit 응답을 직접 관찰한다.
4. secret은 server-side secret manager에 보관하고 client adapter로 contract를 감싼다.

## Sources

- https://github.com/public-apis/public-apis
- https://github.com/marcelscruz/public-apis/blob/main/CONTRIBUTING.md
- https://spec.openapis.org/oas/
- https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API
