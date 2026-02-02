# LiteLLM 프록시 서버 설정

## 학습 목표

- LiteLLM Proxy Server 개념 이해
- 로컬에서 프록시 서버 실행하기
- 클라이언트에서 프록시 서버 사용하기
- Docker로 배포하기

---

## 프록시 서버란?

LiteLLM Proxy는 LLM API 앞에 위치하는 **게이트웨이 서버**입니다.

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Client    │────▶│   LiteLLM   │────▶│     LLM     │
│ (Any Lang)  │     │   Proxy     │     │  Providers  │
└─────────────┘     └─────────────┘     └─────────────┘
      │                    │
      │                    ├── 인증/인가
      │                    ├── 로드 밸런싱
      │                    ├── 비용 추적
      │                    ├── 레이트 리미팅
      │                    └── 로깅
      │
      └── OpenAI 호환 API로 호출
```

### Python SDK vs Proxy Server

| 항목 | Python SDK | Proxy Server |
|------|------------|--------------|
| 사용 언어 | Python만 | 모든 언어 |
| 설치 위치 | 앱에 임베드 | 독립 서버 |
| 중앙 관리 | X | O |
| 팀 협업 | 어려움 | 가상 키로 관리 |
| 추가 기능 | 기본 | 캐싱, DB 연동 등 |

---

## 빠른 시작

### 1. 설치

```bash
pip install 'litellm[proxy]'
```

### 2. 단일 모델로 실행

```bash
# 환경 변수 설정
export OPENAI_API_KEY="sk-..."

# 프록시 서버 실행
litellm --model gpt-4o --port 4000
```

### 3. 클라이언트에서 호출

```bash
# curl로 테스트
curl http://localhost:4000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-4o",
    "messages": [{"role": "user", "content": "Hello!"}]
  }'
```

---

## Config 파일로 실행

### 기본 config.yaml

```yaml
model_list:
  - model_name: gpt-4
    litellm_params:
      model: gpt-4o
      api_key: os.environ/OPENAI_API_KEY

  - model_name: claude
    litellm_params:
      model: claude-3-5-sonnet-20241022
      api_key: os.environ/ANTHROPIC_API_KEY

general_settings:
  master_key: sk-1234  # 관리자 키
```

### 실행

```bash
litellm --config config.yaml --port 4000
```

---

## 클라이언트 사용법

### Python (OpenAI SDK)

```python
from openai import OpenAI

# LiteLLM Proxy를 OpenAI 클라이언트로 사용
client = OpenAI(
    base_url="http://localhost:4000/v1",
    api_key="sk-1234"  # master_key 또는 가상 키
)

response = client.chat.completions.create(
    model="gpt-4",  # config에 정의된 model_name
    messages=[{"role": "user", "content": "안녕하세요!"}]
)

print(response.choices[0].message.content)
```

### JavaScript/TypeScript

```javascript
import OpenAI from 'openai';

const client = new OpenAI({
  baseURL: 'http://localhost:4000/v1',
  apiKey: 'sk-1234',
});

const response = await client.chat.completions.create({
  model: 'gpt-4',
  messages: [{ role: 'user', content: 'Hello!' }],
});

console.log(response.choices[0].message.content);
```

### curl

```bash
curl http://localhost:4000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer sk-1234" \
  -d '{
    "model": "gpt-4",
    "messages": [{"role": "user", "content": "Hello!"}]
  }'
```

---

## Docker로 실행

### 기본 실행

```bash
docker run \
  -e OPENAI_API_KEY=sk-xxx \
  -p 4000:4000 \
  ghcr.io/berriai/litellm:main-latest \
  --model gpt-4o
```

### Config 파일 마운트

```bash
docker run \
  -v $(pwd)/config.yaml:/app/config.yaml \
  -e OPENAI_API_KEY=sk-xxx \
  -e ANTHROPIC_API_KEY=sk-ant-xxx \
  -p 4000:4000 \
  ghcr.io/berriai/litellm:main-latest \
  --config /app/config.yaml
```

### Docker Compose

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
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
    command: --config /app/config.yaml
```

```bash
# 실행
docker-compose up -d

# 로그 확인
docker-compose logs -f
```

---

## 유용한 CLI 옵션

```bash
litellm --help

# 자주 사용하는 옵션
litellm \
  --config config.yaml \    # 설정 파일
  --port 4000 \             # 포트 (기본: 4000)
  --host 0.0.0.0 \          # 호스트 (기본: 0.0.0.0)
  --num_workers 4 \         # 워커 수
  --debug \                 # 디버그 모드
  --detailed_debug          # 상세 디버그
```

