# LiteLLM 로드 밸런싱과 폴백

## 학습 목표

- 로드 밸런싱 개념과 설정 방법 익히기
- 자동 폴백 구성하기
- 고가용성 아키텍처 설계하기

---

## 로드 밸런싱이란?

동일한 `model_name`으로 여러 배포를 설정하면 LiteLLM이 자동으로 요청을 분산합니다.

```
클라이언트 요청: model="gpt-4"
         │
         ▼
    ┌─────────┐
    │ LiteLLM │
    │ Router  │
    └─────────┘
         │
    ┌────┴────┐
    ▼         ▼
┌───────┐ ┌───────┐
│Azure  │ │OpenAI │
│East   │ │Direct │
└───────┘ └───────┘
```

---

## 기본 로드 밸런싱 설정

### 동일 model_name으로 여러 배포

```yaml
# config.yaml
model_list:
  # 같은 model_name "gpt-4"로 2개 배포 → 자동 로드 밸런싱
  - model_name: gpt-4
    litellm_params:
      model: azure/gpt-4-eastus
      api_base: https://eastus.openai.azure.com
      api_key: os.environ/AZURE_EASTUS_KEY

  - model_name: gpt-4
    litellm_params:
      model: azure/gpt-4-westus
      api_base: https://westus.openai.azure.com
      api_key: os.environ/AZURE_WESTUS_KEY
```

---

## 라우팅 전략

### 1. Simple (기본)

라운드 로빈 방식으로 순차 분산:

```yaml
router_settings:
  routing_strategy: simple
```

### 2. Least Busy

가장 여유 있는 배포로 라우팅:

```yaml
router_settings:
  routing_strategy: least-busy
```

### 3. Latency Based

응답 시간이 가장 빠른 배포 우선:

```yaml
router_settings:
  routing_strategy: latency-based-routing
```

### 4. Cost Based

비용이 가장 낮은 모델 우선:

```yaml
router_settings:
  routing_strategy: cost-based-routing
```

---

## 폴백 (Fallback)

### 폴백이란?

메인 모델 실패 시 자동으로 백업 모델로 전환됩니다.

```
요청 → GPT-4 (실패) → Claude (성공) → 응답
```

### 설정 방법

```yaml
# config.yaml
model_list:
  - model_name: main-model
    litellm_params:
      model: gpt-4o
      api_key: os.environ/OPENAI_API_KEY

  - model_name: backup-model
    litellm_params:
      model: claude-3-5-sonnet-20241022
      api_key: os.environ/ANTHROPIC_API_KEY

litellm_settings:
  fallbacks:
    - main-model: [backup-model]
```

### 여러 단계 폴백

```yaml
litellm_settings:
  fallbacks:
    - main-model: [backup-1, backup-2, backup-3]
```

실패 순서: main-model → backup-1 → backup-2 → backup-3

---

## 컨텍스트 윈도우 폴백

입력이 모델의 컨텍스트 윈도우를 초과할 때 자동으로 큰 모델로 전환:

```yaml
litellm_settings:
  context_window_fallbacks:
    - gpt-3.5-turbo: [gpt-4-turbo]  # 16K → 128K
```

---

## 재시도 (Retry) 설정

### 자동 재시도

```yaml
router_settings:
  num_retries: 3              # 최대 재시도 횟수
  retry_after: 1              # 재시도 전 대기 시간 (초)
```

### 쿨다운

실패한 배포를 일정 시간 제외:

```yaml
router_settings:
  cooldown_time: 60           # 60초 동안 해당 배포 제외
```

---

## 실전 예제

### 예제 1: 고가용성 구성

```yaml
# ha-config.yaml
model_list:
  # Primary: Azure (2개 리전)
  - model_name: gpt-4
    litellm_params:
      model: azure/gpt-4-deployment
      api_base: https://eastus.openai.azure.com
      api_key: os.environ/AZURE_EASTUS_KEY
    model_info:
      priority: 1

  - model_name: gpt-4
    litellm_params:
      model: azure/gpt-4-deployment
      api_base: https://westus.openai.azure.com
      api_key: os.environ/AZURE_WESTUS_KEY
    model_info:
      priority: 1

  # Secondary: OpenAI Direct
  - model_name: gpt-4-fallback
    litellm_params:
      model: gpt-4o
      api_key: os.environ/OPENAI_API_KEY
    model_info:
      priority: 2

litellm_settings:
  fallbacks:
    - gpt-4: [gpt-4-fallback]

router_settings:
  routing_strategy: least-busy
  num_retries: 2
  cooldown_time: 30
```

