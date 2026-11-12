---
date: 2026-11-13
tags: [tech]
type: tech-tool-study
status: draft
---

# oRPC Overview

## What

oRPC는 `os` builder로 schema와 handler를 묶어 procedure를 만들고, plain object router에 path를 구성한다. Zod, Valibot, ArkType 등 Standard Schema 호환 validator를 사용할 수 있다.

```ts
const ping = os.input(z.object({ name: z.string() }))
  .handler(({ input }) => ({ message: `Hello, ${input.name}` }))

const router = { ping }
```

## Why

동일 API의 server·validator·typed client·OpenAPI를 별도로 관리하는 비용을 줄인다. router와 business logic은 transport에서 분리되므로 Node HTTP, Fetch API, Fastify, Next.js, Hono, Express, WebSocket adapter에 연결할 수 있다.

## 핵심 특징

| 기능 | 의미 |
| --- | --- |
| `RPCHandler` / `RPCLink` | server adapter와 local-function 같은 typed client 호출 |
| `oc` contract | contract와 implementation을 분리하는 contract-first 경계 |
| OpenAPI | metadata에서 REST route·OpenAPI 3.x 문서·reference UI 생성 |
| typed error | `ORPCError`, procedure/global error declaration |
| stream | `AsyncIterator`를 typed SSE/realtime stream으로 노출 |
| native type | File/Blob, `Date`, `BigInt`, `Set`, `Map` 전송 지원 |
| MCP | schema·metadata·middleware·error handling 재사용 |

다음: [[tech/backend/orpc-typesafe-api-framework/04-learning/01-getting-started|시작하기]] · [[tech/backend/orpc-typesafe-api-framework/02-ecosystem|Ecosystem]]

## Sources

- https://orpc.dev/
- https://orpc.dev/docs/adapters
- https://orpc.dev/docs/contract
- https://orpc.dev/docs/openapi
