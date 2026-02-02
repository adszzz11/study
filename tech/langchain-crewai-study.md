# LangChain & CrewAI 심층 스터디 가이드

> **한 줄 정의**: LangChain은 LLM 애플리케이션을 위한 통합 프레임워크, CrewAI는 다중 AI 에이전트 협업을 위한 오케스트레이션 프레임워크

---

## Part 1: 개요

### 1.1 정의 및 핵심 개념

**LangChain 3줄 요약**:
1. LLM을 다양한 데이터 소스와 도구에 연결하는 통합 프레임워크
2. 프롬프트, 체인, 에이전트, 메모리 등 LLM 앱의 핵심 컴포넌트 제공
3. LangGraph로 복잡한 상태 기반 워크플로우 구축 가능

**CrewAI 3줄 요약**:
1. 역할(Role) 기반 다중 에이전트 시스템 구축 프레임워크
2. 에이전트들이 팀(Crew)으로 협업하여 복잡한 작업 수행
3. LangChain 독립적으로 동작 (2025년 완전 분리)

**핵심 키워드**: `#LLM` `#에이전트` `#RAG` `#다중에이전트` `#자동화`

**LangChain vs CrewAI 비교**:

| 측면 | LangChain | CrewAI |
|------|-----------|--------|
| **철학** | LLM 연결 인프라 | 에이전트 협업 오케스트레이션 |
| **핵심 단위** | Chain, Agent, Tool | Crew, Agent, Task |
| **복잡도** | 유연하지만 복잡 | 역할 기반으로 직관적 |
| **상태 관리** | LangGraph 필요 | 내장 |
| **학습 곡선** | 가파름 | 비교적 완만 |
| **적합 상황** | RAG, 도구 통합 | 다중 에이전트 협업 |

### 1.2 Quick Start

**LangChain Quick Start**:
```bash
pip install langchain langchain-openai
```

```python
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# LLM 초기화
llm = ChatOpenAI(model="gpt-4o-mini")

# 프롬프트 템플릿
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant."),
    ("user", "{input}")
])

# 체인 구성 (LCEL)
chain = prompt | llm | StrOutputParser()

# 실행
response = chain.invoke({"input": "LangChain이 뭐야?"})
print(response)
```

**CrewAI Quick Start**:
```bash
pip install crewai crewai-tools
```

```python
from crewai import Agent, Task, Crew

# 에이전트 정의
researcher = Agent(
    role="연구원",
    goal="주어진 주제에 대해 깊이 있는 정보 수집",
    backstory="당신은 10년 경력의 전문 리서처입니다.",
    verbose=True
)

writer = Agent(
    role="작가",
    goal="수집된 정보를 바탕으로 명확한 글 작성",
    backstory="당신은 수상 경력의 기술 블로거입니다.",
    verbose=True
)

# 태스크 정의
research_task = Task(
    description="AI 에이전트 프레임워크에 대해 조사",
    expected_output="주요 프레임워크 5개와 각각의 장단점",
    agent=researcher
)

write_task = Task(
    description="조사 결과를 바탕으로 블로그 글 작성",
    expected_output="500단어 이상의 블로그 포스트",
    agent=writer
)

# Crew 실행
crew = Crew(
    agents=[researcher, writer],
    tasks=[research_task, write_task],
    verbose=True
)

result = crew.kickoff()
print(result)
```

### 1.3 왜 LangChain/CrewAI인가?

**LangChain 장점**:
- **가장 큰 생태계**: 다양한 통합, 도구, 예제
- **유연성**: 컴포넌트 조합으로 다양한 구조
- **RAG 최적화**: 문서 로더, 벡터 스토어 통합
- **LangGraph**: 복잡한 상태 기반 에이전트

**LangChain 단점**:
- 학습 곡선이 가파름
- 버전 변경이 잦음
- 단순 작업에 오버 엔지니어링

**CrewAI 장점**:
- **직관적 멘탈 모델**: 역할 기반 설계
- **낮은 학습 곡선**: 빠른 시작
- **협업 패턴 내장**: 에이전트 간 통신 자동
- **독립성**: LangChain 없이 동작

