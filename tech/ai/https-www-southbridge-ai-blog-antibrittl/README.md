---
date: 2026-06-24
tags:
  - tech
  - ai
  - agents
  - reliability
  - observability
  - antibrittle-agents
status: learning
type: tech-tool-study
---

# Antibrittle Agents

> **한 줄 정의**: Antibrittle Agents는 긴 task horizon에서 LLM agent의 stochastic failure를 제거하려 하기보다, 실패·분기·재시도·불확실성을 관찰 가능한 구조로 흡수해 더 오래 안정적으로 일하게 만드는 agent architecture/운영 패턴이다.

## 개요

Southbridge의 **Antibrittle Agents** 글은 agent를 단순한 `LLM call`이 아니라 **LLM in a loop with tools and a goal**, 즉 `agentic loop`로 봐야 한다고 주장한다. 긴 작업에서는 한 번의 답변 품질보다 수백~수천 번의 loop 동안 context, tool, decision, retry, handoff를 관리하는 능력이 더 중요하다.

핵심은 모델을 완벽하게 만드는 것이 아니라 **runtime**, **boundary**, **observability**, **accountability**를 설계하는 것이다.

```text
Goal
  -> Agentic loop
      -> Run box metrics
      -> Context boundary / trench
      -> Tool call / script / source receipt
      -> Human interruption point
      -> Recovery or handoff
```

---

## 학습 경로

| 순서 | 파일 | 무엇 |
|------|------|------|
| 1 | [[01-overview\|Overview]] | What/Why, brittleness 문제, 핵심 특징 |
| 2 | [[02-ecosystem\|Ecosystem]] | OpenAI Agents SDK, LangGraph, CrewAI, MCP, A2A, observability 비교 |
| 3 | [[03-references\|References]] | 원문, 공식 문서, reliability 논문 |
| 4 | [[04-learning/01-getting-started\|Getting Started]] | agent loop trace, run box metric, receipts 시작 실습 |
| 5 | [[04-learning/02-deep-dive\|Deep Dive]] | trenches, perturbation test, tool minimalism, human interruption 설계 |
| 6 | [[05-projects\|Projects]] | research, reconciliation, code maintenance, reliability harness 프로젝트 |
| 7 | [[cheatsheet\|Cheatsheet]] | 설계 원칙과 체크리스트 빠른 참조 |

---

## 파일 구조

```text
https-www-southbridge-ai-blog-antibrittl/
├── README.md
├── 01-overview.md
├── 02-ecosystem.md
├── 03-references.md
├── 04-learning/
│   ├── 01-getting-started.md
│   └── 02-deep-dive.md
├── 05-projects.md
└── cheatsheet.md
```

## 30초 핵심

- **Agent primitive**: `LLM call`보다 `agentic loop`가 기본 단위다.
- **긴 horizon 문제**: context rot, tool explosion, fake linear TODO, sibling communication cost, missing rationale가 누적된다.
- **Antibrittle 설계**: run boxes, regions of freedom, trenches, receipts, tool minimalism, human interruption points.
- **운영 목표**: five nines reliability보다 먼저 **five nines accountability**를 확보한다.
- **실전 구현**: OpenAI Agents SDK, LangGraph, CrewAI 같은 runtime 위에 tracing, eval harness, provenance store, MCP/A2A를 조합한다.

## 관련 노트

- [[study/tech/ai/model-context-protocol-mcp]] - tool/data integration layer
- [[study/tech/ai/agent-orchestration/cli-agents]] - CLI agent와 orchestration 관점
- [[study/tech/ai/lazy-codex]] - agent false completion과 verification harness
- [[study/tech/ai/langchain-crewai]] - CrewAI/LangChain 기반 agent workflow

---

**생성일**: 2026-06-24  
**상태**: 학습 중
