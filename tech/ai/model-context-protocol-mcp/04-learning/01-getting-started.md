---
date: 2026-06-08
tags:
  - tech
  - ai
  - mcp
  - learning
type: tech-tool-study
parent: "[[../README]]"
---

# Model Context Protocol (MCP) - 시작하기

> [[../README|목차로 돌아가기]] | [[02-deep-dive|다음: 심화]]

---

## 1. 목표

local `stdio` MCP server를 하나 만들고 MCP Inspector에서 다음 흐름을 확인한다.

- `initialize` lifecycle
- `tools/list` discovery
- `tools/call` invocation
- structured result/error
- host/client/server 책임 분리

---

## 2. 준비

```bash
# Node.js 기반 Inspector 실행
npx @modelcontextprotocol/inspector
```

Inspector에서는 server command와 arguments를 입력해 local process를 MCP server로 띄운다. 예제 server는 TypeScript/Python SDK 중 하나로 만들면 된다.

| 선택 | 장점 | 추천 상황 |
|------|------|----------|
| TypeScript SDK | Node 생태계, desktop/IDE integration 예제가 많음 | JS/TS tool 개발에 익숙할 때 |
| Python SDK | data/automation script와 결합 쉬움 | DB, RAG, internal script를 감쌀 때 |

---

## 3. 첫 번째 Tool 설계

### Tool metadata

```json
{
  "name": "search_notes",
  "description": "Search Obsidian study notes by Korean or English query.",
  "inputSchema": {
    "type": "object",
    "properties": {
      "query": {
        "type": "string",
        "description": "Search query. Use Korean or English keywords."
      },
      "limit": {
        "type": "integer",
        "minimum": 1,
        "maximum": 20,
        "default": 5
      }
    },
    "required": ["query"]
  }
}
```

### 설계 원칙

- Tool name은 짧고 동사 중심으로 작성한다. 예: `search_notes`, `create_issue`, `read_customer`.
- Description은 모델이 **언제 호출해야 하는지** 판단할 수 있게 쓴다.
- `inputSchema`는 JSON Schema로 엄격히 작성한다.
- Error는 모델이 self-correction할 수 있도록 구체적으로 반환한다.

```json
{
  "isError": true,
  "content": [
    {
      "type": "text",
      "text": "limit must be between 1 and 20. Retry with a smaller limit."
    }
  ]
}
```

---

## 4. Inspector에서 확인할 흐름

| 단계 | 확인 method | 확인할 것 |
|------|-------------|-----------|
| 연결 | `initialize` | protocol version, client/server capabilities |
| Tool discovery | `tools/list` | name, description, inputSchema |
| Tool call | `tools/call` | arguments validation, result format |
| Error | `tools/call` | invalid argument에서 structured error 반환 |
| Logging | notification | server log가 host/debug UI에 전달되는지 |

---

## 5. Resource 설계 맛보기

Tool은 action이고, Resource는 context/data다. file/document/DB row를 읽히려면 resource로 설계한다.

```json
{
  "uri": "obsidian://study/tech/ai/model-context-protocol-mcp/README.md",
  "name": "MCP study README",
  "mimeType": "text/markdown",
  "description": "Overview and learning path for MCP study notes."
}
```

| 항목 | 설계 기준 |
|------|-----------|
| URI | stable하고 scope가 명확해야 함 |
| MIME type | host가 rendering/processing을 판단할 수 있게 제공 |
| Pagination | 많은 resource를 노출할 때 cursor 기반으로 제한 |
| Access boundary | roots 또는 server-side ACL로 제한 |

---

## 6. Prompt 설계 맛보기

반복 workflow는 prompt로 제공한다.

```json
{
  "name": "summarize_spec",
  "description": "Summarize an MCP specification page into Korean study-note format.",
  "arguments": [
    {
      "name": "url",
      "description": "Specification URL to summarize",
      "required": true
    }
  ]
}
```

Prompt는 model이 임의로 호출하는 tool보다 사용자 workflow에 가깝다. slash command처럼 "이 작업을 시작해줘"라는 명시적 의도가 있을 때 유용하다.

---

## 7. 트러블슈팅

| 문제 | 원인 | 해결 |
|------|------|------|
| Inspector가 server를 못 띄움 | command/path 오류 | 절대 경로로 command를 입력하고 실행 권한 확인 |
| `tools/list`가 비어 있음 | server capability 등록 누락 | server 초기화 시 tools capability와 handler 확인 |
| tool call이 실패 | schema와 handler argument 불일치 | JSON Schema required/default와 handler validation 맞추기 |
| 모델이 tool을 잘못 호출 | description이 모호함 | "언제 사용/사용하지 말아야 하는지" description에 추가 |
| local file 접근이 과도함 | roots boundary 없음 | host roots 설정 또는 server-side allowlist 적용 |

---

## 실습 체크리스트

- [ ] Inspector로 server 연결 성공
- [ ] `tools/list`에서 tool metadata 확인
- [ ] 정상 `tools/call` 결과 확인
- [ ] 잘못된 argument에서 structured error 확인
- [ ] resource URI와 MIME type 설계
- [ ] prompt template 하나 설계

---

## 관련 노트

- [[study/tech/ai/llm-wiki-study]] - Obsidian vault resource/tool 실습 대상
- [[study/tech/ai/agent-orchestration/cli-agents]] - CLI agent에서 MCP server를 사용하는 흐름
- [[study/tech/ai/litellm]] - host 쪽 LLM gateway와 MCP server를 분리해서 생각하기