### 예제 2: 비용 최적화 구성

```yaml
# cost-optimized-config.yaml
model_list:
  # 저비용 모델 (기본)
  - model_name: chat
    litellm_params:
      model: gpt-3.5-turbo
      api_key: os.environ/OPENAI_API_KEY

  # 고성능 모델 (폴백)
  - model_name: chat-premium
    litellm_params:
      model: gpt-4o
      api_key: os.environ/OPENAI_API_KEY

  # 로컬 모델 (무료, 개발용)
  - model_name: chat-local
    litellm_params:
      model: ollama/llama3.2
      api_base: http://localhost:11434

litellm_settings:
  fallbacks:
    - chat: [chat-premium]

router_settings:
  routing_strategy: cost-based-routing
```

### 예제 3: 멀티 프로바이더 구성

```yaml
# multi-provider-ha.yaml
model_list:
  # OpenAI 계열
  - model_name: primary
    litellm_params:
      model: gpt-4o
      api_key: os.environ/OPENAI_API_KEY

  # Anthropic (폴백 1)
  - model_name: fallback-claude
    litellm_params:
      model: claude-3-5-sonnet-20241022
      api_key: os.environ/ANTHROPIC_API_KEY

  # Groq (폴백 2, 빠름)
  - model_name: fallback-groq
    litellm_params:
      model: groq/llama-3.2-90b-text-preview
      api_key: os.environ/GROQ_API_KEY

litellm_settings:
  fallbacks:
    - primary: [fallback-claude, fallback-groq]

router_settings:
  num_retries: 2
  timeout: 30
  cooldown_time: 60
```

---

## Python에서 직접 라우터 사용

```python
from litellm import Router

# 라우터 설정
router = Router(
    model_list=[
        {
            "model_name": "gpt-4",
            "litellm_params": {
                "model": "gpt-4o",
                "api_key": "sk-xxx"
            }
        },
        {
            "model_name": "gpt-4",
            "litellm_params": {
                "model": "azure/gpt-4",
                "api_base": "https://xxx.openai.azure.com",
                "api_key": "xxx"
            }
        }
    ],
    fallbacks=[{"gpt-4": ["claude"]}],
    routing_strategy="least-busy"
)

# 호출
response = router.completion(
    model="gpt-4",
    messages=[{"role": "user", "content": "Hello!"}]
)
```

---

## 모니터링

### 라우팅 상태 확인

```bash
# 사용 가능한 모델 및 상태
curl http://localhost:4000/v1/models

# 건강 상태
curl http://localhost:4000/health
```

### 로깅으로 라우팅 확인

```yaml
litellm_settings:
  set_verbose: true   # 어떤 배포로 라우팅되는지 로그 출력
```

---

## 가중치 기반 라우팅

특정 배포에 더 많은 트래픽 할당:

```yaml
model_list:
  - model_name: gpt-4
    litellm_params:
      model: azure/gpt-4-eastus
      api_key: os.environ/AZURE_KEY
    tpm: 100000    # 분당 토큰 한도 (높을수록 더 많은 요청)
    rpm: 1000      # 분당 요청 한도

  - model_name: gpt-4
    litellm_params:
      model: gpt-4o
      api_key: os.environ/OPENAI_KEY
    tpm: 50000
    rpm: 500
```

---

## 정리

| 설정 | 용도 |
|------|------|
| 동일 model_name | 자동 로드 밸런싱 |
| `fallbacks` | 실패 시 대체 모델 |
| `routing_strategy` | 분산 방식 선택 |
| `num_retries` | 자동 재시도 |
| `cooldown_time` | 실패 배포 일시 제외 |

### 라우팅 전략 선택 가이드

| 상황 | 추천 전략 |
|------|----------|
| 일반적인 경우 | `simple` |
| 트래픽이 많을 때 | `least-busy` |
| 응답 속도 중요 | `latency-based-routing` |
| 비용 최소화 | `cost-based-routing` |

### 다음 단계

- [[06-budget-tracking|예산 관리]] - 비용 추적 및 제한
- [[../05-projects|실전 프로젝트]] - 종합 적용
