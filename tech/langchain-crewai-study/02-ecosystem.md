# LangChain & CrewAI 에코시스템

## LangChain 에코시스템

### 핵심 패키지 구조

```
langchain 생태계
├── langchain-core       # 핵심 인터페이스, LCEL
├── langchain           # 메인 패키지, 체인, 에이전트
├── langchain-community # 서드파티 통합
├── langchain-openai    # OpenAI 통합
├── langchain-anthropic # Claude 통합
├── langsmith          # 모니터링, 디버깅
└── langgraph          # 그래프 기반 워크플로우
```

### LangChain 통합 생태계

| 카테고리 | 도구 | 설명 |
|----------|------|------|
| **LLM** | OpenAI, Anthropic, Ollama | 다양한 모델 제공자 |
| **벡터 DB** | ChromaDB, Pinecone, Weaviate | 임베딩 저장소 |
| **문서 로더** | PDF, Web, Notion, S3 | 데이터 소스 연결 |
| **검색** | Google, Tavily, DuckDuckGo | 웹 검색 통합 |
| **데이터베이스** | PostgreSQL, MySQL, SQLite | SQL 쿼리 생성 |

### LangSmith

LangChain의 공식 관측(Observability) 플랫폼

```
LangSmith 기능
├── Tracing    # 체인 실행 추적
├── Debugging  # 에러 분석
├── Testing    # 테스트 케이스 관리
├── Evaluation # 품질 평가
└── Monitoring # 프로덕션 모니터링
```

### LangGraph

복잡한 에이전트 워크플로우를 위한 그래프 기반 프레임워크

```python
from langgraph.graph import StateGraph

# 상태 기반 그래프로 복잡한 워크플로우 구성
graph = StateGraph(State)
graph.add_node("agent", agent_node)
graph.add_node("tools", tool_node)
graph.add_edge("agent", "tools")
```

---

## CrewAI 에코시스템

### 핵심 패키지 구조

```
crewai 생태계
├── crewai              # 메인 패키지
├── crewai-tools        # 내장 도구 모음
├── crewai-enterprise   # 엔터프라이즈 기능 (유료)
└── crewai-studio       # 비주얼 빌더 (개발 중)
```

### 내장 도구 (crewai-tools)

| 도구 | 설명 |
|------|------|
| `SerperDevTool` | Google 검색 |
| `WebsiteSearchTool` | 웹사이트 크롤링 |
| `FileReadTool` | 파일 읽기 |
| `DirectoryReadTool` | 디렉토리 탐색 |
| `PDFSearchTool` | PDF 검색 |
| `YoutubeVideoSearchTool` | YouTube 검색 |
| `GithubSearchTool` | GitHub 검색 |
| `CodeInterpreterTool` | 코드 실행 |

### CrewAI Flow

복잡한 워크플로우를 위한 Flow 시스템

```python
from crewai.flow.flow import Flow, listen, start

class MyFlow(Flow):
    @start()
    def first_step(self):
        return "시작"

    @listen(first_step)
    def second_step(self, result):
        return f"결과: {result}"
```

---

## 관련 기술 생태계

### LLM 제공자 비교

| 제공자 | 모델 | 특징 | 가격 |
|--------|------|------|------|
| **OpenAI** | GPT-4o, GPT-4o-mini | 가장 범용적 | 중간 |
| **Anthropic** | Claude 3.5 Sonnet | 긴 컨텍스트, 안전성 | 중간 |
| **Google** | Gemini Pro | 멀티모달 | 저렴 |
| **Ollama** | Llama 3, Mistral | 로컬 실행 | 무료 |
| **Groq** | Llama, Mixtral | 빠른 추론 | 저렴 |

### 벡터 데이터베이스 비교

| DB | 타입 | 특징 | 적합 케이스 |
|----|------|------|-------------|
| **ChromaDB** | 임베디드 | 간단, 로컬 | 프로토타입, 소규모 |
| **Pinecone** | 클라우드 | 관리형, 확장성 | 프로덕션 |
| **Weaviate** | 오픈소스 | 멀티모달 | 복잡한 검색 |
| **Qdrant** | 오픈소스 | 고성능 | 대규모 |
| **pgvector** | PostgreSQL 확장 | SQL 통합 | 기존 PG 사용 시 |

### 에이전트 프레임워크 비교

