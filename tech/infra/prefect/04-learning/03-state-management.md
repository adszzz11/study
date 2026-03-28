# 상태 관리와 에러 처리

## 📌 핵심 개념

Prefect은 모든 Flow/Task 실행의 상태를 자동 추적합니다:

```
Pending → Running → Completed (성공)
Pending → Running → Failed (실패)
Pending → Running → Retrying → ... (재시도)
```

---

## 💻 코드 예제: 고급 에러 처리

```python
from prefect import flow, task
from prefect.states import Failed
import random

@task(retries=3, retry_delay_seconds=[1, 5, 10])  # 점진적 재시도
def unreliable_task():
    """50% 확률로 실패하는 태스크"""
    if random.random() < 0.5:
        raise ValueError("Random failure!")
    return "Success"

@task
def cleanup_on_failure():
    """실패 시 정리 작업"""
    print("Cleaning up resources...")

@flow
def resilient_flow():
    result = unreliable_task(return_state=True)

    if result.is_failed():
        cleanup_on_failure()
        return Failed(message="Task failed after retries")

    return result.result()

# 실행
if __name__ == "__main__":
    final_state = resilient_flow(return_state=True)
    print(f"Flow ended with state: {final_state}")
```

### 자동화(Automations) 설정

```python
from prefect.automations import Automation
from prefect.events.schemas import EventTrigger, Posture

# 프로그래밍 방식 자동화 (Prefect 3.0+)
automation = Automation(
    name="Alert on failure",
    trigger=EventTrigger(
        match={"prefect.state": "Failed"},
        posture=Posture.REACTIVE,
    ),
    actions=[...]  # Slack, Email 등
)
```

---

## ✅ 체크포인트

- [ ] `return_state=True`를 사용해 상태를 확인할 수 있는가?
- [ ] 점진적 재시도(exponential backoff)를 설정할 수 있는가?
- [ ] 실패 시 정리 작업을 트리거할 수 있는가?

---

## ⚠️ 흔한 실수

| 실수 | 해결책 |
|------|--------|
| 예외를 catch하면 Prefect이 실패 인식 못함 | 필요시 `raise` 다시 |
| 재시도 횟수가 너무 많음 | 전체 파이프라인 지연 고려 |

---

## 🔗 더 알아보기

- [State management](https://docs.prefect.io/v3/develop/manage-states)
