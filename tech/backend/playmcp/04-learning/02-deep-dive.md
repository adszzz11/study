---
date: 2026-09-20
tags: [tech]
type: tech-tool-study
status: draft
---

# Deep Dive: Remote MCP, Auth, 운영 안전성

## Remote MCP Checklist

| 영역 | 확인 항목 |
|---|---|
| Transport | Streamable HTTP, HTTPS, protocol/version 호환성 |
| Reliability | connect/read timeout, retry 정책, idempotency, rate limit |
| Observability | request ID, tool name, latency, 결과 상태; token·개인정보 제외 |
| Tool UX | 좁은 JSON Schema, 명확한 description, action 전 확인 단계 |
| Change | endpoint/schema/description 변경 시 등록 정보와 client 호환성 재검증 |

## OAuth 2.0 + PKCE

카카오 기술 설명 기준 PlayMCP는 OAuth 2.0 Client 역할을 수행하며 Authorization Code Grant와 PKCE를 지원한다. server provider는 자기 Authorization Server에 client를 등록하고 필요한 client 정보와 redirect URI 정책을 정합시켜야 한다.

```text
AI client → PlayMCP → Authorization Server
                 └─ Authorization Code + PKCE verifier
Authorization Server → token → PlayMCP → 최소 권한으로 MCP server 호출
```

구현 원칙은 다음과 같다.

- Tool마다 필요한 **최소 scope**만 요청한다.
- access token 만료·refresh·철회와 동의 철회 후의 실패 UX를 설계한다.
- redirect URI와 issuer를 allowlist로 고정하고 state/PKCE 검증을 생략하지 않는다.
- 사용자에게 read, send, purchase처럼 행동의 성격과 대상 데이터를 표시한다.

## Write Tool의 Guardrail

메시지 발송·예약·구매처럼 부작용이 있는 Tool은 read-only Tool보다 보수적으로 설계한다.

1. preview Tool로 영향 범위(대상, 내용, 비용)를 계산한다.
2. 사용자의 명시적 confirmation 없이 실행 Tool을 호출하지 않는다.
3. idempotency key와 audit event를 남겨 중복 실행을 추적한다.
4. revoke·disconnect 후에는 fail closed하고 재인증을 유도한다.

OpenClaw 연동에서 카카오는 10분 유효 OneTime Token과 연결 해제를 안내한다. 이 방식의 세부 적용 여부는 해당 연결의 최신 제품 흐름을 확인한다.

## Cross-client Verification

ChatGPT, Claude, OpenClaw은 connector 설정과 권한 표시가 다를 수 있다. 동일한 사용자 시나리오를 각 client에서 검증하고, 다음 변경 후에는 반드시 다시 테스트한다.

- server endpoint 또는 transport 변경
- Tool name, description, JSON Schema 변경
- OAuth scope, redirect URI, consent screen 변경
- Toolbox 구성 변경

## Sources

- [카카오 기술 블로그 — PlayMCP 개발](https://tech.kakao.com/posts/734)
- [카카오 — 도구함 기능](https://www.kakaocorp.com/page/detail/11817)
- [카카오 — OpenClaw 연동](https://www.kakaocorp.com/page/detail/12012)
- [MCP Server specification](https://modelcontextprotocol.io/specification/2025-06-18/server)
