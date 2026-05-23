# LangGraph 심층 스터디

> 상태를 가진 멀티 에이전트를 위한 **그래프 기반** 저수준 오케스트레이션 — 프로덕션 표준

## 한 줄 정의

**LangGraph**는 노드·엣지·상태로 구성된 **그래프**로 에이전트를 만드는 Python 프레임워크. **체크포인트·재개·HITL·시간여행**을 1급 지원해서 2026년 프로덕션 멀티 에이전트의 사실상 표준이 됐다.

## 3줄 요약

1. **그래프 = 노드(함수) + 엣지(전이) + 상태(공유 메모리)**.
2. **Durable execution**: 실패해도 마지막 체크포인트에서 정확히 재개.
3. **LangSmith 통합**으로 모든 실행 시각화·디버깅.

## 핵심 키워드

`#langgraph` `#stateful-agents` `#graph` `#checkpointing` `#hitl` `#pregel` `#langchain` `#production` `#mit`

## ⚡ Quick Start

```bash
pip install -U langgraph langchain-anthropic
```

```python
from langgraph.graph import StateGraph, START, END
from typing import TypedDict

class State(TypedDict):
    messages: list

def chatbot(state):
    return {"messages": state["messages"] + ["Hi!"]}

g = StateGraph(State)
g.add_node("chat", chatbot)
g.add_edge(START, "chat")
g.add_edge("chat", END)

app = g.compile()
print(app.invoke({"messages": ["Hello"]}))
```

## 📑 목차

| 파일 | 내용 |
|------|------|
| [01-overview.md](01-overview.md) | 그래프 모델·체크포인트·HITL |
| [02-ecosystem.md](02-ecosystem.md) | CrewAI/AutoGen 등과 차이 |
| [03-references.md](03-references.md) | 공식·강의 |
| [04-learning/01-graphs-and-state.md](04-learning/01-graphs-and-state.md) | 그래프 정의 패턴 |
| [04-learning/02-multi-agent.md](04-learning/02-multi-agent.md) | Supervisor/Swarm/Hierarchical |
| [04-learning/03-checkpoints-hitl.md](04-learning/03-checkpoints-hitl.md) | 체크포인트·HITL·시간여행 |
| [04-learning/04-platform-deploy.md](04-learning/04-platform-deploy.md) | LangGraph Platform 배포 |
| [05-projects.md](05-projects.md) | 실전 프로젝트 |
| [cheatsheet.md](cheatsheet.md) | 빠른 참조 |

## 🗓️ 학습 플랜
| Day | 목표 |
|-----|------|
| 1 | Quick Start + 그래프 모델 |
| 2 | 멀티 에이전트 패턴 (Supervisor) |
| 3 | 체크포인트 + HITL |
| 4 | LangSmith 트레이싱 |
| 5+ | 실전 |
