# Prefect 심층 스터디 가이드

> **한 줄 정의**: Python 함수를 프로덕션급 데이터 파이프라인으로 변환하는 워크플로우 오케스트레이션 프레임워크

---

## Part 1: 개요

### 1.1 정의 및 핵심 개념

**3줄 요약**:
1. Python 함수에 데코레이터만 붙이면 자동으로 상태 추적, 실패 처리, 모니터링이 되는 데이터 파이프라인 구축
2. DSL이나 복잡한 설정 파일 없이 순수 Python으로 워크플로우 정의
3. 로컬, 클라우드, 하이브리드 어디서든 실행 가능한 유연한 배포

**핵심 키워드**: `#워크플로우오케스트레이션` `#데이터파이프라인` `#Python` `#ETL` `#MLOps`

**Prefect의 핵심 구성요소**:

| 개념 | 설명 | Git 비유 |
|------|------|----------|
| **Flow** | 워크플로우의 컨테이너, 최상위 함수 | Repository |
| **Task** | 개별 작업 단위, 재사용 가능 | Commit |
| **Deployment** | Flow를 실행 가능한 상태로 패키징 | Release |
| **Work Pool** | 실행 인프라 정의 (K8s, Docker 등) | CI/CD Runner |

### 1.2 Quick Start (30초 체험)

```bash
# 1. 설치 (Python 3.10+ 필요)
pip install prefect

# 2. 간단한 Flow 작성 (hello_prefect.py)
```

```python
from prefect import flow, task

@task
def say_hello(name: str) -> str:
    print(f"Hello, {name}!")
    return f"Hello, {name}!"

@flow(name="My First Flow")
def hello_flow(name: str = "World"):
    result = say_hello(name)
    return result

# 실행
if __name__ == "__main__":
    hello_flow("Prefect")
```

```bash
# 3. 실행
python hello_prefect.py

# 4. UI 확인 (선택)
prefect server start
# 브라우저에서 http://localhost:4200 접속
```

### 1.3 왜 Prefect인가?

**장점**:
- **간단함**: Python 함수에 데코레이터만 추가하면 끝
- **유연함**: 로컬 개발 → 프로덕션 배포까지 동일한 코드
- **강력한 실패 처리**: 자동 재시도, 상태 추적, 알림
- **하이브리드 실행**: 클라우드 컨트롤 플레인 + 자체 인프라 실행
- **Prefect 3.0**: 2024년 출시, 런타임 오버헤드 90% 감소

**단점**:
- 데이터 리니지 기능이 Dagster 대비 약함
- 대규모 엔터프라이즈 기능은 유료 Prefect Cloud에 집중
- Airflow 대비 작은 커뮤니티/에코시스템

**주요 사용 사례**:
- ETL/ELT 데이터 파이프라인
- ML 모델 학습/배포 워크플로우
- 이벤트 기반 자동화
- 정기 리포트 생성

---

## Part 2: 생태계 파악

### 2.1 관련 기술/용어 맵

```
┌─────────────────────────────────────────────────────────────┐
│                    Prefect 생태계                            │
├─────────────────────────────────────────────────────────────┤
│  [Core]                                                      │
│  ├── Flow: 워크플로우 정의                                    │
│  ├── Task: 개별 작업 단위                                     │
│  ├── Deployment: 실행 가능한 워크플로우 패키지                  │
│  └── Work Pool: 실행 인프라 (Docker, K8s, Process)            │
│                                                              │
│  [실행 옵션]                                                  │
│  ├── Prefect Server (Self-hosted): 로컬/자체 서버             │
│  └── Prefect Cloud (Managed): SaaS 관리형                    │
│                                                              │
│  [통합]                                                       │
│  ├── prefect-aws: S3, ECS, Lambda                            │
│  ├── prefect-gcp: GCS, Cloud Run, BigQuery                   │
│  ├── prefect-dbt: dbt Core/Cloud 통합                        │
│  └── prefect-slack: 알림 통합                                 │
└─────────────────────────────────────────────────────────────┘
```

