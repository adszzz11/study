---
date: 2026-10-18
tags: [tech]
type: tech-tool-study
status: draft
---

# Ecosystem과 비교

| 선택지 | 강점 | 한계 / 적합한 경우 |
|---|---|---|
| **awwwards-mcp** | Awwwards 특화 검색, screenshot, design DNA, browser capture, motion 분석을 local MCP로 결합 | markup 변화와 copyright/ToS를 관리해야 한다. reference-to-verification loop에 적합하다. |
| [Apify Awwwards Website Scraper MCP](https://apify.com/easyapi/awwwards-website-scraper/api/mcp) | Hosted MCP와 OAuth/Apify 생태계 | account·service 의존성이 생긴다. design verification 범위는 사용 전 확인한다. |
| [design-mcp](https://github.com/chrismicah/design-mcp) | Dribbble, SaaS 등 다중 source design-pattern corpus | live Awwwards 변화·motion capture보다 curated dataset 조사에 가깝다. |
| 일반 Playwright + 자체 MCP | 대상, 정책, 저장 방식을 전부 통제 | taxonomy, caching, search ranking, design parsing을 직접 구현해야 한다. |

## 선택 기준

- **Awwwards의 실제 site를 기준으로 구현을 검증**하려면 `awwwards-mcp`.
- **운영형 hosted workflow**가 우선이면 Apify를 검토한다.
- **source diversity가 우선**이면 `design-mcp` 같은 corpus 도구를 병행한다.
- **엄격한 수집 정책이나 사내 source**가 있으면 최소 기능의 자체 Playwright MCP가 낫다.

## Versioning

2026-10-18 기준 최신 GitHub release는 `v1.8.0`이다. 초기 stable/alpha 이력이 있으므로 재현 가능한 agent 환경에서는 `npx`의 floating latest보다 version pinning과 release note 확인을 권장한다.

## Sources

- https://github.com/INSANE0777/Awwwards-mcp/releases
- https://apify.com/easyapi/awwwards-website-scraper/api/mcp
- https://github.com/chrismicah/design-mcp
