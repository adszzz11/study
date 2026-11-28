---
date: 2026-11-13
tags: [tech]
type: tech-tool-study
status: draft
---

# oRPC: TypeScript end-to-end typesafe API framework

> **한 줄 정의**: oRPC는 TypeScript procedure를 한 번 정의해 typed RPC client, REST/OpenAPI, MCP tool, realtime stream으로 노출하는 API framework다.

## Overview

서버 endpoint, validation schema, client 호출 코드, API 문서를 따로 유지하면 type drift가 생기기 쉽다. oRPC는 procedure의 input/output type과 runtime validation을 연결하고 code generation 없이 client까지 추론한다. 내부 TypeScript client에는 RPC 개발 경험을, 외부·모바일·파트너에는 REST/OpenAPI interface를 함께 제공하려는 팀에 특히 맞는다.

```text
procedure (schema + handler + metadata)
        ├─ typed RPC client
        ├─ REST route + OpenAPI 3.x
        ├─ SSE / realtime stream
        └─ MCP tool
```

현재 v2 문서는 `beta` package를 안내한다. production에서는 version pinning, breaking change 공지, v1/v2 migration 계획을 먼저 검토한다.

## Learning Path

- [ ] [[tech/backend/orpc-typesafe-api-framework/README|Study Home]]에서 도입 목적과 적용 경계를 확인한다.
- [ ] [[tech/backend/orpc-typesafe-api-framework/01-overview|Overview]]에서 procedure, router, contract의 역할을 이해한다.
- [ ] [[tech/backend/orpc-typesafe-api-framework/04-learning/01-getting-started|시작하기]]로 Zod procedure 두 개와 `RPCLink` 호출을 만든다.
- [ ] context, middleware, `.errors(...)`를 추가해 인증과 typed authorization error를 구현한다.
- [ ] [[tech/backend/orpc-typesafe-api-framework/04-learning/02-deep-dive|Deep Dive]]에서 contract-first, OpenAPI, stream, MCP를 확장한다.
- [ ] [[tech/backend/orpc-typesafe-api-framework/02-ecosystem|Ecosystem]]으로 tRPC·Hono·ts-rest·NestJS 선택 기준을 비교한다.
- [ ] [[tech/backend/orpc-typesafe-api-framework/05-projects|Projects]] 중 하나를 구현하고 [[tech/backend/orpc-typesafe-api-framework/cheatsheet|Cheatsheet]]로 점검한다.
- [ ] [[tech/backend/orpc-typesafe-api-framework/03-references|References]]의 공식 문서로 설치 버전과 runtime 요구사항을 재확인한다.

## When To Use

- TypeScript full-stack에서 internal RPC DX와 public OpenAPI를 동시에 원할 때
- monorepo contract package로 web, mobile, CLI에 typed SDK를 배포할 때
- API procedure를 MCP tool 또는 typed SSE stream으로 재사용할 때

## When Not To Use

- REST의 resource model과 HTTP semantics만이 계약의 중심일 때
- TypeScript client 공유 없이 다른 언어 client가 주 소비자일 때
- beta lifecycle을 추적·고정할 운영 여력이 없을 때

## Related Notes

- [[MOCs/Index]]
- [[MOCs/Backend]]
- [[tech/backend/http/README|HTTP]]
- [[tech/backend/orpc-typesafe-api-framework/01-overview|oRPC Overview]]

## Sources

- https://orpc.dev/
- https://orpc.dev/docs/getting-started
- https://orpc.dev/docs/requirements
- https://github.com/middleapi/orpc/releases
