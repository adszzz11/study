# LiteLLM 개요

## LiteLLM이란?

LiteLLM은 100개 이상의 LLM(대규모 언어 모델) 프로바이더를 **단일 API**로 통합하는 오픈소스 프로젝트입니다. OpenAI API 형식을 표준으로 사용하여 어떤 LLM이든 동일한 방식으로 호출할 수 있습니다.

```python
# OpenAI, Anthropic, Ollama 모두 같은 방식으로 호출
from litellm import completion

# OpenAI
completion(model="gpt-4o", messages=[...])

# Anthropic
completion(model="claude-3-5-sonnet-20241022", messages=[...])

# Ollama (로컬)
completion(model="ollama/llama3.2", messages=[...])
```

---

## 핵심 개념

### 1. 두 가지 사용 방식

#### Python SDK
```python
# 애플리케이션에 직접 임베드
from litellm import completion

response = completion(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Hello!"}]
)
```

#### Proxy Server
```bash
# 독립 서버로 실행 → OpenAI 호환 엔드포인트 제공
litellm --config config.yaml --port 4000

# 클라이언트에서 호출
curl http://localhost:4000/v1/chat/completions \
  -H "Authorization: Bearer sk-xxx" \
  -d '{"model": "gpt-4o", "messages": [...]}'
```

### 2. 모델 이름 규칙

```
[provider]/[model-name]

예시:
- gpt-4o                    → OpenAI (기본)
- claude-3-5-sonnet-20241022 → Anthropic
- azure/gpt-4o-deployment   → Azure OpenAI
- bedrock/anthropic.claude-v2 → AWS Bedrock
- ollama/llama3.2           → Ollama (로컬)
```

### 3. OpenAI 호환성

LiteLLM은 모든 응답을 OpenAI 형식으로 변환합니다:

```python
{
    "id": "chatcmpl-xxx",
    "object": "chat.completion",
    "created": 1234567890,
    "model": "gpt-4o",
    "choices": [{
        "index": 0,
        "message": {
            "role": "assistant",
            "content": "응답 내용"
        },
        "finish_reason": "stop"
    }],
    "usage": {
        "prompt_tokens": 10,
        "completion_tokens": 20,
        "total_tokens": 30
    }
}
```

---

## 주요 기능

### 통합 API
- 100+ 프로바이더 지원
- 동일한 코드로 모든 LLM 호출
- 응답 형식 자동 변환

### 로드 밸런싱 & 폴백
```yaml
model_list:
  - model_name: gpt-4
    litellm_params:
      model: gpt-4o
      api_key: key1
  - model_name: gpt-4
    litellm_params:
      model: azure/gpt-4
      api_key: key2
# 자동으로 두 모델 간 로드 밸런싱
```

### 비용 추적
```python
from litellm import completion

response = completion(model="gpt-4o", messages=[...])

# 비용 정보 확인
print(response._hidden_params["response_cost"])
```

### 가상 키 관리
- 팀/프로젝트별 API 키 발급
- 키별 예산 제한 설정
- 사용량 모니터링

### 스트리밍 지원
```python
response = completion(
    model="gpt-4o",
    messages=[{"role": "user", "content": "긴 이야기를 해주세요"}],
    stream=True
)

for chunk in response:
    print(chunk.choices[0].delta.content, end="")
```

---

## 장점

| 장점 | 설명 |
|------|------|
| **벤더 락인 방지** | 언제든 다른 프로바이더로 전환 가능 |
| **코드 단순화** | 하나의 API로 모든 LLM 통합 |
| **비용 최적화** | 자동 폴백으로 비용/성능 최적화 |
| **셀프호스팅** | 데이터 주권 확보, 내부 네트워크에서 운영 |
| **관찰성** | 비용 추적, 로깅, 모니터링 내장 |
| **확장성** | 프록시 서버로 대규모 트래픽 처리 |

---

## 단점 및 고려사항

| 단점 | 대응 방안 |
|------|----------|
| **추가 레이어** | 레이턴시 증가 (보통 <50ms) |
| **프로바이더 특수 기능** | 일부 기능은 직접 SDK 사용 필요 |
| **학습 곡선** | 설정 파일 문법 익혀야 함 |
| **버전 관리** | 프로바이더 API 변경 시 업데이트 필요 |

---

## 사용 사례

### 1. 스타트업 MVP
```
문제: 여러 LLM을 테스트하고 싶지만 각각 SDK 연동이 번거로움
해결: LiteLLM으로 통합, 모델만 바꿔서 A/B 테스트
```

### 2. 엔터프라이즈 API 게이트웨이
```
문제: 팀별로 다른 LLM을 사용, 비용 관리가 어려움
해결: LiteLLM Proxy로 중앙 관리, 팀별 가상 키와 예산 할당
```

### 3. 고가용성 서비스
```
문제: OpenAI 장애 시 서비스 중단
해결: Azure OpenAI를 폴백으로 설정, 자동 전환
```

### 4. 로컬 개발 환경
```
문제: API 비용을 줄이면서 개발/테스트하고 싶음
해결: 개발은 Ollama, 프로덕션은 GPT-4로 모델만 전환
```

### 5. 멀티 클라우드 전략
```
문제: 특정 클라우드에 의존하고 싶지 않음
해결: AWS Bedrock, Azure, GCP Vertex AI를 모두 설정
```

---

## 아키텍처

### Python SDK 방식
```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│ Application │────▶│   LiteLLM   │────▶│ LLM Provider│
│  (Python)   │     │   Library   │     │             │
└─────────────┘     └─────────────┘     └─────────────┘
```

### Proxy Server 방식
```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Client    │     │   LiteLLM   │     │ LLM Provider│
│ (Any Lang)  │────▶│   Proxy     │────▶│             │
└─────────────┘     │   Server    │     └─────────────┘
                    │             │     ┌─────────────┐
                    │  - Auth     │────▶│ LLM Provider│
                    │  - Rate     │     │             │
                    │  - Budget   │     └─────────────┘
                    └─────────────┘
```

---

## 시작하기

```bash
# 설치
pip install litellm

# 환경 변수 설정
export OPENAI_API_KEY=sk-xxx

# SDK로 바로 사용
python -c "
from litellm import completion
r = completion(model='gpt-4o', messages=[{'role':'user','content':'Hi'}])
print(r.choices[0].message.content)
"

# 또는 프록시 서버 실행
litellm --model gpt-4o --port 4000
```

---

## 다음 단계

- [[02-ecosystem|에코시스템]] - 관련 기술과 비교
- [[04-learning/01-python-sdk|Python SDK 실습]] - 코드로 배우기
- [[04-learning/02-proxy-server|프록시 서버 설정]] - 서버 모드 사용
