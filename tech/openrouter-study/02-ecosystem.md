# OpenRouter 에코시스템

## 관련 기술 맵

```
                    [LLM 제공자]
                         │
    ┌────────────────────┼────────────────────┐
    │                    │                    │
[OpenAI]            [Anthropic]          [Google]
[GPT-4o]            [Claude]             [Gemini]
    │                    │                    │
    └────────────────────┼────────────────────┘
                         │
                   [OpenRouter]  ← 통합 게이트웨이
                         │
    ┌────────────────────┼────────────────────┐
    │                    │                    │
[LangChain]         [직접 SDK]          [LlamaIndex]
[프레임워크]         [OpenAI SDK]        [RAG 특화]
```

---

## 유사 서비스 비교

### LLM 게이트웨이/라우터

| 서비스 | 특징 | 가격 모델 | 주요 차이점 |
|-------|------|----------|-----------|
| **OpenRouter** | 500+ 모델, OpenAI 호환 | Pay-as-you-go | 가장 많은 모델, 라우팅 변형 |
| **LiteLLM** | 오픈소스, 셀프호스팅 | 무료 (셀프호스팅) | 직접 운영 필요 |
| **Portkey** | 엔터프라이즈 기능 | 티어별 가격 | 거버넌스, 보안 특화 |
| **Helicone** | 관측성 특화 | 무료~엔터프라이즈 | 로깅/분석 강점 |

### 상세 비교

#### OpenRouter vs LiteLLM

```python
# OpenRouter - 관리형 서비스
client = openai.OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="sk-or-v1-..."
)

# LiteLLM - 셀프호스팅
# pip install litellm
from litellm import completion

response = completion(
    model="claude-sonnet-4",
    messages=[{"role": "user", "content": "Hello"}],
    api_key="sk-ant-..."  # 직접 관리
)
```

| 항목 | OpenRouter | LiteLLM |
|-----|-----------|---------|
| 호스팅 | 관리형 | 셀프호스팅 |
| 비용 | 마진 포함 | 무료 (인프라 비용만) |
| 설정 | 간단 | 복잡 |
| 폴백 | 자동 | 직접 구현 |
| 적합 대상 | 빠른 시작, 소규모 | 대규모, 비용 최적화 |

#### OpenRouter vs 직접 API 호출

```python
# 직접 호출 - 각 제공자별 SDK 필요
import anthropic
import openai

# Claude
claude_client = anthropic.Anthropic(api_key="sk-ant-...")
claude_response = claude_client.messages.create(...)

# GPT
openai_client = openai.OpenAI(api_key="sk-...")
openai_response = openai_client.chat.completions.create(...)

# OpenRouter - 단일 클라이언트
or_client = openai.OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="sk-or-v1-..."
)
# Claude, GPT 모두 동일한 방식으로 호출
```

---

## 통합 가능한 프레임워크

### 1. LangChain

```python
from langchain_openai import ChatOpenAI

# OpenRouter를 LangChain과 함께 사용
llm = ChatOpenAI(
    model="anthropic/claude-sonnet-4",
    openai_api_key="sk-or-v1-...",
    openai_api_base="https://openrouter.ai/api/v1"
)

response = llm.invoke("안녕하세요!")
```

### 2. LlamaIndex

```python
from llama_index.llms.openai import OpenAI

llm = OpenAI(
    model="anthropic/claude-sonnet-4",
    api_key="sk-or-v1-...",
    api_base="https://openrouter.ai/api/v1"
)
```

### 3. Vercel AI SDK

```typescript
import { createOpenAI } from '@ai-sdk/openai';

const openrouter = createOpenAI({
  baseURL: 'https://openrouter.ai/api/v1',
  apiKey: process.env.OPENROUTER_API_KEY,
});

const result = await generateText({
  model: openrouter('anthropic/claude-sonnet-4'),
  prompt: 'Hello!',
});
```

### 4. Continue (VS Code AI 확장)

```json
// ~/.continue/config.json
{
  "models": [{
    "title": "Claude via OpenRouter",
    "provider": "openai",
    "model": "anthropic/claude-sonnet-4",
    "apiBase": "https://openrouter.ai/api/v1",
    "apiKey": "sk-or-v1-..."
  }]
}
```

---

## 지원 모델 제공자

### 주요 제공자

