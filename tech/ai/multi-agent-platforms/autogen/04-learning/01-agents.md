# 4-1. Agent 기본 (v0.4 기준)

## 🤖 AssistantAgent
```python
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient

model = OpenAIChatCompletionClient(model="gpt-4o")
coder = AssistantAgent(
    name="coder",
    model_client=model,
    system_message="너는 파이썬 전문가. 깨끗한 코드 작성.",
    tools=[python_executor_tool],
)
```

## 👤 UserProxyAgent (v0.2/AG2)
```python
from autogen import UserProxyAgent, AssistantAgent

user = UserProxyAgent(
    "user",
    code_execution_config={"work_dir": "./work", "use_docker": True},
    human_input_mode="ALWAYS",   # NEVER, TERMINATE
)
assistant = AssistantAgent("assistant", llm_config={"config_list": [...]})

user.initiate_chat(assistant, message="피보나치 코드 + 실행")
```

`user`가 `assistant` 생성 코드를 자동 실행 → 결과 보고 다시 대화.

## 🔁 RoundRobinGroupChat (v0.4)
```python
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import MaxMessageTermination

team = RoundRobinGroupChat(
    [coder, reviewer, critic],
    termination_condition=MaxMessageTermination(max_messages=10),
)
result = await team.run(task="피보나치 함수 + 리뷰")
```

## ⚠️ Human Input Mode
- `ALWAYS`: 매 턴마다 사용자 입력 받음
- `TERMINATE`: 종료 신호 시에만
- `NEVER`: 완전 자동

## ✅ 체크포인트
- [ ] 2-agent chat 동작
- [ ] code execution이 Docker에서 격리되는지 확인
- [ ] termination 조건으로 무한 대화 방지

## 🔗 다음 → [02-groupchat.md](02-groupchat.md)
