---
date: 2026-06-24
tags:
  - tech
  - ai
  - agents
  - references
  - reliability
type: tech-tool-study
parent: "[[README]]"
---

# Antibrittle Agents - 참고자료

> [[02-ecosystem|이전: 생태계]] | [[README|목차로 돌아가기]] | [[04-learning/01-getting-started|다음: 시작하기]]

---

## 1. Primary Source

| 자료 | URL | 읽을 포인트 |
|------|-----|-------------|
| Southbridge.AI, **Antibrittle Agents** | https://www.southbridge.ai/blog/antibrittle-agents | agentic loop, run boxes, regions of freedom, trenches, receipts, tool minimalism |

---

## 2. Runtime / Framework Docs

| 자료 | URL | Antibrittle 연결 |
|------|-----|------------------|
| OpenAI, **Agents SDK docs** | https://openai.github.io/openai-agents-python/ | agent loop, tools, handoffs, guardrails, sessions, tracing |
| LangChain, **LangGraph overview** | https://docs.langchain.com/oss/python/langgraph/overview | stateful graph, persistence, human-in-the-loop, fault tolerance |
| CrewAI, **Introduction / Flows / Crews** | https://docs.crewai.com/en/introduction | deterministic Flow와 autonomous Crew 분리 |

---

## 3. Protocols

| 자료 | URL | Antibrittle 연결 |
|------|-----|------------------|
| Model Context Protocol, **MCP intro** | https://modelcontextprotocol.io/docs/getting-started/intro | tool/data/resource access layer |
| A2A Protocol, **official docs** | https://a2a-protocol.org/latest/ | agent-to-agent delegation/discovery |

---

## 4. Reliability / Observability Papers

| 자료 | URL | 읽을 포인트 |
|------|-----|-------------|
| Rabanser et al., **Towards a Science of AI Agent Reliability**, 2026 | https://arxiv.org/abs/2602.16666 | success rate 외 reliability dimension |
| Sinha et al., **The Illusion of Diminishing Returns: Measuring Long Horizon Execution in LLMs**, 2025 | https://arxiv.org/abs/2509.09677 | long-horizon execution measurement |
| Hasan et al., **Model Context Protocol at First Glance**, 2025 | https://arxiv.org/abs/2506.13538 | MCP의 역할과 초기 분석 |
| AgentSight, **System-Level Observability for AI Agents Using eBPF**, 2025 | https://arxiv.org/abs/2508.02736 | agent runtime behavior visibility |

---

## 5. 읽기 순서

1. Southbridge 원문을 읽고 `LLM call -> agentic loop` 전환을 표시한다.
2. [[01-overview]]에서 run boxes, trenches, receipts 용어를 정리한다.
3. OpenAI Agents SDK 또는 LangGraph 문서에서 tracing/checkpoint/handoff primitive를 확인한다.
4. MCP와 A2A를 읽고 tool/data protocol과 agent communication protocol을 구분한다.
5. reliability 논문에서 consistency, robustness, predictability, safety 같은 측정 축을 뽑는다.
6. [[04-learning/01-getting-started]]에서 작은 agent loop trace를 직접 만든다.

---

## 6. 개인 메모 템플릿

```markdown
## Source
- URL:
- Date read:

## Claims
- Claim:
- Evidence:
- Receipt:

## Antibrittle Mapping
- Run box:
- Trench:
- Receipt:
- Human interruption point:

## Open Questions
- 
```

---

## 관련 노트

- [[study/tech/ai/model-context-protocol-mcp/03-references]] - MCP reference set
- [[study/tech/ai/lazy-codex/03-references]] - agent verification/reliability 관련 자료
- [[study/tech/ai/agent-orchestration/README]] - agent orchestration 인접 주제