| 제공자 | 대표 모델 | 특징 |
|-------|----------|------|
| **Anthropic** | Claude 4, Sonnet, Haiku | 긴 컨텍스트, 안전성 |
| **OpenAI** | GPT-4o, GPT-4 Turbo | 범용성, 생태계 |
| **Google** | Gemini 2.0, Gemma | 멀티모달 강점 |
| **Meta** | Llama 3.1 (8B~405B) | 오픈소스, 비용 효율 |
| **Mistral** | Mixtral, Mistral Large | 유럽 AI, 효율성 |
| **Cohere** | Command R+ | RAG 특화 |

### 모델 선택 가이드

```
용도별 추천:
├── 일반 대화/작문
│   └── anthropic/claude-sonnet-4, openai/gpt-4o
├── 코딩
│   └── anthropic/claude-sonnet-4, deepseek/deepseek-coder
├── 긴 문서 처리
│   └── anthropic/claude-sonnet-4 (200K), google/gemini-2.0-flash (1M)
├── 저비용
│   └── meta-llama/llama-3.1-8b:free, openai/gpt-4o-mini
└── 빠른 응답
    └── *:nitro 변형
```

---

## 시장 트렌드

### 2025년 LLM 인프라 동향

1. **통합 API 게이트웨이 부상**
   - OpenRouter $500M 밸류에이션 (2025.06)
   - 단일 제공자 의존 탈피 추세

2. **가격 경쟁 심화**
   - GPT-4o 가격 지속 하락
   - 오픈소스 모델 (Llama, Mixtral) 성능 향상

3. **특화 모델 증가**
   - 코딩: DeepSeek Coder, Codestral
   - 수학/추론: Claude Thinking, o1
   - 멀티모달: Gemini, Claude Vision

4. **엔터프라이즈 기능 강화**
   - 거버넌스, 감사, 규정 준수
   - 프라이빗 배포 옵션

### OpenRouter 로드맵 (예상)

```
현재:
- 500+ 모델 지원
- 라우팅 변형
- BYOK

향후 예상:
- 더 많은 모델/제공자
- 고급 라우팅 (A/B 테스트, 조건부)
- 엔터프라이즈 기능 강화
```

---

## 경쟁 환경

### 시장 포지셔닝

```
                    관리형
                      │
              [OpenRouter]
              [Portkey]
                      │
    간단 ────────────┼──────────── 복잡
                      │
              [LiteLLM]
              [직접 구현]
                      │
                   셀프호스팅
```

### 선택 가이드

| 상황 | 추천 |
|-----|------|
| 빠른 프로토타이핑 | OpenRouter |
| 비용이 최우선 | LiteLLM (셀프호스팅) |
| 엔터프라이즈 규정 준수 | Portkey |
| 관측성/분석 필요 | Helicone + OpenRouter |
| 특정 모델만 사용 | 직접 API |

---

## 아키텍처 패턴

### 1. 기본 패턴

```
[앱] → [OpenRouter] → [LLM 제공자]
```

### 2. 폴백 패턴

```
[앱] → [OpenRouter] → [Claude] (1순위)
                   → [GPT-4o] (2순위, 폴백)
                   → [Gemini] (3순위, 폴백)
```

### 3. 비용 최적화 패턴

```
[앱] → [라우터 로직] → [:free 모델] (일반 요청)
                    → [:floor 모델] (중요 요청)
                    → [프리미엄 모델] (핵심 요청)
```

### 4. 하이브리드 패턴

```
[앱] → [직접 API] (핵심 기능, 레이턴시 중요)
    → [OpenRouter] (부가 기능, 유연성 필요)
```

---

## 핵심 요약

```
OpenRouter 포지션:
- 가장 많은 모델 (500+)
- 가장 쉬운 시작 (OpenAI SDK 호환)
- 관리형 서비스 (인프라 걱정 없음)

대안:
- LiteLLM: 비용 최적화, 셀프호스팅
- Portkey: 엔터프라이즈
- 직접 API: 최저 레이턴시

트렌드:
- 통합 API 게이트웨이 성장
- 가격 경쟁 심화
- 특화 모델 증가
```

---

## 관련 노트

- [[01-overview|개요]]
- [[03-references|참고 자료]]
- [[04-learning/02-models|모델 선택]]
