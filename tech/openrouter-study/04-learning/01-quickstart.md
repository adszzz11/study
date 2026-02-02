# OpenRouter Quick Start

> API 키 발급부터 첫 요청까지

## 1. 계정 생성

### Step 1: 회원가입
1. [openrouter.ai](https://openrouter.ai) 접속
2. "Sign In" 클릭
3. Google 또는 GitHub 계정으로 로그인

### Step 2: API 키 생성
1. 로그인 후 우측 상단 프로필 클릭
2. "Keys" 메뉴 선택
3. "Create Key" 클릭
4. 키 이름 입력 (예: "my-first-key")
5. 생성된 키 복사 (`sk-or-v1-...` 형식)

> **중요**: API 키는 한 번만 표시됩니다. 안전한 곳에 저장하세요.

### Step 3: 크레딧 충전
1. "Credits" 메뉴로 이동
2. "Add Credits" 클릭
3. 금액 선택 (최소 $5 권장)
4. 결제 완료

---

## 2. 환경 설정

### Python 환경

```bash
# OpenAI SDK 설치
pip install openai

# 환경 변수 설정
export OPENROUTER_API_KEY="sk-or-v1-..."
```

### JavaScript/Node.js 환경

```bash
# OpenAI SDK 설치
npm install openai

# 환경 변수 설정
export OPENROUTER_API_KEY="sk-or-v1-..."
```

### 환경 변수 파일 (.env)

```env
# .env 파일
OPENROUTER_API_KEY=sk-or-v1-...
```

> **주의**: `.env` 파일은 `.gitignore`에 추가하세요!

---

## 3. 첫 API 호출

### Python 예제

```python
import os
from openai import OpenAI

# 클라이언트 초기화
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ.get("OPENROUTER_API_KEY")
)

# 첫 요청
response = client.chat.completions.create(
    model="openai/gpt-4o-mini",  # 저렴한 모델로 시작
    messages=[
        {"role": "user", "content": "안녕하세요! OpenRouter 테스트입니다."}
    ]
)

# 응답 출력
print(response.choices[0].message.content)
```

### JavaScript 예제

```javascript
import OpenAI from 'openai';

const client = new OpenAI({
  baseURL: 'https://openrouter.ai/api/v1',
  apiKey: process.env.OPENROUTER_API_KEY,
});

async function main() {
  const response = await client.chat.completions.create({
    model: 'openai/gpt-4o-mini',
    messages: [
      { role: 'user', content: '안녕하세요! OpenRouter 테스트입니다.' }
    ],
  });

  console.log(response.choices[0].message.content);
}

main();
```

### curl 예제

```bash
curl https://openrouter.ai/api/v1/chat/completions \
  -H "Authorization: Bearer $OPENROUTER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "openai/gpt-4o-mini",
    "messages": [
      {"role": "user", "content": "안녕하세요!"}
    ]
  }'
```

---

## 4. 응답 이해하기

### 응답 구조

```json
{
  "id": "gen-1234567890",
  "object": "chat.completion",
  "created": 1234567890,
  "model": "openai/gpt-4o-mini",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "안녕하세요! 반갑습니다."
      },
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 15,
    "completion_tokens": 10,
    "total_tokens": 25
  }
}
```

### 주요 필드 설명

| 필드 | 설명 |
|-----|------|
| `choices[0].message.content` | AI 응답 텍스트 |
| `usage.total_tokens` | 사용된 총 토큰 수 |
| `finish_reason` | 종료 이유 (stop, length 등) |
| `model` | 실제 사용된 모델 |

---

## 5. 기본 옵션

### 온도 (Temperature)

```python
response = client.chat.completions.create(
    model="openai/gpt-4o-mini",
    messages=[{"role": "user", "content": "창의적인 이야기를 써주세요"}],
    temperature=0.9  # 0.0 (결정적) ~ 2.0 (창의적)
)
```

### 최대 토큰

```python
response = client.chat.completions.create(
    model="openai/gpt-4o-mini",
    messages=[{"role": "user", "content": "짧게 답해주세요"}],
    max_tokens=100  # 응답 길이 제한
)
```

### 시스템 메시지

```python
response = client.chat.completions.create(
    model="openai/gpt-4o-mini",
    messages=[
        {"role": "system", "content": "당신은 친절한 한국어 튜터입니다."},
        {"role": "user", "content": "오늘 날씨 어때요?"}
    ]
)
```

---

## 6. 스트리밍

### 스트리밍 응답 (실시간 출력)

```python
stream = client.chat.completions.create(
    model="openai/gpt-4o-mini",
    messages=[{"role": "user", "content": "긴 이야기를 해주세요"}],
    stream=True
)

for chunk in stream:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="", flush=True)
```

### JavaScript 스트리밍

```javascript
const stream = await client.chat.completions.create({
  model: 'openai/gpt-4o-mini',
  messages: [{ role: 'user', content: '긴 이야기를 해주세요' }],
  stream: true,
});

for await (const chunk of stream) {
  const content = chunk.choices[0]?.delta?.content || '';
  process.stdout.write(content);
}
```

---

## 7. 에러 처리

### 기본 에러 처리

```python
from openai import OpenAI, APIError, RateLimitError, AuthenticationError

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ.get("OPENROUTER_API_KEY")
)

try:
    response = client.chat.completions.create(
        model="openai/gpt-4o-mini",
        messages=[{"role": "user", "content": "Hello"}]
    )
    print(response.choices[0].message.content)

except AuthenticationError:
    print("API 키가 올바르지 않습니다.")

except RateLimitError:
    print("요청 한도를 초과했습니다. 잠시 후 다시 시도하세요.")

except APIError as e:
    print(f"API 에러: {e}")
```

### 일반적인 에러 코드

| 코드 | 원인 | 해결 |
|-----|------|------|
| 401 | 인증 실패 | API 키 확인 |
| 402 | 크레딧 부족 | 크레딧 충전 |
| 429 | 요청 한도 초과 | 대기 후 재시도 |
| 500 | 서버 에러 | 다른 모델 시도 |

---

## 8. 크레딧 확인

### API로 잔액 확인

```python
import requests

response = requests.get(
    "https://openrouter.ai/api/v1/auth/key",
    headers={"Authorization": f"Bearer {os.environ.get('OPENROUTER_API_KEY')}"}
)

data = response.json()
print(f"잔액: ${data['data']['limit']}")
print(f"사용량: ${data['data']['usage']}")
```

### 웹에서 확인
1. [openrouter.ai](https://openrouter.ai) 로그인
2. "Credits" 메뉴에서 잔액 확인

---

## 9. 실습 과제

### 과제 1: 기본 챗봇
다양한 모델로 같은 질문을 해보고 응답 비교하기

```python
models = ["openai/gpt-4o-mini", "anthropic/claude-3-haiku"]
question = "파이썬의 장점은 무엇인가요?"

for model in models:
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": question}]
    )
    print(f"\n=== {model} ===")
    print(response.choices[0].message.content)
```

### 과제 2: 토큰 사용량 추적
응답의 토큰 사용량을 출력하기

```python
response = client.chat.completions.create(
    model="openai/gpt-4o-mini",
    messages=[{"role": "user", "content": "Hello"}]
)

print(f"입력 토큰: {response.usage.prompt_tokens}")
print(f"출력 토큰: {response.usage.completion_tokens}")
print(f"총 토큰: {response.usage.total_tokens}")
```

---

## 핵심 요약

```
1. 계정 생성: openrouter.ai에서 Google/GitHub 로그인
2. API 키: Keys 메뉴에서 생성 (sk-or-v1-...)
3. 크레딧: $5 이상 충전 권장
4. 코드: OpenAI SDK + base_url 변경만 하면 끝!

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="sk-or-v1-..."
)
```

---

## 다음 단계

- [[02-models|모델 선택 가이드]] - 다양한 모델 비교
- [[03-openai-sdk|OpenAI SDK 심화]] - 기존 코드 마이그레이션
- [[04-routing-variants|라우팅 변형]] - :nitro, :floor 등

---

## 관련 노트

- [[../01-overview|개요]]
- [[../03-references|참고 자료]]
- [[../cheatsheet|치트시트]]
