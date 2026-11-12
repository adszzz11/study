---
date: 2026-11-13
tags: [tech]
type: tech-tool-study
status: draft
---

# oRPC Cheatsheet

| 항목 | 기억할 점 |
| --- | --- |
| procedure | `os.input(schema).handler(...)`로 validation과 handler를 결합 |
| router | procedure를 plain object path로 조합 |
| client | `createORPCClient` + `RPCLink`, router type으로 호출 추론 |
| validator | Zod, Valibot, ArkType 등 Standard Schema 호환 도구 |
| contract | `oc`로 contract-first package와 implementation 분리 |
| transport | `RPCHandler`를 Node/Fetch/Fastify/Next.js/Hono/Express 등에 mount |
| OpenAPI | metadata에서 REST route와 OpenAPI 3.x document 생성 |
| error | `ORPCError`, `.errors(...)`, global declaration으로 typed error |
| stream | `AsyncIterator` → typed SSE/realtime; retry/resume을 설계 |
| MCP | 같은 procedure 정책을 tool로 재사용; 최소 권한 적용 |

## Release checklist

- [ ] `@orpc/*@beta` version을 pinning했고 release note를 검토했다.
- [ ] Node runtime이 최소 18, 가능하면 22+다.
- [ ] schema validation, auth middleware, typed error를 integration test로 확인했다.
- [ ] OpenAPI document와 실제 REST response가 일치한다.
- [ ] MCP write tool에 allowlist·approval·audit trail이 있다.
- [ ] stream reconnect, resume, duplicate event를 테스트했다.

관련: [[tech/backend/orpc-typesafe-api-framework/03-references|References]] · [[tech/backend/orpc-typesafe-api-framework/README|README]]

## Sources

- https://orpc.dev/docs/getting-started
- https://orpc.dev/docs/requirements
- https://orpc.dev/docs/integrations/mcp
