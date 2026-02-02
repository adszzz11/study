# LangChain + CrewAI 통합

## 개요

LangChain과 CrewAI를 함께 사용하여 더 강력한 AI 에이전트 시스템을 구축하는 방법을 학습한다.

---

## 1. 통합의 이점

### 각 프레임워크의 강점

```
┌─────────────────────────────────────────────────┐
│           LangChain + CrewAI 시너지             │
├─────────────────────────────────────────────────┤
│                                                 │
│  LangChain 강점:                                │
│  ├─ RAG 파이프라인                              │
│  ├─ 다양한 데이터 소스 로더                     │
│  ├─ 벡터 DB 통합                                │
│  ├─ LCEL 체인 구성                              │
│  └─ LangSmith 모니터링                          │
│                                                 │
│  CrewAI 강점:                                   │
│  ├─ 역할 기반 에이전트 설계                     │
│  ├─ 다중 에이전트 협업                          │
│  ├─ Flow 기반 워크플로우                        │
│  └─ 직관적인 팀 구성                            │
│                                                 │
│  통합 시 가능한 것:                             │
│  ├─ RAG 기반 에이전트 시스템                    │
│  ├─ LangChain 도구를 CrewAI에서 활용           │
│  ├─ 복잡한 다단계 RAG + 에이전트 워크플로우     │
│  └─ 중앙화된 모니터링 (LangSmith)               │
│                                                 │
└─────────────────────────────────────────────────┘
```

### 언제 통합을 사용할까?

| 상황 | 권장 |
|------|------|
| 단순 RAG | LangChain만 |
| 다중 에이전트 협업 | CrewAI만 |
| RAG + 에이전트 협업 | 통합 |
| 복잡한 문서 처리 + 분석 | 통합 |
| 외부 도구가 많은 에이전트 | 통합 |

---

## 2. LangChain 도구를 CrewAI에서 사용

### 기본 통합

```python
from crewai import Agent, Task, Crew
from crewai.tools import BaseTool
from langchain_community.tools import DuckDuckGoSearchRun

# LangChain 도구
langchain_search = DuckDuckGoSearchRun()

# CrewAI 도구로 래핑
class LangChainSearchTool(BaseTool):
    name: str = "웹 검색"
    description: str = "DuckDuckGo로 웹 검색을 수행합니다."

    def _run(self, query: str) -> str:
        return langchain_search.run(query)

# CrewAI에서 사용
search_tool = LangChainSearchTool()

researcher = Agent(
    role="연구원",
    goal="최신 정보 조사",
    backstory="검색 전문가",
    tools=[search_tool]
)
```

### 간편한 래퍼 함수

```python
from crewai.tools import tool
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper

# LangChain 도구 생성
wikipedia = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())

# 데코레이터로 CrewAI 도구 변환
@tool("위키피디아 검색")
def wikipedia_search(query: str) -> str:
    """
    위키피디아에서 정보를 검색합니다.

    Args:
        query: 검색할 키워드

    Returns:
        검색 결과
    """
    return wikipedia.run(query)

# 에이전트에 적용
agent = Agent(
    role="연구원",
    goal="정보 조사",
    backstory="위키피디아 전문가",
    tools=[wikipedia_search]
)
```

---

## 3. LangChain RAG + CrewAI 에이전트

### RAG 시스템을 도구로 변환

```python
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from crewai import Agent, Task, Crew
from crewai.tools import tool

# 1. LangChain RAG 파이프라인 구축
def create_rag_chain(docs_url: str):
    # 문서 로드 및 인덱싱
    loader = WebBaseLoader(docs_url)
    documents = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    chunks = splitter.split_documents(documents)

    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    vectorstore = Chroma.from_documents(chunks, embeddings)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 4})

    # RAG 체인
    llm = ChatOpenAI(model="gpt-4o-mini")
    prompt = ChatPromptTemplate.from_template("""
    컨텍스트를 참고하여 질문에 답변하세요.

    컨텍스트:
    {context}

    질문: {question}
    """)

    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    return chain

# 2. RAG 체인을 CrewAI 도구로
docs_rag = create_rag_chain("https://python.langchain.com/docs/concepts/")

@tool("문서 검색")
def search_documentation(question: str) -> str:
    """
    LangChain 공식 문서에서 정보를 검색합니다.

    Args:
        question: 검색할 질문

    Returns:
        문서 기반 답변
    """
    return docs_rag.invoke(question)

# 3. CrewAI 에이전트에서 RAG 도구 사용
doc_expert = Agent(
    role="문서 전문가",
    goal="공식 문서를 기반으로 정확한 정보 제공",
    backstory="""
    당신은 LangChain 문서 전문가입니다.
    공식 문서를 철저히 검색하여 정확한 정보를 제공합니다.
    """,
    tools=[search_documentation],
    verbose=True
)

# 태스크 및 크루
doc_task = Task(
    description="LCEL에 대해 문서를 검색하고 설명해주세요.",
    expected_output="LCEL 상세 설명",
    agent=doc_expert
)

crew = Crew(agents=[doc_expert], tasks=[doc_task])
result = crew.kickoff()
```

