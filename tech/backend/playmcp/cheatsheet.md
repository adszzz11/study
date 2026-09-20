---
date: 2026-09-20
tags: [tech]
type: tech-tool-study
status: draft
---

# PlayMCP Cheatsheet

## Concepts

| 용어 | 빠른 정의 |
|---|---|
| MCP | LLM/client와 외부 data·Tool을 연결하는 protocol |
| MCP server | Prompts, Resources, Tools를 노출하는 구현체 |
| PlayMCP | 등록·탐색·Preview·Toolbox·연결 흐름을 제공하는 카카오 플랫폼 |
| Toolbox | 사용자가 선택한 Tool의 묶음 |
| Streamable HTTP | Remote MCP server에 쓰이는 HTTP transport |
| PKCE | Authorization Code 탈취 위험을 줄이는 OAuth 확장 |

## Build Order

```text
Tool contract → read-only handler → Inspector
→ HTTPS/Streamable HTTP → PlayMCP Preview → Toolbox → client 재검증
```

## Tool Contract

- name: 동사 + 대상 (`search_local_events`)
- description: 사용할 조건, 반환값, 하지 않는 일을 명시
- schema: 최소 field, enum/format, `additionalProperties: false` 고려
- error: 사용자 행동으로 해결 가능한 문장; token·stack trace는 노출 금지

## Release Checklist

- [ ] `initialize`, `tools/list`, `tools/call` 테스트
- [ ] 정상·invalid input·upstream timeout 테스트
- [ ] HTTPS, timeout, rate limit, structured logging 적용
- [ ] OAuth 최소 scope, PKCE, redirect URI/state 검증
- [ ] write Tool의 confirmation·idempotency·audit 적용
- [ ] Preview와 각 AI client에서 Tool selection 재검증
- [ ] endpoint/schema/description 변경 뒤 등록 정보 갱신 여부 확인

## Useful Pointers

- 공개 connector 정보: `https://playmcp.kakao.com/mcp` / `streamable-http` (연결 직전 최신 상태 확인)
- 연결 대상: ChatGPT, Claude, OpenClaw 등은 각 시점의 제품 지원·OAuth 정책을 확인
- 중심 차별점: Kakao account, Kakao service action/data, 카카오톡/Kakao Tools 유통 가능성

## Sources

- [카카오 — 도구함 기능](https://www.kakaocorp.com/page/detail/11817)
- [카카오 — OpenClaw 연동](https://www.kakaocorp.com/page/detail/12012)
- [PlayMCP connector 정보](https://www.tooljunction.io/mcp/playmcp)
