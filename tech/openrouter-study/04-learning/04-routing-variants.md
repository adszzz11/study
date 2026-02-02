# OpenRouter 라우팅 변형

> :nitro, :floor, :free, :thinking으로 속도/비용/기능 최적화

## 라우팅 변형이란?

모델 ID 뒤에 콜론(`:`)과 변형 이름을 붙여 **라우팅 방식을 변경**할 수 있습니다.

```
{provider}/{model}:{variant}

예시:
anthropic/claude-sonnet-4:nitro    # 최고 속도
anthropic/claude-sonnet-4:floor    # 최저 비용
meta-llama/llama-3.1-8b:free       # 무료
anthropic/claude-sonnet-4:thinking # 추론 강화
```

---

## 변형 종류

| 변형 | 목적 | 특징 | 가격 |
|-----|------|------|-----|
| `:nitro` | 최고 속도 | 빠른 응답, 프리미엄 인프라 | 더 비쌈 |
| `:floor` | 최저 비용 | 가장 저렴한 제공자 선택 | 가장 저렴 |
| `:free` | 무료 | 레이트 제한 있음 | 무료 |
| `:thinking` | 추론 강화 | 복잡한 문제 해결 | 모델별 상이 |

---

## :nitro - 최고 속도

### 개념
- **빠른 응답이 필요할 때** 사용
- 프리미엄 인프라 활용
- 실시간 채팅, 자동완성 등에 적합

### 사용법

```python
from openai import OpenAI

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="sk-or-v1-..."
)

# :nitro로 빠른 응답
response = client.chat.completions.create(
    model="anthropic/claude-sonnet-4:nitro",
    messages=[{"role": "user", "content": "빠른 응답이 필요해요!"}]
)
```

### 적합한 상황
- 실시간 채팅 애플리케이션
- 코드 자동완성
- 타이핑 중 제안
- 낮은 레이턴시가 중요한 UX

### 주의사항
- 일반 요청보다 **비용이 높음**
- 모든 모델에서 지원되지 않을 수 있음

---

## :floor - 최저 비용

### 개념
- **같은 모델의 가장 저렴한 제공자** 자동 선택
- 여러 제공자 중 최저가로 라우팅
- 비용 최적화가 중요할 때 사용

### 사용법

```python
# :floor로 최저가 라우팅
response = client.chat.completions.create(
    model="anthropic/claude-sonnet-4:floor",
    messages=[{"role": "user", "content": "비용을 아끼고 싶어요"}]
)

# 응답에서 실제 사용된 제공자 확인
print(f"실제 모델: {response.model}")
```

### 작동 방식

```
요청: claude-sonnet-4:floor
       ↓
OpenRouter 라우터:
  - Anthropic Direct: $3/1M
  - AWS Bedrock: $2.8/1M    ← 선택 (최저가)
  - Azure OpenAI: $3.2/1M
       ↓
AWS Bedrock으로 라우팅
```

### 적합한 상황
- 배치 처리
- 백그라운드 작업
- 속도보다 비용이 중요한 경우
- 대량 처리

### 주의사항
- 응답 시간이 더 길어질 수 있음
- 제공자마다 미세한 동작 차이 가능

---

## :free - 무료

### 개념
- **완전 무료로 사용** 가능
- 레이트 제한 (Rate Limit) 있음
- 테스트, 학습용으로 적합

### 사용법

```python
# 무료 모델 사용
response = client.chat.completions.create(
    model="meta-llama/llama-3.1-8b:free",
    messages=[{"role": "user", "content": "무료로 테스트!"}]
)
```

### 무료 모델 목록 (2025년 기준)

```python
free_models = [
    "meta-llama/llama-3.1-8b:free",
    "meta-llama/llama-3.2-3b:free",
    "mistralai/mistral-7b:free",
    "google/gemma-2-9b:free",
    "qwen/qwen-2-7b:free"
]
```

### 레이트 제한

| 제한 유형 | 일반적인 값 |
|----------|-----------|
| 분당 요청 수 | 10-20 |
| 일일 요청 수 | 50-200 |
| 최대 토큰 | 4K-8K |

### 적합한 상황
- 학습 및 실험
- 프로토타이핑
- 개인 프로젝트
- API 테스트

### 주의사항
- 프로덕션에는 부적합
- 레이트 제한으로 중단될 수 있음
- 응답 품질이 유료 모델보다 낮을 수 있음

---

## :thinking - 추론 강화

### 개념
- **복잡한 추론이 필요한 문제**에 특화
- 모델이 "생각하는 과정"을 거침
- 수학, 논리, 코딩 문제에 효과적

### 사용법

```python
# :thinking으로 추론 강화
response = client.chat.completions.create(
    model="anthropic/claude-sonnet-4:thinking",
    messages=[{
        "role": "user",
        "content": "다음 수학 문제를 풀어주세요: 1부터 100까지의 합은?"
    }]
)
```

### 적합한 상황
- 수학 문제
- 논리 퍼즐
- 복잡한 코딩 문제
- 다단계 추론이 필요한 분석

