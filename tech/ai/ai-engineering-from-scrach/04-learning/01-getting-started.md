---
date: 2026-10-19
tags: [tech]
type: tech-tool-study
status: draft
---

# AI Engineering from Scratch — Getting Started

> [[README|목차로 돌아가기]]

## Goal

한 개의 FastAPI endpoint에서 streaming, structured output, tool calling, token·latency logging을 제공하고, 작지만 측정 가능한 RAG workflow를 만든다.

## 1. Define the Contract First

```text
POST /answer
input:  question, user_id, requested_action
output: answer, citations[], request_id, latency_ms
```

- answer schema를 JSON Schema/Pydantic model로 고정한다.
- `request_id`, model name, prompt version, input/output token, latency를 매 request에 기록한다.
- tool의 input/output과 policy decision을 trace에 남긴다. credential과 PII 원문은 남기지 않는다.

## 2. Build a Minimal RAG

1. 공개 또는 권한이 명확한 문서 50개를 선정한다.
2. parsing → chunking → metadata → embedding/indexing을 분리한다.
3. metadata filter와 retrieval 결과의 source URL을 response에 포함한다.
4. 질문 30개에 대해 top-k retrieval recall, citation correctness, answer faithfulness를 수동 표기한다.

## 3. Add One Read-only Tool

처음에는 `search_documents(query, filters)`처럼 read-only이고 typed된 tool을 쓴다. tool timeout, maximum result size, authorization check를 명시한다. write tool과 autonomous loop는 eval 기준선 이후로 미룬다.

## Done Criteria

- [ ] invalid input과 model format failure가 안전하게 error response가 된다.
- [ ] 모든 answer가 citation 또는 “근거 없음” 상태를 가진다.
- [ ] 30-question baseline과 failure example이 versioned dataset에 있다.
- [ ] latency·token cost의 p50/p95와 request-level trace를 확인할 수 있다.

## Sources

- https://developers.openai.com/api/docs/guides/agents
- https://developers.openai.com/api/docs/guides/evals
- https://developers.llamaindex.ai/python/framework/
