# OpenRouter 비용 관리

> 크레딧 관리, BYOK, 비용 최적화 전략

## 가격 모델

### 1. 기본 Pay-as-you-go

```
OpenRouter 크레딧 구매 → 사용한 만큼 차감

특징:
- 최소 충전: $5
- 마진 포함 가격 (직접 호출보다 약간 높음)
- 간편한 결제
- 모든 모델 즉시 사용 가능
```

### 2. BYOK (Bring Your Own Key)

```
자신의 API 키 등록 → OpenRouter 경유 → 5% 수수료

특징:
- 원본 가격 + 5% 수수료
- 기존 API 키 활용
- 기업 계정/할인 유지 가능
```

---

## 크레딧 관리

### 잔액 확인 (API)

```python
import requests
import os

def check_balance():
    """크레딧 잔액 확인"""
    response = requests.get(
        "https://openrouter.ai/api/v1/auth/key",
        headers={
            "Authorization": f"Bearer {os.environ['OPENROUTER_API_KEY']}"
        }
    )

    data = response.json()["data"]
    return {
        "limit": data.get("limit"),         # 충전된 총액
        "usage": data.get("usage"),          # 사용량
        "remaining": data.get("limit", 0) - data.get("usage", 0)  # 잔액
    }

# 사용
balance = check_balance()
print(f"잔액: ${balance['remaining']:.4f}")
```

### 사용량 추적

```python
def track_usage(response) -> dict:
    """응답에서 사용량 추출"""
    usage = response.usage

    return {
        "prompt_tokens": usage.prompt_tokens,
        "completion_tokens": usage.completion_tokens,
        "total_tokens": usage.total_tokens,
        "model": response.model
    }

# 사용 예시
response = client.chat.completions.create(
    model="openai/gpt-4o-mini",
    messages=[{"role": "user", "content": "Hello"}]
)

usage = track_usage(response)
print(f"총 토큰: {usage['total_tokens']}")
```

### 비용 계산기

```python
# 모델별 가격 (1M 토큰당, 2025년 기준)
PRICES = {
    "anthropic/claude-sonnet-4": {"input": 3.0, "output": 15.0},
    "anthropic/claude-opus-4": {"input": 15.0, "output": 75.0},
    "anthropic/claude-3-haiku": {"input": 0.25, "output": 1.25},
    "openai/gpt-4o": {"input": 2.5, "output": 10.0},
    "openai/gpt-4o-mini": {"input": 0.15, "output": 0.6},
    "google/gemini-2.0-flash": {"input": 0.1, "output": 0.4},
    "meta-llama/llama-3.1-8b:free": {"input": 0, "output": 0},
}

def estimate_cost(model: str, input_tokens: int, output_tokens: int) -> float:
    """비용 추정"""
    if model not in PRICES:
        return -1  # 가격 정보 없음

    price = PRICES[model]
    cost = (input_tokens * price["input"] + output_tokens * price["output"]) / 1_000_000
    return cost

def calculate_cost(response) -> float:
    """실제 응답에서 비용 계산"""
    model = response.model
    usage = response.usage

    return estimate_cost(model, usage.prompt_tokens, usage.completion_tokens)

# 사용
cost = calculate_cost(response)
print(f"예상 비용: ${cost:.6f}")
```

---

## BYOK 설정

### BYOK란?

**Bring Your Own Key** - 자신의 API 키를 OpenRouter에 등록하여 사용

```
장점:
- 원본 가격 + 5% 수수료 (마진 대신)
- 기업 할인/계약 유지
- 기존 크레딧 활용

단점:
- 각 제공자별로 API 키 필요
- 키 관리 복잡성 증가
```

### 설정 방법

