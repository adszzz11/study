---
date: 2026-09-20
tags: [tech]
type: tech-tool-study
status: draft
---

# PlayMCP References

## Primary Sources

1. [카카오 — PlayMCP 베타 오픈 (2025-08-13)](https://www.kakaocorp.com/page/detail/11674): 플랫폼 목적, server 등록·대화 테스트, 초기 카카오 서비스 연결.
2. [카카오 기술 블로그 — PlayMCP: 제로부터 시작하는 MCP 플랫폼 개발 (2025-09-08)](https://tech.kakao.com/posts/734): 플랫폼 구현과 OAuth client 설계 배경.
3. [카카오 — 도구함 기능 (2025-11-24)](https://www.kakaocorp.com/page/detail/11817): Toolbox와 ChatGPT·Claude 연결 흐름.
4. [카카오 — OpenClaw 연동 (2026-05-01)](https://www.kakaocorp.com/page/detail/12012): OpenClaw 지원, 약 200개 server, 10분 OneTime Token.
5. [카카오 — AGENTIC PLAYER 10 (2026-06-17)](https://www.kakaocorp.com/page/detail/12059): Kakao Tools 배포 모델을 활용한 공모전 사례.

## Standards and Ecosystem

6. [MCP Server specification (2025-06-18)](https://modelcontextprotocol.io/specification/2025-06-18/server): Prompts, Resources, Tools 및 server capability의 기준.
7. [Official MCP Registry Reference](https://registry.modelcontextprotocol.io/docs): vendor-neutral registry metadata reference.
8. [Glama MCP Gateway](https://glama.ai/mcp/gateway): gateway와 access-control 운영 계층.

## Connection Reference

9. [PlayMCP connector endpoint 정보](https://www.tooljunction.io/mcp/playmcp): 공개 디렉터리에 기재된 endpoint와 transport 정보. 비공식/변동 가능 정보이므로 실제 연결 전 공식 UI·문서로 다시 검증한다.

## Source Use Rule

- 제품 현황과 사용 흐름은 카카오의 날짜가 있는 발표를 우선한다.
- protocol semantics는 MCP specification 버전을 명시해 인용한다.
- connector URL, 지원 client, OAuth 동작은 배포 시점에 재검증한다.

## Sources

- [카카오 PlayMCP 보도자료 목록 진입점](https://www.kakaocorp.com/page/detail/11674)
- [MCP 공식 문서](https://modelcontextprotocol.io/specification/2025-06-18/server)
