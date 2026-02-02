# LiteLLM 예산 관리와 모니터링

## 학습 목표

- 비용 추적 방법 이해하기
- 예산 제한 설정하기
- 가상 키로 팀별 관리하기
- 모니터링 도구 연동하기

---

## 비용 추적 기본

### LiteLLM의 비용 계산

LiteLLM은 각 프로바이더의 공식 가격을 기반으로 비용을 자동 계산합니다.

```python
from litellm import completion

response = completion(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Hello!"}]
)

# 비용 확인
print(f"입력 토큰: {response.usage.prompt_tokens}")
print(f"출력 토큰: {response.usage.completion_tokens}")
print(f"예상 비용: ${response._hidden_params.get('response_cost', 0):.6f}")
```

### 비용 조회 유틸리티

```python
from litellm import cost_per_token, completion_cost

# 토큰당 비용 확인
input_cost, output_cost = cost_per_token(
    model="gpt-4o",
    prompt_tokens=100,
    completion_tokens=50
)
print(f"입력 비용: ${input_cost:.6f}")
print(f"출력 비용: ${output_cost:.6f}")

# 요청 비용 계산
response = completion(model="gpt-4o", messages=[...])
cost = completion_cost(completion_response=response)
print(f"총 비용: ${cost:.6f}")
```

---

## Proxy Server 비용 추적

### 데이터베이스 설정

비용과 사용량을 저장하려면 데이터베이스가 필요합니다:

```yaml
# config.yaml
general_settings:
  master_key: sk-master-1234
  database_url: postgresql://user:password@localhost:5432/litellm
```

### Docker Compose로 DB 포함 구성

```yaml
# docker-compose.yaml
version: "3.9"
services:
  litellm:
    image: ghcr.io/berriai/litellm:main-latest
    ports:
      - "4000:4000"
    volumes:
      - ./config.yaml:/app/config.yaml
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - DATABASE_URL=postgresql://postgres:postgres@db:5432/litellm
    command: --config /app/config.yaml
    depends_on:
      - db

  db:
    image: postgres:15
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: litellm
    volumes:
      - pgdata:/var/lib/postgresql/data

volumes:
  pgdata:
```

---

## 가상 키 (Virtual Keys)

### 가상 키란?

팀이나 프로젝트별로 발급하는 API 키입니다.

```
┌─────────────┐
│   Team A    │──▶ sk-team-a-xxx ──┐
└─────────────┘                    │
                                   ▼
┌─────────────┐              ┌───────────┐
│   Team B    │──▶ sk-team-b-xxx ──▶│  LiteLLM  │
└─────────────┘                    │   Proxy   │
                                   └───────────┘
┌─────────────┐                    │
│   Team C    │──▶ sk-team-c-xxx ──┘
└─────────────┘
```

### 가상 키 생성

```bash
# API로 키 생성
curl -X POST http://localhost:4000/key/generate \
  -H "Authorization: Bearer sk-master-1234" \
  -H "Content-Type: application/json" \
  -d '{
    "duration": "30d",
    "max_budget": 100.0,
    "models": ["gpt-4", "gpt-3.5-turbo"],
    "metadata": {
      "team": "backend",
      "project": "chatbot"
    }
  }'
```

응답:
```json
{
  "key": "sk-1234567890abcdef",
  "expires": "2024-02-01T00:00:00",
  "max_budget": 100.0
}
```

### 키 정보 조회

```bash
curl http://localhost:4000/key/info \
  -H "Authorization: Bearer sk-1234567890abcdef"
```

### 키 삭제

```bash
curl -X POST http://localhost:4000/key/delete \
  -H "Authorization: Bearer sk-master-1234" \
  -H "Content-Type: application/json" \
  -d '{"keys": ["sk-1234567890abcdef"]}'
```

---

## 예산 제한 설정

### 전체 예산 제한

```yaml
# config.yaml
litellm_settings:
  max_budget: 1000.0          # 총 예산 $1000
  budget_duration: 30d        # 30일 주기
```

### 가상 키별 예산 제한

```bash
# 키 생성 시 예산 설정
curl -X POST http://localhost:4000/key/generate \
  -H "Authorization: Bearer sk-master-1234" \
  -d '{
    "max_budget": 50.0,              # $50 한도
    "budget_duration": "1mo",        # 월간
    "tpm_limit": 100000,             # 분당 토큰 한도
    "rpm_limit": 100                 # 분당 요청 한도
  }'
```

### 모델별 예산

```yaml
model_list:
  - model_name: gpt-4
    litellm_params:
      model: gpt-4o
      api_key: os.environ/OPENAI_API_KEY
    model_info:
      max_budget: 500.0    # 이 모델에 $500 한도
```

---

## 사용량 조회

### 키별 사용량

```bash
curl http://localhost:4000/spend/logs \
  -H "Authorization: Bearer sk-master-1234" \
  -G -d "api_key=sk-team-a-xxx"
```

### 기간별 사용량

```bash
curl http://localhost:4000/spend/logs \
  -H "Authorization: Bearer sk-master-1234" \
  -G \
  -d "start_date=2024-01-01" \
  -d "end_date=2024-01-31"
```