1. [openrouter.ai](https://openrouter.ai) 로그인
2. Settings → API Keys
3. "Add Provider Key" 클릭
4. 제공자 선택 (Anthropic, OpenAI 등)
5. API 키 입력
6. 저장

### BYOK 사용

```python
# BYOK 설정 후 동일하게 사용
# OpenRouter가 자동으로 등록된 키 사용

response = client.chat.completions.create(
    model="anthropic/claude-sonnet-4",  # BYOK 키가 있으면 자동 사용
    messages=[{"role": "user", "content": "Hello"}]
)
```

### 제공자 우선순위 지정

```python
response = client.chat.completions.create(
    model="anthropic/claude-sonnet-4",
    messages=[{"role": "user", "content": "Hello"}],
    extra_body={
        "provider": {
            "order": ["Anthropic"],  # BYOK 키가 있는 제공자 우선
            "allow_fallbacks": True
        }
    }
)
```

---

## 비용 최적화 전략

### 1. 모델 선택 최적화

```python
def select_cost_effective_model(task_complexity: str) -> str:
    """작업 복잡도에 따른 모델 선택"""
    models = {
        "simple": "meta-llama/llama-3.1-8b:free",      # 무료
        "basic": "openai/gpt-4o-mini",                 # $0.15/1M
        "standard": "anthropic/claude-3-haiku",        # $0.25/1M
        "complex": "anthropic/claude-sonnet-4",        # $3/1M
        "expert": "anthropic/claude-opus-4"            # $15/1M
    }
    return models.get(task_complexity, models["basic"])

# 사용
model = select_cost_effective_model("basic")
```

### 2. :floor 변형 활용

```python
# 최저가 제공자 자동 선택
response = client.chat.completions.create(
    model="anthropic/claude-sonnet-4:floor",
    messages=[{"role": "user", "content": "Hello"}]
)
```

### 3. 토큰 절약

```python
# 시스템 프롬프트 최적화
short_system = "간결하게 답변하세요."  # vs 긴 프롬프트

# max_tokens 제한
response = client.chat.completions.create(
    model="openai/gpt-4o-mini",
    messages=[{"role": "user", "content": "요약해줘"}],
    max_tokens=200  # 응답 길이 제한
)

# 불필요한 컨텍스트 제거
def trim_conversation(messages, max_messages=10):
    """대화 기록 제한"""
    if len(messages) > max_messages:
        # 시스템 메시지 + 최근 대화만 유지
        return [messages[0]] + messages[-(max_messages-1):]
    return messages
```

### 4. 캐싱 활용

```python
import hashlib
import json

# 간단한 메모리 캐시
_cache = {}

def cached_completion(model: str, messages: list, **kwargs):
    """동일 요청 캐싱"""
    # 캐시 키 생성
    cache_key = hashlib.md5(
        json.dumps({"model": model, "messages": messages}, sort_keys=True).encode()
    ).hexdigest()

    if cache_key in _cache:
        print("캐시 히트!")
        return _cache[cache_key]

    response = client.chat.completions.create(
        model=model,
        messages=messages,
        **kwargs
    )

    _cache[cache_key] = response
    return response
```

### 5. 배치 처리

```python
import asyncio
from openai import AsyncOpenAI

async_client = AsyncOpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ["OPENROUTER_API_KEY"]
)

async def batch_process(prompts: list, model: str = "openai/gpt-4o-mini"):
    """여러 프롬프트 동시 처리"""
    tasks = [
        async_client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}]
        )
        for prompt in prompts
    ]

    responses = await asyncio.gather(*tasks)
    return [r.choices[0].message.content for r in responses]

# 사용
prompts = ["질문1", "질문2", "질문3"]
results = asyncio.run(batch_process(prompts))
```

---

## 예산 관리

### 일일/월간 한도 설정

```python
import datetime

class BudgetManager:
    def __init__(self, daily_limit: float = 10.0, monthly_limit: float = 100.0):
        self.daily_limit = daily_limit
        self.monthly_limit = monthly_limit
        self.daily_usage = 0.0
        self.monthly_usage = 0.0
        self.last_reset = datetime.date.today()

    def check_budget(self, estimated_cost: float) -> bool:
        """예산 확인"""
        today = datetime.date.today()

        # 일일 리셋
        if today > self.last_reset:
            self.daily_usage = 0.0
            self.last_reset = today

            # 월간 리셋
            if today.day == 1:
                self.monthly_usage = 0.0

        # 예산 체크
        if self.daily_usage + estimated_cost > self.daily_limit:
            print(f"일일 한도 초과: ${self.daily_usage:.2f}/{self.daily_limit:.2f}")
            return False

        if self.monthly_usage + estimated_cost > self.monthly_limit:
            print(f"월간 한도 초과: ${self.monthly_usage:.2f}/{self.monthly_limit:.2f}")
            return False

        return True

    def record_usage(self, cost: float):
        """사용량 기록"""
        self.daily_usage += cost
        self.monthly_usage += cost

# 사용
budget = BudgetManager(daily_limit=5.0, monthly_limit=50.0)

def chat_with_budget(messages, model="openai/gpt-4o-mini"):
    # 예상 비용 계산 (대략적)
    estimated_tokens = sum(len(m["content"]) / 4 for m in messages) + 100
    estimated_cost = estimate_cost(model, int(estimated_tokens), 100)

    if not budget.check_budget(estimated_cost):
        return "예산 초과로 요청을 처리할 수 없습니다."

    response = client.chat.completions.create(
        model=model,
        messages=messages
    )

    actual_cost = calculate_cost(response)
    budget.record_usage(actual_cost)

    return response.choices[0].message.content
```

### 알림 설정

```python
def check_and_alert(threshold: float = 0.8):
    """크레딧 잔액 경고"""
    balance = check_balance()

    if balance["limit"] > 0:
        usage_ratio = balance["usage"] / balance["limit"]

        if usage_ratio >= threshold:
            print(f"경고: 크레딧 {usage_ratio*100:.1f}% 사용됨!")
            print(f"잔액: ${balance['remaining']:.2f}")
            return True

    return False
```

---

## 비용 분석

### 사용량 로깅

```python
import csv
from datetime import datetime

class UsageLogger:
    def __init__(self, log_file: str = "usage_log.csv"):
        self.log_file = log_file

    def log(self, model: str, tokens: int, cost: float, purpose: str = ""):
        """사용량 로깅"""
        with open(self.log_file, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([
                datetime.now().isoformat(),
                model,
                tokens,
                f"{cost:.6f}",
                purpose
            ])

    def get_summary(self) -> dict:
        """사용량 요약"""
        total_cost = 0
        model_usage = {}

        try:
            with open(self.log_file, "r") as f:
                reader = csv.reader(f)
                for row in reader:
                    _, model, tokens, cost, _ = row
                    total_cost += float(cost)
                    model_usage[model] = model_usage.get(model, 0) + int(tokens)
        except FileNotFoundError:
            pass

        return {
            "total_cost": total_cost,
            "model_usage": model_usage
        }

# 사용
logger = UsageLogger()

def chat_with_logging(messages, model, purpose=""):
    response = client.chat.completions.create(
        model=model,
        messages=messages
    )

    cost = calculate_cost(response)
    logger.log(model, response.usage.total_tokens, cost, purpose)

    return response.choices[0].message.content
```

---

## 모델별 비용 비교 (2025년 기준)

### 가격표 (1M 토큰당)

| 모델 | 입력 | 출력 | 월 100K 요청 예상 |
|-----|------|------|----------------|
| claude-opus-4 | $15 | $75 | ~$900 |
| claude-sonnet-4 | $3 | $15 | ~$180 |
| claude-3-haiku | $0.25 | $1.25 | ~$15 |
| gpt-4o | $2.5 | $10 | ~$125 |
| gpt-4o-mini | $0.15 | $0.6 | ~$7.5 |
| gemini-2.0-flash | $0.1 | $0.4 | ~$5 |
| llama-3.1-8b:free | $0 | $0 | $0 |

> 가격은 변동될 수 있습니다. [openrouter.ai/models](https://openrouter.ai/models) 확인

### 비용 시뮬레이션

```python
def simulate_monthly_cost(
    daily_requests: int,
    avg_input_tokens: int = 500,
    avg_output_tokens: int = 200,
    model: str = "openai/gpt-4o-mini"
) -> dict:
    """월간 비용 시뮬레이션"""
    price = PRICES.get(model, {"input": 0, "output": 0})

    daily_cost = (
        daily_requests * avg_input_tokens * price["input"] / 1_000_000 +
        daily_requests * avg_output_tokens * price["output"] / 1_000_000
    )

    return {
        "model": model,
        "daily_requests": daily_requests,
        "daily_cost": daily_cost,
        "monthly_cost": daily_cost * 30,
        "yearly_cost": daily_cost * 365
    }

# 사용
sim = simulate_monthly_cost(1000, model="openai/gpt-4o-mini")
print(f"월간 예상 비용: ${sim['monthly_cost']:.2f}")
```

---

## 핵심 요약

```
비용 최적화 체크리스트:
1. 적절한 모델 선택 (작업 복잡도에 맞게)
2. :floor 변형으로 최저가 라우팅
3. :free 모델로 테스트/개발
4. max_tokens 제한
5. 캐싱 활용
6. BYOK로 5% 절약 (고볼륨)

예산 관리:
- 일일/월간 한도 설정
- 사용량 로깅 및 모니터링
- 잔액 경고 설정

비용 순위 (저 → 고):
:free < gpt-4o-mini < gemini-flash < haiku < sonnet < gpt-4o < opus
```

---

## 다음 단계

- [[../05-projects|실전 프로젝트]]
- [[../cheatsheet|치트시트]]

---

## 관련 노트

- [[02-models|모델 선택]]
- [[04-routing-variants|라우팅 변형]]
- [[../01-overview|개요]]