### 주의사항
- 응답 시간이 더 길 수 있음
- 토큰 사용량이 증가할 수 있음
- 모든 모델에서 지원되지 않음

---

## 변형 비교 실습

### 속도 비교

```python
import time

models = [
    "anthropic/claude-sonnet-4",        # 기본
    "anthropic/claude-sonnet-4:nitro",  # 속도 최적화
    "anthropic/claude-sonnet-4:floor",  # 비용 최적화
]

prompt = "안녕하세요!"

for model in models:
    start = time.time()
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=50
    )
    elapsed = time.time() - start
    print(f"{model}: {elapsed:.2f}초")
```

### 동적 변형 선택

```python
def select_variant(priority: str, model: str) -> str:
    """
    priority: "speed", "cost", "free", "reasoning"
    """
    variant_map = {
        "speed": ":nitro",
        "cost": ":floor",
        "free": ":free",
        "reasoning": ":thinking"
    }

    variant = variant_map.get(priority, "")
    return f"{model}{variant}"

# 사용 예시
model = select_variant("cost", "anthropic/claude-sonnet-4")
print(f"선택된 모델: {model}")  # anthropic/claude-sonnet-4:floor
```

### 폴백과 함께 사용

```python
def chat_optimized(prompt, priority="balanced"):
    """우선순위에 따른 최적화된 채팅"""

    if priority == "speed":
        # 속도 우선: nitro 시도 → 일반
        models = [
            "anthropic/claude-sonnet-4:nitro",
            "anthropic/claude-sonnet-4"
        ]
    elif priority == "cost":
        # 비용 우선: free → floor → 일반
        models = [
            "meta-llama/llama-3.1-8b:free",
            "anthropic/claude-sonnet-4:floor",
            "openai/gpt-4o-mini"
        ]
    else:
        # 균형: 일반 모델
        models = ["anthropic/claude-sonnet-4", "openai/gpt-4o"]

    for model in models:
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}]
            )
            return {
                "model": response.model,
                "content": response.choices[0].message.content
            }
        except Exception as e:
            print(f"{model} 실패: {e}")
            continue

    raise Exception("모든 모델 실패")

# 사용
result = chat_optimized("Hello!", priority="cost")
print(f"사용된 모델: {result['model']}")
```

---

## 실전 패턴

### 1. 개발 vs 프로덕션

```python
import os

def get_model(base_model: str) -> str:
    env = os.environ.get("ENVIRONMENT", "development")

    if env == "development":
        # 개발: 무료 또는 저가
        if "llama" in base_model or "mistral" in base_model:
            return f"{base_model}:free"
        return f"{base_model}:floor"
    else:
        # 프로덕션: 기본 또는 nitro
        return base_model

model = get_model("anthropic/claude-sonnet-4")
```

### 2. 사용자 티어별

```python
def get_model_for_user(user_tier: str) -> str:
    tier_models = {
        "free": "meta-llama/llama-3.1-8b:free",
        "basic": "openai/gpt-4o-mini:floor",
        "premium": "anthropic/claude-sonnet-4",
        "enterprise": "anthropic/claude-sonnet-4:nitro"
    }
    return tier_models.get(user_tier, tier_models["basic"])
```

### 3. 작업 유형별

```python
def get_model_for_task(task_type: str) -> str:
    task_models = {
        "quick_chat": "openai/gpt-4o-mini:nitro",      # 빠른 응답
        "analysis": "anthropic/claude-sonnet-4:thinking",  # 깊은 분석
        "batch": "anthropic/claude-sonnet-4:floor",    # 대량 처리
        "test": "meta-llama/llama-3.1-8b:free"         # 테스트
    }
    return task_models.get(task_type, "openai/gpt-4o-mini")
```

---

## 변형 지원 확인

### 모델별 지원 변형 확인

```python
import requests

def check_variants(model_id: str):
    response = requests.get("https://openrouter.ai/api/v1/models")
    models = response.json()["data"]

    # 해당 모델의 변형 찾기
    variants = [m["id"] for m in models if model_id in m["id"]]
    return variants

# 사용
variants = check_variants("claude-sonnet-4")
print(variants)
# ['anthropic/claude-sonnet-4', 'anthropic/claude-sonnet-4:nitro', ...]
```

---

## 핵심 요약

```
변형 종류:
:nitro    - 속도 최적화 (비용 ↑)
:floor    - 비용 최적화 (속도 ↓)
:free     - 무료 (제한 있음)
:thinking - 추론 강화 (시간 ↑)

선택 가이드:
- 실시간 채팅 → :nitro
- 배치 처리 → :floor
- 테스트/학습 → :free
- 복잡한 문제 → :thinking

사용법:
model="provider/model:variant"
```

---

## 다음 단계

- [[05-multimodal|멀티모달]]
- [[06-cost-management|비용 관리]]
- [[../05-projects|실전 프로젝트]]

---

## 관련 노트

- [[02-models|모델 선택]]
- [[03-openai-sdk|OpenAI SDK]]
- [[../cheatsheet|치트시트]]
