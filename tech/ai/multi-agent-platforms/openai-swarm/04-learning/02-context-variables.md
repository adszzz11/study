# 4-2. Context Variables (공유 상태)

## 🗃️ 사용법

```python
def get_user_name(context_variables):
    return context_variables.get("user_name", "Unknown")

def set_user_name(context_variables, name: str):
    return Result(
        value=f"Set name to {name}",
        context_variables={"user_name": name}
    )

agent = Agent(
    name="Assistant",
    instructions=lambda ctx: f"사용자 이름: {ctx.get('user_name', '아직 모름')}",
    functions=[get_user_name, set_user_name],
)

client.run(
    agent=agent,
    messages=[...],
    context_variables={"user_name": "Simon"},
)
```

- function이 `context_variables` 인자 받으면 자동 주입
- function이 `Result(context_variables=...)` 반환하면 업데이트
- instructions를 lambda로 만들면 동적 시스템 프롬프트

## 🎯 활용 예

### 1. 사용자 정보 영속
```python
context = {"user_id": "u-1", "preferences": {}, "auth_token": "..."}
```

### 2. 카운터·세션 데이터
```python
context = {"turn": 0, "previous_intents": []}
```

### 3. 다른 LLM 클라이언트 주입
```python
context = {"db_conn": conn, "llm_client": llm}
```

## ⚠️ 한계
- 휘발성 — 클라이언트 죽으면 사라짐
- 영속화는 직접 (Redis/Postgres)
- 동시 접근 보호 없음

## 🔗 다음 → [03-streaming.md](03-streaming.md)
