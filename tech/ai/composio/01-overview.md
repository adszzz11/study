---
date: 2026-07-19
tags: [tech]
type: tech-tool-study
status: draft
---

# Composio — Overview

> [[README|목차로 돌아가기]] · [[02-ecosystem|다음: Ecosystem]]

## What

Composio는 AI agent를 외부 service와 연결하는 **agent integration/action infrastructure**다. 단순한 function schema registry가 아니라 다음 lifecycle을 함께 다룬다.

- 어떤 action이 필요한지 찾는 **tool discovery**
- end user별 OAuth/API key를 연결하는 **authentication**
- schema에 맞춰 action을 호출하는 **execution**
- 외부 event를 agent에 전달하는 **triggers**
- 여러 결과를 가공하는 **Sandbox/Workbench**

### Toolkit과 Tool

| 개념 | 의미 | 예시 |
|---|---|---|
| Toolkit | 하나의 service에 대한 action 묶음 | GitHub, Gmail, Slack |
| Tool | agent가 호출하는 개별 action | `GITHUB_CREATE_ISSUE`, `GMAIL_SEND_EMAIL` |
| Tool schema | LLM과 runtime이 공유하는 JSON Schema | input/output field, description |
| Toolkit version | direct/manual execution 시 선택 가능한 connector snapshot | `latest`, `20251027_00` 형식 |

2026-07-19 기준 공식 문서와 repository는 1,000+ toolkits를 표방한다. 일부 과거 페이지의 500+ 표기와 섞일 수 있으므로 숫자는 고정된 benchmark가 아니라 시점별 vendor snapshot으로 해석한다.

## Why

LLM에 외부 API를 붙이는 일은 function schema 작성만으로 끝나지 않는다.

| 문제 | 실제 위험 | Composio의 접근 |
|---|---|---|
| Integration fragmentation | OAuth scope, pagination, rate limit, webhook, error 형식이 service마다 다름 | 유지되는 toolkit과 공통 execution layer |
| Multi-tenant auth | 잘못된 사용자/조직 account로 action을 실행할 수 있음 | `user_id`, Auth Config, Connected Account를 Session에 scope |
| Context bloat | 수백 개 schema가 token을 쓰고 tool-selection 오류를 늘림 | meta tools 기반 dynamic discovery |
| API drift | upstream API와 schema 변경이 application을 깨뜨림 | toolkit version과 connector maintenance |
| Stateful execution | discovery→auth→여러 호출→가공→retry가 이어져야 함 | Session state와 Sandbox/Workbench |
| Side-effect safety | retry가 이메일 중복 발송·중복 결제를 만들 수 있음 | log와 policy hook을 활용하되 승인/idempotency는 app도 설계 |

## Architecture

```text
Application / AI Agent
        │
        │ Provider SDK 또는 MCP
        ▼
Composio Session ─── user_id / allowed tools / auth / state
        │
        ├─ COMPOSIO_SEARCH_TOOLS
        ├─ COMPOSIO_GET_TOOL_SCHEMAS
        ├─ COMPOSIO_MANAGE_CONNECTIONS
        ├─ COMPOSIO_MULTI_EXECUTE_TOOL
        └─ Sandbox / Workbench
        │
        ▼
Connected Account ─── Gmail / Slack / GitHub / SaaS API
```

Session이 묶는 네 영역:

1. **User** — application이 부여한 안정적인 `user_id`
2. **Tool access** — 전체 catalog 또는 allowlist/denylist된 toolkit/tool
3. **Authentication** — managed/custom Auth Config와 Connected Account
4. **Execution state** — logs, tool memory, MCP state, sandbox files

Session ID를 저장하면 multi-turn 대화에서 `composio.use()`로 같은 context를 복구할 수 있다. 단, Session ID 자체를 authorization의 대체물로 취급해서는 안 된다. application의 authenticated user와 Session owner를 매 요청 검증해야 한다.

## Core Features

### Dynamic discovery

기본 Session은 모든 app schema가 아니라 소수의 meta tools를 agent에 제공한다. Agent는 intent로 tool을 검색하고 schema를 얻은 뒤 실행한다.

