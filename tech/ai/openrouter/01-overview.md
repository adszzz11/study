# OpenRouter 개요

## OpenRouter란?

OpenRouter는 **500개 이상의 LLM 모델을 단일 API로 접근**할 수 있게 해주는 통합 AI 게이트웨이이자 마켓플레이스이다.

```
[사용자 앱] → [OpenRouter API] → [Claude, GPT, Llama, Gemini...]
                    ↓
            - 라우팅/로드밸런싱
            - 자동 폴백
            - 비용 최적화
```

### 핵심 가치
- **통합 접근**: 하나의 API 키로 모든 주요 LLM 사용
- **OpenAI 호환**: 기존 OpenAI SDK 코드를 그대로 사용
- **자동 폴백**: 모델 장애 시 자동으로 대체 모델로 전환
- **비용 최적화**: 모델별 가격 비교, 저비용 라우팅 옵션

### 회사 정보
- 2025년 6월 $40M 투자 유치, $500M 밸류에이션
- 급성장 중인 AI 인프라 스타트업

---

## 핵심 개념

### 1. 단일 API 엔드포인트

```python
# OpenAI SDK 그대로 사용, base_url만 변경
client = openai.OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="sk-or-v1-..."
)

# 다양한 모델 호출
response = client.chat.completions.create(
    model="anthropic/claude-sonnet-4",  # Claude
    # model="openai/gpt-4o",            # GPT-4o
    # model="google/gemini-2.0-flash",  # Gemini
    # model="meta-llama/llama-3.1-70b", # Llama
    messages=[{"role": "user", "content": "Hello"}]
)
```

### 2. 모델 ID 형식

```
{provider}/{model-name}:{variant}

예시:
- anthropic/claude-sonnet-4
- openai/gpt-4o
- anthropic/claude-sonnet-4:floor   # 최저가 라우팅
- openai/gpt-4o:nitro               # 최고 속도 라우팅
```

### 3. 라우팅 변형 (Routing Variants)

| 변형 | 용도 | 예시 |
|-----|------|-----|
| `:nitro` | 최고 속도 (더 비쌈) | `claude-sonnet-4:nitro` |
| `:floor` | 최저 비용 | `gpt-4o:floor` |
| `:free` | 무료 (레이트 제한) | `llama-3.1-8b:free` |
| `:thinking` | 추론 강화 | `claude-sonnet-4:thinking` |

### 4. 자동 폴백

```python
response = client.chat.completions.create(
    model="anthropic/claude-sonnet-4",
    messages=[...],
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

---

## 장점

### 1. 개발 편의성
- **단일 API**: 여러 제공자 API 통합 불필요
- **OpenAI 호환**: 기존 코드 재사용
- **빠른 모델 전환**: 코드 수정 없이 모델 변경

### 2. 안정성
- **자동 폴백**: 장애 시 대체 모델 자동 전환
- **로드밸런싱**: 여러 제공자 간 트래픽 분산
- **99.9% 업타임**: 고가용성 보장

### 3. 비용 효율
- **가격 비교**: 동일 모델의 제공자별 가격 비교
- **라우팅 옵션**: `:floor`로 최저가 자동 선택
- **Pay-as-you-go**: 사용한 만큼만 지불

### 4. 유연성
- **BYOK**: 자신의 API 키 사용 가능 (5% 수수료)
- **멀티모달**: 이미지, PDF 지원
- **스트리밍**: SSE 스트리밍 지원

---

## 단점

### 1. 레이턴시 추가
```
직접 호출:     [앱] → [Claude API]
OpenRouter:   [앱] → [OpenRouter] → [Claude API]

추가 레이턴시: 약 25-40ms
```

### 2. 추가 비용
- 기본: OpenRouter 마진이 포함된 가격
- BYOK: 5% 수수료 추가

### 3. 의존성
- OpenRouter 서비스에 대한 의존
- 추가적인 장애 지점 (Single Point of Failure 가능성)

### 4. 일부 기능 제한
- 특정 제공자의 고급 기능 미지원 가능
- 새 모델 출시 시 지연 가능

---

## 사용 사례

### 1. 프로토타이핑/개발

```python
# 빠르게 여러 모델 테스트
models = [
    "anthropic/claude-sonnet-4",
    "openai/gpt-4o",
    "google/gemini-2.0-flash"
]

for model in models:
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": "테스트 프롬프트"}]
    )
    print(f"{model}: {response.choices[0].message.content}")
```

### 2. 비용 최적화 서비스

```python
# 중요도에 따라 다른 모델 사용
def get_response(prompt, priority="normal"):
    if priority == "high":
        model = "anthropic/claude-sonnet-4"
    elif priority == "normal":
        model = "openai/gpt-4o-mini"
    else:
        model = "meta-llama/llama-3.1-8b:free"

    return client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}]
    )
```

### 3. 고가용성 서비스

```python
# 폴백으로 안정성 확보
response = client.chat.completions.create(
    model="anthropic/claude-sonnet-4",
    messages=[...],
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

### 4. 멀티모달 애플리케이션

```python
# 이미지 분석
response = client.chat.completions.create(
    model="anthropic/claude-sonnet-4",
    messages=[{
        "role": "user",
        "content": [
            {"type": "text", "text": "이 이미지를 분석해주세요"},
            {"type": "image_url", "image_url": {"url": image_url}}
        ]
    }]
)
```

---

## 언제 OpenRouter를 사용해야 할까?

### 적합한 경우
- 여러 LLM 모델을 비교/테스트해야 할 때
- 폴백이 필요한 프로덕션 서비스
- 빠른 프로토타이핑이 필요할 때
- 비용 최적화가 중요할 때
- 단일 제공자 의존을 피하고 싶을 때

### 부적합한 경우
- 극도로 낮은 레이턴시가 필요할 때
- 특정 제공자의 고급 기능이 필수일 때
- 규제로 인해 중간 서비스 사용이 불가할 때

---

## 핵심 요약

```
OpenRouter = LLM 라우터 + 마켓플레이스

핵심 특징:
1. 500+ 모델 단일 API
2. OpenAI API 100% 호환
3. 자동 폴백/로드밸런싱
4. 라우팅 변형 (속도/비용/무료)
5. BYOK 지원 (5% 수수료)
6. 멀티모달 지원

Trade-off:
+ 편의성, 유연성, 안정성
- 레이턴시 추가 (25-40ms), 추가 비용
```

---

## 관련 노트

- [[02-ecosystem|에코시스템]]
- [[04-learning/01-quickstart|Quick Start]]
- [[cheatsheet|치트시트]]
