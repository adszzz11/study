# OpenRouter 참고 자료

## 공식 문서

### 핵심 문서
- [OpenRouter 공식 사이트](https://openrouter.ai)
- [API 문서](https://openrouter.ai/docs)
- [모델 목록](https://openrouter.ai/models)
- [가격표](https://openrouter.ai/pricing)

### API 레퍼런스
- [Chat Completions API](https://openrouter.ai/docs#chat-completions)
- [모델 라우팅](https://openrouter.ai/docs#model-routing)
- [인증](https://openrouter.ai/docs#authentication)
- [에러 핸들링](https://openrouter.ai/docs#errors)

### 상태 및 업데이트
- [시스템 상태](https://status.openrouter.ai)
- [Discord 커뮤니티](https://discord.gg/openrouter)

---

## 학습 자료

### 공식 가이드
| 주제 | 링크 | 난이도 |
|-----|------|-------|
| Quick Start | [openrouter.ai/docs](https://openrouter.ai/docs) | 초급 |
| 모델 선택 가이드 | [openrouter.ai/models](https://openrouter.ai/models) | 초급 |
| 라우팅 변형 | [openrouter.ai/docs#routing](https://openrouter.ai/docs) | 중급 |
| BYOK 설정 | [openrouter.ai/docs#byok](https://openrouter.ai/docs) | 중급 |

### 블로그/아티클
- [OpenRouter 소개 - 공식 블로그](https://openrouter.ai/blog)
- [500+ AI Models via One API](https://openrouter.ai/blog)

### 영상 자료
- YouTube에서 "OpenRouter tutorial" 검색
- "OpenRouter vs LiteLLM" 비교 영상

---

## API 빠른 참조

### 엔드포인트

```
Base URL: https://openrouter.ai/api/v1

주요 엔드포인트:
POST /chat/completions  - 채팅 완성
GET  /models            - 모델 목록
GET  /auth/key          - API 키 정보
```

### 인증

```bash
# Header 방식
Authorization: Bearer sk-or-v1-...

# 환경 변수
export OPENROUTER_API_KEY=sk-or-v1-...
```

### 기본 요청 형식

```json
{
  "model": "anthropic/claude-sonnet-4",
  "messages": [
    {"role": "system", "content": "시스템 프롬프트"},
    {"role": "user", "content": "사용자 메시지"}
  ],
  "temperature": 0.7,
  "max_tokens": 1000,
  "stream": false
}
```

### 응답 형식

```json
{
  "id": "gen-...",
  "choices": [{
    "message": {
      "role": "assistant",
      "content": "응답 내용"
    },
    "finish_reason": "stop"
  }],
  "usage": {
    "prompt_tokens": 10,
    "completion_tokens": 50,
    "total_tokens": 60
  }
}
```

---

## 관련 기술 문서

### OpenAI API (호환)
- [OpenAI API 문서](https://platform.openai.com/docs)
- [OpenAI Python SDK](https://github.com/openai/openai-python)
- [Chat Completions Guide](https://platform.openai.com/docs/guides/chat)

### LLM 제공자
- [Anthropic Claude 문서](https://docs.anthropic.com)
- [Google Gemini 문서](https://ai.google.dev/docs)
- [Meta Llama 문서](https://llama.meta.com)

### 통합 프레임워크
- [LangChain 문서](https://python.langchain.com/docs)
- [LlamaIndex 문서](https://docs.llamaindex.ai)
- [Vercel AI SDK](https://sdk.vercel.ai/docs)

---

## 커뮤니티

### 공식 채널
- [Discord](https://discord.gg/openrouter) - 가장 활발한 커뮤니티
- [Twitter/X](https://twitter.com/openrouter)
- [GitHub](https://github.com/openrouter-ai)

### 토론 포럼
- Reddit: r/LocalLLaMA (LLM 일반)
- Hacker News: OpenRouter 검색

### 한국어 커뮤니티
- 카카오 오픈채팅: "AI/LLM 개발자" 검색
- Discord 한국 AI 커뮤니티

---

## 도구 및 유틸리티

### 테스트 도구
```bash
# curl로 API 테스트
curl https://openrouter.ai/api/v1/chat/completions \
  -H "Authorization: Bearer $OPENROUTER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model": "openai/gpt-4o-mini", "messages": [{"role": "user", "content": "test"}]}'

# httpie로 테스트
http POST https://openrouter.ai/api/v1/chat/completions \
  Authorization:"Bearer $OPENROUTER_API_KEY" \
  model=openai/gpt-4o-mini \
  messages:='[{"role": "user", "content": "test"}]'
```

### SDK/라이브러리
```python
# Python - OpenAI SDK (공식 권장)
pip install openai

# JavaScript/TypeScript
npm install openai

# Go
go get github.com/sashabaranov/go-openai
```

### VS Code 확장
- Continue - AI 코드 어시스턴트 (OpenRouter 지원)
- Cody - AI 코딩 어시스턴트

---

## 참고 비교 자료

### 가격 비교 사이트
- [OpenRouter 가격표](https://openrouter.ai/models) - 모델별 실시간 가격
- [LLM Price Comparison](https://llmprices.dev) - 제공자별 가격 비교

### 벤치마크
- [LMSYS Chatbot Arena](https://chat.lmsys.org) - 모델 비교
- [Artificial Analysis](https://artificialanalysis.ai) - 성능/가격 분석

---

## 학습 경로

### 초급 (1주)
1. OpenRouter 공식 문서 Quick Start
2. 계정 생성 및 첫 API 호출
3. 모델 목록 탐색

### 중급 (2주)
1. OpenAI SDK 통합
2. 라우팅 변형 이해
3. 멀티모달 사용
4. 비용 최적화

### 고급 (1개월)
1. 프로덕션 아키텍처
2. 폴백/로드밸런싱
3. BYOK 설정
4. 모니터링/로깅

---

## 트러블슈팅 리소스

### 일반적인 문제
| 문제 | 해결 |
|-----|------|
| 401 Unauthorized | API 키 확인, 크레딧 잔액 확인 |
| 429 Rate Limited | 요청 간격 늘리기, 모델 변경 |
| 500 Server Error | 다른 모델 시도, 상태 페이지 확인 |
| Timeout | 스트리밍 사용, :nitro 변형 시도 |

### 디버깅 팁
```python
# 응답 헤더로 사용량 확인
response = client.chat.completions.create(...)

# 사용량 출력
print(f"Tokens: {response.usage.total_tokens}")
print(f"Model: {response.model}")
```

---

## 핵심 링크 요약

```
필수:
- 공식 문서: openrouter.ai/docs
- 모델 목록: openrouter.ai/models
- 상태: status.openrouter.ai

커뮤니티:
- Discord: discord.gg/openrouter

참고:
- OpenAI SDK: github.com/openai/openai-python
- LangChain: python.langchain.com
```

---

## 관련 노트

- [[01-overview|개요]]
- [[02-ecosystem|에코시스템]]
- [[04-learning/01-quickstart|Quick Start]]