### 2.2 함께 자주 쓰이는 기술 스택

| 영역 | 기술 | 용도 |
|------|------|------|
| **데이터 변환** | dbt | SQL 기반 데이터 모델링 |
| **데이터 저장소** | Snowflake, BigQuery, Postgres | 데이터 웨어하우스 |
| **인프라** | Docker, Kubernetes | 실행 환경 |
| **모니터링** | Datadog, PagerDuty | 알림/모니터링 |
| **ML** | MLflow, Weights & Biases | 실험 추적 |

### 2.3 경쟁/대안 기술 비교

| 기준 | Prefect | Airflow | Dagster |
|------|---------|---------|---------|
| **철학** | 동적 워크플로우 | 태스크 기반 DAG | 에셋 중심 |
| **학습 곡선** | 쉬움 | 가파름 | 보통 |
| **설정 방식** | Pure Python | Python + YAML | Python + YAML |
| **데이터 리니지** | 기본적 | 제한적 | 강력함 |
| **적합 대상** | 스타트업, 민첩한 팀 | 엔터프라이즈 | ML 파이프라인 |
| **월 다운로드** | - | 30M+ | - |

**선택 가이드**:
- **Prefect**: 빠른 시작, 유연한 하이브리드 실행이 필요할 때
- **Airflow**: 광범위한 통합, 대규모 엔터프라이즈 환경
- **Dagster**: 데이터 품질과 리니지가 중요한 ML 파이프라인

### 2.4 최신 트렌드 및 동향 (2025)

- **Prefect 3.0 출시 (2024)**: 런타임 오버헤드 90% 개선, 이벤트 기반 워크플로우 오픈소스화
- **MCP 서버 지원**: Claude, Cursor 등 AI 도구에서 Prefect 문서/워크플로우 직접 접근
- **GenAI 워크플로우 증가**: 30% MLOps, 10% GenAI 관련 사용
- **월 2억 건 이상의 태스크 자동화**: Progressive Insurance, Cash App 등 Fortune 50 기업 사용

---

## Part 3: 레퍼런스

### 3.1 공식 문서 및 필수 링크

