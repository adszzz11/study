# OpenAI Swarm Cheat Sheet

> ⚠️ Educational. 새 프로젝트는 **openai-agents**.

## 🚀 설치
```bash
pip install git+https://github.com/openai/swarm.git
```

## 🧩 기본
```python
from swarm import Swarm, Agent

a = Agent(name="A", instructions="...", functions=[fn])
b = Agent(name="B", instructions="...")

def transfer_to_b():
    return b

a.functions.append(transfer_to_b)

client = Swarm()
result = client.run(agent=a, messages=[{"role":"user","content":"..."}],
                    max_turns=10, stream=False)
print(result.messages[-1]["content"])
```

## 🗃️ Context Variables
```python
client.run(agent=a, messages=[...], context_variables={"k": "v"})

def fn(context_variables, arg: str):
    return Result(value="...", context_variables={"k": "new"})
```

## 🌊 Stream
```python
stream = client.run(agent=a, messages=[...], stream=True)
for chunk in stream:
    print(chunk)
```

## ➡️ Agents SDK 마이그레이션
```python
from agents import Agent, Runner

agent = Agent(name="A", instructions="...", tools=[...], handoffs=[b])
result = await Runner.run(agent, "...")
```

## 🔗 빠른 링크
- Swarm: https://github.com/openai/swarm
- Agents SDK: https://github.com/openai/openai-agents-python
- 본 study: `study/tech/ai/multi-agent-platforms/openai-swarm/`