| 방식 | 적합한 경우 | 주의점 |
|---|---|---|
| Dynamic search | 자유형 assistant, catalog가 큼 | 검색 품질과 허용 범위를 평가해야 함 |
| `preload.tools` | 자주 쓰는 tool이 소수로 알려짐 | 공식 권장처럼 대체로 20개 미만 유지 |
| `direct_tools` preset | 결정론적 workflow, 정확한 목록 | 유연성보다 예측 가능성 우선 |
| Direct execution | backend가 tool name/input을 이미 결정 | LLM discovery가 필요 없음 |

### Authentication

```text
Auth Config (재사용 blueprint)
  └─ Connected Account (특정 사용자의 실제 연결)
       └─ Session에서 선택 또는 pin
```

- **Managed auth**: Composio가 제공하는 OAuth app을 사용한다.
- **Custom auth**: 제품의 OAuth client, branding, scope, quota를 사용한다.
- token 저장과 refresh는 platform이 처리한다.
- managed auth가 없는 toolkit은 custom credential이 필요할 수 있다.
- 복수 account가 있으면 의도한 Connected Account를 명시적으로 pin한다.
- 신규 구현은 deprecated된 `initiate()` 예시보다 Session `authorize()` 또는 hosted `link()` 흐름을 우선 확인한다.

### SDK, framework, MCP

- TypeScript SDK: `@composio/core`
- Python SDK: `composio`
- Provider adapters: OpenAI, OpenAI Agents, Anthropic, Claude Agent SDK, LangChain/LangGraph, LlamaIndex, Gemini, Vercel AI SDK, CrewAI, AutoGen 등
- Hosted MCP: Session별 endpoint를 만들어 framework-independent client에 연결
- CLI: search, link, execute, script workflow 지원

2026-07-16 changelog 기준 Python SDK는 `0.18.0`, TypeScript core는 2026-06에 `0.13.1`이 공개됐다. 둘 다 pre-1.0이므로 dependency를 pin하고 upgrade 전에 migration guide와 changelog를 확인한다.

### Custom tools, triggers, sandbox

| 기능 | 역할 | 중요한 경계 |
|---|---|---|
| Standalone tool | 내부 DB query, business rule 등 local logic | process-local |
| Extension tool | 기존 toolkit 확장, `proxyExecute()`로 인증된 API 호출 | toolkit auth 재사용 |
| Custom toolkit | 여러 내부 tool을 namespace로 묶음 | 배포 위치 확인 |
| Trigger | Gmail 새 메일, GitHub commit 등을 signed webhook으로 수신 | signature, replay, idempotency 검증 |
| Sandbox/Workbench | Python/shell로 여러 tool 결과를 가공 | 필요 없으면 비활성화하고 입력/출력 제한 |

Custom tool은 Session search/multi-execution에 섞일 수 있지만 process-local이다. 따라서 hosted MCP나 remote sandbox가 local code를 자동 실행해 준다고 가정하면 안 된다.

## Strengths and Limits

### 강점

- connector와 auth lifecycle을 제품 개발에서 분리한다.
- user-scoped Session으로 multi-tenant agent의 기본 경계를 제공한다.
- dynamic discovery로 large catalog의 context cost를 줄인다.
- SDK, agent framework, hosted MCP 중 integration surface를 선택할 수 있다.
- trigger와 sandbox까지 action workflow에 포함한다.

### 한계와 책임

- platform abstraction을 써도 least privilege, approval, idempotency는 application 책임이 남는다.
- hosted MCP는 portable하지만 SDK process의 hooks/schema modifier/local custom tools를 우회한다.
- vendor catalog 수량은 connector 품질·action coverage의 독립 benchmark가 아니다.
- pre-1.0 SDK와 빠른 product migration은 upgrade cost를 만든다.
- credential/execution을 외부 platform에 맡기는 vendor, privacy, residency 검토가 필요하다.

## Sources

- https://docs.composio.dev/docs/how-composio-works
- https://docs.composio.dev/docs/configuring-sessions
- https://docs.composio.dev/docs/sessions-vs-direct-execution
- https://docs.composio.dev/reference
- https://docs.composio.dev/reference/api-reference/auth-configs
- https://docs.composio.dev/docs/auth-configuration/connected-accounts
- https://docs.composio.dev/docs/extending-sessions/custom-tools-and-toolkits
- https://docs.composio.dev/reference/changelog

