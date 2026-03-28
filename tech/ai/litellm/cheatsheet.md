# LiteLLM 치트시트

> 빠른 참조용 명령어 및 설정 모음

---

## 설치

```bash
# 기본 설치
pip install litellm

# 프록시 서버 포함
pip install 'litellm[proxy]'

# 버전 확인
pip show litellm
```

---

## 환경 변수

```bash
# OpenAI
export OPENAI_API_KEY="sk-xxx"

# Anthropic
export ANTHROPIC_API_KEY="sk-ant-xxx"

# Azure
export AZURE_API_KEY="xxx"
export AZURE_API_BASE="https://xxx.openai.azure.com"
export AZURE_API_VERSION="2024-02-15-preview"

# AWS Bedrock
export AWS_ACCESS_KEY_ID="xxx"
export AWS_SECRET_ACCESS_KEY="xxx"
export AWS_REGION_NAME="us-east-1"

# Groq
export GROQ_API_KEY="gsk_xxx"
```

---

## Python SDK

### 기본 호출

```python
from litellm import completion

response = completion(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Hello!"}]
)
print(response.choices[0].message.content)
```

### 스트리밍

```python
response = completion(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Hello!"}],
    stream=True
)
for chunk in response:
    print(chunk.choices[0].delta.content, end="")
```

### 비동기

```python
from litellm import acompletion
import asyncio

async def main():
    response = await acompletion(
        model="gpt-4o",
        messages=[{"role": "user", "content": "Hello!"}]
    )
    print(response.choices[0].message.content)

asyncio.run(main())
```

### 파라미터

```python
response = completion(
    model="gpt-4o",
    messages=[...],
    temperature=0.7,      # 창의성 (0-2)
    max_tokens=1000,      # 최대 출력
    timeout=30,           # 타임아웃 (초)
    num_retries=3         # 재시도 횟수
)
```

### 비용 확인

```python
cost = response._hidden_params.get("response_cost", 0)
print(f"Cost: ${cost:.6f}")
```

---

## 모델 이름 규칙

```
gpt-4o                         # OpenAI
gpt-3.5-turbo                  # OpenAI
claude-3-5-sonnet-20241022     # Anthropic
azure/deployment-name          # Azure
bedrock/anthropic.claude-v2    # AWS Bedrock
vertex_ai/gemini-pro           # Google Vertex
ollama/llama3.2                # Ollama
groq/llama-3.2-90b-text-preview # Groq
```

---

## Proxy Server

### 빠른 시작

```bash
# 단일 모델
litellm --model gpt-4o --port 4000

# config 파일
litellm --config config.yaml --port 4000
```

### Docker

```bash
docker run \
  -e OPENAI_API_KEY=sk-xxx \
  -p 4000:4000 \
  ghcr.io/berriai/litellm:main-latest \
  --model gpt-4o
```

### 클라이언트 호출

```bash
curl http://localhost:4000/v1/chat/completions \
  -H "Authorization: Bearer sk-master-key" \
  -H "Content-Type: application/json" \
  -d '{"model": "gpt-4", "messages": [{"role": "user", "content": "Hi"}]}'
```

---

## config.yaml 템플릿

### 최소 설정

```yaml
model_list:
  - model_name: gpt-4
    litellm_params:
      model: gpt-4o
      api_key: os.environ/OPENAI_API_KEY

general_settings:
  master_key: your-master-key
```

### 멀티 프로바이더

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

  - model_name: local
    litellm_params:
      model: ollama/llama3.2
      api_base: http://localhost:11434

general_settings:
  master_key: os.environ/LITELLM_MASTER_KEY
```

### 로드 밸런싱

```yaml
model_list:
  # 같은 model_name으로 여러 배포
  - model_name: gpt-4
    litellm_params:
      model: azure/gpt4-eastus
      api_base: https://eastus.openai.azure.com
      api_key: os.environ/AZURE_EASTUS_KEY

  - model_name: gpt-4
    litellm_params:
      model: azure/gpt4-westus
      api_base: https://westus.openai.azure.com
      api_key: os.environ/AZURE_WESTUS_KEY

router_settings:
  routing_strategy: least-busy
```

### 폴백

```yaml
litellm_settings:
  fallbacks:
    - main-model: [backup-model-1, backup-model-2]
```

### 예산 관리

```yaml
litellm_settings:
  max_budget: 1000.0
  budget_duration: 1mo

general_settings:
  database_url: postgresql://user:pass@host:5432/litellm
```

---

## API 엔드포인트

| 엔드포인트 | 메서드 | 설명 |
|-----------|--------|------|
| `/v1/chat/completions` | POST | 채팅 완성 |
| `/v1/models` | GET | 모델 목록 |
| `/health` | GET | 헬스체크 |
| `/key/generate` | POST | 가상 키 생성 |
| `/key/info` | GET | 키 정보 조회 |
| `/spend/logs` | GET | 사용량 조회 |

---

## 가상 키

### 생성

```bash
curl -X POST http://localhost:4000/key/generate \
  -H "Authorization: Bearer MASTER_KEY" \
  -d '{
    "max_budget": 100.0,
    "models": ["gpt-4", "gpt-3.5"],
    "duration": "30d"
  }'
```

### 조회

```bash
curl http://localhost:4000/key/info \
  -H "Authorization: Bearer YOUR_KEY"
```

---

## 라우팅 전략

| 전략 | 설명 |
|------|------|
| `simple` | 라운드 로빈 (기본) |
| `least-busy` | 가장 여유 있는 배포 |
| `latency-based-routing` | 가장 빠른 응답 |
| `cost-based-routing` | 가장 저렴한 모델 |

---

## 에러 처리

```python
from litellm.exceptions import (
    AuthenticationError,   # 인증 실패
    RateLimitError,        # 한도 초과
    APIConnectionError,    # 연결 실패
    Timeout               # 타임아웃
)
```

---

## 유용한 명령어

```bash
# 버전 확인
litellm --version

# 디버그 모드
litellm --config config.yaml --detailed_debug

# 모델 목록 확인
curl http://localhost:4000/v1/models

# 헬스체크
curl http://localhost:4000/health
```

---

## 참고 링크

- 공식 문서: https://docs.litellm.ai
- GitHub: https://github.com/BerriAI/litellm
- PyPI: https://pypi.org/project/litellm

---

## 빠른 시작 코드

```python
# 복사해서 바로 사용
from litellm import completion
import os

os.environ["OPENAI_API_KEY"] = "sk-xxx"

response = completion(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello!"}
    ]
)
print(response.choices[0].message.content)
```

---

## 트러블슈팅

| 문제 | 해결 |
|------|------|
| `AuthenticationError` | API 키 확인 |
| `RateLimitError` | 재시도 또는 다른 프로바이더 |
| `APIConnectionError` | 네트워크, URL 확인 |
| 모델 없음 | model_name 철자 확인 |
| config 오류 | YAML 문법 검사 |
