# Part 2. Swarm 생태계 (Agents SDK 후계)

## 🔄 Swarm → Agents SDK 전환

| Swarm | Agents SDK |
|-------|-----------|
| `Agent(name, instructions, functions)` | `Agent(name, instructions, tools, handoffs)` |
| `client.run(agent, messages)` | `Runner.run(starting_agent, input)` |
| function return → 에이전트 | `handoffs=[other_agent]` 명시 |
| 동기 | async 우선 |
| 추가 기능 X | guardrails, tracing, voice |

## 🆚 vs 다른 프레임워크

| 항목 | Swarm | LangGraph Swarm | Agency Swarm |
|------|-------|-----------------|--------------|
| 컨셉 | handoff (function return) | handoff (Command) | 통신 흐름 (`>`) |
| 상태 | context_variables | TypedDict + checkpointer | thread persistent |
| 프로덕션 | ✗ | ✅ | ✅ |
| 출처 | OpenAI | LangChain | VRSEN |

## 🌐 Agents SDK의 추가 기능

```python
from agents import Agent, Runner, guardrail

@guardrail
def safety_check(input):
    if "delete database" in input:
        return False
    return True

assistant = Agent(
    name="...",
    instructions="...",
    tools=[...],
    handoffs=[other_agent],
    input_guardrails=[safety_check],
    output_guardrails=[...],
)
```

## 🎯 결정 가이드

| 의도 | 선택 |
|------|------|
| 학습 (handoff 개념 이해) | **Swarm** |
| 프로덕션 + OpenAI 생태계 | **OpenAI Agents SDK** |
| 비OpenAI 모델 위주 | Agency Swarm 또는 LangGraph |

## 🔥 동향
- Swarm은 freeze 상태 (PR 안 받음)
- Agents SDK가 정식 출시 (OpenAI Cookbook 다수 마이그레이션)
- LangGraph가 `langgraph_swarm` 패키지로 같은 컨셉 흡수

## 🔗 다음 → [03-references.md](03-references.md)
