---
date: 2026-09-01
tags: [tech]
type: tech-tool-study
status: draft
---

# References

## 공식 제품 문서

| 자료 | 확인할 내용 |
|---|---|
| [AI Connector setup](https://www.affinity.studio/help/ai-connector-setup/) | 지원 조건, Claude Connector 설치, Affinity MCP server 활성화 |
| [Affinity integrations](https://www.affinity.studio/integrations) | Connector 정의, beta 상태, 비용 안내 |
| [Automation examples](https://www.affinity.studio/blog/automate-design-tasks-affinity-claude) | layer rename, batch resize, vector cleanup, custom tool 사례 |
| [Canva integrations](https://www.affinity.studio/canva-integrations) | Canva AI Studio 기능, plan, local content 관련 설명 |
| [Anthropic Connector guide](https://support.claude.com/en/articles/11176164-use-connectors-to-extend-claude-s-capabilities) | Claude Desktop Connector 설치와 조직 정책 |

## MCP 표준 문서

| 자료 | 핵심 개념 |
|---|---|
| [Architecture](https://modelcontextprotocol.io/specification/2025-06-18/architecture) | Host → Client → Server, JSON-RPC, capability negotiation |
| [Server primitives](https://modelcontextprotocol.io/specification/2025-06-18/server/index) | `tools`, `resources`, `prompts` |
| [Transports](https://modelcontextprotocol.io/specification/2025-06-18/basic/transports) | 표준의 `stdio`, `Streamable HTTP` transport |

> [!caution]
> MCP 표준이 transport를 정의한다는 사실과 Affinity packaged Connector가 내부적으로 어떤 transport, port, tool schema를 쓰는지는 별개의 문제다. Affinity가 공개 contract로 명시하지 않은 내부 구현을 단정하지 않는다.

## 용어

| 용어 | 이 노트에서의 의미 |
|---|---|
| MCP Host | Connector와 model interaction을 관리하는 Claude Desktop |
| MCP Client | 특정 server와 session을 유지하는 Connector 측 구성요소 |
| MCP Server | Affinity capability를 Claude 쪽에 노출하는 local server |
| Tool | model이 argument를 구성해 실행을 요청할 수 있는 action primitive |
| Scripting API | Affinity document model과 작업을 programmatically 제어하는 interface |
| Scripting panel | 검증한 workflow/script를 저장하고 재실행하는 Affinity UI |
| Non-destructive | 원본을 직접 덮어쓰기보다 layer/adjustment 등 되돌리기 쉬운 구조로 편집하는 방식 |

## 조사 범위와 날짜

- 기준일: **2026-09-01**
- 대상: Canva 계열 디자인 앱 **Affinity의 AI Connector for Claude**
- 제외: 동명의 Affinity CRM MCP, Canva AI Studio 자체의 사용법
- 상태: beta이므로 실제 설치 전 공식 setup page를 다시 확인한다.

## Sources

- [Affinity AI Connector setup](https://www.affinity.studio/help/ai-connector-setup/)
- [MCP specification 2025-06-18](https://modelcontextprotocol.io/specification/2025-06-18/)

