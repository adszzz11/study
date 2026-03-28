# LiteLLM Python SDK 기본 사용

## 학습 목표

- LiteLLM Python SDK 설치 및 기본 사용법 익히기
- 다양한 프로바이더 모델 호출하기
- 스트리밍, 비동기 호출 이해하기

---

## 설치

```bash
# 기본 설치
pip install litellm

# 특정 프로바이더 지원 추가 (선택)
pip install litellm[proxy]  # 프록시 서버 기능 포함
```

---

## 환경 변수 설정

API 키는 환경 변수로 설정하는 것이 안전합니다:

```bash
# .env 파일 또는 쉘에서 설정
export OPENAI_API_KEY="sk-..."
export ANTHROPIC_API_KEY="sk-ant-..."
export AZURE_API_KEY="..."
export AZURE_API_BASE="https://your-resource.openai.azure.com"
```

Python에서 직접 설정:

```python
import os

os.environ["OPENAI_API_KEY"] = "sk-..."
os.environ["ANTHROPIC_API_KEY"] = "sk-ant-..."
```

---

## 기본 사용법

### 1. 단순 호출

```python
from litellm import completion

# OpenAI
response = completion(
    model="gpt-4o",
    messages=[
        {"role": "user", "content": "안녕하세요!"}
    ]
)

print(response.choices[0].message.content)
```

### 2. 시스템 메시지 포함

```python
response = completion(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "당신은 친절한 한국어 어시스턴트입니다."},
        {"role": "user", "content": "파이썬이 뭐야?"}
    ]
)

print(response.choices[0].message.content)
```

### 3. 대화 이어가기

```python
messages = [
    {"role": "system", "content": "당신은 요리 전문가입니다."},
    {"role": "user", "content": "김치찌개 레시피 알려줘"},
]

response = completion(model="gpt-4o", messages=messages)
assistant_message = response.choices[0].message.content
print(assistant_message)

# 대화 이어가기
messages.append({"role": "assistant", "content": assistant_message})
messages.append({"role": "user", "content": "재료를 더 간단하게 할 수 있어?"})

response = completion(model="gpt-4o", messages=messages)
print(response.choices[0].message.content)
```

---

## 다양한 프로바이더 사용

```python
from litellm import completion

# OpenAI
response = completion(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Hello!"}]
)

# Anthropic Claude
response = completion(
    model="claude-3-5-sonnet-20241022",
    messages=[{"role": "user", "content": "Hello!"}]
)

# Ollama (로컬)
response = completion(
    model="ollama/llama3.2",
    messages=[{"role": "user", "content": "Hello!"}],
    api_base="http://localhost:11434"  # Ollama 서버 주소
)

# Azure OpenAI
response = completion(
    model="azure/gpt-4o-deployment",  # 배포 이름
    messages=[{"role": "user", "content": "Hello!"}],
    api_base="https://your-resource.openai.azure.com",
    api_version="2024-02-15-preview"
)
```

---

## 스트리밍

응답을 실시간으로 받아 출력합니다:

```python
from litellm import completion

response = completion(
    model="gpt-4o",
    messages=[{"role": "user", "content": "긴 이야기를 해줘"}],
    stream=True
)

for chunk in response:
    content = chunk.choices[0].delta.content
    if content:
        print(content, end="", flush=True)

print()  # 줄바꿈
```

---

## 비동기 호출

여러 요청을 동시에 처리할 때 유용합니다:

```python
import asyncio
from litellm import acompletion

async def get_response(prompt):
    response = await acompletion(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

async def main():
    prompts = [
        "파이썬의 장점은?",
        "자바의 장점은?",
        "Go의 장점은?"
    ]

    # 동시에 3개 요청
    tasks = [get_response(p) for p in prompts]
    results = await asyncio.gather(*tasks)

    for prompt, result in zip(prompts, results):
        print(f"Q: {prompt}")
        print(f"A: {result[:100]}...")
        print()

asyncio.run(main())
```

### 비동기 스트리밍

