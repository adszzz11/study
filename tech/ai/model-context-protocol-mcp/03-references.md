---
date: 2026-06-08
tags:
  - tech
  - ai
  - mcp
  - references
type: tech-tool-study
parent: "[[README]]"
---

# Model Context Protocol (MCP) - 참고자료

> [[02-ecosystem|이전: 생태계]] | [[README|목차로 돌아가기]] | [[04-learning/01-getting-started|다음: 시작하기]]

---

## 공식 Specification

| 자료 | URL | 읽을 포인트 |
|------|-----|-------------|
| MCP Specification 2025-11-25 | https://modelcontextprotocol.io/specification/2025-11-25 | protocol version, lifecycle, feature map |
| MCP Architecture | https://modelcontextprotocol.io/specification/2025-11-25/architecture | host/client/server 관계, session model |
| MCP Transports | https://modelcontextprotocol.io/specification/2025-11-25/basic/transports | `stdio`, `Streamable HTTP`, SSE, session header |
| MCP Authorization | https://modelcontextprotocol.io/specification/2025-11-25/basic/authorization | OAuth/OIDC 기반 remote MCP auth |
| Tools | https://modelcontextprotocol.io/specification/2025-11-25/server/tools | `tools/list`, `tools/call`, schema, human-in-the-loop |
| Resources | https://modelcontextprotocol.io/specification/2025-11-25/server/resources | URI, MIME type, list/read, pagination |
| Prompts | https://modelcontextprotocol.io/specification/2025-11-25/server/prompts | reusable prompt/workflow template |
| Elicitation | https://modelcontextprotocol.io/specification/2025-11-25/client/elicitation | form mode, URL mode user input |
| Changelog | https://modelcontextprotocol.io/specification/2025-11-25/changelog | OIDC discovery, tasks, icon metadata, JSON Schema 2020-12 |

---

## 보안/운영

| 자료 | URL | 읽을 포인트 |
|------|-----|-------------|
| MCP Security Best Practices | https://modelcontextprotocol.io/docs/tutorials/security/security_best_practices | consent, least privilege, prompt injection, audit |
| MCP Registry GitHub | https://github.com/modelcontextprotocol/registry | server discovery, registry metadata, ecosystem 방향 |

### 보안 체크 포인트

- Tool은 external side effect를 만들 수 있으므로 host/user approval 흐름이 필요하다.
- Resource는 sensitive data exposure가 생기기 쉬워 URI scope, MIME type, access boundary를 명확히 한다.
- Prompt injection은 external resource나 tool result를 통해 들어올 수 있으므로 trusted/untrusted context를 구분한다.
- Remote MCP는 OAuth/OIDC, session handling, token storage, audit logging을 함께 설계한다.

---

## 생태계 발표/가이드

| 자료 | URL | 읽을 포인트 |
|------|-----|-------------|
| Anthropic MCP launch | https://www.anthropic.com/news/model-context-protocol | MCP 공개 배경과 초기 방향 |
| Anthropic AAIF donation | https://www.anthropic.com/news/donating-the-model-context-protocol-and-establishing-of-the-agentic-ai-foundation | vendor-neutral governance 전환 |
| OpenAI Responses API remote MCP | https://openai.com/index/new-tools-and-features-in-the-responses-api/ | OpenAI Responses API에서 remote MCP 사용 흐름 |
| OpenAI MCP/connectors guide | https://developers.openai.com/api/docs/guides/tools-connectors-mcp | OpenAI tool connector로 MCP 연결 |
| Google ADK MCP | https://adk.dev/mcp/ | Agent Development Kit에서 MCP 사용 |
| Linux Foundation A2A announcement | https://www.linuxfoundation.org/press/linux-foundation-launches-the-agent2agent-protocol-project-to-enable-secure-intelligent-communication-between-ai-agents | A2A와 MCP의 역할 구분 |
| Microsoft official MCP C# SDK v1.0 | https://devblogs.microsoft.com/dotnet/release-v10-of-the-official-mcp-csharp-sdk/ | C# SDK와 enterprise/.NET 생태계 |

---

## 학습 순서

1. **Architecture**: Host/Client/Server 책임 분리부터 읽는다.
2. **Tools**: `tools/list`, `tools/call`, `inputSchema`, structured error를 확인한다.
3. **Resources/Prompts**: tool과 다른 context/workflow primitive를 구분한다.
4. **Transports**: local `stdio`와 remote `Streamable HTTP`를 비교한다.
5. **Authorization/Security**: remote MCP 운영 전 OAuth/OIDC와 security best practices를 읽는다.
6. **Changelog**: `2025-11-25` 변경점을 확인해 최신 feature와 구현 격차를 구분한다.

---

## 관련 노트

- [[study/tech/ai/litellm]] - OpenAI-compatible LLM gateway와 MCP connector의 결합 가능성
- [[study/tech/ai/openclaw-study]] - messenger/agent gateway를 MCP로 확장할 수 있는 맥락
- [[study/tech/ai/agent-orchestration/cli-agents]] - CLI agent tool integration과 MCP server 연결
