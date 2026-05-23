# AutoGen / AG2 심층 스터디

> Microsoft 출신, 멀티 에이전트 **대화형 협업**의 원조. 지금은 maintenance 모드 + ag2ai 포크.

## 한 줄 정의

**AutoGen**은 여러 에이전트가 **자연어 대화**로 협업하도록 설계된 Python 프레임워크. GroupChat·debate·합의 도출이 강점. v0.4(AG2)에서 event-driven·async-first로 재설계됐다.

## 3줄 요약

1. **대화가 1급 시민**: 에이전트 간 다중턴 채팅으로 작업 진행.
2. **두 갈래**: 본가 microsoft/autogen은 maintenance, ag2ai/ag2가 활발.
3. **AutoGen Studio**(노코드 GUI)로 프로토타입 빠름.

## 핵심 키워드

`#autogen` `#ag2` `#group-chat` `#conversation` `#microsoft` `#multi-agent` `#assistant-agent` `#user-proxy` `#mit`

## ⚡ Quick Start (v0.4)

```bash
pip install -U "autogen-agentchat" "autogen-ext[openai]"
```

```python
import asyncio
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient

async def main():
    model = OpenAIChatCompletionClient(model="gpt-4o")
    agent = AssistantAgent("assistant", model_client=model)
    result = await agent.run(task="피보나치 10번째 수 계산")
    print(result.messages[-1].content)

asyncio.run(main())
```

## 📑 목차
| 파일 | 내용 |
|------|------|
| [01-overview.md](01-overview.md) | v0.2 vs v0.4·AG2 분기 |
| [02-ecosystem.md](02-ecosystem.md) | LangGraph/CrewAI와 차이 |
| [03-references.md](03-references.md) | 공식·논문 |
| [04-learning/01-agents.md](04-learning/01-agents.md) | AssistantAgent·UserProxy |
| [04-learning/02-groupchat.md](04-learning/02-groupchat.md) | GroupChat·Selector |
| [04-learning/03-tools-and-functions.md](04-learning/03-tools-and-functions.md) | 도구·function calling |
| [04-learning/04-studio.md](04-learning/04-studio.md) | AutoGen Studio GUI |
| [05-projects.md](05-projects.md) | 실전 프로젝트 |
| [cheatsheet.md](cheatsheet.md) | 빠른 참조 |