| 리소스 | URL | 설명 |
|--------|-----|------|
| 🟢 공식 문서 | [docs.prefect.io](https://docs.prefect.io/) | 가장 중요한 레퍼런스 |
| 🟢 GitHub | [github.com/PrefectHQ/prefect](https://github.com/PrefectHQ/prefect) | 소스 코드 및 이슈 |
| 🟢 Prefect Cloud | [app.prefect.cloud](https://app.prefect.cloud/) | 관리형 서비스 |
| 🟡 MCP 서버 | [docs.prefect.io/mcp](https://docs.prefect.io/mcp) | AI 도구 통합 |

### 3.2 추천 학습 자료

**🟢 입문**:
- [Prefect Quickstart](https://docs.prefect.io/latest/getting-started/quickstart/) - 공식 빠른 시작 가이드
- [DataCamp: ML Workflow Orchestration with Prefect](https://www.datacamp.com/tutorial/ml-workflow-orchestration-with-prefect) - ML 워크플로우 튜토리얼

**🟡 중급**:
- [Prefect How-to Guides](https://docs.prefect.io/v3/how-to-guides/) - 실전 가이드 모음
- [Prefect 2 → 3 마이그레이션](https://docs.prefect.io/latest/guides/upgrade-guide-prefect-2-to-prefect-3/) - 버전 업그레이드

**🔴 고급**:
- [Prefect Blog](https://www.prefect.io/blog/) - 고급 패턴 및 사례 연구
- [Prefect Community Slack](https://prefect.io/slack) - 실시간 질의응답

### 3.3 커뮤니티 및 질문할 곳

- **Prefect Community Slack**: 가장 활발한 커뮤니티
- **GitHub Discussions**: [github.com/PrefectHQ/prefect/discussions](https://github.com/PrefectHQ/prefect/discussions)
- **Stack Overflow**: `[prefect]` 태그

### 3.4 실무 예제/오픈소스 프로젝트

- [Prefect Recipes](https://github.com/PrefectHQ/prefect-recipes) - 공식 예제 모음
- [Prefect Collections](https://docs.prefect.io/integrations/) - 통합 패키지 모음 (AWS, GCP, dbt 등)

---

## Part 4: 상세 학습 로드맵

### 4.1 Flow와 Task 기초

📌 **핵심 개념**

Flow는 워크플로우의 진입점이고, Task는 그 안에서 실행되는 개별 작업 단위입니다.

```
Flow (전체 파이프라인)
  └── Task A (데이터 추출)
  └── Task B (데이터 변환)
  └── Task C (데이터 적재)
```

💻 **코드 예제: ETL 파이프라인**

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
    # 필요한 필드만 추출
    return [
        {"id": item["id"], "name": item["name"]}
        for item in raw_data.get("items", [])
    ]

@task
def load_data(data: list) -> int:
    """데이터 저장 (예: DB에 삽입)"""
    # 실제로는 DB 저장 로직
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

✅ **체크포인트**
- [ ] `@flow`와 `@task` 데코레이터의 차이점을 설명할 수 있는가?
- [ ] Task에 재시도(retry) 설정을 추가할 수 있는가?
- [ ] Flow 실행 결과를 UI에서 확인할 수 있는가?

⚠️ **흔한 실수**
- Task 안에서 다른 Task를 직접 호출하면 추적이 안 됨 → Flow 내에서 호출
- `log_prints=True` 없이 print 사용하면 로그에 안 남음

🔗 **더 알아보기**: [Write and run flows](https://docs.prefect.io/v3/develop/write-flows)

---

### 4.2 Deployment와 스케줄링

📌 **핵심 개념**

Deployment는 Flow를 "실행 가능한 상태"로 패키징한 것입니다. 스케줄, 파라미터, 실행 환경을 정의합니다.

💻 **코드 예제: Cron 스케줄 배포**

```python
from prefect import flow
from prefect.schedules import CronSchedule

@flow(log_prints=True)
def daily_report():
    print("Generating daily report...")
    # 리포트 생성 로직
    return "Report generated"

# 방법 1: 코드에서 직접 배포
if __name__ == "__main__":
    daily_report.serve(
        name="daily-report-deployment",
        cron="0 9 * * *",  # 매일 오전 9시
        tags=["reporting", "daily"],
        parameters={}
    )
```

```bash
# 방법 2: CLI로 배포
prefect deploy hello_prefect.py:hello_flow \
    --name my-deployment \
    --cron "0 9 * * *"
```

**prefect.yaml 설정 파일**:
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

✅ **체크포인트**
- [ ] `serve()`와 `deploy()`의 차이를 이해하는가?
- [ ] Cron 표현식으로 스케줄을 설정할 수 있는가?
- [ ] Work Pool이 무엇인지 설명할 수 있는가?

⚠️ **흔한 실수**
- `serve()`는 프로세스가 살아있어야 실행됨 (개발용)
- 프로덕션에서는 `deploy()` + Work Pool 사용

🔗 **더 알아보기**: [Deployments](https://docs.prefect.io/v3/deploy/)

---

### 4.3 상태 관리와 에러 처리

📌 **핵심 개념**

Prefect은 모든 Flow/Task 실행의 상태를 자동 추적합니다:
- **Pending** → **Running** → **Completed** (성공)
- **Pending** → **Running** → **Failed** (실패)
- **Pending** → **Running** → **Retrying** → ... (재시도)

💻 **코드 예제: 고급 에러 처리**

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
        # 커스텀 실패 상태 반환
        return Failed(message="Task failed after retries")

    return result.result()

# 실행
if __name__ == "__main__":
    final_state = resilient_flow(return_state=True)
    print(f"Flow ended with state: {final_state}")
```

**자동화(Automations) 설정**:
```python
# Prefect Cloud/Server UI에서 설정하거나 API 사용
# 예: Flow 실패 시 Slack 알림

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

✅ **체크포인트**
- [ ] `return_state=True`를 사용해 상태를 확인할 수 있는가?
- [ ] 점진적 재시도(exponential backoff)를 설정할 수 있는가?
- [ ] 실패 시 정리 작업을 트리거할 수 있는가?

⚠️ **흔한 실수**
- 예외를 catch하면 Prefect이 실패를 인식 못함 → 필요시 `raise` 다시
- 재시도 횟수가 너무 많으면 전체 파이프라인 지연

🔗 **더 알아보기**: [State management](https://docs.prefect.io/v3/develop/manage-states)

---

### 4.4 병렬 실행과 동시성

📌 **핵심 개념**

Prefect은 비동기(async) 실행과 동시 태스크 실행을 지원합니다.

💻 **코드 예제: 병렬 태스크 실행**

```python
from prefect import flow, task
import asyncio

@task
def process_item(item: int) -> int:
    """개별 아이템 처리"""
    import time
    time.sleep(1)  # 시뮬레이션
    return item * 2

@flow
def parallel_processing():
    items = [1, 2, 3, 4, 5]

    # 방법 1: .map() 사용 - 자동 병렬화
    results = process_item.map(items)
    return [r.result() for r in results]

# 비동기 버전
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
    # 동기 버전
    print(parallel_processing())

    # 비동기 버전
    print(asyncio.run(async_parallel_flow()))
```

**동시성 제한**:
```python
from prefect import flow, task
from prefect.tasks import task_input_hash
from prefect.concurrency.sync import concurrency

@task(cache_key_fn=task_input_hash, cache_expiration=timedelta(hours=1))
def rate_limited_api_call(endpoint: str):
    # 동시 실행 제한
    with concurrency("api-rate-limit", occupy=1):
        response = httpx.get(endpoint)
        return response.json()
```

✅ **체크포인트**
- [ ] `.map()`을 사용해 병렬 처리를 구현할 수 있는가?
- [ ] 동시성 제한이 필요한 상황을 설명할 수 있는가?
- [ ] async Flow와 sync Flow의 차이를 이해하는가?

⚠️ **흔한 실수**
- `.map()` 결과는 PrefectFuture → `.result()` 호출 필요
- 과도한 병렬화는 리소스 고갈 초래

🔗 **더 알아보기**: [Task runners](https://docs.prefect.io/v3/develop/task-runners)

---

### 4.5 Work Pools와 인프라 관리

📌 **핵심 개념**

Work Pool은 Flow가 실행될 인프라를 정의합니다:
- **Process**: 로컬 프로세스
- **Docker**: 컨테이너 실행
- **Kubernetes**: K8s Job으로 실행

💻 **설정 예제: Docker Work Pool**

```bash
# 1. Work Pool 생성
prefect work-pool create my-docker-pool --type docker

# 2. Worker 시작 (Flow 실행을 대기)
prefect worker start --pool my-docker-pool
```

```python
# 3. Flow 배포 시 Work Pool 지정
from prefect import flow

@flow
def containerized_flow():
    return "Running in Docker!"

if __name__ == "__main__":
    containerized_flow.deploy(
        name="docker-deployment",
        work_pool_name="my-docker-pool",
        image="my-registry/my-image:latest"
    )
```

**prefect.yaml로 인프라 설정**:
```yaml
# prefect.yaml
deployments:
  - name: k8s-etl
    entrypoint: flows/etl.py:etl_pipeline
    work_pool:
      name: kubernetes-pool
      job_variables:
        image: "{{ build-image.image }}"
        cpu_request: "500m"
        memory_request: "1Gi"

build:
  - prefect_docker.deployments.steps.build_docker_image:
      id: build-image
      dockerfile: Dockerfile
      image_name: my-flow
      tag: latest
```

✅ **체크포인트**
- [ ] Work Pool의 역할을 설명할 수 있는가?
- [ ] Docker/Kubernetes Work Pool을 설정할 수 있는가?
- [ ] Worker의 역할을 이해하는가?

⚠️ **흔한 실수**
- Worker를 시작하지 않으면 Deployment가 실행되지 않음
- Work Pool 타입과 Worker 타입이 일치해야 함

🔗 **더 알아보기**: [Work pools](https://docs.prefect.io/v3/deploy/infrastructure-concepts/work-pools)

---

### 4.6 Prefect Cloud vs Self-hosted

📌 **핵심 개념**

| 기능 | Prefect Cloud | Self-hosted Server |
|------|--------------|-------------------|
| 설치 | 없음 (SaaS) | `prefect server start` |
| 비용 | 유료 플랜 | 무료 |
| 인증 | 내장 | 직접 구현 |
| 자동화 | 전체 기능 | 일부 제한 |
| 지원 | 공식 지원 | 커뮤니티 |

💻 **Self-hosted 서버 시작**:

```bash
# 1. Prefect 서버 시작
prefect server start

# 2. 다른 터미널에서 API URL 설정
prefect config set PREFECT_API_URL="http://localhost:4200/api"

# 3. Flow 실행 - 자동으로 서버에 기록됨
python my_flow.py
```

**Prefect Cloud 연결**:
```bash
# API 키 설정
prefect cloud login --key YOUR_API_KEY

# 또는 환경 변수
export PREFECT_API_KEY="YOUR_API_KEY"
export PREFECT_API_URL="https://api.prefect.cloud/api/accounts/..."
```

✅ **체크포인트**
- [ ] 언제 Cloud vs Self-hosted를 선택해야 하는지 판단할 수 있는가?
- [ ] Self-hosted 서버를 시작하고 연결할 수 있는가?

🔗 **더 알아보기**: [Prefect Cloud](https://docs.prefect.io/cloud/)

---

## Part 5: 실전 프로젝트

### 5.1 미니 프로젝트 아이디어

| 난이도 | 프로젝트 | 학습 포인트 |
|--------|---------|------------|
| 🟢 | GitHub 리포지토리 스타 수 모니터링 | API 호출, 스케줄링 |
| 🟢 | 날씨 데이터 수집 파이프라인 | 재시도, 로깅 |
| 🟡 | 웹 스크래핑 → DB 저장 ETL | 병렬 처리, 에러 핸들링 |
| 🟡 | Slack 알림 연동 일일 리포트 | 자동화, 통합 |
| 🔴 | ML 모델 학습/배포 파이프라인 | 서브플로우, 아티팩트 |

### 5.2 단계별 구현 가이드: 날씨 데이터 수집

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
    # 로컬 테스트
    # weather_pipeline(api_key="your-actual-key")

    # 스케줄 배포 (매 시간)
    weather_pipeline.serve(
        name="hourly-weather",
        cron="0 * * * *",
        parameters={"api_key": "your-api-key"}
    )
```

### 5.3 Best Practices

**코드 구조**:
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

**운영 권장사항**:

1. **환경 분리**: 개발/스테이징/프로덕션 Work Pool 분리
2. **비밀 관리**: Prefect Blocks 또는 환경 변수 사용
3. **모니터링**: 자동화(Automations)로 실패 알림 설정
4. **버전 관리**: Flow 코드와 prefect.yaml 함께 Git 관리
5. **테스트**: Task 단위로 유닛 테스트 작성

```python
# 비밀 관리 예시
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

---

## 요약

Prefect은 Python 개발자가 가장 쉽게 시작할 수 있는 워크플로우 오케스트레이션 도구입니다:

- **시작**: `pip install prefect` → `@flow`, `@task` 데코레이터 추가
- **운영**: `prefect server start` 또는 Prefect Cloud
- **배포**: `flow.serve()` 또는 `prefect deploy`
- **확장**: Work Pool로 Docker/K8s 인프라 연결

다음 단계:
1. [공식 Quickstart](https://docs.prefect.io/latest/getting-started/quickstart/) 따라하기
2. 간단한 ETL 파이프라인 만들어보기
3. Prefect Cloud 무료 티어로 모니터링 체험
