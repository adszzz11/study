# 4-3. 체크포인트·HITL·시간여행

## 💾 Checkpointer

```python
from langgraph.checkpoint.postgres import PostgresSaver
# 또는 SqliteSaver, MemorySaver, RedisSaver

checkpointer = PostgresSaver.from_conn_string("postgresql://...")
checkpointer.setup()   # 한 번만

app = g.compile(checkpointer=checkpointer)

config = {"configurable": {"thread_id": "user-123-session-1"}}
app.invoke({"messages": [...]}, config=config)
```

**핵심**: `thread_id`로 대화·세션 구분. 같은 thread_id면 이전 상태 자동 로드.

## ⏪ State 조회/수정

```python
# 현재 상태
state = app.get_state(config)
print(state.values, state.next)   # 다음에 실행될 노드

# 과거 state 목록 (시간여행)
for hist in app.get_state_history(config):
    print(hist.config["configurable"]["checkpoint_id"], hist.values)

# 특정 체크포인트로 되돌리기
old_config = {"configurable": {"thread_id": "...", "checkpoint_id": "..."}}
app.invoke(None, config=old_config)   # 그 시점에서 재실행
```

## ⏸️ Interrupt (HITL)

### 방식 1: 명시적 interrupt
```python
from langgraph.types import interrupt, Command

def approval_node(state):
    answer = interrupt({"question": "이거 발행할까요?", "draft": state["draft"]})
    return {"approved": answer == "yes"}

g.add_node("approval", approval_node)
```

실행 시:
```python
# 첫 invoke - interrupt에서 멈춤
result = app.invoke({"draft": "..."}, config=config)
print(result["__interrupt__"])   # {"question": "...", "draft": "..."}

# 사용자 입력 받은 후
result = app.invoke(Command(resume="yes"), config=config)
```

### 방식 2: interrupt_before / interrupt_after
```python
app = g.compile(
    checkpointer=checkpointer,
    interrupt_before=["risky_node"],   # 이 노드 전에 항상 멈춤
)
```

## 🌳 State 편집 후 재실행

```python
# 위험한 노드 직전에 stop
app.invoke({"msg": "..."}, config)
state = app.get_state(config)

# 사용자가 state 일부 수정
app.update_state(config, {"draft": "edited by human"})

# 이어서 진행
app.invoke(None, config)
```

## 🌐 실전 패턴: 외부 알림 + 비동기 승인

```python
async def approval(state):
    # 텔레그램으로 발송
    await telegram.send_message(state["chat_id"], 
        f"승인 필요: {state['action']}")
    
    # interrupt — 텔레그램 callback이 resume 호출
    decision = interrupt({"action": state["action"]})
    return {"approved": decision == "approved"}
```

텔레그램 webhook이 들어오면:
```python
@app.post("/telegram/webhook")
async def webhook(req):
    if req.callback_data == "approve":
        await langgraph.invoke(
            Command(resume="approved"),
            config={"configurable": {"thread_id": req.thread_id}}
        )
```

## ✅ 체크포인트
- [ ] PostgresSaver로 영속 체크포인트 동작
- [ ] thread_id 바꿔도 이전 컨텍스트 분리
- [ ] interrupt → resume 흐름 동작
- [ ] state 편집 후 이어서 실행 가능
- [ ] LangSmith에서 시간여행 시각화 확인

## 🔗 다음 → [04-platform-deploy.md](04-platform-deploy.md)
