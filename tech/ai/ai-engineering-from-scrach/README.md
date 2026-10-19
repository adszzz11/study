---
date: 2026-10-19
tags: [tech]
type: tech-tool-study
status: draft
---

# AI Engineering from Scratch

> **한 줄 정의**: AI engineering from scratch는 foundation model을 새로 학습시키는 일이 아니라, LLM·데이터·tools·workflow·evaluation·observability·security를 조합해 신뢰성 있는 AI product를 설계·운영하는 engineering discipline이다.

## Overview

AI product의 핵심 난제는 모델 호출 자체보다 확률적인 model output과 외부 data·tool·권한을 안전하게 연결하고, 결과를 측정해 반복 개선하는 데 있다. RAG, tool calling, MCP integration, long-running agent는 모두 backend 운영 문제를 동반한다.

```text
User/API → API & Auth → Orchestrator / Agent state machine
                         ↕
                  Model ↔ Tools / MCP / RAG / DB
                         ↓
              Guardrails & approval gates
                         ↓
             Response + trace + evaluation data
                         ↓
              Offline/online evaluation → 개선·배포
```

## Learning Path

- [ ] [[01-overview|개요]] — What/Why와 설계 원칙 이해
- [ ] [[02-ecosystem|생태계]] — model, orchestration, RAG, observability 선택지 비교
- [ ] [[03-references|참고자료]] — 공식 specification과 운영 문서 확인
- [ ] [[04-learning/01-getting-started|시작하기]] — 단일 LLM API endpoint와 최소 RAG 구현
- [ ] [[04-learning/02-deep-dive|심화]] — workflow, evals, observability, security hardening
- [ ] [[05-projects|프로젝트]] — 단계별 portfolio project 설계
- [ ] [[cheatsheet|치트시트]] — 배포 전 빠른 점검표

## When To Use

- LLM을 product API, 내부 업무 자동화, knowledge app에 연결할 때
- RAG, tool calling, MCP 또는 human approval이 필요한 multi-step workflow를 설계할 때
- 품질 regression, token cost, latency, security risk를 운영 지표로 관리해야 할 때

## When Not To Use

- 단순한 deterministic rule 또는 기존 search/filter만으로 요구사항을 충족할 때
- evaluation set, user authorization, 운영 owner 없이 autonomous agent를 배포하려 할 때
- irreversible action을 model output만으로 즉시 실행하려 할 때

## Related Notes

- [[MOCs/Index]]
- [[MOCs/AI]]
- [[tech/ai/model-context-protocol-mcp/README|Model Context Protocol (MCP)]] — tool·context integration의 permission boundary

## Sources

- https://developers.openai.com/api/docs/guides/agents
- https://developers.openai.com/api/docs/guides/evals
- https://modelcontextprotocol.io/specification/2025-06-18
- https://docs.langchain.com/oss/python/langgraph/overview
- https://opentelemetry.io/docs/specs/semconv/gen-ai/
