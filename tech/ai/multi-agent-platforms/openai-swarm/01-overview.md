# Part 1. OpenAI Swarm 개요

## 📌 두 가지 추상화로 끝

### 1. Routine = 에이전트 시스템
```python
agent = Agent(
    name="Sales",
    instructions="고객 상담 + 결제 안내",
    functions=[process_refund, transfer_to_support],
)
```

### 2. Handoff = 다음 에이전트 반환
```python
def transfer_to_support():
    """결제 외 문의는 support에게"""
    return support_agent   # ← 이게 핸드오프
```

LLM이 `transfer_to_support()` 호출 → 함수가 다음 에이전트 반환 → Swarm이 자동으로 대화 통제권 이양.

## 🎯 핵심 디자인

- **Stateless 클라이언트** — 서버 상태 X, Chat Completions API 직접 호출
- **컨텍스트 변수** — `context_variables` dict로 thread 전체 공유 상태
- **Function 자동 스키마 생성** — Python type hint → OpenAI function calling 스키마
- **Streaming 지원** — `client.run(stream=True)`

## ⚠️ Educational의 의미

공식 README: "**not intended for production**". 의미:
- 인증·sandbox·관측성 ✗
- 영속 상태 ✗
- handoff 깊이/루프 통제 약함
- 비동기 우선 X

## 🔄 후계자: OpenAI Agents SDK

- 같은 handoffs 컨셉 유지
- async-first
- guardrails (입출력 검증)
- tracing
- 비OpenAI 모델 지원 (LiteLLM 등)
- production-ready

## ⚖️ 장단점

### ✅ 장점
- **20분이면 다 이해** — 학습 자료로 우수
- **handoffs 패턴의 정수** — LangGraph Swarm도 이 컨셉 차용
- **300줄도 안 되는 코드** — 내부 읽기 가능

### ❌ 단점
- production ✗
- maintenance ✗ (Agents SDK로 이전)
- OpenAI 종속
- 4명 이상 핸드오프 시 복잡도 ↑

## 🎯 적합도

| 상황 | 적합 |
|------|------|
| 멀티 에이전트 개념 학습 | ⭐⭐⭐⭐⭐ |
| 핸드오프 패턴 이해 | ⭐⭐⭐⭐⭐ |
| 프로덕션 | ✗ (Agents SDK로) |
| 빠른 데모 | ⭐⭐⭐ |

## 🔗 다음 → [02-ecosystem.md](02-ecosystem.md)
