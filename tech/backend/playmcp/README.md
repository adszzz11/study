---
date: 2026-09-20
tags: [tech]
type: tech-tool-study
status: draft
---

# PlayMCP Tool Study

> **한 줄 정의**: PlayMCP는 MCP(Model Context Protocol) server의 등록·탐색·테스트·인증과 외부 AI client 연결을 제공하는 카카오의 한국형 AI-agent 도구 플랫폼이다.

## Overview

LLM이 일정 조회나 지도 검색처럼 실제 작업을 하려면 외부 Tool이 필요하다. MCP는 그 연결을 표준화하지만, server 개발자는 배포·discovery·인증·client 설정·검증을 따로 해결해야 한다. PlayMCP는 이 흐름에 Catalog, 대화형 Preview, Toolbox, 인증 연결을 제공한다.

```text
Remote MCP server → PlayMCP Catalog / Preview / Toolbox
                         ↓ Kakao account 인증
              ChatGPT · Claude · OpenClaw · Kakao Tools
                         ↓
                  자연어 요청 → tool call → 원 server
```

카카오 서비스와의 연결, 카카오톡 기반의 유통 경로가 핵심 차별점이다. 2026-05-01 카카오 발표 기준으로 카카오 서비스와 외부 MCP server 약 200개가 등록되어 있었다.

## Learning Path

- [ ] [[01-overview]]에서 PlayMCP가 해결하는 문제와 구성 요소를 이해한다.
- [ ] [[02-ecosystem]]에서 Official MCP Registry, Glama, 직접 배포의 경계를 비교한다.
- [ ] [[04-learning/01-getting-started]]로 read-only MCP Tool을 만들고 Inspector로 검증한다.
- [ ] [[04-learning/02-deep-dive]]에서 Streamable HTTP, OAuth 2.0 + PKCE, 운영 안전성을 설계한다.
- [ ] [[05-projects]]에서 실제 사용자 시나리오 하나를 최소 권한 Tool로 구현한다.
- [ ] [[cheatsheet]]로 등록·연결·장애 점검 항목을 확인한다.
- [ ] [[03-references]]의 1차 자료로 제품 상태와 사양 버전을 재확인한다.

## When To Use

- 카카오 서비스와 연결되는 agent 경험을 만들거나 국내 사용자 대상 MCP를 배포할 때
- 하나의 Kakao account 인증과 Toolbox로 여러 Tool을 관리하고 싶을 때
- MCP server의 Tool selection을 대화형 Preview에서 빠르게 검증할 때

## When Not To Use

- 기업 내부망, data residency, 인증·권한 정책을 전부 직접 통제해야 할 때
- platform dependency를 최소화한 독립적인 `stdio` 또는 remote MCP 배포가 목표일 때
- Tool을 실행시키기보다 단순 문서 검색·정적 데이터 배포만 해결하면 될 때

## Related Notes

- [[MOCs/Index]]
- [[MOCs/Backend]]
- [[tech/backend/http/README]] - Remote MCP의 HTTPS 요청·응답과 timeout을 이해하는 기반 노트

## Sources

- [카카오 — PlayMCP 베타 오픈 (2025-08-13)](https://www.kakaocorp.com/page/detail/11674)
- [카카오 — 도구함 기능 (2025-11-24)](https://www.kakaocorp.com/page/detail/11817)
- [카카오 — OpenClaw 연동 (2026-05-01)](https://www.kakaocorp.com/page/detail/12012)
- [MCP Server specification](https://modelcontextprotocol.io/specification/2025-06-18/server)
