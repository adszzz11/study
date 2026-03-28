# LiteLLM 참고 자료

## 공식 자료

### 필수 링크

| 자료 | URL | 설명 |
|------|-----|------|
| 공식 문서 | [docs.litellm.ai](https://docs.litellm.ai) | 가장 중요한 자료 |
| GitHub | [github.com/BerriAI/litellm](https://github.com/BerriAI/litellm) | 소스 코드, 이슈 |
| PyPI | [pypi.org/project/litellm](https://pypi.org/project/litellm/) | 설치, 버전 정보 |
| Docker Hub | [ghcr.io/berriai/litellm](https://github.com/BerriAI/litellm/pkgs/container/litellm) | 컨테이너 이미지 |

### 공식 문서 구조

```
docs.litellm.ai
├── Getting Started        ← 처음 시작하기
├── Completion             ← 기본 API 사용법
├── Proxy Server           ← 서버 모드 상세
├── Supported Providers    ← 프로바이더별 설정
├── Router                 ← 로드 밸런싱, 폴백
├── Budget Manager         ← 예산 관리
└── Observability          ← 로깅, 모니터링
```

---

## 문서 빠른 참조

### 자주 찾는 페이지

| 주제 | 문서 링크 |
|------|----------|
| 빠른 시작 | [docs.litellm.ai/docs/](https://docs.litellm.ai/docs/) |
| 지원 모델 목록 | [docs.litellm.ai/docs/providers](https://docs.litellm.ai/docs/providers) |
| Proxy 설정 | [docs.litellm.ai/docs/proxy/configs](https://docs.litellm.ai/docs/proxy/configs) |
| 가상 키 | [docs.litellm.ai/docs/proxy/virtual_keys](https://docs.litellm.ai/docs/proxy/virtual_keys) |
| 로드 밸런싱 | [docs.litellm.ai/docs/routing](https://docs.litellm.ai/docs/routing) |
| 비용 추적 | [docs.litellm.ai/docs/proxy/cost_tracking](https://docs.litellm.ai/docs/proxy/cost_tracking) |

### 프로바이더별 설정

| 프로바이더 | 문서 |
|-----------|------|
| OpenAI | [docs.litellm.ai/docs/providers/openai](https://docs.litellm.ai/docs/providers/openai) |
| Anthropic | [docs.litellm.ai/docs/providers/anthropic](https://docs.litellm.ai/docs/providers/anthropic) |
| Azure | [docs.litellm.ai/docs/providers/azure](https://docs.litellm.ai/docs/providers/azure) |
| AWS Bedrock | [docs.litellm.ai/docs/providers/bedrock](https://docs.litellm.ai/docs/providers/bedrock) |
| Ollama | [docs.litellm.ai/docs/providers/ollama](https://docs.litellm.ai/docs/providers/ollama) |
| Vertex AI | [docs.litellm.ai/docs/providers/vertex](https://docs.litellm.ai/docs/providers/vertex) |

---

## 학습 자료

### 튜토리얼/가이드

| 자료 | 유형 | 대상 |
|------|------|------|
| [공식 Getting Started](https://docs.litellm.ai/docs/) | 문서 | 입문 |
| [LiteLLM GitHub Examples](https://github.com/BerriAI/litellm/tree/main/cookbook) | 코드 | 중급 |
| [Proxy Deployment Guide](https://docs.litellm.ai/docs/proxy/deploy) | 문서 | 중급 |

### 영상 자료

YouTube에서 "LiteLLM tutorial" 검색 시 관련 영상을 찾을 수 있습니다.

### 블로그/아티클

- [BerriAI 공식 블로그](https://www.litellm.ai/blog) - 업데이트, 사용 사례
- Medium/Dev.to에서 "LiteLLM" 검색 - 커뮤니티 튜토리얼

---

## 커뮤니티

### 공식 채널

| 채널 | URL | 용도 |
|------|-----|------|
| GitHub Issues | [github.com/BerriAI/litellm/issues](https://github.com/BerriAI/litellm/issues) | 버그 리포트, 기능 요청 |
| GitHub Discussions | [github.com/BerriAI/litellm/discussions](https://github.com/BerriAI/litellm/discussions) | Q&A, 아이디어 |
| Discord | 공식 문서에서 링크 확인 | 실시간 소통 |

### 질문하기 좋은 곳

1. **GitHub Issues**: 버그나 기능 관련
2. **Discord**: 빠른 도움, 일반 질문
3. **Stack Overflow**: `litellm` 태그로 검색/질문

---

## 관련 프로젝트 문서

### LLM 프로바이더

| 프로바이더 | 문서 |
|-----------|------|
| OpenAI | [platform.openai.com/docs](https://platform.openai.com/docs) |
| Anthropic | [docs.anthropic.com](https://docs.anthropic.com) |
| Azure OpenAI | [learn.microsoft.com/azure/ai-services/openai](https://learn.microsoft.com/en-us/azure/ai-services/openai/) |
| AWS Bedrock | [docs.aws.amazon.com/bedrock](https://docs.aws.amazon.com/bedrock/) |
| Ollama | [ollama.ai](https://ollama.ai) |

### 연동 프레임워크

| 프레임워크 | 문서 |
|-----------|------|
| LangChain | [python.langchain.com](https://python.langchain.com) |
| LlamaIndex | [docs.llamaindex.ai](https://docs.llamaindex.ai) |

---

## 버전 및 변경사항

### 버전 확인

```bash
# 설치된 버전 확인
pip show litellm

# 최신 버전 확인
pip index versions litellm
```

### Changelog

- [GitHub Releases](https://github.com/BerriAI/litellm/releases) - 릴리스 노트
- [CHANGELOG.md](https://github.com/BerriAI/litellm/blob/main/CHANGELOG.md) - 상세 변경사항

### 업그레이드

```bash
# 최신 버전으로 업그레이드
pip install --upgrade litellm

# 특정 버전 설치
pip install litellm==1.x.x
```

---

## 유용한 코드 저장소

### 공식 예제

```bash
# LiteLLM cookbook 클론
git clone https://github.com/BerriAI/litellm.git
cd litellm/cookbook
```

### 템플릿 프로젝트

- Docker Compose 템플릿: 공식 문서의 deployment 섹션
- Kubernetes 배포: Helm chart 또는 수동 설정

---

## 자료 정리 팁

### 북마크 추천 구조

```
LiteLLM/
├── 공식
│   ├── 문서 홈
│   ├── GitHub
│   └── PyPI
├── 학습
│   ├── Getting Started
│   ├── Proxy 설정
│   └── 프로바이더 목록
└── 참고
    ├── OpenAI 문서
    ├── Anthropic 문서
    └── LangChain 문서
```

---

## 다음 단계

- [[04-learning/01-python-sdk|Python SDK 실습]] - 코드로 시작하기
- [[04-learning/02-proxy-server|프록시 서버]] - 서버 모드 배우기
