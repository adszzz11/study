# OpenAI SDK로 OpenRouter 사용하기

> 기존 OpenAI 코드를 OpenRouter로 쉽게 마이그레이션

## 핵심 개념

OpenRouter는 OpenAI API와 100% 호환됩니다. 기존 OpenAI SDK 코드에서 **두 가지만 변경**하면 됩니다:

1. `base_url` → `https://openrouter.ai/api/v1`
2. `api_key` → OpenRouter API 키

---

## 마이그레이션 가이드

### Before (OpenAI 직접 사용)

```python
from openai import OpenAI

client = OpenAI(
    api_key="sk-..."  # OpenAI API 키
)

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Hello"}]
)
```

### After (OpenRouter 사용)

```python
from openai import OpenAI

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",  # 추가
    api_key="sk-or-v1-..."                    # OpenRouter 키로 변경
)

response = client.chat.completions.create(
    model="openai/gpt-4o",  # provider/ 접두사 추가
    messages=[{"role": "user", "content": "Hello"}]
)
```

---

## Python 설정

### 기본 설정

```python
import os
from openai import OpenAI

# 환경 변수에서 API 키 로드
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ.get("OPENROUTER_API_KEY")
)
```

### 헤더 추가 (선택)

```python
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ.get("OPENROUTER_API_KEY"),
    default_headers={
        "HTTP-Referer": "https://myapp.com",  # 앱 URL (분석용)
        "X-Title": "My Application"            # 앱 이름 (분석용)
    }
)
```

---

## JavaScript/TypeScript 설정

### Node.js

```javascript
import OpenAI from 'openai';

const client = new OpenAI({
  baseURL: 'https://openrouter.ai/api/v1',
  apiKey: process.env.OPENROUTER_API_KEY,
  defaultHeaders: {
    'HTTP-Referer': 'https://myapp.com',
    'X-Title': 'My Application',
  },
});

async function main() {
  const response = await client.chat.completions.create({
    model: 'anthropic/claude-sonnet-4',
    messages: [{ role: 'user', content: 'Hello!' }],
  });

  console.log(response.choices[0].message.content);
}

main();
```

### 브라우저 (주의: API 키 노출 위험)

```javascript
// 주의: 프로덕션에서는 서버 사이드 사용 권장
import OpenAI from 'openai';

const client = new OpenAI({
  baseURL: 'https://openrouter.ai/api/v1',
  apiKey: 'sk-or-v1-...',
  dangerouslyAllowBrowser: true, // 브라우저 사용 허용
});
```

---

## 주요 기능 사용

### 1. 채팅 완성

```python
response = client.chat.completions.create(
    model="anthropic/claude-sonnet-4",
    messages=[
        {"role": "system", "content": "당신은 친절한 AI 어시스턴트입니다."},
        {"role": "user", "content": "오늘 기분이 어때요?"}
    ],
    temperature=0.7,
    max_tokens=500
)

print(response.choices[0].message.content)
```

### 2. 스트리밍

```python
stream = client.chat.completions.create(
    model="anthropic/claude-sonnet-4",
    messages=[{"role": "user", "content": "긴 이야기를 들려주세요"}],
    stream=True
)

for chunk in stream:
    content = chunk.choices[0].delta.content
    if content:
        print(content, end="", flush=True)
```

### 3. 대화 기록 유지

```python
conversation = [
    {"role": "system", "content": "당신은 수학 튜터입니다."}
]

def chat(user_message):
    conversation.append({"role": "user", "content": user_message})

    response = client.chat.completions.create(
        model="openai/gpt-4o-mini",
        messages=conversation
    )

    assistant_message = response.choices[0].message.content
    conversation.append({"role": "assistant", "content": assistant_message})

    return assistant_message

# 사용
print(chat("1+1은?"))
print(chat("그럼 2+2는?"))
print(chat("방금 내가 뭘 물어봤지?"))
```

### 4. 함수 호출 (Function Calling)

```python
import json

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "주어진 위치의 날씨를 가져옵니다",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "도시 이름 (예: 서울)"
                    }
                },
                "required": ["location"]
            }
        }
    }
]

response = client.chat.completions.create(
    model="openai/gpt-4o",
    messages=[{"role": "user", "content": "서울 날씨 어때?"}],
    tools=tools,
    tool_choice="auto"
)

# 함수 호출 확인
if response.choices[0].message.tool_calls:
    tool_call = response.choices[0].message.tool_calls[0]
    function_name = tool_call.function.name
    arguments = json.loads(tool_call.function.arguments)
    print(f"호출: {function_name}({arguments})")
```

### 5. JSON 모드

