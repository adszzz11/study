# 4-2. Multi-Agent 패턴

## 👮 Supervisor 패턴 (가장 흔함)

```
       Supervisor
       /   |    \
   agent1 agent2 agent3
```

중앙 supervisor가 LLM으로 누가 일할지 결정.

```python
from langgraph.graph import StateGraph, MessagesState
from langgraph.prebuilt import create_react_agent
from langchain_anthropic import ChatAnthropic

llm = ChatAnthropic(model="claude-opus-4-7")

researcher = create_react_agent(llm, tools=[search_tool], name="researcher")
writer    = create_react_agent(llm, tools=[file_write_tool], name="writer")

def supervisor(state):
    # supervisor도 LLM이 결정
    resp = llm.with_structured_output(Route).invoke([
        {"role": "system", "content": "다음에 누가 일해야 하나?"},
        *state["messages"],
    ])
    return {"next": resp.next}

def route(state):
    return state["next"]   # "researcher" | "writer" | "FINISH"

g = StateGraph(MessagesState)
g.add_node("supervisor", supervisor)
g.add_node("researcher", researcher)
g.add_node("writer", writer)

g.add_edge(START, "supervisor")
g.add_conditional_edges("supervisor", route, {
    "researcher": "researcher",
    "writer": "writer",
    "FINISH": END,
})
g.add_edge("researcher", "supervisor")
g.add_edge("writer", "supervisor")
```

`langgraph-supervisor` prebuilt 패키지도 있음.

## 🐝 Swarm 패턴 (Handoffs)

```
agent1 ⇄ agent2 ⇄ agent3
```

에이전트끼리 직접 핸드오프. 중앙 라우터 없음.

```python
from langgraph_swarm import create_swarm, create_handoff_tool

researcher = create_react_agent(
    llm, name="researcher",
    tools=[search_tool, create_handoff_tool(agent_name="writer")],
)
writer = create_react_agent(
    llm, name="writer",
    tools=[file_write_tool, create_handoff_tool(agent_name="researcher")],
)

swarm = create_swarm([researcher, writer], default_active_agent="researcher")
```

각 에이전트가 다른 에이전트를 호출하는 도구를 가짐.

## 🏢 Hierarchical 패턴

```
    Top Supervisor
   /             \
Research Team   Writing Team
  /   \           /   \
 r1   r2         w1   w2
```

Supervisor의 Supervisor. 큰 시스템에 적합.

```python
research_team = build_supervisor_graph([r1, r2])    # 서브그래프
writing_team = build_supervisor_graph([w1, w2])

top = StateGraph(MessagesState)
top.add_node("research", research_team)   # 서브그래프를 노드로
top.add_node("writing", writing_team)
top.add_node("top_super", top_supervisor_fn)
# ... edges
```

## 🆚 패턴 선택

| 상황 | 패턴 |
|------|------|
| 단순 — 3-5명 | Supervisor |
| 에이전트들이 동등한 위치 | Swarm |
| 큰 조직 (10+) | Hierarchical |
| 명확한 단계 (조사→작성→발행) | 선형 그래프 (multi-agent 안 써도 됨) |

## ✅ 체크포인트
- [ ] Supervisor 3-agent 동작
- [ ] Swarm handoff 동작
- [ ] LangSmith trace에서 호출 순서 확인

## 🔗 다음 → [03-checkpoints-hitl.md](03-checkpoints-hitl.md)
