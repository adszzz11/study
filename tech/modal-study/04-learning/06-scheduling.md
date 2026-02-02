---
date: 2026-02-02
tags:
  - tech
  - modal
  - scheduling
  - cron
  - tutorial
parent: "[[../README]]"
---

# Modal - 스케줄링과 Cron

> [[05-volumes|이전: 볼륨]] | [[../README|목차]] | [[../05-projects|다음: 실전 프로젝트]]

---

## 1. 스케줄링 개요

### Modal 스케줄링이란?

Modal에서 함수를 주기적으로 실행하는 기능입니다.

사용 사례:
- 주기적 데이터 수집
- 정기 배치 작업
- 모니터링 및 알림
- 백업 작업

---

## 2. @modal.Schedule() 기본

### Cron 표현식 사용

```python
import modal

app = modal.App("scheduled-job")

# 매 시간 정각에 실행
@app.function(schedule=modal.Cron("0 * * * *"))
def hourly_job():
    print("매 시간 실행!")
    return "완료"
```

### 주기 지정 (Period)

```python
# 5분마다 실행
@app.function(schedule=modal.Period(minutes=5))
def every_5_minutes():
    print("5분마다 실행!")

# 1시간마다 실행
@app.function(schedule=modal.Period(hours=1))
def every_hour():
    print("1시간마다 실행!")

# 1일마다 실행
@app.function(schedule=modal.Period(days=1))
def daily():
    print("매일 실행!")
```

---

## 3. Cron 표현식

### Cron 형식

```
분 시 일 월 요일
*  *  *  *  *

예시:
0 9 * * *     = 매일 오전 9시
0 */2 * * *   = 2시간마다
0 0 * * 1     = 매주 월요일 자정
0 0 1 * *     = 매월 1일 자정
*/30 * * * *  = 30분마다
```

### 자주 사용하는 패턴

| 패턴 | Cron 표현식 | 설명 |
|------|------------|------|
| 매분 | `* * * * *` | 1분마다 |
| 매시간 | `0 * * * *` | 정각마다 |
| 매일 자정 | `0 0 * * *` | 자정에 |
| 매일 오전 9시 | `0 9 * * *` | 오전 9시 |
| 매주 월요일 | `0 0 * * 1` | 월요일 자정 |
| 매월 1일 | `0 0 1 * *` | 매월 1일 자정 |
| 평일 오전 9시 | `0 9 * * 1-5` | 월~금 9시 |

### Modal에서 Cron 사용

```python
import modal

app = modal.App("cron-examples")

# 매일 오전 9시 (UTC)
@app.function(schedule=modal.Cron("0 9 * * *"))
def morning_report():
    generate_daily_report()

# 평일 오후 6시
@app.function(schedule=modal.Cron("0 18 * * 1-5"))
def weekday_summary():
    send_daily_summary()

# 매주 일요일 자정
@app.function(schedule=modal.Cron("0 0 * * 0"))
def weekly_backup():
    backup_data()
```

---

## 4. 실전 예제: 데이터 수집

### 주기적 웹 스크래핑

```python
import modal

app = modal.App("data-collector")

image = modal.Image.debian_slim().pip_install(
    "requests", "beautifulsoup4"
)

data_volume = modal.Volume.from_name("collected-data", create_if_missing=True)

# 1시간마다 데이터 수집
@app.function(
    image=image,
    schedule=modal.Period(hours=1),
    volumes={"/data": data_volume}
)
def collect_data():
    import requests
    from bs4 import BeautifulSoup
    from datetime import datetime
    import json

    # 데이터 수집
    response = requests.get("https://example.com/api/data")
    data = response.json()

    # 타임스탬프와 함께 저장
    timestamp = datetime.now().isoformat()
    filename = f"/data/collected_{timestamp}.json"

    with open(filename, "w") as f:
        json.dump(data, f)

    data_volume.commit()
    print(f"데이터 수집 완료: {filename}")
```

### API 상태 모니터링

```python
import modal

app = modal.App("health-monitor")

image = modal.Image.debian_slim().pip_install("requests")

# 5분마다 헬스체크
@app.function(
    image=image,
    schedule=modal.Period(minutes=5),
    secrets=[modal.Secret.from_name("slack-webhook")]
)
def health_check():
    import requests
    import os

    endpoints = [
        "https://api.example.com/health",
        "https://service.example.com/status"
    ]

    for url in endpoints:
        try:
            response = requests.get(url, timeout=10)
            if response.status_code != 200:
                send_alert(f"서비스 이상: {url}")
        except Exception as e:
            send_alert(f"서비스 다운: {url} - {e}")

def send_alert(message):
    import os
    webhook_url = os.environ["SLACK_WEBHOOK"]
    requests.post(webhook_url, json={"text": message})
```