```python
response = client.chat.completions.create(
    model="openai/gpt-4o-mini",
    messages=[
        {"role": "system", "content": "JSON 형식으로 응답하세요."},
        {"role": "user", "content": "사과에 대한 정보를 알려주세요"}
    ],
    response_format={"type": "json_object"}
)

import json
data = json.loads(response.choices[0].message.content)
print(data)
```

---

## OpenRouter 전용 기능

### 1. 폴백 설정

```python
response = client.chat.completions.create(
    model="anthropic/claude-sonnet-4",
    messages=[{"role": "user", "content": "Hello"}],
    extra_body={
        "route": "fallback",
        "models": [
            "anthropic/claude-sonnet-4",
            "openai/gpt-4o",
            "google/gemini-2.0-flash"
        ]
    }
)
```

### 2. 제공자 선호도

```python
response = client.chat.completions.create(
    model="anthropic/claude-sonnet-4",
    messages=[{"role": "user", "content": "Hello"}],
    extra_body={
        "provider": {
            "order": ["Anthropic", "AWS Bedrock"],
            "allow_fallbacks": True
        }
    }
)
```

### 3. 라우팅 변형

```python
# 최저가 라우팅
response = client.chat.completions.create(
    model="anthropic/claude-sonnet-4:floor",
    messages=[{"role": "user", "content": "Hello"}]
)

# 최고 속도 라우팅
response = client.chat.completions.create(
    model="openai/gpt-4o:nitro",
    messages=[{"role": "user", "content": "Hello"}]
)
```

---

## 비동기 사용

### Python AsyncIO

```python
import asyncio
from openai import AsyncOpenAI

client = AsyncOpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ.get("OPENROUTER_API_KEY")
)

async def get_response(prompt):
    response = await client.chat.completions.create(
        model="openai/gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

async def main():
    # 여러 요청 동시 실행
    prompts = ["1+1=?", "2+2=?", "3+3=?"]
    results = await asyncio.gather(*[get_response(p) for p in prompts])

    for prompt, result in zip(prompts, results):
        print(f"{prompt} → {result}")

asyncio.run(main())
```

### JavaScript Async

```javascript
async function getMultipleResponses(prompts) {
  const promises = prompts.map(prompt =>
    client.chat.completions.create({
      model: 'openai/gpt-4o-mini',
      messages: [{ role: 'user', content: prompt }],
    })
  );

  const responses = await Promise.all(promises);
  return responses.map(r => r.choices[0].message.content);
}
```

---

## 에러 처리 패턴

### 재시도 로직

```python
from openai import OpenAI, RateLimitError, APIError
import time

def chat_with_retry(messages, max_retries=3):
    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model="openai/gpt-4o-mini",
                messages=messages
            )
            return response.choices[0].message.content

        except RateLimitError:
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt  # 지수 백오프
                print(f"Rate limited. Waiting {wait_time}s...")
                time.sleep(wait_time)
            else:
                raise

        except APIError as e:
            print(f"API Error: {e}")
            raise

# 사용
result = chat_with_retry([{"role": "user", "content": "Hello"}])
```

### 폴백 패턴

```python
def chat_with_fallback(messages):
    models = [
        "anthropic/claude-sonnet-4",
        "openai/gpt-4o",
        "openai/gpt-4o-mini"
    ]

    for model in models:
        try:
            response = client.chat.completions.create(
                model=model,
                messages=messages
            )
            print(f"Success with {model}")
            return response.choices[0].message.content
        except Exception as e:
            print(f"Failed {model}: {e}")
            continue

    raise Exception("All models failed")
```

---

## 환경별 설정

### 개발/프로덕션 분리

```python
import os

def get_client():
    env = os.environ.get("ENVIRONMENT", "development")

    if env == "production":
        return OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=os.environ["OPENROUTER_API_KEY"],
            timeout=30.0,
            max_retries=3
        )
    else:
        return OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=os.environ.get("OPENROUTER_API_KEY", "test-key"),
            timeout=60.0,
            max_retries=1
        )

client = get_client()
```

---

## 핵심 요약

```python
# OpenAI SDK → OpenRouter 마이그레이션

# 변경 전
client = OpenAI(api_key="sk-...")
model = "gpt-4o"

# 변경 후
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",  # 1. base_url 추가
    api_key="sk-or-v1-..."                    # 2. API 키 변경
)
model = "openai/gpt-4o"  # 3. provider/ 접두사 추가

# 나머지 코드는 동일!
```

---

## 다음 단계

- [[04-routing-variants|라우팅 변형]] - :nitro, :floor 등
- [[05-multimodal|멀티모달]] - 이미지, PDF
- [[06-cost-management|비용 관리]]

---

## 관련 노트

- [[01-quickstart|Quick Start]]
- [[02-models|모델 선택]]
- [[../cheatsheet|치트시트]]
