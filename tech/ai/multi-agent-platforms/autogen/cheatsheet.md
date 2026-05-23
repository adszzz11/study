# AutoGen / AG2 Cheat Sheet

## 🚀 설치

### v0.4
```bash
pip install -U "autogen-agentchat" "autogen-ext[openai]"
pip install -U "autogenstudio"
```

### v0.2 / AG2
```bash
pip install pyautogen        # v0.2 본가
pip install ag2              # ag2ai/ag2
```

## 🧩 v0.4 패턴
```python
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.teams import SelectorGroupChat, RoundRobinGroupChat
from autogen_agentchat.conditions import TextMentionTermination, MaxMessageTermination
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_core.tools import FunctionTool
```

## 🗣️ v0.2/AG2 패턴
```python
from autogen import AssistantAgent, UserProxyAgent, GroupChat, GroupChatManager
```

## 🛠️ Tool 정의
```python
# v0.4
weather = FunctionTool(fn, description="...")
agent = AssistantAgent(name, model_client, tools=[weather])

# v0.2
@user.register_for_execution()
@assistant.register_for_llm(description="...")
def weather(city: str) -> str:
    return ...
```

## 🐳 코드 실행 (격리)
```python
from autogen.coding import DockerCommandLineCodeExecutor
executor = DockerCommandLineCodeExecutor(image="python:3.12-slim", timeout=60)
```

## 🎨 Studio
```bash
autogenstudio ui --port 8081
```

## 🔗 빠른 링크
- v0.4: https://microsoft.github.io/autogen/
- AG2: https://docs.ag2.ai/
- 본 study: `study/tech/ai/multi-agent-platforms/autogen/`
