---
date: 2026-06-08
tags:
  - tech
  - ai
  - mcp
  - deep-dive
type: tech-tool-study
parent: "[[../README]]"
---

# Model Context Protocol (MCP) - 심화

> [[01-getting-started|이전: 시작하기]] | [[../README|목차로 돌아가기]] | [[../05-projects|다음: 프로젝트]]

---

## 1. Remote MCP와 Streamable HTTP

local `stdio` server는 desktop/CLI 실습에 좋지만, 조직 단위 integration은 remote MCP가 더 중요하다. Streamable HTTP는 POST/GET, optional SSE streaming, session header, protocol version header를 사용해 server와 통신한다.

| 항목 | `stdio` | `Streamable HTTP` |
|------|---------|-------------------|
| 배포 | local process | remote HTTP service |
| 인증 | host/local 환경에 의존 | OAuth/OIDC, bearer token, enterprise policy |
| Streaming | stdout message stream | optional SSE streaming |
| Session | process lifetime 중심 | `MCP-Session-Id` header |
| Version | server/client init 중심 | `MCP-Protocol-Version` header |
| 적합한 경우 | desktop, local tool, 빠른 실험 | SaaS connector, 사내 API, multi-user 환경 |

---

## 2. Authorization 설계

Remote MCP에서는 server가 external system에 접근하므로 auth가 핵심이다.

```text
Host/Client
  -> OAuth/OIDC discovery
  -> authorization flow
  -> access token 획득
  -> Streamable HTTP MCP request
  -> MCP Server
  -> External System
```

### 체크리스트

- [ ] Authorization server metadata discovery를 지원하는가?
- [ ] Client ID metadata가 host/client별로 관리되는가?
- [ ] Token scope가 tool/resource별 최소 권한으로 제한되는가?
- [ ] User consent가 destructive tool call 전에 다시 확인되는가?
- [ ] Audit log에 user, tool name, arguments, result summary가 남는가?
- [ ] Prompt injection으로 tool call이 유도될 때 차단/확인할 수 있는가?

---

## 3. Tool output과 error 설계

MCP tool은 모델이 호출하므로 output은 사람이 읽기 좋은 것과 기계가 후속 판단하기 좋은 것을 함께 고려한다.

| 설계 항목 | 권장 방식 |
|-----------|----------|
| Success result | 요약 text + structured JSON content를 분리 |
| Error result | `isError: true`와 재시도 가능한 구체적 안내 |
| Destructive action | dry-run 또는 confirmation token 패턴 사용 |
| Long-running action | progress notification 또는 experimental tasks 사용 |
| Sensitive result | 최소 필요한 field만 반환하고 redaction 적용 |

```json
{
  "isError": true,
  "content": [
    {
      "type": "text",
      "text": "customer_id is required. Ask the user for a customer id before retrying."
    }
  ]
}
```

---

## 4. Resources vs Tools

| 질문 | Resource | Tool |
|------|----------|------|
| "이 데이터를 읽기만 하는가?" | 적합 | 가능하지만 과함 |
| "외부 side effect가 있는가?" | 부적합 | 적합 |
| "모델이 action으로 호출해야 하는가?" | 보조 context | 적합 |
| "파일/문서/DB row를 browse해야 하는가?" | 적합 | 검색 action은 tool로 가능 |
| "권한 경계를 URI로 표현할 수 있는가?" | 적합 | tool argument validation 필요 |

### 예시

```text
resources/list
  -> obsidian://study/tech/ai/litellm/README.md
  -> obsidian://study/tech/ai/llm-wiki-study/README.md

tools/list
  -> search_notes(query, limit)
  -> create_note(path, title, template)
```

---

## 5. Prompts와 workflow 재사용

Prompt는 tool보다 사용자 의도에 가깝다. 반복되는 업무 절차를 prompt로 노출하면 host UI에서 slash command처럼 사용할 수 있다.

| Prompt | 목적 | Arguments |
|--------|------|-----------|
| `summarize_spec` | 공식 문서를 한국어 학습 노트로 요약 | `url`, `target_level` |
| `compare_tools` | 두 integration 기술 비교 | `tool_a`, `tool_b`, `criteria` |
| `draft_mcp_tool` | API endpoint를 MCP tool schema로 변환 | `endpoint`, `operation` |

```json
{
  "method": "prompts/get",
  "params": {
    "name": "compare_tools",
    "arguments": {
      "tool_a": "MCP",
      "tool_b": "A2A",
      "criteria": "agent interoperability"
    }
  }
}
```

---

## 6. Elicitation과 Sampling

### Elicitation

Server가 작업을 계속하기 위해 사용자 입력이 필요할 때 client/host에 요청한다. `2025-11-25` spec은 form mode와 URL mode를 지원한다.

| Mode | 사용 예 |
|------|---------|
| Form mode | missing parameter, confirmation, choice selection |
| URL mode | OAuth-like external approval, external form, web console 이동 |

### Sampling

Server가 client를 통해 LLM generation을 요청하는 기능이다. API key와 model routing은 host/client가 통제한다.

```text
MCP Server
  -> sampling/createMessage
  -> MCP Client/Host
  -> LLM provider
  -> response
  -> MCP Server
```

Sampling을 쓰면 server가 자체 API key를 보유하지 않고도 요약/분류 같은 LLM 작업을 요청할 수 있다. 다만 host별 지원 여부와 user consent 정책을 확인해야 한다.

---

## 7. Registry와 enterprise 운영

MCP server가 많아지면 "어떤 server를 믿고 설치/연결할 것인가"가 운영 문제로 바뀐다.

| 운영 항목 | 질문 |
|-----------|------|
| Discovery | server metadata, version, icon, capabilities를 어디서 찾는가? |
| Trust | publisher identity와 signature를 검증하는가? |
| Upgrade | protocol version과 server version 호환성을 관리하는가? |
| Policy | 특정 tool/resource를 조직 정책으로 제한할 수 있는가? |
| Observability | request, tool call, auth event, error를 추적하는가? |

---

## 8. Deep-dive 실습 과제

| 과제 | 목표 |
|------|------|
| Remote server 설계 | `search_notes`를 Streamable HTTP MCP server로 설계 |
| OAuth scope 설계 | `notes:read`, `notes:write`, `notes:admin` scope 분리 |
| Resource pagination | vault note 목록을 cursor 기반으로 반환 |
| Prompt template | `summarize_spec` prompt를 MCP prompt로 노출 |
| Elicitation | destructive write 전에 사용자 confirmation 요청 |
| Task/progress | 긴 ingest 작업의 progress notification 설계 |

---

## 관련 노트

- [[study/tech/ai/llm-wiki-study]] - resource/prompt/workflow 설계 대상
- [[study/tech/ai/openclaw-study]] - remote gateway와 notification workflow 맥락
- [[study/tech/ai/multi-agent-platforms]] - MCP와 A2A/agent collaboration의 역할 분리
