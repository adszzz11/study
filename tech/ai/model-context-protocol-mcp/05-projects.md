---
date: 2026-06-08
tags:
  - tech
  - ai
  - mcp
  - projects
type: tech-tool-study
parent: "[[README]]"
---

# Model Context Protocol (MCP) - 실전 프로젝트

> [[README|목차로 돌아가기]]

---

## 1. 프로젝트 아이디어

| 프로젝트 | 난이도 | 학습 포인트 |
|----------|--------|------------|
| Obsidian note search MCP server | ⭐ | local `stdio`, `tools/list`, `tools/call`, resource URI |
| Internal API MCP wrapper | ⭐⭐ | OpenAPI wrapping, auth, structured error, least privilege |
| RAG/vector search MCP server | ⭐⭐ | search tool, document resource, citation, pagination |
| GitHub issue triage MCP server | ⭐⭐ | destructive action confirmation, audit log, rate limit |
| Remote MCP enterprise connector | ⭐⭐⭐ | Streamable HTTP, OAuth/OIDC, session, registry metadata |
| LLM Wiki ingest workflow server | ⭐⭐⭐ | prompts, resources, long-running task/progress, contradiction flagging |

---

## 2. 프로젝트 1 - Obsidian note search MCP server

### 목표

이 vault의 `study/tech/ai` 노트를 검색하고 읽는 MCP server를 만든다.

| Feature | 설계 |
|---------|------|
| Tool | `search_notes(query, limit)` |
| Resource | `obsidian://study/tech/ai/{path}` |
| Prompt | `summarize_note(path, style)` |
| Transport | local `stdio` |
| Safety | read-only, allowlist path |

### 구조 예시

```text
obsidian-mcp/
├── package.json
├── src/
│   ├── server.ts
│   ├── tools/
│   │   └── search-notes.ts
│   ├── resources/
│   │   └── read-note.ts
│   └── prompts/
│       └── summarize-note.ts
└── README.md
```

### 체크리스트

- [ ] `study/tech/ai` 하위만 검색하도록 allowlist 적용
- [ ] `rg` 또는 index 기반 검색 사용
- [ ] 결과는 title, path, snippet, modified time을 포함
- [ ] resource read는 markdown MIME type 반환
- [ ] path traversal 방지

---

## 3. 프로젝트 2 - Internal API MCP wrapper

### 목표

사내 REST API를 MCP tool로 감싸 여러 AI host에서 재사용한다.

```text
AI Host
  -> MCP Client
    -> Internal API MCP Server
      -> CRM/ERP/Internal DB API
```

| Tool | 설명 | 주의점 |
|------|------|--------|
| `find_customer` | 고객 검색 | PII redaction |
| `get_invoice` | invoice 조회 | scope와 audit log |
| `create_ticket` | support ticket 생성 | confirmation 또는 dry-run |
| `summarize_account` | account 상태 요약 | sampling 사용 가능 |

### Best practice

- OpenAPI schema를 출발점으로 삼되, agent가 쓰기 좋은 tool 단위로 재설계한다.
- Read-only tool부터 시작하고 write/destructive tool은 confirmation flow를 둔다.
- Error message는 "무엇을 다시 물어봐야 하는지"를 포함한다.
- Tool result에는 internal raw payload 전체를 반환하지 않는다.

---

## 4. 프로젝트 3 - Remote MCP server

### 목표

Streamable HTTP와 OAuth/OIDC를 사용하는 remote MCP server를 설계한다.

| 영역 | 구현 포인트 |
|------|-------------|
| Transport | POST/GET, optional SSE, `MCP-Session-Id` |
| Version | `MCP-Protocol-Version` header 처리 |
| Auth | OAuth/OIDC discovery, token validation, scope check |
| Observability | request id, user id, tool name, latency, error log |
| Policy | tool별 allow/deny, tenant boundary |
| Resilience | timeout, retry, resumability, idempotency |

```text
remote-mcp/
├── server/
│   ├── http-transport
│   ├── auth
│   ├── tools
│   ├── resources
│   └── audit
├── docs/
│   ├── oauth.md
│   └── tool-catalog.md
└── tests/
    ├── protocol
    └── security
```

---

## 5. Best Practices

| 영역 | 원칙 |
|------|------|
| Tool design | name은 명확하게, description은 호출 조건까지 포함 |
| Schema | JSON Schema를 좁게 잡고 required/default/min/max를 명시 |
| Error | 모델이 재시도할 수 있는 structured error 반환 |
| Resources | URI, MIME type, pagination, access boundary 명확화 |
| Prompts | 반복 workflow를 user-controlled template으로 제공 |
| Security | least privilege, user consent, audit log, redaction |
| Remote | OAuth/OIDC, session, timeout, retry, version compatibility |
| Operations | server metadata, registry, upgrade policy, monitoring |

---

## 6. 실무 적용 시 고려사항

### 성능

- Tool call latency가 model response latency에 직접 영향을 준다.
- External API timeout은 짧게 잡고, 긴 작업은 task/progress pattern으로 분리한다.
- Resource list는 pagination을 기본으로 둔다.
- Cache 가능한 resource는 ETag/version/hash를 함께 관리한다.

### 보안

- Tool result는 prompt injection source가 될 수 있다.
- Destructive action은 dry-run, confirmation, explicit user approval을 둔다.
- Remote MCP는 OAuth scope, tenant boundary, audit log 없이는 운영하지 않는다.
- File resource는 roots/allowlist/path normalization을 함께 적용한다.

### 모니터링

- tool name, argument shape, latency, error rate, user approval 여부를 기록한다.
- PII나 secret이 log에 남지 않도록 redaction한다.
- Host별 feature 지원 차이를 compatibility matrix로 관리한다.
- Protocol version과 SDK version을 함께 추적한다.

---

## 7. 관련 노트

- [[study/tech/ai/llm-wiki-study]] - Obsidian/LLM Wiki MCP server 프로젝트와 직접 연결
- [[study/tech/ai/litellm]] - remote MCP host가 사용할 LLM routing/gateway 설계
- [[study/tech/ai/openclaw-study]] - messenger gateway와 agent workflow 통합 아이디어
