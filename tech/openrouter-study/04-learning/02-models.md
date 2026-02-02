# OpenRouter 모델 선택 가이드

> 500+ 모델 중 최적의 모델 찾기

## 모델 ID 형식

```
{provider}/{model-name}:{variant}

예시:
anthropic/claude-sonnet-4          # 기본
anthropic/claude-sonnet-4:floor    # 최저가 라우팅
openai/gpt-4o:nitro                # 최고 속도
meta-llama/llama-3.1-8b:free       # 무료
```

---

## 주요 모델 비교

### 프리미엄 모델 (고성능)

| 모델 | 특징 | 컨텍스트 | 추천 용도 |
|-----|------|---------|----------|
| `anthropic/claude-sonnet-4` | 최고 성능, 긴 컨텍스트 | 200K | 복잡한 분석, 코딩 |
| `openai/gpt-4o` | 범용 최고 성능 | 128K | 범용, 멀티모달 |
| `google/gemini-2.0-flash` | 빠른 응답, 긴 컨텍스트 | 1M | 긴 문서 처리 |
| `anthropic/claude-opus-4` | 최상위 성능 | 200K | 연구, 고급 분석 |

### 밸런스 모델 (성능/비용)

| 모델 | 특징 | 컨텍스트 | 추천 용도 |
|-----|------|---------|----------|
| `openai/gpt-4o-mini` | 저렴하고 빠름 | 128K | 일반 대화, 요약 |
| `anthropic/claude-3-haiku` | 빠르고 저렴 | 200K | 간단한 작업 |
| `google/gemini-1.5-flash` | 빠른 응답 | 1M | 빠른 처리 필요 |

### 무료/저가 모델

| 모델 | 특징 | 컨텍스트 | 추천 용도 |
|-----|------|---------|----------|
| `meta-llama/llama-3.1-8b:free` | 무료, 오픈소스 | 128K | 테스트, 학습 |
| `mistralai/mistral-7b:free` | 무료, 효율적 | 32K | 간단한 작업 |
| `google/gemma-2-9b:free` | 무료, Google | 8K | 실험 |

### 특화 모델

| 모델 | 특화 분야 | 추천 용도 |
|-----|----------|----------|
| `deepseek/deepseek-coder` | 코딩 | 코드 생성/분석 |
| `mistralai/codestral` | 코딩 | 코드 특화 |
| `perplexity/sonar-large` | 검색 통합 | 정보 검색 |

---

## 모델 목록 조회

### API로 조회

```python
import requests

response = requests.get("https://openrouter.ai/api/v1/models")
models = response.json()["data"]

# 모델 목록 출력
for model in models[:10]:  # 처음 10개
    print(f"{model['id']}: ${model['pricing']['prompt']}/1K tokens")
```

### 필터링 예시

```python
# Claude 모델만 필터링
claude_models = [m for m in models if "claude" in m["id"]]

# 무료 모델만 필터링
free_models = [m for m in models if ":free" in m["id"] or
               float(m["pricing"]["prompt"]) == 0]

# 컨텍스트 100K 이상 모델
long_context = [m for m in models if m["context_length"] >= 100000]
```

---

## 용도별 모델 선택

### 1. 일반 대화/챗봇

```python
# 추천: 비용 효율적인 모델
models_for_chat = [
    "openai/gpt-4o-mini",        # 가성비 최고
    "anthropic/claude-3-haiku",  # 빠르고 저렴
    "google/gemini-1.5-flash",   # 빠른 응답
]
```

### 2. 코딩/개발

```python
# 추천: 코딩 성능이 뛰어난 모델
models_for_coding = [
    "anthropic/claude-sonnet-4",  # 전반적 최고
    "deepseek/deepseek-coder",    # 코딩 특화
    "openai/gpt-4o",              # 범용 고성능
]
```

### 3. 긴 문서 처리

```python
# 추천: 긴 컨텍스트 지원 모델
models_for_long_docs = [
    "google/gemini-2.0-flash",    # 1M 토큰
    "anthropic/claude-sonnet-4",  # 200K 토큰
    "openai/gpt-4o",              # 128K 토큰
]
```

### 4. 비용 최소화

```python
# 추천: 무료 또는 저가 모델
models_for_budget = [
    "meta-llama/llama-3.1-8b:free",   # 무료
    "openai/gpt-4o-mini",             # 매우 저렴
    "anthropic/claude-3-haiku",       # 저렴
]
```

### 5. 최고 품질 (비용 무관)

```python
# 추천: 프리미엄 모델
models_for_quality = [
    "anthropic/claude-opus-4",    # 최상위
    "anthropic/claude-sonnet-4",  # 고성능
    "openai/gpt-4o",              # 범용 최고
]
```

---

## 모델 선택 실습

### 동일 프롬프트로 여러 모델 비교

```python
import os
from openai import OpenAI

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ.get("OPENROUTER_API_KEY")
)

# 테스트할 모델들
models = [
    "openai/gpt-4o-mini",
    "anthropic/claude-3-haiku",
    "meta-llama/llama-3.1-8b:free"
]

prompt = "파이썬으로 피보나치 수열을 계산하는 함수를 작성해주세요."

results = {}
for model in models:
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500
        )
        results[model] = {
            "content": response.choices[0].message.content,
            "tokens": response.usage.total_tokens
        }
        print(f"✓ {model} 완료")
    except Exception as e:
        print(f"✗ {model} 실패: {e}")

# 결과 비교
for model, result in results.items():
    print(f"\n{'='*50}")
    print(f"모델: {model}")
    print(f"토큰: {result['tokens']}")
    print(f"응답:\n{result['content'][:300]}...")
```

