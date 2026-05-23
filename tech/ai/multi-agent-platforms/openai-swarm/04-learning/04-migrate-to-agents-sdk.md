# 4-4. OpenAI Agents SDK로 마이그레이션

## 🚀 설치
```bash
pip install openai-agents
```

## 🔁 코드 변환

### Swarm
```python
from swarm import Swarm, Agent

def transfer_to_support():
    return support

triage = Agent(name="Triage", functions=[transfer_to_support])
client = Swarm()
result = client.run(agent=triage, messages=[{"role":"user","content":"..."}])
```

### Agents SDK
```python
from agents import Agent, Runner

triage = Agent(
    name="Triage",
    instructions="질문 분류",
    handoffs=[support],   # ← Swarm의 return → handoffs 리스트로
)
result = await Runner.run(triage, "...")
```

## ✨ 새 기능

### Guardrails
```python
from agents import input_guardrail, GuardrailFunctionOutput

@input_guardrail
async def safety(ctx, agent, input):
    bad = "drop database" in input
    return GuardrailFunctionOutput(
        output_info={"reason": "destructive"} if bad else None,
        tripwire_triggered=bad,
    )

agent = Agent(..., input_guardrails=[safety])
```

### Tracing
```python
import logfire
logfire.configure()
logfire.instrument_openai_agents()
# 자동으로 모든 핸드오프·LLM call trace
```

### 비OpenAI 모델 (LiteLLM)
```python
from agents.models.litellm_model import LitellmModel

agent = Agent(
    name="...",
    model=LitellmModel(model="anthropic/claude-opus-4-7"),
)
```

### Voice
```python
from agents.voice import VoicePipeline
# 음성 입력/출력 1급 지원
```

## ✅ 마이그레이션 체크리스트
- [ ] `Swarm` → `Runner.run` (async)
- [ ] function return → `handoffs=[]`
- [ ] `context_variables` → `RunContextWrapper`
- [ ] streaming → `Runner.run_streamed`
- [ ] guardrails 추가
- [ ] tracing 켜기

## 🔗 본 vault 내
- 다음 → [../05-projects.md](../05-projects.md)
