# Flow와 Task 기초

## 📌 핵심 개념

Flow는 워크플로우의 진입점이고, Task는 그 안에서 실행되는 개별 작업 단위입니다.

```
Flow (전체 파이프라인)
  └── Task A (데이터 추출)
  └── Task B (데이터 변환)
  └── Task C (데이터 적재)
```

---

## 💻 코드 예제: ETL 파이프라인

```python
from prefect import flow, task
import httpx

@task(retries=3, retry_delay_seconds=10)
def extract_data(url: str) -> dict:
    """API에서 데이터 추출 - 3회 재시도"""
    response = httpx.get(url)
    response.raise_for_status()
    return response.json()

@task
def transform_data(raw_data: dict) -> list:
    """데이터 변환 로직"""
    return [
        {"id": item["id"], "name": item["name"]}
        for item in raw_data.get("items", [])
    ]

@task
def load_data(data: list) -> int:
    """데이터 저장 (예: DB에 삽입)"""
    print(f"Loaded {len(data)} records")
    return len(data)

@flow(name="ETL Pipeline", log_prints=True)
def etl_pipeline(api_url: str):
    raw = extract_data(api_url)
    transformed = transform_data(raw)
    count = load_data(transformed)
    return count

# 실행
if __name__ == "__main__":
    result = etl_pipeline("https://api.example.com/data")
    print(f"Pipeline completed: {result} records processed")
```

---

## ✅ 체크포인트

- [ ] `@flow`와 `@task` 데코레이터의 차이점을 설명할 수 있는가?
- [ ] Task에 재시도(retry) 설정을 추가할 수 있는가?
- [ ] Flow 실행 결과를 UI에서 확인할 수 있는가?

---

## ⚠️ 흔한 실수

| 실수 | 해결책 |
|------|--------|
| Task 안에서 다른 Task 직접 호출 | Flow 내에서 호출하여 추적 가능하게 |
| `log_prints=True` 없이 print 사용 | Flow에 `log_prints=True` 옵션 추가 |

---

## 🔗 더 알아보기

- [Write and run flows](https://docs.prefect.io/v3/develop/write-flows)
