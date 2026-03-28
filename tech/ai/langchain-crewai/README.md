# LangChain & CrewAI 학습 가이드

## 개요

LLM 애플리케이션 개발과 다중 AI 에이전트 협업을 위한 핵심 프레임워크 학습 자료

## 목차

### 기초 개념
- [[01-overview|개요]] - 핵심 개념, 장단점, 사용 사례
- [[02-ecosystem|에코시스템]] - 관련 기술, 비교, 트렌드
- [[03-references|참고 자료]] - 공식 문서, 학습 자료, 커뮤니티

### 실습 학습
- [[04-learning/01-langchain-basics|LangChain 기초]] - Chain, LLM, Prompt
- [[04-learning/02-lcel|LCEL]] - LangChain Expression Language
- [[04-learning/03-rag|RAG]] - Retrieval-Augmented Generation
- [[04-learning/04-crewai-basics|CrewAI 기초]] - Agent, Task, Crew
- [[04-learning/05-crewai-advanced|CrewAI 고급]] - Flow, Tools, Memory
- [[04-learning/06-integration|통합 활용]] - LangChain + CrewAI

### 실전 적용
- [[05-projects|프로젝트]] - 실전 프로젝트, Best Practices
- [[cheatsheet|치트시트]] - 빠른 참조

---

## Quick Start

### LangChain 설치

```bash
# 기본 설치
pip install langchain langchain-openai

# 추가 패키지 (필요시)
pip install langchain-community langchain-core
pip install chromadb  # 벡터 DB
pip install langsmith  # 모니터링
```

### CrewAI 설치

```bash
# 기본 설치
pip install crewai crewai-tools

# 또는 uv 사용 (권장)
uv pip install crewai crewai-tools
```

### 환경 설정

```bash
# .env 파일 생성
export OPENAI_API_KEY="your-api-key"
export LANGCHAIN_TRACING_V2="true"  # LangSmith 활성화
export LANGCHAIN_API_KEY="your-langsmith-key"
```

### 첫 번째 LangChain 코드

```python
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

# LLM 초기화
llm = ChatOpenAI(model="gpt-4o-mini")

# 프롬프트 템플릿
prompt = ChatPromptTemplate.from_messages([
    ("system", "당신은 친절한 AI 어시스턴트입니다."),
    ("user", "{input}")
])

# LCEL로 체인 구성
chain = prompt | llm

# 실행
response = chain.invoke({"input": "안녕하세요!"})
print(response.content)
```

### 첫 번째 CrewAI 코드

```python
from crewai import Agent, Task, Crew

# 에이전트 정의
researcher = Agent(
    role="연구원",
    goal="주어진 주제에 대해 철저히 조사하기",
    backstory="당신은 경험 많은 연구원입니다."
)

# 태스크 정의
research_task = Task(
    description="AI 트렌드에 대해 조사해주세요",
    expected_output="핵심 트렌드 요약 리포트",
    agent=researcher
)

# 크루 구성 및 실행
crew = Crew(agents=[researcher], tasks=[research_task])
result = crew.kickoff()
print(result)
```

---

## 학습 플랜

### Week 1: LangChain 기초
| 일차 | 학습 내용 | 실습 |
|------|-----------|------|
| 1일 | LLM, Prompt 개념 | 기본 체인 구성 |
| 2일 | LCEL 문법 | 파이프 연산자 활용 |
| 3일 | Memory, Chat History | 대화형 챗봇 |
| 4-5일 | RAG 기초 | 문서 QA 시스템 |

### Week 2: LangChain 심화
| 일차 | 학습 내용 | 실습 |
|------|-----------|------|
| 1-2일 | Agent, Tools | 도구 사용 에이전트 |
| 3일 | Output Parser | 구조화된 출력 |
| 4-5일 | LangSmith | 디버깅 및 평가 |

### Week 3: CrewAI 기초
| 일차 | 학습 내용 | 실습 |
|------|-----------|------|
| 1일 | Agent, Task 개념 | 단일 에이전트 |
| 2일 | Crew, Process | 다중 에이전트 |
| 3일 | Tools 활용 | 커스텀 도구 |
| 4-5일 | Memory, Flow | 고급 워크플로우 |

### Week 4: 통합 및 프로젝트
| 일차 | 학습 내용 | 실습 |
|------|-----------|------|
| 1-2일 | LangChain + CrewAI | 통합 아키텍처 |
| 3-5일 | 미니 프로젝트 | 실전 애플리케이션 |

---

## 학습 팁

1. **API 키 관리**: `.env` 파일 사용, 절대 커밋하지 않기
2. **비용 관리**: `gpt-4o-mini` 모델로 시작, 토큰 사용량 모니터링
3. **디버깅**: LangSmith 적극 활용
4. **문서 참조**: 공식 문서를 자주 확인 (버전 변경 빈번)
5. **커뮤니티**: Discord, GitHub Issues 활용

---

## 관련 링크

- [LangChain 공식 문서](https://python.langchain.com)
- [CrewAI 공식 문서](https://docs.crewai.com)
- [LangSmith](https://smith.langchain.com)
- [OpenAI API](https://platform.openai.com)
