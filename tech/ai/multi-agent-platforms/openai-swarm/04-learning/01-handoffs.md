# 4-1. Handoff 패턴 깊이

## 🔁 기본 핸드오프

```python
from swarm import Agent

triage = Agent(name="Triage", instructions="질문 분류")
sales = Agent(name="Sales")
support = Agent(name="Support")

def transfer_to_sales():
    """결제·요금 문의"""
    return sales

def transfer_to_support():
    """기술 문제"""
    return support

triage.functions = [transfer_to_sales, transfer_to_support]
```

LLM이 자연어로 분류 → 적절한 transfer 함수 호출 → 자동 핸드오프.

## 🎯 다층 핸드오프

```python
support.functions = [escalate_to_engineer, return_to_triage]
engineer.functions = [resolve, return_to_support]

# user → triage → support → engineer → support → 응답
```

핸드오프 깊이 깊어질수록 컨텍스트 길어짐 + 비용↑. **3-4 단계 권장**.

## 🚦 핸드오프 + 인자 동시 전달

```python
def transfer_to_sales(reason: str):
    """판매 위임 + 이유 전달"""
    print(f"Reason: {reason}")   # 로깅
    return sales
```

인자가 있어도 OK. LLM이 함수 시그니처 보고 자동 채움.

## ⚠️ 핸드오프 루프

```python
triage → sales → triage → sales → ...   # 무한 루프 가능
```

방지:
- `max_turns` 명시: `client.run(..., max_turns=10)`
- 각 에이전트 instructions에 "이미 위임받은 작업은 다시 위임 ✗" 명시

## ✅ 체크포인트
- [ ] 2-agent 핸드오프 동작
- [ ] 인자 있는 핸드오프 동작
- [ ] `max_turns`로 루프 차단 확인

## 🔗 다음 → [02-context-variables.md](02-context-variables.md)
