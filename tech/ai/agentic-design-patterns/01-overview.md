---
date: 2026-10-27
tags: [tech]
type: tech-tool-study
status: draft
---

# Overview

## What

Antonio Gullí의 《Agentic Design Patterns: A Hands-On Guide to Building Intelligent Systems》는 LLM application을 agent system으로 확장할 때 쓰는 21개 재사용 pattern을 다룬다. Chaining, Routing, Parallelization, Reflection, Tool Use, Planning, Multi-Agent부터 Memory, MCP, Goal Monitoring, Exception Recovery, HITL, RAG, Guardrails, Evaluation까지 연결한다.

## Why

단일 prompt는 단순 Q&A에는 적합하지만, 외부 API 실행·다단계 계획·상태 유지·실패 복구·안전 검토가 필요한 작업에는 제어 지점이 부족하다. pattern으로 분해하면 각 단계의 입력, 실패, 비용, 종료 조건, 승인 여부를 명시할 수 있다.

Anthropic의 구분처럼 고정된 code path를 따르는 것은 `workflow`, 모델이 tool과 다음 단계를 동적으로 선택하는 것은 `agent`다. 먼저 단순하고 결정적인 workflow를 만들고, 실제로 필요한 곳만 agentic decision으로 바꾼다.

## 특징

| 특징 | 의미 |
|---|---|
| 21 patterns | 설계·리뷰 때 공통 vocabulary를 제공한다. |
| Runnable code | 개념만이 아니라 실습 출발점을 제공한다. |
| Framework-agnostic | LangChain/LangGraph, CrewAI, Google ADK를 canvas로 쓰되 특정 vendor 종속을 목표로 하지 않는다. |
| Reliability 중심 | tool schema, recovery, approval, trace, evaluation을 기능과 동등하게 다룬다. |

## 권장 흐름

```text
User → Router/Planner → Tool · RAG · Worker → Critic/Evaluator
                                      ↓
                       Guardrail + Human Approval → Observability
```

고위험 write action은 approval gate 뒤에 두고, tool은 least privilege로 제한하며, 실행마다 trace와 evaluation 근거를 남긴다.

## Sources

- https://link.springer.com/book/10.1007/978-3-032-01402-3
- https://www.anthropic.com/research/building-effective-agents
