# LiteLLM 100+ 프로바이더 연결

## 학습 목표

- 주요 LLM 프로바이더 연결 방법 익히기
- 프로바이더별 설정 차이 이해하기
- 로컬 LLM 연결하기

---

## 프로바이더 모델 이름 규칙

```
[provider_prefix]/[model_name]

예시:
- gpt-4o                    # OpenAI (prefix 없음)
- claude-3-5-sonnet-20241022 # Anthropic (prefix 없음)
- azure/deployment-name     # Azure OpenAI
- bedrock/model-id          # AWS Bedrock
- vertex_ai/model-name      # Google Vertex AI
- ollama/model-name         # Ollama
```

---

## 주요 프로바이더 설정

### 1. OpenAI

가장 기본적인 프로바이더입니다.

```python
# Python SDK
from litellm import completion
import os

os.environ["OPENAI_API_KEY"] = "sk-xxx"

response = completion(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Hello!"}]
)
```

```yaml
# config.yaml
model_list:
  - model_name: gpt-4
    litellm_params:
      model: gpt-4o
      api_key: os.environ/OPENAI_API_KEY

  - model_name: gpt-4-turbo
    litellm_params:
      model: gpt-4-turbo
      api_key: os.environ/OPENAI_API_KEY
```

**사용 가능한 모델**: gpt-4o, gpt-4-turbo, gpt-3.5-turbo, o1-preview, o1-mini 등

---

### 2. Anthropic (Claude)

```python
# Python SDK
import os
os.environ["ANTHROPIC_API_KEY"] = "sk-ant-xxx"

response = completion(
    model="claude-3-5-sonnet-20241022",
    messages=[{"role": "user", "content": "Hello!"}]
)
```

```yaml
# config.yaml
model_list:
  - model_name: claude-sonnet
    litellm_params:
      model: claude-3-5-sonnet-20241022
      api_key: os.environ/ANTHROPIC_API_KEY

  - model_name: claude-haiku
    litellm_params:
      model: claude-3-haiku-20240307
      api_key: os.environ/ANTHROPIC_API_KEY
```

**사용 가능한 모델**: claude-3-5-sonnet-20241022, claude-3-opus-20240229, claude-3-haiku-20240307 등

---

### 3. Azure OpenAI

Azure에 배포된 OpenAI 모델을 사용합니다.

```python
# Python SDK
import os
os.environ["AZURE_API_KEY"] = "xxx"
os.environ["AZURE_API_BASE"] = "https://your-resource.openai.azure.com"
os.environ["AZURE_API_VERSION"] = "2024-02-15-preview"

response = completion(
    model="azure/your-deployment-name",
    messages=[{"role": "user", "content": "Hello!"}]
)
```

```yaml
# config.yaml
model_list:
  - model_name: gpt-4-azure
    litellm_params:
      model: azure/gpt4-deployment      # Azure 배포 이름
      api_base: https://your-resource.openai.azure.com
      api_key: os.environ/AZURE_API_KEY
      api_version: "2024-02-15-preview"
```

---

### 4. AWS Bedrock

AWS에서 제공하는 다양한 모델을 사용합니다.

```python
# Python SDK
import os
os.environ["AWS_ACCESS_KEY_ID"] = "xxx"
os.environ["AWS_SECRET_ACCESS_KEY"] = "xxx"
os.environ["AWS_REGION_NAME"] = "us-east-1"

response = completion(
    model="bedrock/anthropic.claude-3-sonnet-20240229-v1:0",
    messages=[{"role": "user", "content": "Hello!"}]
)
```

```yaml
# config.yaml
model_list:
  - model_name: bedrock-claude
    litellm_params:
      model: bedrock/anthropic.claude-3-sonnet-20240229-v1:0
      aws_access_key_id: os.environ/AWS_ACCESS_KEY_ID
      aws_secret_access_key: os.environ/AWS_SECRET_ACCESS_KEY
      aws_region_name: us-east-1

  - model_name: bedrock-llama
    litellm_params:
      model: bedrock/meta.llama3-70b-instruct-v1:0
      aws_access_key_id: os.environ/AWS_ACCESS_KEY_ID
      aws_secret_access_key: os.environ/AWS_SECRET_ACCESS_KEY
      aws_region_name: us-east-1
```

**사용 가능한 모델**: Claude, Llama, Titan, Mistral 등

---

### 5. Google Vertex AI

```python
# Python SDK
import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/path/to/service-account.json"

response = completion(
    model="vertex_ai/gemini-pro",
    messages=[{"role": "user", "content": "Hello!"}],
    vertex_project="your-project-id",
    vertex_location="us-central1"
)
```

```yaml
# config.yaml
model_list:
  - model_name: gemini
    litellm_params:
      model: vertex_ai/gemini-pro
      vertex_project: your-project-id
      vertex_location: us-central1
```

---

### 6. Ollama (로컬 LLM)

무료로 로컬에서 LLM을 실행합니다.

#### Ollama 설치 및 실행

```bash
# Ollama 설치 (macOS)
brew install ollama

# 모델 다운로드 및 실행
ollama run llama3.2
```

#### LiteLLM에서 사용

```python
# Python SDK
response = completion(
    model="ollama/llama3.2",
    messages=[{"role": "user", "content": "Hello!"}],
    api_base="http://localhost:11434"
)
```

```yaml
# config.yaml
model_list:
  - model_name: local
    litellm_params:
      model: ollama/llama3.2
      api_base: http://localhost:11434

  - model_name: local-codellama
    litellm_params:
      model: ollama/codellama
      api_base: http://localhost:11434
```

