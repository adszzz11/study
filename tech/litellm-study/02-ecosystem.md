# LiteLLM 에코시스템

## 관련 기술 스택

### LLM 프로바이더

| 프로바이더 | 모델 예시 | LiteLLM 접두사 |
|-----------|----------|---------------|
| OpenAI | gpt-4o, gpt-4-turbo | (없음, 기본) |
| Anthropic | claude-3-5-sonnet | anthropic/ |
| Azure OpenAI | gpt-4 (배포명) | azure/ |
| AWS Bedrock | claude, llama | bedrock/ |
| Google Vertex AI | gemini-pro | vertex_ai/ |
| Ollama | llama3.2, mistral | ollama/ |
| Hugging Face | 다양한 오픈소스 | huggingface/ |
| Cohere | command-r | cohere_chat/ |
| Together AI | 다양한 오픈소스 | together_ai/ |
| Groq | llama-3.2-90b | groq/ |

### 함께 사용하는 도구

```
┌─────────────────────────────────────────────────────────────┐
│                     Application Layer                        │
│  - LangChain: LLM 애플리케이션 프레임워크                      │
│  - LlamaIndex: RAG 특화 프레임워크                            │
│  - Semantic Kernel: Microsoft의 AI 오케스트레이션             │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                     Gateway Layer                            │
│  - LiteLLM: LLM 통합 게이트웨이 ◀── 현재 학습 중              │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                     Infrastructure Layer                     │
│  - Docker/Kubernetes: 컨테이너 오케스트레이션                 │
│  - Redis: 캐싱, 레이트 리미팅                                 │
│  - PostgreSQL: 사용량/로그 저장                               │
│  - Prometheus/Grafana: 모니터링                              │
└─────────────────────────────────────────────────────────────┘
```

---

## 경쟁/대안 기술 비교

### LLM 게이트웨이 비교

| 기능 | LiteLLM | OpenRouter | Portkey | AI Gateway (Cloudflare) |
|------|---------|------------|---------|------------------------|
| 오픈소스 | O | X | 부분 | X |
| 셀프호스팅 | O | X | O | X |
| 프로바이더 수 | 100+ | 50+ | 20+ | 10+ |
| Python SDK | O | X | O | X |
| 가상 키 | O | O | O | O |
| 비용 추적 | O | O | O | O |
| 로드 밸런싱 | O | X | O | O |
| 무료 티어 | 무제한(셀프) | 제한적 | 제한적 | 제한적 |

### 언제 LiteLLM을 선택할까?

```
LiteLLM 추천:
├── 셀프호스팅이 필수인 경우 (데이터 주권)
├── 100+ 프로바이더 지원이 필요한 경우
├── Python 기반 프로젝트
├── 비용을 최소화하고 싶은 경우
└── 커스터마이징이 필요한 경우

OpenRouter 추천:
├── 관리형 서비스 선호
├── 빠른 시작이 필요
└── 인프라 관리 부담을 줄이고 싶음

Portkey 추천:
├── 엔터프라이즈급 기능 필요
├── 상용 지원 필요
└── 고급 분석 기능 필요
```

---

## LangChain과의 통합

LiteLLM은 LangChain과 자연스럽게 통합됩니다:

```python
# 방법 1: LiteLLM을 직접 ChatOpenAI 백엔드로 사용
from langchain_openai import ChatOpenAI

# LiteLLM Proxy를 OpenAI 엔드포인트로 지정
llm = ChatOpenAI(
    model="gpt-4o",
    base_url="http://localhost:4000/v1",
    api_key="sk-litellm-key"
)

# 방법 2: LiteLLM의 ChatLiteLLM 사용
from langchain_community.chat_models import ChatLiteLLM

llm = ChatLiteLLM(model="anthropic/claude-3-5-sonnet-20241022")
```

---

## 인프라 구성 예시

### 개발 환경
```
개발자 PC
    │
    └── LiteLLM (Python SDK)
            │
            ├── Ollama (로컬, 무료)
            └── OpenAI (필요시)
```

### 스테이징 환경
```
Docker Compose
    │
    ├── LiteLLM Proxy (컨테이너)
    │       │
    │       ├── OpenAI
    │       └── Anthropic
    │
    └── Redis (레이트 리미팅)
```

### 프로덕션 환경
```
Kubernetes Cluster
    │
    ├── LiteLLM Proxy (여러 Pod)
    │       │
    │       ├── Azure OpenAI (Primary)
    │       ├── AWS Bedrock (Secondary)
    │       └── OpenAI (Fallback)
    │
    ├── PostgreSQL (사용량 저장)
    ├── Redis (캐싱, 레이트 리미팅)
    └── Prometheus + Grafana (모니터링)
```

---

## 트렌드와 전망

### 2024-2025 LLM 게이트웨이 트렌드

1. **멀티 모델 전략 확산**
   - 단일 프로바이더 의존 → 멀티 프로바이더 전략
   - 비용/성능/가용성 최적화 필요성 증가

2. **AI 거버넌스 강화**
   - 비용 관리, 사용량 추적 필수화
   - 팀별 접근 제어 요구 증가

3. **온프레미스 LLM 성장**
   - Ollama, vLLM 등 로컬 추론 도구 발전
   - 하이브리드 구성 (로컬 + 클라우드) 증가

4. **표준화 움직임**
   - OpenAI 형식이 사실상 표준으로 자리잡음
   - LiteLLM 같은 통합 레이어의 중요성 증가

### LiteLLM 로드맵 (참고)

- 더 많은 프로바이더 지원
- 고급 캐싱 전략
- 향상된 관찰성 (Observability)
- 엔터프라이즈 기능 강화

---

## 관련 학습 자료

### 필수 선행 지식
- Python 기초
- REST API 개념
- 환경 변수 사용법

### 추천 학습 순서
```
1. OpenAI API 기초 이해
        ↓
2. LiteLLM Python SDK
        ↓
3. LiteLLM Proxy Server
        ↓
4. Docker 기본 (배포용)
        ↓
5. 모니터링 도구 (선택)
```

### 함께 공부하면 좋은 기술
- **LangChain**: LLM 애플리케이션 개발
- **Docker**: 컨테이너화 및 배포
- **Redis**: 캐싱 및 레이트 리미팅
- **Prometheus/Grafana**: 모니터링

---

## 다음 단계

- [[03-references|참고 자료]] - 공식 문서 및 학습 리소스
- [[04-learning/01-python-sdk|Python SDK]] - 실습 시작
