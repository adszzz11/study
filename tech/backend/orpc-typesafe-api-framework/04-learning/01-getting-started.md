---
date: 2026-11-13
tags: [tech]
type: tech-tool-study
status: draft
---

# oRPC Getting Started

## 목표

두 procedure를 정의하고 `/rpc` adapter와 `RPCLink` client로 호출한다. v2 문서가 안내하는 beta version은 lockfile로 고정한다.

```sh
pnpm add @orpc/server@beta @orpc/client@beta zod
```

## 실습 순서

1. `os.input(...).handler(...)`로 `health`, `greet` procedure를 만든다.
2. `{ health, greet }` plain object router를 `RPCHandler`에 전달한다.
3. Node 또는 Next.js Fetch adapter에서 `/rpc`로 mount한다.
4. `createORPCClient`와 `RPCLink`에 router type을 제공하고 `client.greet(...)`를 호출한다.
5. invalid input이 runtime validation에서 거절되는지, TypeScript가 잘못된 호출을 막는지 확인한다.

```ts
// 개념 예시: 현재 adapter별 정확한 API는 공식 Getting Started로 확인
const greet = os.input(z.object({ name: z.string().min(1) }))
  .handler(({ input }) => ({ greeting: `Hello ${input.name}` }))
```

## 완료 기준

- 컴파일 시 input/output type이 client에 추론된다.
- invalid request는 handler에 도달하지 않는다.
- transport code가 business handler를 직접 복제하지 않는다.

다음: [[tech/backend/orpc-typesafe-api-framework/04-learning/02-deep-dive|Deep Dive]] · [[tech/backend/orpc-typesafe-api-framework/01-overview|Overview]]

## Sources

- https://orpc.dev/docs/getting-started
- https://orpc.dev/docs/adapters