**팁**: Docker에서 Ollama 연결 시 `host.docker.internal` 사용

```yaml
api_base: http://host.docker.internal:11434
```

---

### 7. Groq

빠른 추론 속도가 특징입니다.

```python
# Python SDK
import os
os.environ["GROQ_API_KEY"] = "gsk_xxx"

response = completion(
    model="groq/llama-3.2-90b-text-preview",
    messages=[{"role": "user", "content": "Hello!"}]
)
```

```yaml
# config.yaml
model_list:
  - model_name: groq-llama
    litellm_params:
      model: groq/llama-3.2-90b-text-preview
      api_key: os.environ/GROQ_API_KEY
```

---

### 8. Together AI

다양한 오픈소스 모델을 제공합니다.

```python
import os
os.environ["TOGETHERAI_API_KEY"] = "xxx"

response = completion(
    model="together_ai/meta-llama/Llama-3.2-90B-Vision-Instruct-Turbo",
    messages=[{"role": "user", "content": "Hello!"}]
)
```

```yaml
# config.yaml
model_list:
  - model_name: together-llama
    litellm_params:
      model: together_ai/meta-llama/Llama-3.2-90B-Vision-Instruct-Turbo
      api_key: os.environ/TOGETHERAI_API_KEY
```

---

### 9. Cohere

```python
import os
os.environ["COHERE_API_KEY"] = "xxx"

response = completion(
    model="cohere_chat/command-r-plus",
    messages=[{"role": "user", "content": "Hello!"}]
)
```

```yaml
# config.yaml
model_list:
  - model_name: cohere
    litellm_params:
      model: cohere_chat/command-r-plus
      api_key: os.environ/COHERE_API_KEY
```

---

### 10. Hugging Face

```python
import os
os.environ["HUGGINGFACE_API_KEY"] = "hf_xxx"

response = completion(
    model="huggingface/microsoft/phi-2",
    messages=[{"role": "user", "content": "Hello!"}]
)
```

```yaml
# config.yaml
model_list:
  - model_name: huggingface-phi
    litellm_params:
      model: huggingface/microsoft/phi-2
      api_key: os.environ/HUGGINGFACE_API_KEY
```

---

## 멀티 프로바이더 설정

여러 프로바이더를 함께 사용하는 실전 예제:

```yaml
# multi-provider-config.yaml
model_list:
  # 고성능 (프리미엄)
  - model_name: premium
    litellm_params:
      model: gpt-4o
      api_key: os.environ/OPENAI_API_KEY

  - model_name: premium
    litellm_params:
      model: claude-3-5-sonnet-20241022
      api_key: os.environ/ANTHROPIC_API_KEY

  # 일반
  - model_name: standard
    litellm_params:
      model: gpt-3.5-turbo
      api_key: os.environ/OPENAI_API_KEY

  # 빠른 응답
  - model_name: fast
    litellm_params:
      model: groq/llama-3.2-90b-text-preview
      api_key: os.environ/GROQ_API_KEY

  # 저비용/로컬
  - model_name: local
    litellm_params:
      model: ollama/llama3.2
      api_base: http://localhost:11434

general_settings:
  master_key: os.environ/LITELLM_MASTER_KEY
```

---

## 프로바이더별 환경 변수 요약

| 프로바이더 | 환경 변수 |
|-----------|----------|
| OpenAI | `OPENAI_API_KEY` |
| Anthropic | `ANTHROPIC_API_KEY` |
| Azure | `AZURE_API_KEY`, `AZURE_API_BASE`, `AZURE_API_VERSION` |
| AWS Bedrock | `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_REGION_NAME` |
| Vertex AI | `GOOGLE_APPLICATION_CREDENTIALS` |
| Groq | `GROQ_API_KEY` |
| Together AI | `TOGETHERAI_API_KEY` |
| Cohere | `COHERE_API_KEY` |
| Hugging Face | `HUGGINGFACE_API_KEY` |

---

## 테스트 스크립트

```python
# test_providers.py
from litellm import completion
import os

# 환경 변수 설정 확인
providers = {
    "OpenAI": ("gpt-4o", "OPENAI_API_KEY"),
    "Anthropic": ("claude-3-5-sonnet-20241022", "ANTHROPIC_API_KEY"),
    "Groq": ("groq/llama-3.2-90b-text-preview", "GROQ_API_KEY"),
}

for name, (model, key) in providers.items():
    if os.environ.get(key):
        try:
            response = completion(
                model=model,
                messages=[{"role": "user", "content": "Say 'OK'"}],
                max_tokens=10
            )
            print(f"[OK] {name}: {response.choices[0].message.content}")
        except Exception as e:
            print(f"[FAIL] {name}: {e}")
    else:
        print(f"[SKIP] {name}: {key} not set")
```

---

## 정리

| 프로바이더 | 접두사 | 특징 |
|-----------|--------|------|
| OpenAI | (없음) | 기본, 가장 범용 |
| Anthropic | (없음) | 긴 컨텍스트, 안전성 |
| Azure | `azure/` | 엔터프라이즈, SLA |
| Bedrock | `bedrock/` | AWS 통합, 다양한 모델 |
| Vertex AI | `vertex_ai/` | GCP 통합, Gemini |
| Ollama | `ollama/` | 로컬, 무료 |
| Groq | `groq/` | 빠른 추론 |

### 다음 단계

- [[05-load-balancing|로드 밸런싱]] - 여러 프로바이더 조합
- [[06-budget-tracking|예산 관리]] - 비용 모니터링
