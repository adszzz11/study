# LiteLLM config.yaml 작성법

## 학습 목표

- config.yaml 구조 이해하기
- 모델 설정 방법 익히기
- 환경 변수 활용하기
- 고급 설정 옵션 알아보기

---

## 기본 구조

```yaml
# config.yaml 기본 구조
model_list:           # 모델 정의 (필수)
  - model_name: ...
    litellm_params: ...

general_settings:     # 서버 설정
  master_key: ...

litellm_settings:     # LiteLLM 동작 설정
  drop_params: true

router_settings:      # 라우터 설정 (로드밸런싱 등)
  routing_strategy: ...

environment_variables: # 환경 변수 정의
  KEY: value
```

---

## model_list 상세

### 기본 형식

```yaml
model_list:
  - model_name: my-gpt-4          # 클라이언트가 호출할 이름
    litellm_params:
      model: gpt-4o               # 실제 프로바이더 모델
      api_key: os.environ/OPENAI_API_KEY
```

### 주요 프로바이더별 설정

#### OpenAI

```yaml
model_list:
  - model_name: gpt-4
    litellm_params:
      model: gpt-4o
      api_key: os.environ/OPENAI_API_KEY
      # 선택 옵션
      organization: org-xxx
      timeout: 30
      max_retries: 3
```

#### Anthropic

```yaml
model_list:
  - model_name: claude
    litellm_params:
      model: claude-3-5-sonnet-20241022
      api_key: os.environ/ANTHROPIC_API_KEY
```

#### Azure OpenAI

```yaml
model_list:
  - model_name: azure-gpt4
    litellm_params:
      model: azure/my-deployment-name
      api_base: https://my-resource.openai.azure.com
      api_key: os.environ/AZURE_API_KEY
      api_version: "2024-02-15-preview"
```

#### AWS Bedrock

```yaml
model_list:
  - model_name: bedrock-claude
    litellm_params:
      model: bedrock/anthropic.claude-3-sonnet-20240229-v1:0
      aws_access_key_id: os.environ/AWS_ACCESS_KEY_ID
      aws_secret_access_key: os.environ/AWS_SECRET_ACCESS_KEY
      aws_region_name: us-east-1
```

#### Ollama (로컬)

```yaml
model_list:
  - model_name: local-llama
    litellm_params:
      model: ollama/llama3.2
      api_base: http://localhost:11434
```

#### Google Vertex AI

```yaml
model_list:
  - model_name: gemini
    litellm_params:
      model: vertex_ai/gemini-pro
      vertex_project: my-project
      vertex_location: us-central1
```

---

## 환경 변수 사용

### 방법 1: os.environ 접두사

```yaml
model_list:
  - model_name: gpt-4
    litellm_params:
      model: gpt-4o
      api_key: os.environ/OPENAI_API_KEY  # 환경 변수 참조
```

### 방법 2: environment_variables 섹션

```yaml
environment_variables:
  OPENAI_API_KEY: "sk-xxx"  # 직접 설정 (비권장)
  ANTHROPIC_API_KEY: "sk-ant-xxx"

model_list:
  - model_name: gpt-4
    litellm_params:
      model: gpt-4o
      api_key: os.environ/OPENAI_API_KEY
```

### 방법 3: .env 파일

```bash
# .env 파일
OPENAI_API_KEY=sk-xxx
ANTHROPIC_API_KEY=sk-ant-xxx
```

```bash
# 실행 시 자동 로드
litellm --config config.yaml
```

---

## general_settings

```yaml
general_settings:
  # 인증
  master_key: sk-master-1234      # 관리자 키

  # 데이터베이스 (가상 키, 사용량 저장)
  database_url: postgresql://user:pass@host:5432/litellm

  # 서버 설정
  allow_user_auth: true           # 사용자 인증 허용

  # 알림
  alerting: ["slack"]
  alerting_threshold: 300         # 초 단위
```

---

## litellm_settings

```yaml
litellm_settings:
  # 로깅
  set_verbose: true               # 상세 로그
  json_logs: true                 # JSON 형식 로그

  # 동작 설정
  drop_params: true               # 지원 안 되는 파라미터 무시
  request_timeout: 600            # 요청 타임아웃 (초)

  # 캐싱
  cache: true
  cache_params:
    type: redis
    host: localhost
    port: 6379

  # 콜백
  success_callback: ["langfuse"]
  failure_callback: ["langfuse"]

  # 폴백
  fallbacks: [
    {"gpt-4": ["claude", "azure-gpt4"]}
  ]

  # 예산 관리
  max_budget: 100.0               # 총 예산 ($)
```

