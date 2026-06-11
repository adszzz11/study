---
date: 2026-06-08
tags:
  - tech
  - ai
  - mcp
  - cheatsheet
type: tech-tool-study
parent: "[[README]]"
---

# Model Context Protocol (MCP) - 치트시트

> [[README|목차로 돌아가기]]

---

## 핵심 구조

```text
AI Host
  -> MCP Client
    -> MCP Server
      -> External System
```

| 구성요소 | 역할 |
|----------|------|
| Host | 사용자와 LLM이 만나는 AI application. client 관리, consent, sampling 조율 |
| Client | host 내부 connector. server와 1:1 stateful session |
| Server | external system adapter. tools/resources/prompts 노출 |
| Protocol | JSON-RPC 2.0 기반 lifecycle, negotiation, method call |

---

## 자주 쓰는 Method

| 영역 | Method | 설명 |
|------|--------|------|
| Lifecycle | `initialize` | protocol version과 capabilities 교환 |
| Lifecycle | `notifications/initialized` | 초기화 완료 알림 |
| Tools | `tools/list` | tool metadata와 input schema discovery |
| Tools | `tools/call` | tool 실행 |
| Resources | `resources/list` | resource 목록 discovery |
| Resources | `resources/read` | resource 읽기 |
| Prompts | `prompts/list` | prompt template 목록 |
| Prompts | `prompts/get` | prompt template 렌더링 |
| Roots | `roots/list` | server가 접근 가능한 root 목록 |
| Sampling | `sampling/createMessage` | server가 client를 통해 LLM generation 요청 |
| Elicitation | `elicitation/create` | server가 사용자 추가 입력 요청 |

---

## Transport

| Transport | 핵심 | 사용 |
|-----------|------|------|
| `stdio` | stdin/stdout JSON-RPC | local tool, desktop app, 개발/디버깅 |
| `Streamable HTTP` | POST/GET, optional SSE, session header | remote MCP, enterprise connector |

```http
POST /mcp HTTP/1.1
MCP-Protocol-Version: 2025-11-25
MCP-Session-Id: <session-id>
Authorization: Bearer <token>
Content-Type: application/json
```

---

## Tool 설계

```json
{
  "name": "search_notes",
  "description": "Search Obsidian study notes by Korean or English query.",
  "inputSchema": {
    "type": "object",
    "properties": {
      "query": { "type": "string" },
      "limit": { "type": "integer", "minimum": 1, "maximum": 20, "default": 5 }
    },
    "required": ["query"]
  }
}
```

| 체크 | 기준 |
|------|------|
| Name | 짧고 명확한 snake_case |
| Description | 언제 사용해야 하는지 포함 |
| Schema | required, enum, min/max, default 명시 |
| Error | 재시도 가능한 구체적 message |
| Side effect | confirmation 또는 dry-run |

---

## Resource 설계

```json
{
  "uri": "obsidian://study/tech/ai/model-context-protocol-mcp/README.md",
  "name": "MCP README",
  "mimeType": "text/markdown"
}
```

| 체크 | 기준 |
|------|------|
| URI | stable, scoped, path traversal 방지 |
| MIME type | host rendering 판단 가능 |
| Pagination | 많은 목록은 cursor 기반 |
| Boundary | roots/allowlist/ACL 적용 |

---

## Prompt 설계

```json
{
  "name": "summarize_spec",
  "description": "Summarize an MCP specification page into Korean study-note format.",
  "arguments": [
    { "name": "url", "required": true },
    { "name": "target_level", "required": false }
  ]
}
```

| Prompt에 적합한 것 | Tool에 적합한 것 |
|--------------------|------------------|
| 반복 workflow | 외부 system action |
| slash command 성격 | search/create/update/delete |
| 사용자 주도 template | 모델 주도 function call |

---

## Security

| 위험 | 대응 |
|------|------|
| Prompt injection | external content를 untrusted context로 취급 |
| Over-permission | least privilege scope, roots, allowlist |
| Destructive action | explicit approval, dry-run, confirmation token |
| Sensitive output | redaction, field filtering |
| Remote auth | OAuth/OIDC, token validation, tenant boundary |
| Audit gap | user, tool, arguments summary, result, timestamp 기록 |

---

## 최신 Spec 포인트

| 항목 | 의미 |
|------|------|
| Protocol version | `2025-11-25` |
| OIDC discovery | remote authorization discovery 강화 |
| OAuth Client ID Metadata Documents | client metadata 관리 |
| URL mode elicitation | 외부 URL 기반 사용자 입력 |
| Sampling tool calls | sampling 중 tool call 지원 |
| Experimental tasks | long-running workflow 지원 방향 |
| Icon metadata | host UI 표시 개선 |
| JSON Schema 2020-12 | schema 표현력 개선 |

---

## 한 줄 구분

| 기술 | 기억할 문장 |
|------|-------------|
| MCP | Agent가 tool/data/prompt를 발견하고 호출하는 protocol |
| Function Calling | 특정 model API 안의 tool schema |
| OpenAPI | REST API contract |
| A2A | Agent끼리 대화/협업하는 protocol |
| LangChain tools | framework 내부 tool abstraction |
| RAG | private knowledge retrieval pipeline |

---

## 관련 노트

- [[study/tech/ai/litellm]] - LLM gateway와 MCP connector를 함께 설계
- [[study/tech/ai/llm-wiki-study]] - vault knowledge를 MCP resource/tool로 노출
- [[study/tech/ai/multi-agent-platforms]] - agent framework와 protocol 생태계 비교
