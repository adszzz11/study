# 4-1. Role + Action 패턴

## 🎭 Role 정의

```python
from metagpt.roles import Role
from metagpt.actions import Action

class TechResearcher(Role):
    name: str = "Riley"
    profile: str = "Tech Researcher"
    goal: str = "최신 기술 트렌드 조사"
    constraints: str = "출처 명시. 추측 금지."

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_actions([SearchWeb, SummarizeFindings])
        self._watch([UserRequirement])   # 구독: UserRequirement 메시지
```

## ⚡ Action 정의

```python
class SearchWeb(Action):
    PROMPT_TEMPLATE: str = """다음 주제 검색 후 5개 결과:
주제: {topic}
형식: bullet, [출처](url)"""

    async def run(self, topic: str):
        prompt = self.PROMPT_TEMPLATE.format(topic=topic)
        rsp = await self._aask(prompt)   # LLM 호출
        return rsp
```

## 🔄 Action 체이닝

```python
class WriteCode(Action):
    async def run(self, context):
        # 이전 step (Architect 설계)을 context로 받음
        design = context["design"]
        code = await self._aask(f"이 설계로 코드 작성:\n{design}")
        
        # 결과를 Engineer 다음 step (RunCode)에 전달
        return ActionOutput(code=code, next_action="RunCode")
```

## ✅ 체크포인트
- [ ] Role subclass 1개 작성
- [ ] Action 2개 정의 + 체이닝
- [ ] `_watch`로 다른 Role 메시지 구독
- [ ] 실행 시 메시지 흐름 로그 확인

## 🔗 다음 → [02-environment-messaging.md](02-environment-messaging.md)