---

## Health Check

### 기본 헬스체크

```bash
curl http://localhost:4000/health
```

### 모델별 헬스체크

```bash
curl http://localhost:4000/health/liveliness
curl http://localhost:4000/health/readiness
```

---

## 지원 엔드포인트

| 엔드포인트 | 설명 |
|-----------|------|
| `/v1/chat/completions` | 채팅 완성 (주로 사용) |
| `/v1/completions` | 텍스트 완성 |
| `/v1/embeddings` | 임베딩 |
| `/v1/models` | 사용 가능한 모델 목록 |
| `/health` | 서버 상태 |
| `/key/generate` | 가상 키 생성 |
| `/spend/logs` | 사용량 로그 |

---

## 로깅 설정

### 콘솔 로깅

```yaml
# config.yaml
litellm_settings:
  set_verbose: true  # 상세 로그
```

### 파일 로깅

```yaml
litellm_settings:
  log_file: /var/log/litellm.log
```

### 콜백 설정 (외부 서비스)

```yaml
litellm_settings:
  success_callback: ["langfuse"]
  failure_callback: ["langfuse"]

environment_variables:
  LANGFUSE_PUBLIC_KEY: "pk-xxx"
  LANGFUSE_SECRET_KEY: "sk-xxx"
```

---

## 실습 예제

### 예제 1: 로컬 개발 환경

```yaml
# dev-config.yaml
model_list:
  - model_name: gpt-4
    litellm_params:
      model: gpt-4o
      api_key: os.environ/OPENAI_API_KEY

general_settings:
  master_key: dev-key-1234

litellm_settings:
  set_verbose: true
```

```bash
# 실행
export OPENAI_API_KEY="sk-..."
litellm --config dev-config.yaml --port 4000

# 테스트
curl http://localhost:4000/v1/chat/completions \
  -H "Authorization: Bearer dev-key-1234" \
  -H "Content-Type: application/json" \
  -d '{"model": "gpt-4", "messages": [{"role": "user", "content": "테스트"}]}'
```

### 예제 2: 여러 모델 제공

```yaml
# multi-model-config.yaml
model_list:
  # OpenAI 모델들
  - model_name: gpt-4
    litellm_params:
      model: gpt-4o
      api_key: os.environ/OPENAI_API_KEY

  - model_name: gpt-3.5
    litellm_params:
      model: gpt-3.5-turbo
      api_key: os.environ/OPENAI_API_KEY

  # Anthropic
  - model_name: claude
    litellm_params:
      model: claude-3-5-sonnet-20241022
      api_key: os.environ/ANTHROPIC_API_KEY

  # 로컬 Ollama
  - model_name: local-llama
    litellm_params:
      model: ollama/llama3.2
      api_base: http://host.docker.internal:11434

general_settings:
  master_key: sk-master-1234
```

### 예제 3: Python 클라이언트

```python
from openai import OpenAI

# Proxy에 연결
client = OpenAI(
    base_url="http://localhost:4000/v1",
    api_key="dev-key-1234"
)

# 여러 모델 테스트
models = ["gpt-4", "claude", "local-llama"]

for model in models:
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": "1+1=?"}],
            max_tokens=50
        )
        print(f"{model}: {response.choices[0].message.content}")
    except Exception as e:
        print(f"{model}: 오류 - {e}")
```

---

## 문제 해결

### 자주 발생하는 문제

| 문제 | 해결 방법 |
|------|----------|
| 연결 거부 | 포트 확인, 방화벽 확인 |
| 인증 실패 | API 키 또는 master_key 확인 |
| 모델 없음 | config.yaml의 model_name 확인 |
| 타임아웃 | LLM 프로바이더 상태 확인 |

### 디버그 모드

```bash
# 상세 로그 출력
litellm --config config.yaml --detailed_debug
```

---

## 정리

| 명령어 | 설명 |
|--------|------|
| `litellm --model gpt-4o` | 단일 모델로 빠른 시작 |
| `litellm --config config.yaml` | 설정 파일로 시작 |
| `docker run ghcr.io/berriai/litellm` | Docker로 시작 |

### 다음 단계

- [[03-config-yaml|config.yaml 상세]] - 설정 파일 깊게 배우기
- [[05-load-balancing|로드 밸런싱]] - 고가용성 설정
- [[06-budget-tracking|예산 관리]] - 비용 추적 및 제한
