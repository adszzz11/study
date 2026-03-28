# OpenRouter 치트시트

> 빠른 참조용 핵심 정보

## 기본 설정

### Python

```python
from openai import OpenAI

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="sk-or-v1-..."
)
```

### JavaScript

```javascript
import OpenAI from 'openai';

const client = new OpenAI({
  baseURL: 'https://openrouter.ai/api/v1',
  apiKey: 'sk-or-v1-...',
});
```

### curl

```bash
curl https://openrouter.ai/api/v1/chat/completions \
  -H "Authorization: Bearer $OPENROUTER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model": "openai/gpt-4o-mini", "messages": [{"role": "user", "content": "Hi"}]}'
```

---

## 모델 ID 형식

```
{provider}/{model}:{variant}

예시:
anthropic/claude-sonnet-4          # 기본
anthropic/claude-sonnet-4:nitro    # 속도 최적화
anthropic/claude-sonnet-4:floor    # 비용 최적화
meta-llama/llama-3.1-8b:free       # 무료
```

---

## 주요 모델

| 모델 | 용도 | 가격대 |
|-----|------|-------|
| `anthropic/claude-sonnet-4` | 고성능, 코딩 | 중상 |
| `openai/gpt-4o` | 범용 | 중상 |
| `openai/gpt-4o-mini` | 가성비 | 저 |
| `anthropic/claude-3-haiku` | 빠른 응답 | 저 |
| `google/gemini-2.0-flash` | 긴 문서 | 저 |
| `meta-llama/llama-3.1-8b:free` | 무료 | 무료 |

---

## 라우팅 변형

| 변형 | 설명 | 사용 시점 |
|-----|------|----------|
| `:nitro` | 최고 속도 | 실시간 채팅 |
| `:floor` | 최저 비용 | 배치 처리 |
| `:free` | 무료 | 테스트/학습 |
| `:thinking` | 추론 강화 | 복잡한 문제 |

---

## 기본 요청

```python
response = client.chat.completions.create(
    model="openai/gpt-4o-mini",
    messages=[
        {"role": "system", "content": "시스템 프롬프트"},
        {"role": "user", "content": "사용자 메시지"}
    ],
    temperature=0.7,
    max_tokens=500
)

print(response.choices[0].message.content)
```

---

## 스트리밍

```python
stream = client.chat.completions.create(
    model="openai/gpt-4o-mini",
    messages=[{"role": "user", "content": "Hello"}],
    stream=True
)

for chunk in stream:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="")
```

---

## 이미지 분석

```python
response = client.chat.completions.create(
    model="anthropic/claude-sonnet-4",
    messages=[{
        "role": "user",
        "content": [
            {"type": "text", "text": "설명해주세요"},
            {"type": "image_url", "image_url": {"url": "https://..."}}
        ]
    }]
)
```

### Base64 이미지

```python
import base64

with open("image.png", "rb") as f:
    img_b64 = base64.b64encode(f.read()).decode()

# url: f"data:image/png;base64,{img_b64}"
```

---

## 폴백 설정

```python
response = client.chat.completions.create(
    model="anthropic/claude-sonnet-4",
    messages=[...],
    extra_body={
        "route": "fallback",
        "models": [
            "anthropic/claude-sonnet-4",
            "openai/gpt-4o",
            "openai/gpt-4o-mini"
        ]
    }
)
```

---

## JSON 모드

```python
response = client.chat.completions.create(
    model="openai/gpt-4o-mini",
    messages=[
        {"role": "system", "content": "JSON으로 응답"},
        {"role": "user", "content": "사과 정보"}
    ],
    response_format={"type": "json_object"}
)

import json
data = json.loads(response.choices[0].message.content)
```

---

## 사용량 확인

```python
# 응답에서
print(response.usage.total_tokens)

# API로 잔액 확인
import requests
r = requests.get(
    "https://openrouter.ai/api/v1/auth/key",
    headers={"Authorization": f"Bearer {api_key}"}
)
print(r.json()["data"])
```

---

## 에러 처리

```python
from openai import RateLimitError, AuthenticationError, APIError

try:
    response = client.chat.completions.create(...)
except AuthenticationError:
    print("API 키 오류")
except RateLimitError:
    print("요청 한도 초과")
except APIError as e:
    print(f"API 오류: {e}")
```

---

## 환경 변수

```bash
export OPENROUTER_API_KEY=sk-or-v1-...
```

```python
import os
api_key = os.environ.get("OPENROUTER_API_KEY")
```

---

## 비용 절약 팁

1. `:floor` 사용 - 최저가 자동 선택
2. `:free` 모델로 테스트
3. `max_tokens` 제한
4. 적절한 모델 선택 (gpt-4o-mini vs claude-sonnet-4)
5. 캐싱 활용
6. BYOK (5% 수수료)

---

## 자주 쓰는 패턴

### 대화 유지

```python
messages = [{"role": "system", "content": "..."}]

def chat(user_msg):
    messages.append({"role": "user", "content": user_msg})
    response = client.chat.completions.create(
        model="openai/gpt-4o-mini",
        messages=messages
    )
    assistant_msg = response.choices[0].message.content
    messages.append({"role": "assistant", "content": assistant_msg})
    return assistant_msg
```

### 재시도

```python
import time

def retry_chat(messages, retries=3):
    for i in range(retries):
        try:
            return client.chat.completions.create(
                model="openai/gpt-4o-mini",
                messages=messages
            )
        except RateLimitError:
            time.sleep(2 ** i)
    raise Exception("Max retries exceeded")
```

---

## 링크

- 공식 문서: [openrouter.ai/docs](https://openrouter.ai/docs)
- 모델 목록: [openrouter.ai/models](https://openrouter.ai/models)
- 상태: [status.openrouter.ai](https://status.openrouter.ai)
- Discord: [discord.gg/openrouter](https://discord.gg/openrouter)

---

## 관련 노트

- [[README|학습 가이드]]
- [[01-overview|개요]]
- [[04-learning/01-quickstart|Quick Start]]
