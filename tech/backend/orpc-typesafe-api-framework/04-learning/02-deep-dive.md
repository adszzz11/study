---
date: 2026-11-13
tags: [tech]
type: tech-tool-study
status: draft
---

# oRPC Deep Dive

## 1. Auth와 typed error

context와 middleware로 identity를 주입하고 `.errors(...)` 및 `ORPCError`로 authorization failure를 API contract에 올린다. error code, 사용자 노출 메시지, audit log를 분리한다.

## 2. Contract-first monorepo

`@repo/api-contract`에는 `oc` 기반 input/output/error contract를, server package에는 implementation을 둔다. web·Expo·CLI는 contract type 기반 client를 사용해 implementation dependency를 피한다.

## 3. OpenAPI와 stream

OpenAPI metadata를 붙여 REST endpoint와 specification을 만들고 Scalar 또는 Swagger UI에서 검증한다. `async function*` procedure는 SSE로 노출하고 reconnect 시 event ID, retry, resume 및 backpressure를 시험한다.

## 4. MCP 노출

`@orpc/mcp`에서 동일 procedure의 schema·metadata·middleware·error handling을 재사용한다. write 권한 tool은 allowlist, least privilege, human approval을 추가한다.

| 점검 | 질문 |
| --- | --- |
| version | beta breaking change를 pinning·CI로 감지하는가? |
| runtime | Node 18 최소/Node 22+ 권장 조건을 충족하는가? |
| security | MCP tool이 필요한 procedure와 권한만 노출하는가? |
| reliability | stream reconnect와 duplicate event를 처리하는가? |

관련: [[tech/backend/orpc-typesafe-api-framework/05-projects|Projects]] · [[tech/backend/orpc-typesafe-api-framework/cheatsheet|Cheatsheet]]

## Sources

- https://orpc.dev/docs/contract
- https://orpc.dev/docs/openapi
- https://orpc.dev/docs/integrations/mcp
- https://orpc.dev/docs/requirements
