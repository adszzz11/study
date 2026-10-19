---
date: 2026-10-19
tags: [tech]
type: tech-tool-study
status: draft
---

# AI Engineering from Scratch — References

> [[README|목차로 돌아가기]]

## Primary Documentation

1. [OpenAI — Agents documentation](https://developers.openai.com/api/docs/guides/agents) — agent loop, tools, orchestration
2. [OpenAI — Evals guide](https://developers.openai.com/api/docs/guides/evals) — eval dataset과 grader 설계
3. [Model Context Protocol — Specification](https://modelcontextprotocol.io/specification/2025-06-18) — host/client/server와 JSON-RPC protocol
4. [LangGraph — Overview](https://docs.langchain.com/oss/python/langgraph/overview) — durable, stateful workflow
5. [LlamaIndex — Framework documentation](https://developers.llamaindex.ai/python/framework/) — ingestion, retrieval, evaluation component

## Operations and Security

6. [MLflow — Agents and LLMs](https://mlflow.org/docs/latest/genai/) — tracing, evaluation, monitoring
7. [Google ADK — Documentation](https://google.github.io/adk-docs/) — model, tools, memory, evaluation, deployment lifecycle
8. [Google Agents CLI — Development lifecycle](https://google.github.io/agents-cli/guide/development/) — agent development workflow
9. [OpenTelemetry — GenAI semantic conventions](https://opentelemetry.io/docs/specs/semconv/gen-ai/) — vendor-neutral trace attributes
10. [OWASP — Top 10 for LLM Applications](https://genai.owasp.org/llmrisk/) — prompt injection과 data leakage threat model

## Reading Order

MCP specification으로 integration boundary를 이해하고, LangGraph 또는 ADK 문서로 stateful workflow를 본다. 이어서 OpenAI Evals와 MLflow/OpenTelemetry 문서로 측정·trace 기준을 세운 뒤, OWASP를 기준으로 abuse case를 test fixture에 포함한다.
