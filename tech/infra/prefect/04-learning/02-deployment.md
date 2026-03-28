# Deployment와 스케줄링

## 📌 핵심 개념

Deployment는 Flow를 "실행 가능한 상태"로 패키징한 것입니다. 스케줄, 파라미터, 실행 환경을 정의합니다.

---

## 💻 코드 예제: Cron 스케줄 배포

### 방법 1: 코드에서 직접 배포

```python
from prefect import flow

@flow(log_prints=True)
def daily_report():
    print("Generating daily report...")
    return "Report generated"

if __name__ == "__main__":
    daily_report.serve(
        name="daily-report-deployment",
        cron="0 9 * * *",  # 매일 오전 9시
        tags=["reporting", "daily"],
        parameters={}
    )
```

### 방법 2: CLI로 배포

```bash
prefect deploy hello_prefect.py:hello_flow \
    --name my-deployment \
    --cron "0 9 * * *"
```

### 방법 3: prefect.yaml 설정 파일

```yaml
# prefect.yaml
name: my-project
prefect-version: 3.0.0

deployments:
  - name: daily-etl
    entrypoint: flows/etl.py:etl_pipeline
    schedule:
      cron: "0 6 * * *"
    parameters:
      api_url: "https://api.example.com/data"
    work_pool:
      name: my-docker-pool
```

---

## ✅ 체크포인트

- [ ] `serve()`와 `deploy()`의 차이를 이해하는가?
- [ ] Cron 표현식으로 스케줄을 설정할 수 있는가?
- [ ] Work Pool이 무엇인지 설명할 수 있는가?

---

## ⚠️ 흔한 실수

| 실수 | 해결책 |
|------|--------|
| `serve()` 사용 시 프로세스 종료되면 실행 안 됨 | 개발용으로만 사용, 프로덕션은 `deploy()` |
| Work Pool 없이 `deploy()` 사용 | Work Pool 먼저 생성 필요 |

---

## 🔗 더 알아보기

- [Deployments](https://docs.prefect.io/v3/deploy/)
