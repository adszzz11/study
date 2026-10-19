---
date: 2026-10-19
tags: [tech]
type: tech-tool-study
status: draft
---

# AI Engineering from Scratch — Ecosystem

> [[README|목차로 돌아가기]]

## Ecosystem Map

| 범주 | 선택지 | 강점 | 적합한 경우 | 주의점 |
|---|---|---|---|---|
| Model/API | OpenAI Responses/Agents, Anthropic Claude, Gemini | managed tools, multimodal, reasoning | 빠른 product delivery | provider abstraction·cost control 필요 |
| Agent orchestration | LangGraph, OpenAI Agents SDK, Google ADK | stateful workflow, native ecosystem | tool use, durable execution, multi-step jobs | simple Q&A의 과도한 agent화 금지 |
| RAG/data framework | LlamaIndex, LangChain, custom pipeline | connector, indexing, retrieval abstraction | 문서·DB 기반 knowledge app | framework이 retrieval quality를 보장하지 않음 |
| Interoperability | MCP, A2A | tools·context·agent 연결 표준 | 여러 internal/external integration | server trust, OAuth, permission boundary |
| Observability/eval | LangSmith, MLflow, Phoenix, provider evals | trace, dataset, experiment, monitor | quality regression 방지 | PII retention·sampling policy 필요 |
| Serving | FastAPI/Node, Cloud Run, Kubernetes, managed runtime | API, queue, autoscaling, secrets | production traffic, async jobs | latency와 rate limit 설계 필요 |

## Selection Heuristics

- **MVP**: managed model API + FastAPI/Node + structured output + request logging으로 시작한다.
- **Knowledge app**: retrieval quality가 병목이므로 vector DB 선정 전 corpus, ACL, citation, recall eval을 만든다.
- **Long-running workflow**: persistence와 retry가 필요하면 graph/state-machine runtime을 검토한다.
- **Cross-tool integration**: MCP를 쓸 때 server별 trust level, OAuth scope, approval UX를 별도 설계한다.
- **High-risk domain**: framework보다 policy enforcement, audit event, human review를 먼저 확정한다.

## Avoid False Comparisons

LangGraph, LlamaIndex, MCP, MLflow는 서로 대체재가 아니다. 각각 workflow, data/retrieval, interoperability, observability를 다룬다. 선택의 기준은 “가장 많은 기능”이 아니라 현재 workflow의 빈 layer와 운영 책임이다.

## Sources

- https://developers.openai.com/api/docs/guides/agents
- https://docs.langchain.com/oss/python/langgraph/overview
- https://developers.llamaindex.ai/python/framework/
- https://google.github.io/adk-docs/
- https://mlflow.org/docs/latest/genai/