### 복합 RAG 시스템

```python
from crewai import Agent, Task, Crew, Process
from crewai.tools import tool
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import PyPDFLoader, WebBaseLoader

class MultiSourceRAG:
    """다중 소스 RAG 시스템"""

    def __init__(self):
        self.embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
        self.llm = ChatOpenAI(model="gpt-4o-mini")
        self.vectorstores = {}

    def add_pdf_source(self, name: str, pdf_path: str):
        loader = PyPDFLoader(pdf_path)
        self._add_source(name, loader)

    def add_web_source(self, name: str, url: str):
        loader = WebBaseLoader(url)
        self._add_source(name, loader)

    def _add_source(self, name: str, loader):
        documents = loader.load()
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, chunk_overlap=200
        )
        chunks = splitter.split_documents(documents)
        self.vectorstores[name] = Chroma.from_documents(
            chunks, self.embeddings
        )

    def query(self, source: str, question: str) -> str:
        if source not in self.vectorstores:
            return f"소스 '{source}'를 찾을 수 없습니다."

        retriever = self.vectorstores[source].as_retriever(
            search_kwargs={"k": 4}
        )
        docs = retriever.invoke(question)
        context = "\n\n".join(doc.page_content for doc in docs)

        response = self.llm.invoke(f"""
        컨텍스트를 참고하여 질문에 답변하세요.

        컨텍스트:
        {context}

        질문: {question}
        """)

        return response.content

# RAG 시스템 초기화
rag_system = MultiSourceRAG()
rag_system.add_web_source("langchain", "https://python.langchain.com/docs/")
rag_system.add_web_source("crewai", "https://docs.crewai.com/")

# CrewAI 도구로 변환
@tool("LangChain 문서 검색")
def search_langchain(question: str) -> str:
    """LangChain 문서에서 검색합니다."""
    return rag_system.query("langchain", question)

@tool("CrewAI 문서 검색")
def search_crewai(question: str) -> str:
    """CrewAI 문서에서 검색합니다."""
    return rag_system.query("crewai", question)

# 에이전트 구성
comparison_expert = Agent(
    role="프레임워크 비교 전문가",
    goal="LangChain과 CrewAI를 비교 분석한다",
    backstory="AI 프레임워크 전문가",
    tools=[search_langchain, search_crewai],
    verbose=True
)
```

---

## 4. 하이브리드 아키텍처

### LangChain 체인 + CrewAI 워크플로우

```python
from crewai.flow.flow import Flow, listen, start
from crewai import Agent, Task, Crew
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

class HybridWorkflow(Flow):
    def __init__(self):
        super().__init__()
        self.llm = ChatOpenAI(model="gpt-4o-mini")

    @start()
    def preprocess_with_langchain(self):
        """LangChain으로 전처리"""
        # LCEL 체인으로 입력 처리
        prompt = ChatPromptTemplate.from_template("""
        다음 요청을 분석하고 세부 작업으로 분해하세요:

        요청: {request}

        작업 목록 (번호로 구분):
        """)

        chain = prompt | self.llm | StrOutputParser()
        tasks = chain.invoke({"request": self.inputs.get("request", "")})

        return tasks

    @listen(preprocess_with_langchain)
    def execute_with_crewai(self, tasks):
        """CrewAI 에이전트로 실행"""
        # 동적으로 에이전트 생성
        worker = Agent(
            role="작업 실행자",
            goal="주어진 작업을 순서대로 완료한다",
            backstory="효율적인 작업 실행 전문가",
            verbose=True
        )

        execution_task = Task(
            description=f"""
            다음 작업들을 순서대로 실행하세요:

            {tasks}

            각 작업의 결과를 상세히 기록하세요.
            """,
            expected_output="작업 실행 결과 리포트",
            agent=worker
        )

        crew = Crew(
            agents=[worker],
            tasks=[execution_task]
        )

        return crew.kickoff()

    @listen(execute_with_crewai)
    def postprocess_with_langchain(self, results):
        """LangChain으로 후처리"""
        # 결과 정리 체인
        prompt = ChatPromptTemplate.from_template("""
        다음 실행 결과를 정리하여 최종 리포트를 작성하세요:

        결과:
        {results}

        최종 리포트:
        """)

        chain = prompt | self.llm | StrOutputParser()
        final_report = chain.invoke({"results": str(results)})

        return final_report

# 실행
workflow = HybridWorkflow()
result = workflow.kickoff(inputs={"request": "AI 에이전트에 대한 블로그 포스트 작성"})
print(result)
```