---

## 5. 스케줄 작업 관리

### 배포

```bash
# 스케줄 작업 배포
modal deploy app.py

# 배포된 앱에서 스케줄 확인
modal app list
```

### 로그 확인

```bash
# 스케줄 작업 로그 보기
modal app logs <app-name>
```

### 수동 실행

```python
# 스케줄된 함수도 수동 실행 가능
@app.function(schedule=modal.Period(hours=1))
def scheduled_task():
    return "실행됨"

@app.local_entrypoint()
def main():
    # 테스트를 위해 수동 실행
    result = scheduled_task.remote()
    print(result)
```

---

## 6. 에러 처리

### 재시도 설정

```python
@app.function(
    schedule=modal.Period(hours=1),
    retries=3  # 실패 시 3번 재시도
)
def reliable_job():
    try:
        do_work()
    except Exception as e:
        print(f"에러 발생: {e}")
        raise  # 재시도를 위해 에러 다시 발생
```

### 알림 전송

```python
@app.function(
    schedule=modal.Period(hours=1),
    secrets=[modal.Secret.from_name("notifications")]
)
def monitored_job():
    import os

    try:
        result = do_work()
        # 성공 알림 (선택)
        notify(f"작업 성공: {result}")
    except Exception as e:
        # 실패 알림
        notify(f"작업 실패: {e}")
        raise
```

---

## 7. 타임존 고려

### UTC 기준

Modal의 Cron은 **UTC** 기준입니다.

```python
# 한국 시간 오전 9시 = UTC 자정
@app.function(schedule=modal.Cron("0 0 * * *"))
def korean_morning():
    # 한국 기준 오전 9시에 실행
    pass
```

### 타임존 변환 팁

| 한국 시간 | UTC |
|----------|-----|
| 09:00 | 00:00 |
| 12:00 | 03:00 |
| 18:00 | 09:00 |
| 00:00 | 15:00 (전날) |

```python
# 한국 시간 기준 스케줄 예시
schedules = {
    "한국 오전 9시": modal.Cron("0 0 * * *"),    # UTC 00:00
    "한국 정오": modal.Cron("0 3 * * *"),        # UTC 03:00
    "한국 오후 6시": modal.Cron("0 9 * * *"),    # UTC 09:00
}
```

---

## 8. 실전 예제: 일일 리포트

```python
import modal
from datetime import datetime, timedelta

app = modal.App("daily-report")

image = modal.Image.debian_slim().pip_install(
    "pandas", "jinja2", "requests"
)

report_volume = modal.Volume.from_name("reports", create_if_missing=True)

# 매일 한국시간 오전 9시 (UTC 00:00)
@app.function(
    image=image,
    schedule=modal.Cron("0 0 * * *"),
    volumes={"/reports": report_volume},
    secrets=[modal.Secret.from_name("email-config")]
)
def daily_report():
    import pandas as pd
    import os

    # 어제 날짜
    yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

    # 데이터 수집
    data = collect_metrics(yesterday)

    # 리포트 생성
    df = pd.DataFrame(data)
    report_path = f"/reports/{yesterday}_report.html"
    df.to_html(report_path)

    report_volume.commit()

    # 이메일 발송
    send_email(
        to=os.environ["REPORT_EMAIL"],
        subject=f"일일 리포트 - {yesterday}",
        body=df.to_html()
    )

    print(f"리포트 생성 및 발송 완료: {yesterday}")
```

---

## 9. 체크리스트

### 학습 확인

- [ ] modal.Period() 사용 가능
- [ ] modal.Cron() 표현식 이해
- [ ] 주기적 작업 배포 가능
- [ ] 에러 처리 및 재시도 설정 가능
- [ ] 타임존 차이 이해 (UTC vs 한국 시간)
- [ ] 스케줄 작업 모니터링 가능

---

## 다음 단계

> [!tip] 다음으로
> 스케줄링을 배웠다면 [[../05-projects|실전 프로젝트]]에서 종합 예제를 실습하세요.

---

## References

- [Modal Scheduling Guide](https://modal.com/docs/guide/cron)
- [Cron Expression Generator](https://crontab.guru)
