---
date: 2026-07-19
tags: [tech]
type: tech-tool-study
status: draft
---

# Composio — Cheatsheet

> [[05-projects|이전: Projects]] · [[README|목차]]

## Mental Model

```text
User intent
  -> Session(user + access + auth + state)
      -> discover schema
          -> execute with Connected Account
              -> external SaaS
```

## Core Terms

| 용어 | 한 줄 설명 |
|---|---|
| Session | user, tool access, auth, execution state를 묶는 중심 abstraction |
| Toolkit | GitHub/Gmail 같은 service별 action 묶음 |
| Tool | `GITHUB_CREATE_ISSUE` 같은 개별 action |
| Auth Config | auth method, scope, OAuth client를 담는 재사용 blueprint |
| Connected Account | 특정 user가 인증한 실제 service account |
| Managed auth | Composio OAuth app을 쓰는 연결 |
| Custom auth | 제품 자체 OAuth client/credential을 쓰는 연결 |
| Trigger | 외부 event를 signed webhook으로 전달 |
| Sandbox/Workbench | Session의 persistent Python/shell execution environment |
| Hosted MCP | Session tools를 MCP endpoint로 노출하는 경로 |

## Meta Tools

| Tool | 역할 |
|---|---|
| `COMPOSIO_SEARCH_TOOLS` | natural-language intent로 필요한 tool 탐색 |
| `COMPOSIO_GET_TOOL_SCHEMAS` | 선택한 tool의 input/output schema 확보 |
| `COMPOSIO_MANAGE_CONNECTIONS` | Connect Link/OAuth connection 처리 |
| `COMPOSIO_MULTI_EXECUTE_TOOL` | 하나 이상의 tool 실행과 연속 작업 |

## Mode Selector

```text
많은 app + 자유형 intent?       dynamic Session
알려진 tool이 소수(<20 정도)?  preload/fixed tools
code가 tool/input을 결정?       direct execution
MCP client portability?         hosted MCP
local hooks/custom tools?       provider SDK path
```

## Auth Model

```text
Auth Config
  └─ Connected Account(user-specific)
       └─ Session에 명시적으로 pin
```

- immutable application `user_id` 사용
- app user ↔ Session owner 매 요청 검증
- account를 자동 추론하지 않기
- least-privilege OAuth scope
- 신규 flow는 `authorize()`/`link()` 우선 확인
- revoke/expire/reauth UX 준비

## Hosted MCP Gotcha

Hosted MCP는 SDK process를 우회하므로 다음이 적용되지 않는다.

- `beforeExecute`
- `afterExecute`
- schema modifier
- process-local custom tools

중요 policy는 모든 execution path가 공유하는 backend authorization layer에서 강제한다.

## Side-effect Safety

```text
resolve exact input
  -> preview
      -> approve input hash
          -> execute once
              -> verify remote state
                  -> audit
```

- timeout은 failure 확정이 아니다.
- blind retry 금지, remote state 먼저 조회
- idempotency key와 dedupe 사용
- arguments가 바뀌면 재승인
- delete/payment/send는 별도 allowlist와 approval

## Trigger Checklist

- signature 검증
- timestamp/replay window 검증
- event ID dedupe
- user/tenant/Connected Account binding 확인
- webhook에서는 durable queue까지만
- worker retry와 downstream idempotency 분리

## Sandbox Checklist

- 필요 없으면 off
- untrusted tool output을 shell command로 연결하지 않기
- network/file/CPU/time/output 제한
- secret과 PII redaction
- persistent file retention과 tenant boundary 정의

## Version Snapshot

| 항목 | 2026-07-19 조사 snapshot |
|---|---|
| Python | `composio==0.18.0` (2026-07-16 changelog) |
| TypeScript | `@composio/core@0.13.1` (2026-06) |
| Catalog claim | 1,000+ toolkits |
| Stability | pre-1.0 — pin + changelog + migration test |

## Pre-flight

- [ ] 필요한 exact action/schema 확인
- [ ] managed/custom auth와 scope 확인
- [ ] tool allowlist와 account pin 설정
- [ ] SDK vs hosted MCP 경로 선택
- [ ] approval/idempotency/audit 설계
- [ ] schema/discovery golden test
- [ ] pricing/quota/version 재확인

## Sources

- https://docs.composio.dev/docs/how-composio-works
- https://docs.composio.dev/docs/configuring-sessions
- https://docs.composio.dev/docs/sessions-vs-direct-execution
- https://docs.composio.dev/docs/sessions-via-mcp
- https://docs.composio.dev/reference/changelog
- https://github.com/composiohq/composio