```python
import asyncio
from litellm import acompletion

async def stream_response():
    response = await acompletion(
        model="gpt-4o",
        messages=[{"role": "user", "content": "긴 이야기를 해줘"}],
        stream=True
    )

    async for chunk in response:
        content = chunk.choices[0].delta.content
        if content:
            print(content, end="", flush=True)

asyncio.run(stream_response())
```

---

## 유용한 파라미터

```python
response = completion(
    model="gpt-4o",
    messages=[{"role": "user", "content": "창의적인 이야기"}],

    # 응답 제어
    temperature=0.7,      # 창의성 (0.0~2.0, 기본 1.0)
    max_tokens=1000,      # 최대 토큰 수
    top_p=0.9,           # nucleus sampling

    # 동작 제어
    timeout=30,          # 타임아웃 (초)
    num_retries=3,       # 재시도 횟수

    # 메타데이터
    user="user-123",     # 사용자 식별
    metadata={           # 커스텀 메타데이터
        "session_id": "abc123"
    }
)
```

---

## 응답 구조

```python
response = completion(
    model="gpt-4o",
    messages=[{"role": "user", "content": "안녕"}]
)

# 응답 내용
print(response.choices[0].message.content)

# 메타 정보
print(f"모델: {response.model}")
print(f"ID: {response.id}")

# 토큰 사용량
print(f"입력 토큰: {response.usage.prompt_tokens}")
print(f"출력 토큰: {response.usage.completion_tokens}")
print(f"총 토큰: {response.usage.total_tokens}")

# 비용 (LiteLLM이 계산)
cost = response._hidden_params.get("response_cost", 0)
print(f"예상 비용: ${cost:.6f}")
```

---

## 에러 처리

```python
from litellm import completion
from litellm.exceptions import (
    AuthenticationError,
    RateLimitError,
    APIConnectionError,
    Timeout
)

def safe_completion(prompt):
    try:
        response = completion(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            timeout=30
        )
        return response.choices[0].message.content

    except AuthenticationError:
        print("API 키가 유효하지 않습니다")
    except RateLimitError:
        print("요청 한도 초과, 잠시 후 다시 시도하세요")
    except APIConnectionError:
        print("API 연결 실패")
    except Timeout:
        print("요청 시간 초과")
    except Exception as e:
        print(f"알 수 없는 오류: {e}")

    return None

result = safe_completion("안녕하세요")
if result:
    print(result)
```

---

## 실습 예제

### 예제 1: 간단한 챗봇

```python
from litellm import completion

def chat():
    messages = [
        {"role": "system", "content": "당신은 친절한 AI 어시스턴트입니다."}
    ]

    print("챗봇입니다. 'quit'을 입력하면 종료합니다.\n")

    while True:
        user_input = input("You: ")
        if user_input.lower() == 'quit':
            break

        messages.append({"role": "user", "content": user_input})

        response = completion(
            model="gpt-4o",
            messages=messages
        )

        assistant_message = response.choices[0].message.content
        messages.append({"role": "assistant", "content": assistant_message})

        print(f"AI: {assistant_message}\n")

if __name__ == "__main__":
    chat()
```

### 예제 2: 여러 모델 비교

```python
from litellm import completion
import time

def compare_models(prompt):
    models = [
        "gpt-4o",
        "claude-3-5-sonnet-20241022",
    ]

    for model in models:
        print(f"\n=== {model} ===")
        start = time.time()

        try:
            response = completion(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                timeout=30
            )

            elapsed = time.time() - start
            content = response.choices[0].message.content
            tokens = response.usage.total_tokens

            print(f"응답 시간: {elapsed:.2f}초")
            print(f"토큰 수: {tokens}")
            print(f"응답: {content[:200]}...")

        except Exception as e:
            print(f"오류: {e}")

compare_models("파이썬의 장점 3가지를 알려줘")
```

---

## 정리

| 함수 | 용도 |
|------|------|
| `completion()` | 동기 호출 |
| `acompletion()` | 비동기 호출 |
| `stream=True` | 스트리밍 응답 |

### 다음 단계

- [[02-proxy-server|프록시 서버 설정]] - 서버 모드 배우기
- [[04-providers|프로바이더 연결]] - 다양한 LLM 연결하기
