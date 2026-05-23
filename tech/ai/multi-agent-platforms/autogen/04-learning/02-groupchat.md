# 4-2. GroupChat / Team

## 🗣️ v0.2/AG2 GroupChat

```python
from autogen import GroupChat, GroupChatManager

groupchat = GroupChat(
    agents=[user, coder, reviewer, critic],
    messages=[],
    max_round=10,
    speaker_selection_method="auto",   # 또는 round_robin, manual, custom function
)
manager = GroupChatManager(groupchat=groupchat, llm_config=llm_config)

user.initiate_chat(manager, message="...")
```

## 🎯 SelectorGroupChat (v0.4)

```python
from autogen_agentchat.teams import SelectorGroupChat
from autogen_agentchat.conditions import TextMentionTermination

team = SelectorGroupChat(
    [coder, reviewer, critic],
    model_client=model,
    selector_prompt="""다음에 누가 말해야 할까?
역할들: {roles}
대화: {history}
다음 발화자만 출력.""",
    termination_condition=TextMentionTermination("APPROVED"),
)
```

selector_prompt가 LLM에게 다음 발화자 선택을 위임. critic이 "APPROVED" 말하면 종료.

## 💸 비용 주의

GroupChat 비용 = `agents × rounds × tokens_per_turn × model_price`

4-agent × 5 round = 최소 20 LLM call. 신중히:
- `max_round` 제한
- 라운드별 메시지 truncate
- selector를 작은 모델로 (gpt-4o-mini)
- 핵심 토론만 GroupChat, 단순 작업은 Sequential

## 🆚 SelectorGroupChat vs RoundRobinGroupChat

| 패턴 | 사용 |
|------|------|
| **RoundRobin** | 매 라운드마다 정해진 순서. 비용 예측 가능 |
| **Selector** | LLM이 누가 말할지 결정. 동적 |

## ✅ 체크포인트
- [ ] 3-agent GroupChat 동작
- [ ] termination 조건 동작
- [ ] selector_prompt로 발화자 선택 통제
- [ ] 비용 모니터링 (logging level INFO)

## 🔗 다음 → [03-tools-and-functions.md](03-tools-and-functions.md)
