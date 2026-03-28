# 참고 자료 및 학습 리소스

## 공식 문서

### LangChain

| 리소스 | URL | 설명 |
|--------|-----|------|
| **Python 문서** | [python.langchain.com](https://python.langchain.com) | 메인 문서 |
| **JS/TS 문서** | [js.langchain.com](https://js.langchain.com) | JavaScript 버전 |
| **API Reference** | [api.python.langchain.com](https://api.python.langchain.com) | API 상세 |
| **GitHub** | [github.com/langchain-ai/langchain](https://github.com/langchain-ai/langchain) | 소스 코드 |
| **LangSmith** | [smith.langchain.com](https://smith.langchain.com) | 모니터링 플랫폼 |
| **LangGraph** | [langchain-ai.github.io/langgraph](https://langchain-ai.github.io/langgraph) | 그래프 워크플로우 |

### CrewAI

| 리소스 | URL | 설명 |
|--------|-----|------|
| **공식 문서** | [docs.crewai.com](https://docs.crewai.com) | 메인 문서 |
| **GitHub** | [github.com/crewAIInc/crewAI](https://github.com/crewAIInc/crewAI) | 소스 코드 |
| **Examples** | [github.com/crewAIInc/crewAI-examples](https://github.com/crewAIInc/crewAI-examples) | 예제 모음 |

---

## 학습 자료

### 무료 강좌

| 강좌 | 플랫폼 | 설명 |
|------|--------|------|
| **LangChain 공식 튜토리얼** | LangChain Docs | 단계별 가이드 |
| **LangChain Academy** | LangChain | 공식 학습 과정 |
| **DeepLearning.AI LangChain** | DeepLearning.AI | Andrew Ng 협업 |
| **CrewAI Crash Course** | YouTube | 빠른 입문 |

### 추천 YouTube 채널

| 채널 | 설명 |
|------|------|
| **LangChain** | 공식 채널, 튜토리얼 |
| **AI Jason** | LangChain/CrewAI 실습 |
| **Matt Williams** | 에이전트 프레임워크 비교 |
| **Sam Witteveen** | 심층 튜토리얼 |

### 추천 블로그/아티클

| 출처 | 주제 |
|------|------|
| **LangChain 블로그** | 새 기능, 베스트 프랙티스 |
| **Towards AI** | LLM 애플리케이션 패턴 |
| **Medium - AI/ML 태그** | 실전 경험 공유 |

---

## 커뮤니티

### Discord

| 커뮤니티 | 링크 |
|----------|------|
| **LangChain Discord** | [discord.gg/langchain](https://discord.gg/langchain) |
| **CrewAI Discord** | [discord.gg/crewai](https://discord.gg/crewai) |
| **OpenAI Discord** | [discord.gg/openai](https://discord.gg/openai) |

### GitHub

- **LangChain Issues**: 버그 리포트, 기능 요청
- **LangChain Discussions**: 질문, 아이디어 공유
- **CrewAI Issues**: 버그 및 기능 요청

### 한국어 커뮤니티

| 커뮤니티 | 설명 |
|----------|------|
| **모두의AI** | AI 개발자 커뮤니티 |
| **LangChain 한국 사용자 모임** | 카카오톡 오픈채팅 |
| **AI 스터디 그룹** | 디스코드 서버 |

---

## 책

### 영문

| 제목 | 저자 | 설명 |
|------|------|------|
| **Building LLM Apps** | O'Reilly | LangChain 실전 |
| **Generative AI with LangChain** | Packt | 포괄적 가이드 |

### 한국어

| 제목 | 출판사 | 설명 |
|------|--------|------|
| **랭체인으로 LLM 기반 AI 서비스 개발하기** | 위키북스 | 한국어 입문서 |
| **만들면서 배우는 LLM 애플리케이션** | 한빛미디어 | 실습 중심 |

---

## 유용한 도구

### 개발 도구

| 도구 | 설명 |
|------|------|
| **LangSmith** | LangChain 추적, 디버깅 |
| **Langfuse** | 오픈소스 LLM 관측 |
| **Weights & Biases** | 실험 추적 |
| **Helicone** | LLM 프록시, 모니터링 |

### 테스트/평가

| 도구 | 설명 |
|------|------|
| **LangSmith Evaluation** | 평가 프레임워크 |
| **RAGAS** | RAG 평가 메트릭 |
| **DeepEval** | LLM 테스팅 |

### 벡터 DB 클라이언트

| 도구 | 설명 |
|------|------|
| **ChromaDB Dashboard** | 로컬 벡터 DB 시각화 |
| **Pinecone Console** | Pinecone 관리 UI |

---

## API 문서

### LLM 제공자

| 제공자 | API 문서 |
|--------|----------|
| **OpenAI** | [platform.openai.com/docs](https://platform.openai.com/docs) |
| **Anthropic** | [docs.anthropic.com](https://docs.anthropic.com) |
| **Google AI** | [ai.google.dev/docs](https://ai.google.dev/docs) |
| **Ollama** | [ollama.ai/docs](https://ollama.ai/docs) |

### 벡터 DB

| DB | 문서 |
|----|------|
| **ChromaDB** | [docs.trychroma.com](https://docs.trychroma.com) |
| **Pinecone** | [docs.pinecone.io](https://docs.pinecone.io) |
| **Weaviate** | [weaviate.io/developers](https://weaviate.io/developers) |

---

## 템플릿/보일러플레이트

### LangChain 템플릿

```bash
# LangChain 템플릿 확인
langchain app list

# 템플릿으로 프로젝트 시작
langchain app new my-app --package rag-conversation
```

### CrewAI 템플릿

```bash
# CrewAI 프로젝트 생성
crewai create crew my-crew

# 생성되는 구조
my-crew/
├── src/my_crew/
│   ├── config/
│   │   ├── agents.yaml
│   │   └── tasks.yaml
│   ├── crew.py
│   └── main.py
├── pyproject.toml
└── README.md
```

### GitHub 템플릿

| 템플릿 | 설명 |
|--------|------|
| **langchain-template** | 기본 LangChain 앱 |
| **langchain-rag-template** | RAG 시스템 |
| **crewai-template** | 기본 CrewAI 앱 |

---

## 학습 순서 권장

### 입문자

```
1. OpenAI API 기초
   ↓
2. LangChain 기초 (Prompt, LLM, Chain)
   ↓
3. LCEL 문법
   ↓
4. 간단한 RAG
   ↓
5. CrewAI 기초
```

### 중급자

```
1. LangChain Agent, Tools
   ↓
2. 고급 RAG (하이브리드, 리랭킹)
   ↓
3. LangSmith 활용
   ↓
4. CrewAI Flow, Memory
   ↓
5. LangGraph 기초
```

### 고급자

```
1. LangGraph 고급
   ↓
2. 프로덕션 배포
   ↓
3. 평가 시스템 구축
   ↓
4. 커스텀 에이전트 설계
```

---

## 주간 업데이트 확인

정기적으로 확인할 리소스:

- [ ] LangChain Release Notes
- [ ] CrewAI Changelog
- [ ] LangChain 블로그
- [ ] AI/LLM 뉴스레터

---

## 다음 단계

- [[04-learning/01-langchain-basics|LangChain 기초 실습]] - 코드로 배우기
- [[04-learning/04-crewai-basics|CrewAI 기초 실습]] - 에이전트 구축
