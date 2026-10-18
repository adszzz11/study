---
date: 2026-10-18
tags: [tech]
type: tech-tool-study
status: draft
---

# public-apis Cheatsheet

## 채택 전 질문

```text
공식 docs는 있는가? → auth / pricing / quota / ToS 확인
OpenAPI 또는 collection은 있는가? → contract 검증·자동화
CORS가 되는가? → 아니오: BFF 필요
429/5xx 때 어떻게 되는가? → Retry-After, backoff, fallback
```

## HTTP 상태 코드

| 코드 | client 동작 |
|---|---|
| `2xx` | payload와 pagination 처리 |
| `400` | request/schema 수정 |
| `401` | credential 누락·만료 확인 |
| `403` | scope·권한·plan 확인 |
| `404` | path/resource/version 확인 |
| `429` | `Retry-After` 존중, backoff |
| `5xx` | 제한된 retry, 관측·fallback |

## 안전한 요청 골격

```bash
curl --fail-with-body --max-time 10 \
  -H 'Accept: application/json' \
  'https://api.example.com/v1/resources?limit=20'
```

## Do / Don't

- Do: directory는 후보 발굴에, 공식 docs는 채택 판단에 사용한다.
- Do: key는 secret manager/server-side에 둔다.
- Do: timeout·pagination·rate-limit handling을 기본값으로 둔다.
- Don't: listing의 CORS/auth/free 표기를 production 보증으로 간주하지 않는다.
- Don't: API key를 source, client bundle, 로그에 남기지 않는다.

## Sources

- https://www.rfc-editor.org/rfc/rfc9110
- https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API
- https://spec.openapis.org/oas/
