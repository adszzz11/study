---
date: 2026-10-18
tags: [tech]
type: tech-tool-study
status: draft
---

# API Discovery 생태계

| 선택지 | 성격 | 강점 | 주의점 / 적합한 상황 |
|---|---|---|---|
| [public-apis](https://github.com/public-apis/public-apis) | 오픈소스 curated directory | 넓은 주제 탐색, 공개 기여 | live endpoint·무료 tier·SLA 보증 없음; 후보 발굴용 |
| [APIs.io](https://apis.io/apis/public-apis/public-apis-directory/) | machine-readable catalog | API·MCP로 catalog 검색 | metadata와 provider contract를 별도 검증 |
| [Postman API Network](https://learning.postman.com/latest-v-12/docs/postman-api-network/overview) | discovery + collection | 즉시 실행, verified team, Guided Auth | workspace 최신성·권한 범위 확인 |
| [RapidAPI Hub](https://docs.rapidapi.com/v2.0/) | marketplace | 탐색, browser test, 통합 key/billing | 중개 pricing·quota와 원 provider 정책을 함께 검토 |
| Provider 공식 docs | source of truth | SLA, auth, limits, ToS 확인 | 검색 편의성은 낮아도 production 전 필수 |
| [Free Public APIs API](https://github.com/go-api-libs/freepublicapis/blob/main/api/openapi.json) | directory API | OpenAPI 3.1 programmatic discovery | 일일 limit과 자체 health 정의 확인 |

## 선택 기준

- **발견**: public-apis 또는 APIs.io로 domain 후보를 넓게 모은다.
- **실행 학습**: collection이 있다면 Postman으로 auth와 request/response를 빠르게 확인한다.
- **구매·통합**: marketplace는 billing 편의를 주지만 provider 원문 정책을 대체하지 않는다.
- **채택**: 공식 docs와 실제 sandbox 호출 결과를 기준으로 한다.

## 2025–2026 흐름

목록 탐색만이 아니라 OpenAPI/OAS, Postman collection, interactive docs, marketplace, MCP 검색으로 discovery와 실행 contract를 연결한다. OAS는 SDK generation, validation, mock, test, agent tool 등록에 쓸 수 있는 machine-readable contract다.

## Sources

- https://apis.io/apis/public-apis/public-apis-directory/
- https://learning.postman.com/latest-v-12/docs/postman-api-network/overview
- https://docs.rapidapi.com/v2.0/
- https://spec.openapis.org/oas/
