---
date: 2026-07-19
tags: [tech]
type: tech-tool-study
status: draft
---

# Composio

> **한 줄 정의**: Composio는 AI agent가 외부 서비스에서 실제 action을 수행하도록 tool discovery, per-user authentication, execution, triggers, sandbox를 통합하는 agent integration/action infrastructure다.

## Overview

Composio는 Gmail, Slack, GitHub 같은 SaaS API를 agent에 연결할 때 반복되는 OAuth, token refresh, schema 관리, tool discovery, webhook, 실행 상태 문제를 하나의 platform abstraction으로 묶는다.

핵심 단위는 **Session**이다. Session은 애플리케이션의 안정적인 `user_id`, 허용된 toolkit/tool, 사용자의 Connected Account, 실행 상태를 함께 scope한다. Agent는 모든 connector schema를 prompt에 싣는 대신 소수의 meta tools로 필요한 tool을 runtime에 찾고, 인증하고, 실행할 수 있다.

```text
AI Agent
  -> Composio Session
      -> tool discovery / auth / execution / sandbox
          -> Connected Account
              -> Gmail / Slack / GitHub / SaaS API
```

> [!warning] 조사 시점
> 이 노트는 2026-07-19 기준이다. catalog 수량, 가격, SDK version, API surface는 빠르게 바뀌므로 도입 직전에 공식 docs와 changelog를 다시 확인한다.

## Learning Path

- [ ] [[01-overview|Overview]] — What/Why, Session 중심 architecture 이해
- [ ] [[02-ecosystem|Ecosystem]] — direct API, MCP, agent framework, iPaaS와 비교
- [ ] [[03-references|References]] — 공식 docs, API reference, changelog 읽기
- [ ] [[04-learning/01-getting-started|Getting started]] — 첫 Session과 user connection 흐름 설계
- [ ] [[04-learning/02-deep-dive|Deep dive]] — auth isolation, discovery, hooks, trigger, sandbox 심화
- [ ] [[05-projects|Projects]] — 실제 agent integration 프로젝트로 검증
- [ ] [[cheatsheet|Cheatsheet]] — 용어, 선택 기준, 운영 checklist 복습

## When To Use

- 여러 외부 SaaS를 쓰는 AI assistant를 빠르게 구축할 때
- 각 end user의 권한으로 action을 실행하는 multi-tenant agent가 필요할 때
- 많은 tool 중 필요한 것만 runtime에 찾아 context bloat를 줄이고 싶을 때
- OAuth lifecycle, connector update, trigger, execution log를 직접 운영하고 싶지 않을 때
- provider SDK 또는 hosted MCP를 통해 여러 agent framework에 같은 integration layer를 제공할 때
- 여러 API 결과를 Python/shell로 가공하는 stateful workflow가 필요할 때

## When Not To Use

- 외부 API가 하나이고 고정된 read-only endpoint 몇 개만 호출하면 될 때
- compliance 또는 data residency 때문에 credential과 execution을 제3자 platform에 맡길 수 없을 때
- 모든 auth, retry, rate limit, audit 동작을 application이 완전히 통제해야 할 때
- hosted MCP를 쓰면서 local hooks, schema modifier, process-local custom tool까지 기대할 때
- 결정론적 backend job인데 LLM 기반 dynamic discovery가 불필요할 때
- high-risk side effect에 대한 승인, idempotency, 보상 transaction을 별도로 설계할 여력이 없을 때

## Related Notes

- [[MOCs/Index]]
- [[MOCs/AI]]
- [[tech/ai/model-context-protocol-mcp/README|Model Context Protocol (MCP)]] — hosted MCP 경로와 protocol layer 비교
- [[tech/ai/litellm/README|LiteLLM]] — model gateway와 action infrastructure의 역할 분리
- [[tech/ai/agent-orchestration/cli-agents|CLI Agents]] — agent runtime에서 tool을 사용하는 맥락

## Sources

- https://docs.composio.dev/docs
- https://docs.composio.dev/docs/how-composio-works
- https://docs.composio.dev/docs/configuring-sessions
- https://docs.composio.dev/docs/sessions-vs-direct-execution
- https://github.com/composiohq/composio

