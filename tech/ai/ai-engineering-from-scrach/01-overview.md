---
date: 2026-10-19
tags: [tech]
type: tech-tool-study
status: draft
---

# AI Engineering from Scratch — Overview

> [[README|목차로 돌아가기]]

## What

AI engineering from scratch는 pretraining을 뜻하지 않는다. 이미 제공되는 foundation model을 model layer로 삼고, data, tools, stateful workflow, evaluation, observability, security를 결합하여 실제 사용자가 신뢰할 수 있는 product를 만드는 discipline이다.

## Why

chat completion 하나는 짧은 demo가 될 수 있지만, production에서는 다음이 즉시 문제가 된다.

- model output은 확률적이므로 동일 입력에서도 품질과 형식이 흔들린다.
- retrieval이 틀리거나 오래되면 답변은 fluent해도 근거가 없다.
- tool과 MCP server는 외부 data access 및 side effect를 열어 prompt injection·권한 오용 위험을 만든다.
- trace와 eval이 없으면 regression, latency, token cost를 재현하거나 원인을 찾기 어렵다.

## Core Characteristics

| Layer | 책임 | 설계 기준 |
|---|---|---|
| Product | 사용자·성공 기준·실패 허용 범위 | human escalation 조건을 먼저 정의 |
| Model | quality, latency, cost, structured output | provider abstraction과 fallback |
| Context/RAG | ingestion부터 citation까지 | freshness, ACL, retrieval eval |
| Tools | typed action 실행 | idempotency, timeout, audit log |
| Workflow | 상태·재시도·approval 제어 | deterministic code와 LLM 판단 분리 |
| Operations | eval, trace, governance | deployment 전후에 같은 지표 측정 |

## Architecture Principles

1. **Product-first**: multi-agent를 시작점으로 삼지 말고, 한 개의 measurable workflow를 먼저 검증한다.
2. **Small typed tools**: tool schema는 작고 명확하게 하고 validation, timeout, retry, rate limit을 둔다.
3. **RAG as data system**: chunking·metadata·hybrid retrieval·reranking·citation을 각각 측정한다.
4. **Explicit control flow**: publish, payment, deletion 같은 side effect에는 confirmation 또는 approval gate를 둔다.
5. **Evaluation-first**: golden dataset과 regression suite를 source code처럼 versioning한다.

## Security Baseline

untrusted document, web page, tool output은 instruction이 아니라 **data**로 취급한다. system instruction과 구획하고, per-tool scoped credential, allowlist, sandbox, output validation, PII redaction을 적용한다. destructive action은 human approval 없이 실행하지 않는다.

## Sources

- https://modelcontextprotocol.io/specification/2025-06-18
- https://docs.langchain.com/oss/python/langgraph/overview
- https://genai.owasp.org/llmrisk/
