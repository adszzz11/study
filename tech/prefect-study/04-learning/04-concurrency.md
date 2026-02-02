# 병렬 실행과 동시성

## 📌 핵심 개념

Prefect은 비동기(async) 실행과 동시 태스크 실행을 지원합니다.

---

## 💻 코드 예제: 병렬 태스크 실행

### 방법 1: .map() 사용

```python
from prefect import flow, task

@task
def process_item(item: int) -> int:
    """개별 아이템 처리"""
    import time
    time.sleep(1)  # 시뮬레이션
    return item * 2

@flow
def parallel_processing():
    items = [1, 2, 3, 4, 5]

    # .map() 사용 - 자동 병렬화
    results = process_item.map(items)
    return [r.result() for r in results]

if __name__ == "__main__":
    print(parallel_processing())
```

### 방법 2: 비동기 버전

```python
from prefect import flow, task
import asyncio

@task
async def async_process(item: int) -> int:
    await asyncio.sleep(1)
    return item * 2

@flow
async def async_parallel_flow():
    items = [1, 2, 3, 4, 5]

    # 비동기 병렬 실행
    tasks = [async_process(i) for i in items]
    results = await asyncio.gather(*tasks)
    return results

if __name__ == "__main__":
    print(asyncio.run(async_parallel_flow()))
```

### 동시성 제한

```python
from prefect import flow, task
from prefect.concurrency.sync import concurrency
from datetime import timedelta

@task(cache_key_fn=task_input_hash, cache_expiration=timedelta(hours=1))
def rate_limited_api_call(endpoint: str):
    with concurrency("api-rate-limit", occupy=1):
        response = httpx.get(endpoint)
        return response.json()
```

---

## ✅ 체크포인트

- [ ] `.map()`을 사용해 병렬 처리를 구현할 수 있는가?
- [ ] 동시성 제한이 필요한 상황을 설명할 수 있는가?
- [ ] async Flow와 sync Flow의 차이를 이해하는가?

---

## ⚠️ 흔한 실수

| 실수 | 해결책 |
|------|--------|
| `.map()` 결과는 PrefectFuture | `.result()` 호출 필요 |
| 과도한 병렬화 | 리소스 고갈 주의 |

---

## 🔗 더 알아보기

- [Task runners](https://docs.prefect.io/v3/develop/task-runners)
