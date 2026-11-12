---
date: 2026-11-13
tags: [tech]
type: tech-tool-study
status: draft
---

# oRPC Projects

## SaaS BFF

Next.js, TanStack Query, Better Auth, PostgreSQL을 oRPC router로 연결하고, 외부 고객에는 OpenAPI endpoint를 제공한다. internal RPC와 external REST의 authorization policy가 같은지 테스트한다.

## AI operations console

관리 API 중 승인된 procedure만 MCP tool로 expose한다. read/write tool을 분리하고 write에는 approval과 audit trail을 추가한다.

## Monorepo typed SDK

contract package를 publish하고 web, Expo mobile, internal CLI가 같은 typed client를 사용하게 한다. consumer가 server implementation을 import하지 않는지 확인한다.

## Realtime collaboration

document 또는 job status를 typed SSE로 보낸다. reconnect 후 event ID 기반 resume, duplicate suppression, timeout을 검증한다.

## NestJS modernization

기존 Nest controller의 domain service 앞에 oRPC contract를 적용해 typed client와 OpenAPI를 함께 확보한다. 한 번에 교체하지 말고 bounded context별로 전환한다.

관련: [[tech/backend/orpc-typesafe-api-framework/02-ecosystem|Ecosystem]] · [[tech/backend/orpc-typesafe-api-framework/04-learning/02-deep-dive|Deep Dive]]

## Sources

- https://orpc.dev/docs/openapi
- https://orpc.dev/docs/integrations/mcp
- https://orpc.dev/docs/contract
