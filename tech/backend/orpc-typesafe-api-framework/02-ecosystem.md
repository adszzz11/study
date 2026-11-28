---
date: 2026-11-13
tags: [tech]
type: tech-tool-study
status: draft
---

# oRPC Ecosystem and Comparison

| 선택지 | 강점 | oRPC 대비 적합한 경우 |
| --- | --- | --- |
| oRPC | RPC DX, contract-first, OpenAPI, MCP, typed stream 통합 | TypeScript full-stack과 외부 REST/AI agent interface를 함께 운영할 때 |
| tRPC | 성숙한 TypeScript RPC ecosystem | OpenAPI가 핵심이 아니고 tRPC 자산·팀 경험이 클 때 |
| Hono | 가볍고 빠른 multi-runtime web framework | HTTP routing, middleware, edge-first framework가 우선일 때 |
| ts-rest | contract-first REST와 OpenAPI 중심 | REST contract와 HTTP semantics가 최우선일 때 |
| NestJS + OpenAPI | DI, module, enterprise convention | NestJS architecture를 표준으로 유지할 때 |

oRPC 공식 비교는 세 도구가 end-to-end input/output type safety를 제공한다고 설명한다. 다만 oRPC의 contract-first와 first-class OpenAPI 장점 평가는 공급자 자료이므로 팀의 기존 framework 경험과 API 소비자 구성을 함께 검증한다.

선택 질문:

- internal TypeScript client와 public REST client를 동시에 지원해야 하는가?
- contract package가 implementation package와 독립 배포되어야 하는가?
- MCP와 SSE를 같은 procedure 정책 아래 두려는가?

관련: [[tech/backend/orpc-typesafe-api-framework/01-overview|Overview]] · [[tech/backend/orpc-typesafe-api-framework/05-projects|Projects]]

## Sources

- https://orpc.dev/docs/comparison
- https://trpc.io/
- https://hono.dev/
- https://ts-rest.com/
