---
date: 2026-07-19
tags: [tech]
type: tech-tool-study
status: draft
---

# Composio — Ecosystem

> [[01-overview|이전: Overview]] · [[README|목차]] · [[03-references|다음: References]]

## Positioning

Composio는 model provider나 agent orchestrator 자체가 아니다. **agent와 외부 service 사이에서 connector, user auth, discovery, execution을 담당하는 action layer**다.

```text
Model API / Agent Framework
          ↓ decides
Composio / MCP / custom integration
          ↓ executes
External SaaS APIs
```

## Alternatives Comparison

| 선택지 | 잘하는 일 | 직접 책임질 것 | 적합한 경우 |
|---|---|---|---|
| Composio Sessions | managed connectors, per-user auth, dynamic discovery, execution state | app-level approval, tenancy validation, domain policy | 여러 SaaS를 쓰는 multi-user agent |
| Direct API integration | 세밀한 control, 최소 dependency | OAuth, refresh, retry, schema, webhook, drift 전부 | API가 적고 규제가 강한 deterministic system |
| Function calling only | model에 callable schema 제공 | 실제 API client, auth, lifecycle, audit | 소수의 이미 구현된 internal function |
| Self-hosted MCP server | protocol portability, hosting/data control | connector 구현·운영, auth, update, observability | 표준 MCP가 필요하고 운영 역량이 있음 |
| Composio hosted MCP | Session tool을 여러 MCP client에 빠르게 노출 | SDK hook이 필요한 policy는 다른 계층에 구현 | portability와 setup speed 우선 |
| Agent framework tools | graph, memory, agent orchestration과 밀착 | connector와 user auth의 지속 관리 | framework 안에 tool이 이미 존재 |
| General iPaaS/workflow | deterministic app-to-app automation | agent-native schema/discovery 설계 | 정해진 trigger/action business automation |

> [!note] 비교 수량 주의
> vendor가 공개한 connector/tool 수는 분류 기준과 action depth가 다르다. 숫자만으로 coverage나 reliability를 비교하지 말고 실제 필요한 action, auth mode, scope, rate limit을 proof of concept에서 확인한다.

## Composio vs MCP

둘은 배타적 경쟁재가 아니다.

| 항목 | MCP | Composio |
|---|---|---|
| 본질 | agent/tool 연결 protocol | connector/auth/execution platform |
| 제공 범위 | message, discovery, invocation contract | maintained toolkit, Connected Account, Session, trigger, sandbox |
| Hosting | local 또는 remote server를 사용자가 선택 | hosted Session별 MCP endpoint 제공 가능 |
| Auth | server/client가 protocol에 맞춰 구현 | managed/custom Auth Config와 token lifecycle 제공 |
| Portability | 여러 MCP-compatible host | MCP endpoint를 사용하면 높음 |
| Local policy | server 구현에 직접 넣기 쉬움 | provider SDK path의 hooks/custom tools가 유리 |

### Hosted MCP trade-off

Hosted MCP 요청은 SDK process를 통과하지 않으므로 다음 기능이 적용되지 않는다.

- `beforeExecute` / `afterExecute`
- schema modifier
- process-local custom tools

따라서 client portability가 핵심이면 hosted MCP, local business logic과 policy enforcement가 핵심이면 provider SDK/direct path가 더 적합하다.

## Composio vs Direct Execution

| 질문 | Dynamic Session | Fixed/preloaded | Direct execution |
|---|---|---|---|
| tool을 누가 고르는가? | agent가 runtime 검색 | agent가 작은 목록에서 선택 | application code |
| context cost | 낮은 시작 비용 | tool 수에 비례 | agent prompt에 불필요할 수 있음 |
| 결정성 | 상대적으로 낮음 | 중간~높음 | 가장 높음 |
| 대표 사용 | 범용 assistant | 좁은 domain agent | batch/job/backend endpoint |

선택 규칙:

```text
자유형 intent + 많은 app       -> dynamic Session
알려진 tool이 대체로 < 20개    -> preload/fixed tools
tool과 arguments를 code가 결정 -> direct execution
```

## Composio vs Agent Framework

LangGraph, CrewAI, OpenAI Agents SDK 같은 framework는 planning, state graph, handoff, memory를 담당한다. Composio는 그 안에 넣을 외부 action과 end-user connection을 제공한다.

```text
LangGraph: workflow/orchestration
OpenAI/Anthropic: reasoning/model tool call
Composio: SaaS tool + user authentication + execution
MCP: optional transport/protocol
```

하나의 제품에서 네 계층을 함께 쓸 수 있다. abstraction이 겹치는 지점—retry, state, tool filtering—의 owner를 명확히 정하지 않으면 중복 retry나 불명확한 audit log가 생긴다.

## Selection Checklist

도입 전에 필요한 실제 workflow 하나를 골라 아래를 검증한다.

- [ ] 필요한 toolkit에 정확한 action과 field가 있는가?
- [ ] managed auth가 있는가, custom OAuth client가 필요한가?
- [ ] 필요한 OAuth scope를 최소화할 수 있는가?
- [ ] organization/user/복수 account를 명시적으로 pin할 수 있는가?
- [ ] destructive action에 approval과 idempotency key를 둘 수 있는가?
- [ ] SDK hooks가 필요한가, hosted MCP로 충분한가?
- [ ] trigger signature와 replay protection을 검증할 수 있는가?
- [ ] rate limit, timeout, retry, partial failure가 관찰 가능한가?
- [ ] toolkit/SDK version을 pin하고 upgrade test를 할 수 있는가?
- [ ] credential storage, data residency, retention 조건이 조직 정책에 맞는가?

## Related Notes

- [[tech/ai/model-context-protocol-mcp/README|Model Context Protocol (MCP)]]
- [[tech/ai/litellm/README|LiteLLM]]
- [[tech/ai/agent-orchestration/cli-agents|CLI Agents]]

## Sources

- https://docs.composio.dev/docs/sessions-vs-direct-execution
- https://docs.composio.dev/docs/sessions-via-mcp
- https://docs.composio.dev/docs/configuring-sessions
- https://docs.composio.dev/docs/extending-sessions/custom-tools-and-toolkits
- https://modelcontextprotocol.io/

