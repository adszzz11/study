---
date: 2026-10-18
tags: [tech]
type: tech-tool-study
status: draft
---

> **한 줄 정의**: **public-apis**는 공개적으로 문서화된 HTTP API를 분야별로 발견·비교·실험하도록 돕는 community-curated API directory와 그 생태계다.

## Overview

`public-apis`는 API 자체나 품질 보증 서비스가 아니라 후보를 찾는 출발점이다. 각 후보는 provider 공식 문서에서 인증, 요금, quota, SLA, version/deprecation, ToS를 다시 검증해야 한다.

- [[01-overview|What / Why / 특징]]
- [[02-ecosystem|Discovery 생태계와 선택지 비교]]
- [[03-references|공식 참고 자료]]
- [[cheatsheet|HTTP API 치트시트]]

## Learning Path

- [ ] [[04-learning/01-getting-started|01. Getting Started]]: domain 선택, 공식 docs 검증, 첫 `GET` 호출
- [ ] [[04-learning/02-deep-dive|02. Deep Dive]]: auth·pagination·retry·CORS·OpenAPI를 client에 적용
- [ ] [[05-projects|03. Projects]]: BFF와 discovery dashboard로 운영 관점을 익히기

## When To Use

- 새 product 기능에 연결할 외부 API 후보를 넓게 탐색할 때
- public data, weather, geo, payment, AI 등 domain별 provider를 비교할 때
- API discovery workflow와 OpenAPI/collection 기반 실행을 학습할 때

## When Not To Use

- production provider의 uptime, 보안, 가격, 지원 정책을 directory listing만으로 판단할 때
- API key를 browser bundle에 넣어도 되는지 결정할 때
- 법적·규제 요구가 있어 vendor due diligence가 필요한 경우의 최종 근거로 사용할 때

## Related Notes

- [[MOCs/Index]]
- [[MOCs/Devtools]]
- [[tech/devtools/ripgrep/README|ripgrep]]
- [[01-overview]] · [[02-ecosystem]] · [[05-projects]]

## Sources

- https://github.com/public-apis/public-apis
- https://github.com/marcelscruz/public-apis/blob/main/CONTRIBUTING.md
- https://spec.openapis.org/oas/
- https://www.rfc-editor.org/rfc/rfc9110
- https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API
