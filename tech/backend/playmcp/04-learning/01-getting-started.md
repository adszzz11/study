---
date: 2026-09-20
tags: [tech]
type: tech-tool-study
status: draft
---

# Getting Started: 첫 MCP Tool부터 PlayMCP Preview까지

## Goal

쓰기 작업이나 결제가 없는 read-only Tool 하나를 만들고 `initialize → tools/list → tools/call` 순서로 검증한다. 예시는 `search_local_events`처럼 외부 API를 조회해 구조화한 결과만 돌려주는 Tool이다.

## 1. Tool Contract 설계

Tool name은 동사로 시작하고, description에는 언제 써야 하는지와 반환 한계를 쓴다. input은 JSON Schema로 좁게 정의한다.

```json
{
  "name": "search_local_events",
  "description": "지정한 지역과 날짜의 공개 지역 행사를 조회한다. 예약이나 알림 발송은 하지 않는다.",
  "inputSchema": {
    "type": "object",
    "properties": {
      "region": { "type": "string", "description": "시·군·구" },
      "date": { "type": "string", "format": "date" }
    },
    "required": ["region", "date"],
    "additionalProperties": false
  }
}
```

## 2. SDK로 최소 구현

TypeScript/Python MCP SDK 중 팀 stack에 맞는 것을 택한다. handler에서는 input 검증, upstream timeout, 오류를 사용자에게 이해 가능한 메시지로 변환하는 일을 먼저 한다.

```ts
server.tool("search_local_events", schema, async ({ region, date }) => {
  const events = await eventApi.search({ region, date, timeoutMs: 3_000 });
  return { content: [{ type: "text", text: JSON.stringify(events) }] };
});
```

이 코드는 개념 예시다. 실제 SDK API, 응답 포맷, 배포 설정은 선택한 SDK의 현재 문서를 따른다.

## 3. Inspector 검증

- `initialize`에서 protocol version과 server capability를 확인한다.
- `tools/list`에 name, description, input schema가 의도대로 노출되는지 본다.
- 정상 입력, 누락 입력, 잘못된 날짜, upstream timeout을 각각 `tools/call`로 실행한다.
- model이 오해할 수 있는 description, 너무 넓은 schema, 내부 오류 원문을 수정한다.

## 4. Remote 배포와 PlayMCP 등록

1. Streamable HTTP를 지원하는 HTTPS endpoint를 배포한다.
2. request ID, latency, tool name, 성공/실패를 structured log로 남긴다. 민감 input·token은 기록하지 않는다.
3. PlayMCP에 server를 등록하고 Preview 대화로 Tool selection을 검증한다.
4. Toolbox에 담은 뒤 대상 client에서도 같은 read-only 시나리오를 시험한다.

## Done Criteria

- [ ] schema가 최소 입력과 실패 입력을 모두 거부/처리한다.
- [ ] Inspector에서 세 MCP lifecycle 호출이 성공한다.
- [ ] Preview가 관련 요청에서만 Tool을 선택한다.
- [ ] timeout과 오류가 민감정보 없이 설명된다.

## Sources

- [MCP Server specification](https://modelcontextprotocol.io/specification/2025-06-18/server)
- [카카오 — PlayMCP 베타 오픈](https://www.kakaocorp.com/page/detail/11674)
