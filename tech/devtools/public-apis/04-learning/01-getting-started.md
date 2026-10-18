---
date: 2026-10-18
tags: [tech]
type: tech-tool-study
status: draft
---

# Getting Started: 후보 검증과 첫 호출

## 목표

directory에서 후보 하나를 고르고, provider 공식 문서를 근거로 실제 접근 조건을 검증한다.

## 1. 후보 카드 만들기

관심 domain의 API마다 아래를 기록한다.

| 항목 | 확인 질문 |
|---|---|
| Contract | OpenAPI 또는 호출 예제가 있는가? |
| Access | API key/OAuth가 필요한가? scope는 무엇인가? |
| Cost | free tier, quota, overage가 무엇인가? |
| Operations | rate limit, SLA, deprecation policy는? |
| Browser | CORS가 허용되는가? |

## 2. `curl`로 response 관찰

공식 문서의 sandbox 또는 무인증 `GET` endpoint를 사용한다. 실제 key는 shell history·로그에 남기지 않는다.

```bash
curl --include --max-time 10 'https://api.example.com/v1/resources?limit=10'
```

다음 상태를 의도적으로 또는 문서로 확인한다.

- `200`: 성공 payload와 pagination link/header
- `401` / `403`: 인증 누락·권한 부족의 차이
- `404`: path 또는 resource 부재
- `429`: rate limit header와 reset 시간
- `5xx`: provider failure 시 timeout/retry 정책

## 3. secret 분리

```bash
# .env는 VCS에 추가하지 않는다.
API_BASE_URL=https://api.example.com
PROVIDER_API_KEY=replace-me
```

API key는 browser bundle이나 analytics/log에 포함하지 않는다. browser 앱에서는 key를 보유한 backend/BFF가 provider를 호출하도록 설계한다.

## 완료 기준

- [ ] 공식 docs의 pricing, quota, ToS, deprecation을 확인했다.
- [ ] 정상 응답과 하나 이상의 오류 응답을 기록했다.
- [ ] key가 source, frontend bundle, 로그에 노출되지 않음을 확인했다.

## Sources

- https://github.com/public-apis/public-apis
- https://www.rfc-editor.org/rfc/rfc9110
- https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API