**CrewAI 단점**:
- LangChain보다 작은 생태계
- 커스터마이징 제한
- 복잡한 워크플로우에는 제약

---

## Part 2: 생태계 파악

### 2.1 관련 기술/용어 맵

```
┌─────────────────────────────────────────────────────────────┐
│                    LangChain 생태계                          │
├─────────────────────────────────────────────────────────────┤
│  [Core]                                                      │
│  ├── langchain-core: 기본 추상화                             │
│  ├── langchain: 체인, 에이전트, 메모리                        │
│  └── langchain-community: 서드파티 통합                      │
│                                                              │
│  [Integrations]                                              │
│  ├── langchain-openai: OpenAI 모델                           │
│  ├── langchain-anthropic: Claude 모델                        │
│  └── langchain-google-genai: Gemini 모델                     │
│                                                              │
│  [LangGraph]                                                 │
│  └── 상태 기반 에이전트 워크플로우                            │
│                                                              │
│  [LangSmith]                                                 │
│  └── 모니터링, 디버깅, 평가                                  │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                    CrewAI 생태계                             │
├─────────────────────────────────────────────────────────────┤
│  [Core]                                                      │
│  ├── Agent: 역할, 목표, 배경을 가진 AI 유닛                  │
│  ├── Task: 수행할 작업 정의                                  │
│  ├── Crew: 에이전트들의 팀                                   │
│  └── Process: 실행 방식 (sequential, hierarchical)          │
│                                                              │
│  [Tools]                                                     │
│  ├── crewai-tools: 내장 도구 (검색, 파일 등)                 │
│  └── 커스텀 도구 정의                                        │
│                                                              │
│  [Enterprise]                                                │
│  ├── CrewAI Enterprise: 관리형 서비스                        │
│  └── CrewAI Studio: 비주얼 빌더                              │
└─────────────────────────────────────────────────────────────┘
```

### 2.2 함께 자주 쓰이는 기술 스택

| 영역 | 기술 | 용도 |
|------|------|------|
| **LLM** | OpenAI, Claude, Gemini | 추론 엔진 |
| **벡터 DB** | Pinecone, Qdrant, Chroma | 임베딩 저장 |
| **문서 처리** | Docling, Unstructured | RAG 전처리 |
| **웹 도구** | Firecrawl, Browserless | 웹 데이터 수집 |
| **모니터링** | LangSmith, Helicone | 관측성 |

### 2.3 경쟁/대안 기술 비교

| 기준 | LangChain | CrewAI | AutoGen | Semantic Kernel |
|------|-----------|--------|---------|-----------------|
| **개발사** | LangChain Inc | CrewAI Inc | Microsoft | Microsoft |
| **철학** | 통합 인프라 | 역할 기반 팀 | 대화 중심 | 엔터프라이즈 |
| **다중 에이전트** | LangGraph | 네이티브 | 네이티브 | 제한적 |
| **학습 곡선** | 높음 | 낮음 | 중간 | 중간 |
| **언어** | Python/JS | Python | Python/.NET | Python/C#/Java |
| **월 다운로드** | 가장 많음 | 138만+ | 증가 중 | - |

**선택 가이드**:
- **LangChain**: RAG, 복잡한 도구 통합, 대규모 생태계 필요
- **CrewAI**: 역할 기반 다중 에이전트, 빠른 프로토타이핑
- **AutoGen**: 대화 중심 에이전트, 연구/실험
- **LangGraph**: LangChain과 함께 복잡한 워크플로우

### 2.4 최신 트렌드 및 동향 (2025)

**LangChain**:
- **LangGraph 성장**: 상태 기반 에이전트 표준화
- **LCEL (LangChain Expression Language)**: 선언적 체인 구성
- **Agent2Agent 프로토콜**: 프레임워크 간 에이전트 통신
- **MCP (Model Context Protocol)**: Anthropic과 표준화 협력

**CrewAI**:
- **LangChain 완전 분리 (2025)**: 독립 프레임워크로 성장
- **Agentic RAG**: 쿼리 재작성 등 고급 RAG
- **멀티모달 지원**: 이미지, 오디오 처리
- **벡터 DB 통합**: Qdrant, Pinecone, Weaviate 네이티브