### 응답 시간 측정

```python
import time

def measure_response_time(model, prompt):
    start = time.time()
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=100
    )
    elapsed = time.time() - start
    return elapsed, response.usage.total_tokens

models = ["openai/gpt-4o-mini", "anthropic/claude-3-haiku"]
prompt = "1+1은?"

for model in models:
    elapsed, tokens = measure_response_time(model, prompt)
    print(f"{model}: {elapsed:.2f}초, {tokens} 토큰")
```

---

## 동적 모델 선택

### 조건에 따른 모델 선택

```python
def select_model(task_type, priority="balanced"):
    """
    task_type: "chat", "code", "analysis", "simple"
    priority: "speed", "quality", "cost", "balanced"
    """
    model_map = {
        ("chat", "speed"): "anthropic/claude-3-haiku",
        ("chat", "quality"): "anthropic/claude-sonnet-4",
        ("chat", "cost"): "openai/gpt-4o-mini",
        ("chat", "balanced"): "openai/gpt-4o-mini",

        ("code", "speed"): "anthropic/claude-3-haiku",
        ("code", "quality"): "anthropic/claude-sonnet-4",
        ("code", "cost"): "deepseek/deepseek-coder",
        ("code", "balanced"): "anthropic/claude-sonnet-4",

        ("analysis", "speed"): "google/gemini-1.5-flash",
        ("analysis", "quality"): "anthropic/claude-opus-4",
        ("analysis", "cost"): "openai/gpt-4o-mini",
        ("analysis", "balanced"): "anthropic/claude-sonnet-4",

        ("simple", "speed"): "meta-llama/llama-3.1-8b:free",
        ("simple", "quality"): "openai/gpt-4o-mini",
        ("simple", "cost"): "meta-llama/llama-3.1-8b:free",
        ("simple", "balanced"): "meta-llama/llama-3.1-8b:free",
    }

    return model_map.get((task_type, priority), "openai/gpt-4o-mini")

# 사용 예시
model = select_model("code", "quality")
print(f"선택된 모델: {model}")
```

### 토큰 수에 따른 모델 선택

```python
def select_model_by_tokens(estimated_tokens):
    """토큰 수에 따라 적절한 모델 선택"""
    if estimated_tokens > 100000:
        return "google/gemini-2.0-flash"  # 1M 컨텍스트
    elif estimated_tokens > 30000:
        return "anthropic/claude-sonnet-4"  # 200K 컨텍스트
    else:
        return "openai/gpt-4o-mini"  # 128K 컨텍스트

# 사용 예시
model = select_model_by_tokens(50000)
```

---

## 모델 가격 비교

### 주요 모델 가격 (2025년 기준, 1M 토큰당)

| 모델 | 입력 | 출력 | 비고 |
|-----|------|------|-----|
| claude-opus-4 | $15 | $75 | 최고 성능 |
| claude-sonnet-4 | $3 | $15 | 균형 |
| claude-3-haiku | $0.25 | $1.25 | 가성비 |
| gpt-4o | $2.5 | $10 | 범용 |
| gpt-4o-mini | $0.15 | $0.6 | 저렴 |
| gemini-2.0-flash | $0.1 | $0.4 | 매우 저렴 |
| llama-3.1-8b:free | $0 | $0 | 무료 |

> 가격은 변동될 수 있습니다. [openrouter.ai/models](https://openrouter.ai/models)에서 최신 가격 확인

### 비용 계산 예시

```python
def estimate_cost(model, input_tokens, output_tokens):
    """대략적인 비용 계산"""
    # 예시 가격 (실제 가격은 API 또는 웹사이트 확인)
    prices = {
        "anthropic/claude-sonnet-4": (3.0, 15.0),  # (입력, 출력) per 1M
        "openai/gpt-4o-mini": (0.15, 0.6),
        "meta-llama/llama-3.1-8b:free": (0, 0),
    }

    if model not in prices:
        return "가격 정보 없음"

    input_price, output_price = prices[model]
    cost = (input_tokens * input_price + output_tokens * output_price) / 1_000_000
    return f"${cost:.6f}"

# 사용 예시
print(estimate_cost("anthropic/claude-sonnet-4", 1000, 500))
```

---

## 핵심 요약

```
모델 선택 기준:
1. 용도 (대화, 코딩, 분석, 긴 문서)
2. 우선순위 (속도, 품질, 비용)
3. 컨텍스트 길이 필요량

추천 조합:
- 일반/테스트: gpt-4o-mini (가성비)
- 코딩: claude-sonnet-4 (성능)
- 긴 문서: gemini-2.0-flash (1M 컨텍스트)
- 무료: llama-3.1-8b:free

팁:
- 먼저 저렴한 모델로 테스트
- 필요시 고성능 모델로 업그레이드
- :floor 변형으로 비용 최적화
```

---

## 다음 단계

- [[03-openai-sdk|OpenAI SDK 심화]]
- [[04-routing-variants|라우팅 변형]]
- [[06-cost-management|비용 관리]]

---

## 관련 노트

- [[../01-overview|개요]]
- [[../03-references|참고 자료]]
- [[../cheatsheet|치트시트]]
