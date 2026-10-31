---
date: 2026-10-27
tags: [tech]
type: tech-tool-study
status: draft
---

# Ecosystem and comparison

| 대상 | 강점 | 적합한 경우 | 유의점 |
|---|---|---|---|
| 이 책 | 21개 pattern을 설계 언어로 체계화하고 여러 framework 예시를 든다. | agent architecture를 넓게 설계·리뷰할 때 | framework API는 빠르게 변하므로 최신 docs를 함께 본다. |
| Anthropic guide | workflow/agent 선택 기준이 간결하다. | 입문과 MVP 설계 | 책보다 pattern 범위·구현 깊이가 작다. |
| Google Cloud guide | deployment, cost, security trade-off를 다룬다. | enterprise/cloud architecture | Google Cloud 중심의 운영 가이드다. |
| LangGraph | state, durable execution, HITL, observability 제어가 강하다. | long-running, stateful workflow | 저수준 orchestration이라 초기 학습량이 크다. |
| CrewAI | role/task/crew 중심으로 빠르게 team prototype을 만든다. | 역할 기반 multi-agent 실험 | 역할을 늘리기 전 evaluation과 종료 조건을 만든다. |
| Google ADK | multi-agent workflow, evaluation, deployment, MCP/A2A 통합을 제공한다. | Google ecosystem 또는 polyglot agent 개발 | 버전 변화에 맞춘 최신 문서 확인이 필요하다. |

## Protocols are complementary

- `MCP (Model Context Protocol)`: agent가 tool·data source에 연결하는 표준이다.
- `A2A (Agent2Agent)`: 독립 agent 사이의 협업·task delegation을 위한 표준이다.

둘은 대체재가 아니다. 한 agent가 MCP로 검색 또는 DB tool을 호출하면서, A2A로 별도 specialist agent와 협업할 수 있다.

## 선택 기준

1. 우선 single-agent에서 prompt, tool schema, failure handling, evaluation을 안정화한다.
2. durable state 또는 사람이 재개하는 장기 작업이면 LangGraph 같은 orchestration을 평가한다.
3. 역할별 context·권한·평가가 실제로 분리될 때만 multi-agent framework를 도입한다.

## Sources

- https://docs.cloud.google.com/architecture/choose-design-pattern-agentic-ai-system
- https://adk.dev/
- https://docs.langchain.com/oss/python/langgraph/overview
- https://docs.crewai.com/
- https://modelcontextprotocol.io/docs/getting-started/intro
- https://a2a-protocol.org/latest/