---

## Part 3: 레퍼런스

### 3.1 공식 문서 및 필수 링크

**LangChain**:
| 리소스 | URL | 설명 |
|--------|-----|------|
| 🟢 공식 문서 | [python.langchain.com](https://python.langchain.com/docs/) | Python 문서 |
| 🟢 LangGraph | [langchain-ai.github.io/langgraph](https://langchain-ai.github.io/langgraph/) | 워크플로우 문서 |
| 🟢 GitHub | [github.com/langchain-ai/langchain](https://github.com/langchain-ai/langchain) | 소스 코드 |
| 🟡 LangSmith | [smith.langchain.com](https://smith.langchain.com/) | 모니터링 |

**CrewAI**:
| 리소스 | URL | 설명 |
|--------|-----|------|
| 🟢 공식 문서 | [docs.crewai.com](https://docs.crewai.com/) | 메인 문서 |
| 🟢 GitHub | [github.com/crewAIInc/crewAI](https://github.com/crewAIInc/crewAI) | 소스 코드 |
| 🟡 Examples | [github.com/crewAIInc/crewAI-examples](https://github.com/crewAIInc/crewAI-examples) | 예제 모음 |

### 3.2 추천 학습 자료

**🟢 입문**:
- [LangChain Quickstart](https://python.langchain.com/docs/get_started/quickstart) - 공식 시작 가이드
- [CrewAI Documentation](https://docs.crewai.com/) - 공식 문서

**🟡 중급**:
- [LangChain RAG Tutorial](https://python.langchain.com/docs/tutorials/rag/) - RAG 구축
- [CrewAI Tasks Guide](https://docs.crewai.com/en/concepts/tasks) - 태스크 심화

**🔴 고급**:
- [LangGraph Conceptual Guides](https://langchain-ai.github.io/langgraph/concepts/) - 상태 기반 에이전트
- [CrewAI Flows](https://docs.crewai.com/en/concepts/flows) - 복잡한 워크플로우

### 3.3 커뮤니티 및 질문할 곳

- **LangChain Discord**: 가장 활발한 커뮤니티
- **CrewAI Discord**: 공식 지원
- **GitHub Issues**: 버그 리포트, 기능 요청

---

## Part 4: 상세 학습 로드맵

### 4.1 LangChain 기초: LCEL과 체인

📌 **핵심 개념**

LCEL(LangChain Expression Language)은 파이프(`|`) 연산자로 컴포넌트를 연결하는 선언적 문법입니다.

💻 **코드 예제: LCEL 기본**

```python
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from pydantic import BaseModel, Field

llm = ChatOpenAI(model="gpt-4o-mini")

# 1. 기본 체인
prompt = ChatPromptTemplate.from_template(
    "다음 주제에 대해 3줄로 요약해줘: {topic}"
)
chain = prompt | llm | StrOutputParser()

result = chain.invoke({"topic": "인공지능"})
print(result)

# 2. 구조화된 출력
class Summary(BaseModel):
    title: str = Field(description="요약 제목")
    points: list[str] = Field(description="핵심 포인트 3가지")
    conclusion: str = Field(description="결론")

structured_prompt = ChatPromptTemplate.from_template(
    "다음 주제를 분석해줘: {topic}"
)

structured_chain = (
    structured_prompt
    | llm.with_structured_output(Summary)
)

summary = structured_chain.invoke({"topic": "LangChain"})
print(f"제목: {summary.title}")
print(f"포인트: {summary.points}")

# 3. 병렬 실행 (RunnableParallel)
from langchain_core.runnables import RunnableParallel

pros_chain = ChatPromptTemplate.from_template("{topic}의 장점은?") | llm | StrOutputParser()
cons_chain = ChatPromptTemplate.from_template("{topic}의 단점은?") | llm | StrOutputParser()

parallel_chain = RunnableParallel(
    pros=pros_chain,
    cons=cons_chain
)

result = parallel_chain.invoke({"topic": "Python"})
print(f"장점: {result['pros']}")
print(f"단점: {result['cons']}")

# 4. 조건부 라우팅
from langchain_core.runnables import RunnableBranch

def classify_query(query: str) -> str:
    if "코드" in query or "code" in query.lower():
        return "code"
    return "general"

code_chain = ChatPromptTemplate.from_template("코드 질문: {query}") | llm
general_chain = ChatPromptTemplate.from_template("일반 질문: {query}") | llm

router = RunnableBranch(
    (lambda x: classify_query(x["query"]) == "code", code_chain),
    general_chain  # 기본값
)

result = router.invoke({"query": "파이썬 코드 작성해줘"})
```

✅ **체크포인트**
- [ ] LCEL 문법(`|`)을 이해하는가?
- [ ] `with_structured_output()`으로 구조화 출력을 할 수 있는가?
- [ ] `RunnableParallel`로 병렬 실행을 할 수 있는가?

⚠️ **흔한 실수**
- `invoke()` 입력은 항상 딕셔너리
- 프롬프트 변수명과 입력 키 일치 필요

🔗 **더 알아보기**: [LCEL](https://python.langchain.com/docs/expression_language/)

---

### 4.2 LangChain: RAG 구축

📌 **핵심 개념**

RAG(Retrieval-Augmented Generation)는 외부 문서에서 관련 정보를 검색하여 LLM 응답을 개선합니다.

💻 **코드 예제: RAG 파이프라인**

```python
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough

# 1. 문서 로드
loader = WebBaseLoader("https://docs.prefect.io/v3/develop/write-flows")
documents = loader.load()

# 2. 청킹
splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)
chunks = splitter.split_documents(documents)

# 3. 벡터 스토어 생성
embeddings = OpenAIEmbeddings()
vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory="./chroma_db"
)

# 4. 검색기 설정
retriever = vectorstore.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 4}
)

# 5. RAG 체인 구성
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

prompt = ChatPromptTemplate.from_template("""
다음 컨텍스트를 사용하여 질문에 답변하세요.
컨텍스트에 없는 내용은 모른다고 답하세요.

컨텍스트:
{context}

질문: {question}

답변:
""")

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
)

# 6. 질문하기
answer = rag_chain.invoke("Prefect에서 flow를 어떻게 정의하나요?")
print(answer.content)
```

**고급 RAG: Reranking**:
```python
from langchain.retrievers import ContextualCompressionRetriever
from langchain_cohere import CohereRerank

# Cohere Reranker 사용
compressor = CohereRerank(top_n=3)
compression_retriever = ContextualCompressionRetriever(
    base_compressor=compressor,
    base_retriever=retriever
)

# Reranking 적용된 RAG
rag_chain_reranked = (
    {"context": compression_retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
)
```

✅ **체크포인트**
- [ ] 문서 로딩 → 청킹 → 임베딩 → 검색 흐름을 이해하는가?
- [ ] 벡터 스토어를 생성하고 검색기를 설정할 수 있는가?
- [ ] RAG 체인을 구성할 수 있는가?

⚠️ **흔한 실수**
- 청크 크기가 너무 크면 검색 정확도 저하
- 임베딩 모델과 검색 모델 일치 필요

🔗 **더 알아보기**: [RAG Tutorial](https://python.langchain.com/docs/tutorials/rag/)

---

### 4.3 LangChain: 도구와 에이전트

📌 **핵심 개념**

에이전트는 LLM이 도구를 선택하고 사용하여 작업을 수행하는 시스템입니다.

💻 **코드 예제: 도구와 에이전트**

```python
from langchain_openai import ChatOpenAI
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.tools import tool
from langchain_community.tools import DuckDuckGoSearchRun

# 1. 커스텀 도구 정의
@tool
def calculate(expression: str) -> str:
    """수학 표현식을 계산합니다. 예: '2 + 2', '10 * 5'"""
    try:
        result = eval(expression)
        return str(result)
    except:
        return "계산 오류"

@tool
def get_weather(city: str) -> str:
    """도시의 현재 날씨를 가져옵니다."""
    # 실제로는 API 호출
    return f"{city}의 날씨: 맑음, 20°C"

# 2. 도구 목록
search = DuckDuckGoSearchRun()
tools = [calculate, get_weather, search]

# 3. 프롬프트 설정
prompt = ChatPromptTemplate.from_messages([
    ("system", "당신은 도움이 되는 AI 어시스턴트입니다. 도구를 사용하여 질문에 답하세요."),
    MessagesPlaceholder(variable_name="chat_history", optional=True),
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad")
])

# 4. 에이전트 생성
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
agent = create_tool_calling_agent(llm, tools, prompt)

# 5. 에이전트 실행기
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    max_iterations=5
)

# 6. 실행
result = agent_executor.invoke({
    "input": "서울 날씨 알려주고, 123 * 456 계산해줘"
})
print(result["output"])
```

**메모리가 있는 에이전트**:
```python
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

message_history = ChatMessageHistory()

agent_with_history = RunnableWithMessageHistory(
    agent_executor,
    lambda session_id: message_history,
    input_messages_key="input",
    history_messages_key="chat_history"
)

# 대화 히스토리 유지
response1 = agent_with_history.invoke(
    {"input": "내 이름은 철수야"},
    config={"configurable": {"session_id": "user1"}}
)

response2 = agent_with_history.invoke(
    {"input": "내 이름이 뭐였지?"},
    config={"configurable": {"session_id": "user1"}}
)
```

✅ **체크포인트**
- [ ] `@tool` 데코레이터로 커스텀 도구를 만들 수 있는가?
- [ ] 에이전트를 생성하고 실행할 수 있는가?
- [ ] 메모리를 추가하여 대화 히스토리를 유지할 수 있는가?

⚠️ **흔한 실수**
- 도구 설명(docstring)이 명확해야 LLM이 올바르게 선택
- `max_iterations` 설정으로 무한 루프 방지

🔗 **더 알아보기**: [Agents](https://python.langchain.com/docs/modules/agents/)

---

### 4.4 CrewAI: 에이전트와 태스크

📌 **핵심 개념**

CrewAI의 핵심은 Agent(역할), Task(작업), Crew(팀)입니다. 각 에이전트는 명확한 역할과 목표를 가집니다.

💻 **코드 예제: 에이전트와 태스크 정의**

```python
from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool, WebsiteSearchTool

# 1. 도구 설정
search_tool = SerperDevTool()  # Google 검색
web_tool = WebsiteSearchTool()  # 웹사이트 검색

# 2. 에이전트 정의
researcher = Agent(
    role="시장 분석가",
    goal="AI 시장 동향과 주요 플레이어 분석",
    backstory="""
    당신은 10년 경력의 테크 시장 분석가입니다.
    시장 트렌드를 파악하고 통찰력 있는 분석을 제공합니다.
    """,
    tools=[search_tool, web_tool],
    verbose=True,
    allow_delegation=False  # 다른 에이전트에게 위임 금지
)

analyst = Agent(
    role="데이터 분석가",
    goal="수집된 정보를 바탕으로 정량적 분석 수행",
    backstory="""
    당신은 데이터 기반 의사결정 전문가입니다.
    복잡한 데이터를 명확한 인사이트로 변환합니다.
    """,
    verbose=True
)

writer = Agent(
    role="보고서 작성자",
    goal="분석 결과를 명확하고 설득력 있는 보고서로 작성",
    backstory="""
    당신은 비즈니스 커뮤니케이션 전문가입니다.
    복잡한 정보를 이해하기 쉽게 전달합니다.
    """,
    verbose=True
)

# 3. 태스크 정의
research_task = Task(
    description="""
    AI 에이전트 프레임워크 시장을 조사하세요:
    1. 주요 5개 프레임워크 식별
    2. 각 프레임워크의 장단점
    3. 시장 점유율 및 성장 추이
    """,
    expected_output="각 프레임워크에 대한 상세 조사 결과",
    agent=researcher
)

analysis_task = Task(
    description="""
    조사 결과를 분석하세요:
    1. 프레임워크 비교 매트릭스 작성
    2. 사용 사례별 추천
    3. 미래 트렌드 예측
    """,
    expected_output="비교 분석 표와 추천 사항",
    agent=analyst,
    context=[research_task]  # 이전 태스크 결과 참조
)

report_task = Task(
    description="""
    분석 결과를 바탕으로 보고서를 작성하세요:
    1. 임원 요약 (1페이지)
    2. 상세 분석 (3-5페이지)
    3. 추천 및 결론
    """,
    expected_output="완성된 시장 분석 보고서",
    agent=writer,
    context=[research_task, analysis_task]
)

# 4. Crew 생성 및 실행
crew = Crew(
    agents=[researcher, analyst, writer],
    tasks=[research_task, analysis_task, report_task],
    process=Process.sequential,  # 순차 실행
    verbose=True
)

result = crew.kickoff()
print(result)
```

**태스크 가드레일**:
```python
from crewai import Task
from pydantic import BaseModel

# 출력 스키마 정의
class MarketReport(BaseModel):
    summary: str
    key_findings: list[str]
    recommendations: list[str]

# 가드레일 적용 태스크
report_task = Task(
    description="시장 분석 보고서 작성",
    expected_output="구조화된 시장 보고서",
    agent=writer,
    output_pydantic=MarketReport  # 출력 검증
)
```

✅ **체크포인트**
- [ ] Agent의 role, goal, backstory를 설정할 수 있는가?
- [ ] Task 간 의존성(context)을 설정할 수 있는가?
- [ ] 출력 스키마로 결과를 검증할 수 있는가?

⚠️ **흔한 실수**
- backstory가 너무 짧으면 에이전트 행동이 불명확
- context 순서 중요 (이전 태스크 먼저)

🔗 **더 알아보기**: [Tasks](https://docs.crewai.com/en/concepts/tasks)

---

### 4.5 CrewAI: 프로세스와 협업

📌 **핵심 개념**

CrewAI는 Sequential(순차), Hierarchical(계층적) 프로세스를 지원합니다.

💻 **코드 예제: 다양한 프로세스**

```python
from crewai import Agent, Task, Crew, Process

# 1. Sequential (순차) - 기본값
sequential_crew = Crew(
    agents=[researcher, analyst, writer],
    tasks=[task1, task2, task3],
    process=Process.sequential
)

# 2. Hierarchical (계층적) - 매니저가 조율
manager = Agent(
    role="프로젝트 매니저",
    goal="팀을 조율하고 프로젝트 완수",
    backstory="당신은 경험 많은 프로젝트 매니저입니다."
)

hierarchical_crew = Crew(
    agents=[researcher, analyst, writer],
    tasks=[task1, task2, task3],
    process=Process.hierarchical,
    manager_agent=manager  # 매니저 지정
)

# 3. 에이전트 위임 (Delegation)
delegating_agent = Agent(
    role="팀 리더",
    goal="작업 분배 및 조율",
    backstory="...",
    allow_delegation=True  # 다른 에이전트에게 위임 가능
)

# 4. 콜백으로 모니터링
def task_callback(task_output):
    print(f"태스크 완료: {task_output.description}")
    print(f"결과: {task_output.raw[:100]}...")

crew = Crew(
    agents=[researcher, writer],
    tasks=[task1, task2],
    task_callback=task_callback
)

# 5. 입력 변수 전달
crew = Crew(
    agents=[researcher],
    tasks=[Task(
        description="다음 주제를 조사: {topic}",
        expected_output="조사 결과",
        agent=researcher
    )]
)

result = crew.kickoff(inputs={"topic": "LangChain vs CrewAI"})
```

**비동기 실행**:
```python
import asyncio

async def run_crew():
    crew = Crew(agents=[...], tasks=[...])
    result = await crew.kickoff_async()
    return result

# 여러 Crew 병렬 실행
async def parallel_crews():
    crew1 = Crew(agents=[...], tasks=[...])
    crew2 = Crew(agents=[...], tasks=[...])

    results = await asyncio.gather(
        crew1.kickoff_async(),
        crew2.kickoff_async()
    )
    return results
```

✅ **체크포인트**
- [ ] Sequential과 Hierarchical 프로세스의 차이를 이해하는가?
- [ ] 입력 변수를 태스크에 전달할 수 있는가?
- [ ] 콜백으로 실행을 모니터링할 수 있는가?

⚠️ **흔한 실수**
- Hierarchical은 추가 LLM 호출로 비용 증가
- 위임은 명확한 역할 분리 시에만 효과적

🔗 **더 알아보기**: [Processes](https://docs.crewai.com/en/concepts/processes)

---

### 4.6 LangGraph: 상태 기반 에이전트

📌 **핵심 개념**

LangGraph는 그래프 기반 상태 관리로 복잡한 에이전트 워크플로우를 구축합니다.

💻 **코드 예제: LangGraph 기본**

```python
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage
from typing import TypedDict, Annotated
import operator

# 1. 상태 정의
class AgentState(TypedDict):
    messages: Annotated[list, operator.add]
    next_step: str

# 2. 노드 함수 정의
llm = ChatOpenAI(model="gpt-4o-mini")

def researcher_node(state: AgentState) -> AgentState:
    """조사 수행"""
    messages = state["messages"]
    response = llm.invoke(messages + [HumanMessage(content="이 주제를 조사해줘")])
    return {"messages": [response], "next_step": "analyst"}

def analyst_node(state: AgentState) -> AgentState:
    """분석 수행"""
    messages = state["messages"]
    response = llm.invoke(messages + [HumanMessage(content="이 정보를 분석해줘")])
    return {"messages": [response], "next_step": "end"}

# 3. 라우터 함수
def router(state: AgentState) -> str:
    return state["next_step"]

# 4. 그래프 구성
workflow = StateGraph(AgentState)

# 노드 추가
workflow.add_node("researcher", researcher_node)
workflow.add_node("analyst", analyst_node)

# 엣지 추가
workflow.set_entry_point("researcher")
workflow.add_conditional_edges(
    "researcher",
    router,
    {"analyst": "analyst", "end": END}
)
workflow.add_conditional_edges(
    "analyst",
    router,
    {"end": END}
)

# 5. 컴파일 및 실행
app = workflow.compile()

result = app.invoke({
    "messages": [HumanMessage(content="AI 에이전트에 대해 알려줘")],
    "next_step": "researcher"
})

for msg in result["messages"]:
    print(msg.content)
```

**체크포인트와 Human-in-the-loop**:
```python
from langgraph.checkpoint.memory import MemorySaver

# 체크포인터 설정
memory = MemorySaver()
app = workflow.compile(checkpointer=memory)

# 중간 상태 저장
config = {"configurable": {"thread_id": "session1"}}
result = app.invoke(initial_state, config)

# 나중에 재개
resumed = app.invoke(None, config)  # 저장된 상태에서 재개
```

✅ **체크포인트**
- [ ] StateGraph의 노드와 엣지를 정의할 수 있는가?
- [ ] 조건부 라우팅을 구현할 수 있는가?
- [ ] 체크포인트로 상태를 저장/복원할 수 있는가?

⚠️ **흔한 실수**
- 상태 업데이트는 불변(immutable) 방식
- 순환 그래프 주의 (무한 루프 방지)

🔗 **더 알아보기**: [LangGraph](https://langchain-ai.github.io/langgraph/)

---

## Part 5: 실전 프로젝트

### 5.1 미니 프로젝트 아이디어

| 난이도 | 프로젝트 | 학습 포인트 |
|--------|---------|------------|
| 🟢 | 문서 QA 챗봇 | LangChain RAG |
| 🟢 | 뉴스 요약 봇 | CrewAI 기본 |
| 🟡 | 연구 논문 분석기 | 다중 에이전트 |
| 🟡 | 코드 리뷰 에이전트 | 도구 통합 |
| 🔴 | 자동 콘텐츠 생성 파이프라인 | Crew + LangGraph |

### 5.2 단계별 구현 가이드: 리서치 팀 에이전트

**목표**: 주제를 조사하고 보고서를 작성하는 다중 에이전트 시스템

```python
# research_crew.py
from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool
from langchain_openai import ChatOpenAI
import os

class ResearchCrew:
    def __init__(self):
        os.environ["OPENAI_API_KEY"] = "your-key"
        os.environ["SERPER_API_KEY"] = "your-key"

        self.search_tool = SerperDevTool()
        self._setup_agents()
        self._setup_tasks()

    def _setup_agents(self):
        self.researcher = Agent(
            role="Senior Research Analyst",
            goal="Conduct thorough research on given topics",
            backstory="""You are a senior research analyst with 15 years of experience
            in technology and market research. You excel at finding reliable sources
            and synthesizing complex information.""",
            tools=[self.search_tool],
            verbose=True
        )

        self.analyst = Agent(
            role="Data Analyst",
            goal="Analyze research findings and extract insights",
            backstory="""You are a data analyst specializing in trend analysis
            and market intelligence. You turn raw data into actionable insights.""",
            verbose=True
        )

        self.writer = Agent(
            role="Technical Writer",
            goal="Create clear, comprehensive reports",
            backstory="""You are a technical writer with expertise in creating
            executive summaries and detailed reports for business audiences.""",
            verbose=True
        )

    def _setup_tasks(self):
        self.research_task = Task(
            description="""
            Research the following topic: {topic}

            Your research should include:
            1. Current state and trends
            2. Key players and their offerings
            3. Recent developments (last 6 months)
            4. Future outlook

            Use reliable sources and cite them.
            """,
            expected_output="Comprehensive research findings with sources",
            agent=self.researcher
        )

        self.analysis_task = Task(
            description="""
            Analyze the research findings and provide:
            1. SWOT analysis
            2. Comparison matrix of key players
            3. Key insights and patterns
            4. Risk factors to consider
            """,
            expected_output="Structured analysis with insights",
            agent=self.analyst,
            context=[self.research_task]
        )

        self.report_task = Task(
            description="""
            Write a professional report including:
            1. Executive Summary (1 paragraph)
            2. Key Findings (bullet points)
            3. Detailed Analysis
            4. Recommendations
            5. Conclusion

            Format the report in Markdown.
            """,
            expected_output="Complete report in Markdown format",
            agent=self.writer,
            context=[self.research_task, self.analysis_task]
        )

    def run(self, topic: str) -> str:
        crew = Crew(
            agents=[self.researcher, self.analyst, self.writer],
            tasks=[self.research_task, self.analysis_task, self.report_task],
            process=Process.sequential,
            verbose=True
        )

        result = crew.kickoff(inputs={"topic": topic})
        return result

# 실행
if __name__ == "__main__":
    crew = ResearchCrew()
    report = crew.run("AI Agent Frameworks in 2025")
    print(report)

    # 파일로 저장
    with open("report.md", "w") as f:
        f.write(str(report))
```

### 5.3 Best Practices

**프로젝트 구조**:
```
ai-agents-project/
├── src/
│   ├── agents/
│   │   ├── researcher.py
│   │   └── writer.py
│   ├── tasks/
│   │   └── research_tasks.py
│   ├── tools/
│   │   └── custom_tools.py
│   └── crews/
│       └── research_crew.py
├── config/
│   ├── agents.yaml
│   └── tasks.yaml
├── tests/
├── .env
└── main.py
```

**운영 권장사항**:

1. **비용 관리**: 토큰 사용량 모니터링 (LangSmith)
2. **에러 처리**: 재시도 로직, 폴백 전략
3. **로깅**: 모든 에이전트 행동 기록
4. **테스트**: 단위 테스트, 프롬프트 테스트
5. **버전 관리**: 프롬프트와 설정 버전 관리

```python
# 에러 처리 예시
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4, max=10)
)
def safe_crew_run(crew, inputs):
    try:
        return crew.kickoff(inputs=inputs)
    except Exception as e:
        print(f"Error: {e}")
        raise
```

---

## 요약

LangChain과 CrewAI는 각각의 강점이 있는 AI 에이전트 프레임워크입니다:

**LangChain**:
- RAG, 도구 통합, 복잡한 체인에 최적
- LCEL로 선언적 파이프라인 구성
- LangGraph로 상태 기반 워크플로우

**CrewAI**:
- 역할 기반 다중 에이전트에 최적
- 직관적인 Agent-Task-Crew 모델
- 빠른 프로토타이핑

다음 단계:
1. LangChain: [RAG Tutorial](https://python.langchain.com/docs/tutorials/rag/) 따라하기
2. CrewAI: [공식 문서](https://docs.crewai.com/) 예제 실행
3. 간단한 다중 에이전트 프로젝트 구현