---

## router_settings

```yaml
router_settings:
  # 라우팅 전략
  routing_strategy: least-busy    # simple, least-busy, latency-based-routing

  # 레이트 리미팅
  num_retries: 3
  timeout: 30

  # 쿨다운 (실패 시)
  cooldown_time: 60               # 실패한 모델 제외 시간 (초)

  # 병렬 요청
  enable_pre_call_checks: true
```

---

## 실전 예제

### 예제 1: 개발 환경

```yaml
# dev-config.yaml
model_list:
  - model_name: gpt-4
    litellm_params:
      model: gpt-4o
      api_key: os.environ/OPENAI_API_KEY

  - model_name: local
    litellm_params:
      model: ollama/llama3.2
      api_base: http://localhost:11434

general_settings:
  master_key: dev-1234

litellm_settings:
  set_verbose: true
  drop_params: true
```

### 예제 2: 프로덕션 환경

```yaml
# prod-config.yaml
model_list:
  # Primary
  - model_name: gpt-4
    litellm_params:
      model: azure/gpt-4-deployment
      api_base: os.environ/AZURE_API_BASE
      api_key: os.environ/AZURE_API_KEY
      api_version: "2024-02-15-preview"

  # Fallback
  - model_name: gpt-4
    litellm_params:
      model: gpt-4o
      api_key: os.environ/OPENAI_API_KEY

  # 저비용 모델
  - model_name: gpt-3.5
    litellm_params:
      model: gpt-3.5-turbo
      api_key: os.environ/OPENAI_API_KEY

general_settings:
  master_key: os.environ/LITELLM_MASTER_KEY
  database_url: os.environ/DATABASE_URL

litellm_settings:
  drop_params: true
  cache: true
  cache_params:
    type: redis
    host: os.environ/REDIS_HOST
    port: 6379

  fallbacks:
    - gpt-4: [gpt-3.5]

router_settings:
  routing_strategy: least-busy
  num_retries: 3
  cooldown_time: 60
```

### 예제 3: 팀별 설정

```yaml
# team-config.yaml
model_list:
  # 개발팀 - 빠른 모델
  - model_name: dev-model
    litellm_params:
      model: gpt-3.5-turbo
      api_key: os.environ/OPENAI_API_KEY
    model_info:
      description: "개발팀용 빠른 모델"

  # 데이터팀 - 고성능 모델
  - model_name: data-model
    litellm_params:
      model: gpt-4o
      api_key: os.environ/OPENAI_API_KEY
    model_info:
      description: "데이터팀용 고성능 모델"

general_settings:
  master_key: os.environ/LITELLM_MASTER_KEY
  database_url: os.environ/DATABASE_URL
```

### 예제 4: 로드 밸런싱

```yaml
# lb-config.yaml
model_list:
  # 동일 model_name으로 여러 배포 설정 → 자동 로드 밸런싱
  - model_name: gpt-4
    litellm_params:
      model: azure/gpt4-deployment-eastus
      api_base: https://eastus.openai.azure.com
      api_key: os.environ/AZURE_EASTUS_KEY

  - model_name: gpt-4
    litellm_params:
      model: azure/gpt4-deployment-westus
      api_base: https://westus.openai.azure.com
      api_key: os.environ/AZURE_WESTUS_KEY

router_settings:
  routing_strategy: least-busy
```

---

## 설정 검증

### 문법 확인

```bash
# YAML 문법 검사
python -c "import yaml; yaml.safe_load(open('config.yaml'))"
```

### 실행 테스트

```bash
# 디버그 모드로 실행
litellm --config config.yaml --detailed_debug

# 모델 목록 확인
curl http://localhost:4000/v1/models
```

---

## 자주 하는 실수

| 실수 | 해결 |
|------|------|
| 들여쓰기 오류 | 스페이스 2칸 통일 |
| 환경 변수 미설정 | `os.environ/` 접두사 확인 |
| model_name 오타 | 클라이언트 호출 이름과 일치 확인 |
| api_base 누락 | Azure, Ollama는 필수 |

---

## 정리

```yaml
# 최소 설정 템플릿
model_list:
  - model_name: default
    litellm_params:
      model: gpt-4o
      api_key: os.environ/OPENAI_API_KEY

general_settings:
  master_key: your-master-key
```

### 다음 단계

- [[04-providers|프로바이더 연결]] - 각 프로바이더 상세 설정
- [[05-load-balancing|로드 밸런싱]] - 고가용성 구성
- [[06-budget-tracking|예산 관리]] - 비용 제한 설정