| 프레임워크 | 특징 | 적합 케이스 |
|------------|------|-------------|
| **LangChain Agent** | 유연, 도구 중심 | 단일 에이전트 |
| **LangGraph** | 그래프 기반, 복잡 워크플로우 | 조건부 로직 |
| **CrewAI** | 역할 기반, 팀 협업 | 다중 에이전트 |
| **AutoGen** | Microsoft, 대화 기반 | 연구, 실험 |
| **Agency Swarm** | 계층적 에이전트 | 복잡한 조직 |

---

## 트렌드 및 발전 방향

### 2024-2025 주요 트렌드

```
┌─────────────────────────────────────────────────┐
│              AI 에이전트 트렌드                  │
├─────────────────────────────────────────────────┤
│                                                 │
│  1. 에이전트 협업                               │
│     └─ 단일 → 다중 에이전트 시스템              │
│                                                 │
│  2. RAG 고도화                                  │
│     └─ 단순 검색 → 하이브리드, Agentic RAG     │
│                                                 │
│  3. 로컬 LLM                                    │
│     └─ 클라우드 → 온프레미스 실행              │
│                                                 │
│  4. 관측성(Observability)                       │
│     └─ 추적, 평가, 모니터링 중요성 증가         │
│                                                 │
│  5. 구조화된 출력                               │
│     └─ 텍스트 → JSON, Pydantic 스키마           │
│                                                 │
└─────────────────────────────────────────────────┘
```

### LangChain 발전 방향

1. **LCEL 중심**: 레거시 Chain에서 LCEL로 전환
2. **LangGraph 강화**: 복잡한 에이전트 워크플로우
3. **LangSmith 통합**: 전체 수명주기 관리
4. **표준화**: LangChain Expression Language 표준

### CrewAI 발전 방향

1. **Flow 시스템**: 복잡한 워크플로우 관리
2. **메모리 강화**: 장기 메모리, 지식 공유
3. **엔터프라이즈**: 대규모 배포, 관리 기능
4. **비주얼 빌더**: 코드 없이 크루 구성

---

## 기술 스택 조합 예시

### RAG 시스템 스택

```
┌─────────────────────────────────────────────────┐
│              RAG 시스템 스택                     │
├─────────────────────────────────────────────────┤
│  데이터 소스: PDF, Web, Notion                  │
│       ↓                                         │
│  로더: LangChain Document Loaders               │
│       ↓                                         │
│  임베딩: OpenAI Embeddings                      │
│       ↓                                         │
│  벡터 DB: ChromaDB (개발) / Pinecone (프로덕션) │
│       ↓                                         │
│  검색: LangChain Retriever                      │
│       ↓                                         │
│  LLM: GPT-4o-mini                               │
│       ↓                                         │
│  모니터링: LangSmith                            │
└─────────────────────────────────────────────────┘
```

### 콘텐츠 자동화 스택

```
┌─────────────────────────────────────────────────┐
│           콘텐츠 자동화 스택                     │
├─────────────────────────────────────────────────┤
│  워크플로우: CrewAI                              │
│       ↓                                         │
│  ┌──────────────────────────────────────┐      │
│  │  연구원 Agent ─────→ 작성자 Agent   │      │
│  │      ↓                    ↓         │      │
│  │  Serper 검색          편집자 Agent   │      │
│  │  LangChain RAG                      │      │
│  └──────────────────────────────────────┘      │
│       ↓                                         │
│  LLM: GPT-4o (품질) / GPT-4o-mini (비용)       │
│       ↓                                         │
│  출력: Markdown, PDF                            │
└─────────────────────────────────────────────────┘
```

---

## 패키지 버전 호환성

### LangChain 권장 버전 (2025년)

```bash
# requirements.txt
langchain>=0.2.0
langchain-core>=0.2.0
langchain-openai>=0.1.0
langchain-community>=0.2.0
chromadb>=0.4.0
```

### CrewAI 권장 버전 (2025년)

```bash
# requirements.txt
crewai>=0.30.0
crewai-tools>=0.4.0
```

### 주의사항

- LangChain은 버전 변경이 빈번함 - 공식 마이그레이션 가이드 참고
- CrewAI는 상대적으로 안정적이나 새 기능 추가가 활발함
- 프로젝트 시작 시 버전 고정 권장 (`pip freeze`)

---

## 다음 단계

- [[03-references|참고 자료]] - 학습 리소스 모음
- [[04-learning/01-langchain-basics|LangChain 기초]] - 실습 시작
