# LangGraph Cheat Sheet

## 🚀 설치
```bash
pip install -U langgraph langchain-anthropic langgraph-checkpoint-postgres
```

## 🧩 그래프
```python
from langgraph.graph import StateGraph, START, END

g = StateGraph(State)
g.add_node("a", fn_a)
g.add_edge(START, "a")
g.add_edge("a", "b")
g.add_conditional_edges("b", router, {"x": "c", "y": END})
app = g.compile(checkpointer=checkpointer)
```

## 🗃️ State + Reducer
```python
from typing import Annotated, TypedDict
from operator import add

class S(TypedDict):
    messages: Annotated[list, add]   # 누적
    user: str                        # 덮어쓰기
```

## 🤖 Prebuilt
```python
from langgraph.prebuilt import create_react_agent, ToolNode
agent = create_react_agent(llm, tools=[...])
```

## 💾 Checkpointer
```python
from langgraph.checkpoint.memory import MemorySaver
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.checkpoint.postgres import PostgresSaver
```

## ⏸️ HITL
```python
from langgraph.types import interrupt, Command

# 노드 내
answer = interrupt({"question": "..."})

# 재개
app.invoke(Command(resume="yes"), config=config)
```

## ⏪ 시간여행
```python
state = app.get_state(config)
history = list(app.get_state_history(config))
app.update_state(config, {"field": "new value"})
```

## 🐝 Multi-Agent
```python
# Supervisor
from langgraph_supervisor import create_supervisor

# Swarm
from langgraph_swarm import create_swarm, create_handoff_tool
```

## 🚀 Deploy
```bash
pip install langgraph-cli
langgraph dev         # 로컬
langgraph deploy      # Platform
```

```json
// langgraph.json
{
  "dependencies": ["."],
  "graphs": {"my": "./app.py:graph"},
  "env": ".env"
}
```

## 🔗 빠른 링크
- 공식: https://langchain-ai.github.io/langgraph/
- GitHub: https://github.com/langchain-ai/langgraph
- 본 study: `study/tech/ai/multi-agent-platforms/langgraph/`