### 모듈화된 아키텍처

```python
from abc import ABC, abstractmethod
from typing import Any

# 추상 처리기
class Processor(ABC):
    @abstractmethod
    def process(self, input_data: Any) -> Any:
        pass

# LangChain 처리기
class LangChainProcessor(Processor):
    def __init__(self, chain):
        self.chain = chain

    def process(self, input_data: Any) -> Any:
        return self.chain.invoke(input_data)

# CrewAI 처리기
class CrewAIProcessor(Processor):
    def __init__(self, crew: Crew):
        self.crew = crew

    def process(self, input_data: Any) -> Any:
        return self.crew.kickoff(inputs=input_data)

# 파이프라인 빌더
class HybridPipeline:
    def __init__(self):
        self.processors = []

    def add(self, processor: Processor) -> "HybridPipeline":
        self.processors.append(processor)
        return self

    def run(self, input_data: Any) -> Any:
        result = input_data
        for processor in self.processors:
            result = processor.process(result)
        return result

# 사용 예
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser

llm = ChatOpenAI(model="gpt-4o-mini")

# 전처리 체인
preprocess_chain = (
    ChatPromptTemplate.from_template("분석: {input}")
    | llm
    | StrOutputParser()
)

# CrewAI 크루
analysis_crew = Crew(
    agents=[analyst],
    tasks=[analysis_task]
)

# 파이프라인 구성
pipeline = (
    HybridPipeline()
    .add(LangChainProcessor(preprocess_chain))
    .add(CrewAIProcessor(analysis_crew))
)

# 실행
result = pipeline.run({"input": "AI 시장 분석"})
```

---

## 5. LangSmith로 통합 모니터링

### 환경 설정

```bash
export LANGCHAIN_TRACING_V2=true
export LANGCHAIN_API_KEY=your-langsmith-key
export LANGCHAIN_PROJECT=langchain-crewai-integration
```

### 추적 활성화

```python
import os

# 환경 변수 설정
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "my-hybrid-project"

from langchain.callbacks.tracers import LangChainTracer
from crewai import Crew

# LangSmith 트레이서
tracer = LangChainTracer(project_name="my-hybrid-project")

# CrewAI에서도 LangChain LLM 사용 시 자동 추적
```

---

## 6. 실전 예제: 문서 분석 시스템

