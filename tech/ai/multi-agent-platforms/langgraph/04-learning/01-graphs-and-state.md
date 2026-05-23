# 4-1. 그래프와 상태

## 📌 핵심 3요소

```python
from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
from operator import add

# 1. State 정의
class State(TypedDict):
    messages: Annotated[list, add]   # reducer: 리스트에 누적
    counter: int                     # reducer 없음: 덮어쓰기

# 2. Nodes 정의 (함수)
def step1(state: State) -> dict:
    return {"messages": ["from step1"], "counter": 1}

def step2(state: State) -> dict:
    return {"messages": ["from step2"], "counter": state["counter"] + 1}

# 3. Graph 조립
g = StateGraph(State)
g.add_node("a", step1)
g.add_node("b", step2)
g.add_edge(START, "a")
g.add_edge("a", "b")
g.add_edge("b", END)

app = g.compile()
print(app.invoke({"messages": [], "counter": 0}))
# {"messages": ["from step1", "from step2"], "counter": 2}
```

## 🔀 Conditional Edges (분기)

```python
def router(state: State) -> str:
    if state["counter"] > 5:
        return "done"
    return "loop"

g.add_conditional_edges(
    "step",
    router,
    {"done": END, "loop": "step"}    # 같은 노드로 루프!
)
```

## 🔁 Reducer (상태 병합)

State의 각 필드에 `Annotated[type, reducer]`:

```python
class State(TypedDict):
    messages: Annotated[list, add]              # 리스트 누적
    score: Annotated[int, lambda a, b: a + b]   # 합산
    user: str                                   # reducer 없음: 덮어쓰기
```

병렬 노드가 같은 필드를 업데이트하면 reducer로 병합 — race condition 자동 해결.

## ⚙️ ToolNode + Agent 패턴

```python
from langgraph.prebuilt import create_react_agent
from langchain_anthropic import ChatAnthropic

agent = create_react_agent(
    ChatAnthropic(model="claude-opus-4-7"),
    tools=[search_tool, calculator],
)
# 이미 컴파일된 그래프. 바로 invoke 가능.
result = agent.invoke({"messages": [("user", "2024년 노벨상은?")]})
```

`create_react_agent`는 LangGraph가 빌트인 제공하는 ReAct 그래프.

## ✅ 체크포인트
- [ ] 위 Quick Start 코드 동작
- [ ] State 필드에 add reducer 적용 시 누적됨
- [ ] conditional_edges로 분기 동작
- [ ] create_react_agent로 tool 호출되는 에이전트 만듦

## ⚠️ 함정
| 증상 | 원인 |
|------|------|
| State에 변경 사항 안 반영 | 함수가 dict 반환해야 (전체가 아닌 변경분만) |
| 루프가 무한 실행 | recursion_limit (기본 25) 도달 시 에러 — config로 조정 |
| 병렬 노드 충돌 | reducer 미정의. Annotated로 명시 |
| LangChain message 형식 | `from langchain_core.messages import HumanMessage, AIMessage` |

## 🔗 다음 → [02-multi-agent.md](02-multi-agent.md)