### 사용량 리포트

```bash
curl http://localhost:4000/spend/report \
  -H "Authorization: Bearer sk-master-1234"
```

---

## 레이트 리미팅

### 전역 설정

```yaml
router_settings:
  global_max_parallel_requests: 100   # 전체 동시 요청 한도
```

### 키별 설정

```bash
curl -X POST http://localhost:4000/key/generate \
  -d '{
    "tpm_limit": 50000,      # 분당 토큰
    "rpm_limit": 50,         # 분당 요청
    "max_parallel_requests": 10
  }'
```

### Redis 기반 레이트 리미팅

```yaml
general_settings:
  database_url: os.environ/DATABASE_URL

router_settings:
  redis_host: localhost
  redis_port: 6379
```

---

## 모니터링 연동

### Langfuse

```yaml
litellm_settings:
  success_callback: ["langfuse"]
  failure_callback: ["langfuse"]

environment_variables:
  LANGFUSE_PUBLIC_KEY: pk-xxx
  LANGFUSE_SECRET_KEY: sk-xxx
  LANGFUSE_HOST: https://cloud.langfuse.com
```

### Prometheus 메트릭

```yaml
litellm_settings:
  success_callback: ["prometheus"]
```

```bash
# 메트릭 조회
curl http://localhost:4000/metrics
```

### Custom Callback

```python
# custom_callback.py
import litellm

def my_callback(kwargs, completion_response, start_time, end_time):
    cost = completion_response._hidden_params.get("response_cost", 0)
    model = kwargs.get("model")
    # 커스텀 로직 (DB 저장, 알림 등)
    print(f"Model: {model}, Cost: ${cost:.6f}")

litellm.success_callback = [my_callback]
```

---

## 알림 설정

### Slack 알림

```yaml
general_settings:
  alerting: ["slack"]
  alerting_threshold: 300        # 5분 내 응답 없으면 알림

environment_variables:
  SLACK_WEBHOOK_URL: https://hooks.slack.com/services/xxx
```

### 예산 초과 알림

```yaml
litellm_settings:
  max_budget: 1000.0
  budget_alert_threshold: 0.9   # 90% 도달 시 알림
```

---

## 실전 예제

### 예제 1: 팀별 예산 관리

```yaml
# team-budget-config.yaml
model_list:
  - model_name: gpt-4
    litellm_params:
      model: gpt-4o
      api_key: os.environ/OPENAI_API_KEY

  - model_name: gpt-3.5
    litellm_params:
      model: gpt-3.5-turbo
      api_key: os.environ/OPENAI_API_KEY

general_settings:
  master_key: os.environ/LITELLM_MASTER_KEY
  database_url: os.environ/DATABASE_URL
  alerting: ["slack"]

litellm_settings:
  max_budget: 5000.0            # 전체 $5000
  budget_duration: 1mo
```

팀별 키 생성:
```bash
# 프론트엔드팀 - $500/월, GPT-3.5만
curl -X POST http://localhost:4000/key/generate \
  -H "Authorization: Bearer $MASTER_KEY" \
  -d '{
    "max_budget": 500.0,
    "budget_duration": "1mo",
    "models": ["gpt-3.5"],
    "metadata": {"team": "frontend"}
  }'

# 백엔드팀 - $1000/월, 모든 모델
curl -X POST http://localhost:4000/key/generate \
  -H "Authorization: Bearer $MASTER_KEY" \
  -d '{
    "max_budget": 1000.0,
    "budget_duration": "1mo",
    "metadata": {"team": "backend"}
  }'
```

### 예제 2: 비용 대시보드

```python
import requests

PROXY_URL = "http://localhost:4000"
MASTER_KEY = "sk-master-xxx"

def get_spend_report():
    headers = {"Authorization": f"Bearer {MASTER_KEY}"}

    # 전체 사용량
    response = requests.get(
        f"{PROXY_URL}/spend/report",
        headers=headers
    )
    report = response.json()

    print("=== 비용 리포트 ===")
    print(f"총 사용량: ${report.get('total_spend', 0):.2f}")

    # 키별 사용량
    logs = requests.get(
        f"{PROXY_URL}/spend/logs",
        headers=headers
    ).json()

    print("\n=== 키별 사용량 ===")
    for log in logs[:10]:
        print(f"- {log['api_key'][:20]}...: ${log['spend']:.4f}")

get_spend_report()
```

---

## 정리

| 기능 | 설정 위치 |
|------|----------|
| 전체 예산 | `litellm_settings.max_budget` |
| 키별 예산 | `/key/generate` API |
| 레이트 리미팅 | `router_settings` |
| 사용량 조회 | `/spend/logs` API |
| 알림 | `general_settings.alerting` |

### 필수 구성

1. 데이터베이스 연결 (`database_url`)
2. 마스터 키 설정 (`master_key`)
3. 가상 키 발급
4. 예산 제한 설정

### 다음 단계

- [[../05-projects|실전 프로젝트]] - 종합 적용
- [[../cheatsheet|치트시트]] - 빠른 참조