```python
from crewai import Agent, Task, Crew
from crewai.tools import tool
from crewai.flow.flow import Flow, listen, start
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from pydantic import BaseModel
from typing import List

# 상태 정의
class DocumentAnalysisState(BaseModel):
    file_path: str = ""
    chunks_count: int = 0
    key_topics: List[str] = []
    summary: str = ""
    insights: str = ""
    report: str = ""

class DocumentAnalysisSystem(Flow[DocumentAnalysisState]):
    def __init__(self):
        super().__init__()
        self.embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
        self.llm = ChatOpenAI(model="gpt-4o-mini")
        self.vectorstore = None
        self.retriever = None

    @start()
    def index_document(self):
        """LangChain으로 문서 인덱싱"""
        # 문서 로드
        loader = PyPDFLoader(self.state.file_path)
        documents = loader.load()

        # 분할
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        chunks = splitter.split_documents(documents)
        self.state.chunks_count = len(chunks)

        # 벡터 저장소 생성
        self.vectorstore = Chroma.from_documents(
            chunks, self.embeddings
        )
        self.retriever = self.vectorstore.as_retriever(
            search_kwargs={"k": 5}
        )

        return f"인덱싱 완료: {len(chunks)}개 청크"

    @listen(index_document)
    def analyze_with_crew(self, index_result):
        """CrewAI로 문서 분석"""

        # RAG 도구 생성
        @tool("문서 검색")
        def search_document(query: str) -> str:
            """인덱싱된 문서에서 정보를 검색합니다."""
            docs = self.retriever.invoke(query)
            return "\n\n".join(doc.page_content for doc in docs)

        # 에이전트 정의
        topic_analyst = Agent(
            role="주제 분석가",
            goal="문서의 핵심 주제를 파악한다",
            backstory="문서 분석 전문가",
            tools=[search_document],
            verbose=True
        )

        summarizer = Agent(
            role="요약 전문가",
            goal="문서를 명확하게 요약한다",
            backstory="요약 작성 전문가",
            tools=[search_document],
            verbose=True
        )

        insight_generator = Agent(
            role="인사이트 생성자",
            goal="문서에서 핵심 인사이트를 도출한다",
            backstory="분석 및 인사이트 전문가",
            tools=[search_document],
            verbose=True
        )

        # 태스크 정의
        topic_task = Task(
            description="""
            문서의 핵심 주제 5개를 파악하세요.
            문서 검색 도구를 활용하여 주요 내용을 확인하세요.
            """,
            expected_output="핵심 주제 5개 목록",
            agent=topic_analyst
        )

        summary_task = Task(
            description="""
            문서 전체를 300단어 내외로 요약하세요.
            핵심 주제들을 포함해야 합니다.
            """,
            expected_output="300단어 요약",
            agent=summarizer,
            context=[topic_task]
        )

        insight_task = Task(
            description="""
            문서에서 3-5개의 핵심 인사이트를 도출하세요.
            실행 가능한 제안이 포함되어야 합니다.
            """,
            expected_output="핵심 인사이트 목록",
            agent=insight_generator,
            context=[topic_task, summary_task]
        )

        # 크루 실행
        crew = Crew(
            agents=[topic_analyst, summarizer, insight_generator],
            tasks=[topic_task, summary_task, insight_task],
            verbose=True
        )

        result = crew.kickoff()

        # 결과 저장
        self.state.summary = summary_task.output.raw if summary_task.output else ""
        self.state.insights = insight_task.output.raw if insight_task.output else ""

        return result

    @listen(analyze_with_crew)
    def generate_report(self, analysis_result):
        """최종 리포트 생성"""

        report_writer = Agent(
            role="리포트 작성자",
            goal="분석 결과를 종합하여 리포트 작성",
            backstory="리포트 작성 전문가",
            verbose=True
        )

        report_task = Task(
            description=f"""
            다음 분석 결과를 바탕으로 최종 리포트를 작성하세요:

            요약:
            {self.state.summary}

            인사이트:
            {self.state.insights}

            리포트 구조:
            1. 개요
            2. 핵심 발견
            3. 상세 분석
            4. 결론 및 제언
            """,
            expected_output="마크다운 형식의 분석 리포트",
            agent=report_writer,
            output_file="output/document_analysis_report.md"
        )

        crew = Crew(
            agents=[report_writer],
            tasks=[report_task]
        )

        result = crew.kickoff()
        self.state.report = result.raw

        return self.state.report

# 실행
system = DocumentAnalysisSystem()
system.state.file_path = "sample_document.pdf"
result = system.kickoff()
print(result)
```

---

## 핵심 요약

```
┌─────────────────────────────────────────────────┐
│ LangChain + CrewAI 통합 핵심                     │
├─────────────────────────────────────────────────┤
│ 도구 통합:                                       │
│ - LangChain 도구 → @tool 데코레이터로 래핑      │
│ - RAG 체인 → CrewAI 도구로 변환                 │
├─────────────────────────────────────────────────┤
│ 아키텍처 패턴:                                   │
│ - LangChain: 전처리, RAG, 후처리                │
│ - CrewAI: 다중 에이전트 작업 실행               │
│ - Flow: 전체 워크플로우 조율                    │
├─────────────────────────────────────────────────┤
│ 모니터링:                                        │
│ - LangSmith로 통합 추적                          │
│ - LANGCHAIN_TRACING_V2=true                     │
└─────────────────────────────────────────────────┘
```

## 다음 단계

- [[../05-projects|실전 프로젝트]] - 완전한 애플리케이션 구축
- [[../cheatsheet|치트시트]] - 빠른 참조
