# Part 5: 실전 프로젝트

## 5.1 미니 프로젝트 아이디어

| 난이도 | 프로젝트 | 학습 포인트 |
|--------|---------|------------|
| 🟢 | GitHub 리포지토리 스타 수 모니터링 | API 호출, 스케줄링 |
| 🟢 | 날씨 데이터 수집 파이프라인 | 재시도, 로깅 |
| 🟡 | 웹 스크래핑 → DB 저장 ETL | 병렬 처리, 에러 핸들링 |
| 🟡 | Slack 알림 연동 일일 리포트 | 자동화, 통합 |
| 🔴 | ML 모델 학습/배포 파이프라인 | 서브플로우, 아티팩트 |

---

## 5.2 단계별 구현 가이드: 날씨 데이터 수집

**목표**: OpenWeather API에서 날씨 데이터를 수집하여 JSON 파일로 저장

```python
# weather_pipeline.py
from prefect import flow, task
from prefect.artifacts import create_markdown_artifact
import httpx
import json
from datetime import datetime
from pathlib import Path

@task(retries=2, retry_delay_seconds=5)
def fetch_weather(city: str, api_key: str) -> dict:
    """날씨 데이터 가져오기"""
    url = f"http://api.openweathermap.org/data/2.5/weather"
    params = {"q": city, "appid": api_key, "units": "metric"}

    response = httpx.get(url, params=params)
    response.raise_for_status()
    return response.json()

@task
def transform_weather(raw_data: dict) -> dict:
    """필요한 필드만 추출"""
    return {
        "city": raw_data["name"],
        "temperature": raw_data["main"]["temp"],
        "humidity": raw_data["main"]["humidity"],
        "description": raw_data["weather"][0]["description"],
        "timestamp": datetime.now().isoformat()
    }

@task
def save_to_file(data: dict, output_dir: str = "./data") -> str:
    """JSON 파일로 저장"""
    Path(output_dir).mkdir(exist_ok=True)

    filename = f"{data['city']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    filepath = Path(output_dir) / filename

    with open(filepath, "w") as f:
        json.dump(data, f, indent=2)

    return str(filepath)

@task
def create_report(data: dict) -> None:
    """Prefect 아티팩트로 리포트 생성"""
    markdown = f"""
## Weather Report: {data['city']}

| Metric | Value |
|--------|-------|
| Temperature | {data['temperature']}°C |
| Humidity | {data['humidity']}% |
| Conditions | {data['description']} |
| Recorded | {data['timestamp']} |
"""
    create_markdown_artifact(
        key="weather-report",
        markdown=markdown,
        description="Latest weather data"
    )

@flow(name="Weather Data Pipeline", log_prints=True)
def weather_pipeline(
    cities: list[str] = ["Seoul", "Tokyo", "New York"],
    api_key: str = "your-api-key"
):
    """여러 도시의 날씨 데이터 수집"""
    all_data = []

    for city in cities:
        raw = fetch_weather(city, api_key)
        transformed = transform_weather(raw)
        filepath = save_to_file(transformed)
        create_report(transformed)

        print(f"✅ {city}: {transformed['temperature']}°C")
        all_data.append(transformed)

    return all_data

if __name__ == "__main__":
    # 스케줄 배포 (매 시간)
    weather_pipeline.serve(
        name="hourly-weather",
        cron="0 * * * *",
        parameters={"api_key": "your-api-key"}
    )
```

---

## 5.3 Best Practices

### 프로젝트 구조

```
my-prefect-project/
├── flows/
│   ├── __init__.py
│   ├── etl.py
│   └── reporting.py
├── tasks/
│   ├── __init__.py
│   ├── extract.py
│   ├── transform.py
│   └── load.py
├── tests/
│   └── test_flows.py
├── prefect.yaml
├── requirements.txt
└── README.md
```

### 운영 권장사항

| 항목 | 권장사항 |
|------|---------|
| **환경 분리** | 개발/스테이징/프로덕션 Work Pool 분리 |
| **비밀 관리** | Prefect Blocks 또는 환경 변수 사용 |
| **모니터링** | 자동화(Automations)로 실패 알림 설정 |
| **버전 관리** | Flow 코드와 prefect.yaml 함께 Git 관리 |
| **테스트** | Task 단위로 유닛 테스트 작성 |

### 비밀 관리 예시

```python
from prefect.blocks.system import Secret

# Block 생성 (UI 또는 코드)
secret_block = Secret(value="my-api-key")
secret_block.save("openweather-api-key")

# 사용
@task
def fetch_with_secret():
    api_key = Secret.load("openweather-api-key").get()
    # ...
```
