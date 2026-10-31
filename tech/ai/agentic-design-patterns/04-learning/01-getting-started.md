---
date: 2026-10-27
tags: [tech]
type: tech-tool-study
status: draft
---

# Getting started: smallest useful workflow

## 1. Prompt Chaining을 먼저 만든다

`입력 정규화 → 추출 → 검증 → 최종 응답`의 고정 경로로 시작한다. 각 단계의 출력은 다음 단계가 읽는 typed schema로 제한한다.

```text
raw request → normalize_request → extract_facts → validate_facts → response
```

각 단계에 입력/출력, model, timeout, 재시도 가능 여부를 기록한다. 검증 단계가 실패하면 그럴듯한 답을 만들지 말고 재질문 또는 human escalation으로 끝낸다.

## 2. Tool Use 하나를 안전하게 붙인다

검색, DB, API 중 read-only tool 하나를 선택한다.

```json
{
  "name": "search_knowledge_base",
  "input": {"query": "string", "limit": "integer (1-5)"},
  "output": {"results": "array", "source_ids": "array"}
}
```

- invalid argument, timeout, retry 횟수, tool result ID를 trace에 남긴다.
- tool error를 모델에게 그대로 신뢰시키지 말고, 재시도·fallback·중단 규칙을 code로 둔다.
- write tool은 이 단계에서 제외한다.

## 3. RAG와 citation을 추가한다

검색 결과의 source ID/URL을 최종 답변 citation으로 강제한다. 답할 근거가 없을 때는 “근거 없음”을 허용하고, hallucination 사례를 evaluation set에 넣는다.

## 완료 기준

- 정상·빈 결과·잘못된 argument·timeout 입력을 모두 실행했다.
- 답변이 source와 함께 나오거나, 근거 부족을 명확히 표시한다.
- 각 run에서 latency, tool 호출 수, 실패 이유를 확인할 수 있다.

## Sources

- https://www.anthropic.com/research/building-effective-agents
- https://link.springer.com/book/10.1007/978-3-032-01402-3
