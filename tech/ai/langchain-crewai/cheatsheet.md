# LangChain & CrewAI 치트시트

## 빠른 참조

---

## 설치

```bash
# LangChain
pip install langchain langchain-openai langchain-core langchain-community
pip install chromadb  # 벡터 DB

# CrewAI
pip install crewai crewai-tools

# 환경 변수
export OPENAI_API_KEY="sk-..."
export LANGCHAIN_TRACING_V2="true"
export LANGCHAIN_API_KEY="..."
```

---

## LangChain 핵심

### LLM

```python
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)
response = llm.invoke("안녕!")
print(response.content)
```

### Prompt

```python
from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_messages([
    ("system", "당신은 {role}입니다."),
    ("human", "{input}")
])

messages = prompt.format_messages(role="번역가", input="안녕하세요")
```

### LCEL Chain

```python
from langchain_core.output_parsers import StrOutputParser

chain = prompt | llm | StrOutputParser()
result = chain.invoke({"role": "번역가", "input": "안녕"})
```

### RAG

```python
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

# 로드 & 분할
loader = PyPDFLoader("doc.pdf")
docs = loader.load()
splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
chunks = splitter.split_documents(docs)

# 인덱싱
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
vectorstore = Chroma.from_documents(chunks, embeddings)

# 검색
retriever = vectorstore.as_retriever(search_kwargs={"k": 4})
docs = retriever.invoke("질문")
```

### 실행 메서드

```python
chain.invoke(input)       # 단일 동기
chain.stream(input)       # 스트리밍
chain.batch(inputs)       # 배치
chain.ainvoke(input)      # 비동기
```

---

## LCEL 패턴

### 병렬 실행

```python
from langchain_core.runnables import RunnableParallel

parallel = RunnableParallel(
    summary=summary_chain,
    translation=translate_chain
)
result = parallel.invoke({"text": "..."})
```

### 조건부 분기

```python
from langchain_core.runnables import RunnableBranch

branch = RunnableBranch(
    (lambda x: x["type"] == "A", chain_a),
    (lambda x: x["type"] == "B", chain_b),
    default_chain
)
```

### 커스텀 함수

```python
from langchain_core.runnables import RunnableLambda

def custom_fn(x):
    return x.upper()

chain = prompt | llm | StrOutputParser() | RunnableLambda(custom_fn)
```

### 값 전달/추가

```python
from langchain_core.runnables import RunnablePassthrough

# 그대로 전달
chain = RunnablePassthrough() | llm

# 값 추가
chain = RunnablePassthrough.assign(extra=lambda x: x["a"] + x["b"])
```

---

## CrewAI 핵심

### Agent

```python
from crewai import Agent

agent = Agent(
    role="연구원",
    goal="조사 수행",
    backstory="경험 많은 연구원",
    tools=[search_tool],
    verbose=True
)
```

### Task

```python
from crewai import Task

task = Task(
    description="주제에 대해 조사하세요: {topic}",
    expected_output="조사 리포트",
    agent=agent,
    context=[previous_task],  # 의존성
    output_file="output.md"
)
```

### Crew

```python
from crewai import Crew, Process

crew = Crew(
    agents=[agent1, agent2],
    tasks=[task1, task2],
    process=Process.sequential,  # 또는 hierarchical
    verbose=True,
    memory=True
)

result = crew.kickoff(inputs={"topic": "AI"})
```

### 커스텀 도구

```python
from crewai.tools import tool

@tool("계산기")
def calculator(expression: str) -> str:
    """수학 계산을 수행합니다."""
    return str(eval(expression))
```

---

## CrewAI Flow

```python
from crewai.flow.flow import Flow, listen, start

class MyFlow(Flow):
    @start()
    def step1(self):
        return "결과1"

    @listen(step1)
    def step2(self, result):
        return f"처리: {result}"

flow = MyFlow()
result = flow.kickoff()
```

---

## 통합 패턴

### LangChain 도구 → CrewAI

```python
from crewai.tools import tool
from langchain_community.tools import DuckDuckGoSearchRun

langchain_search = DuckDuckGoSearchRun()

@tool("웹 검색")
def search(query: str) -> str:
    """웹 검색을 수행합니다."""
    return langchain_search.run(query)

agent = Agent(..., tools=[search])
```

### LangChain RAG → CrewAI 도구

```python
# RAG 체인 생성 (LangChain)
rag_chain = create_rag_chain()

# CrewAI 도구로 래핑
@tool("문서 검색")
def search_docs(question: str) -> str:
    """문서에서 정보를 검색합니다."""
    return rag_chain.invoke(question)

# CrewAI 에이전트에서 사용
agent = Agent(..., tools=[search_docs])
```

---

## 자주 사용하는 import

```python
# LangChain Core
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain_core.runnables import (
    RunnablePassthrough,
    RunnableParallel,
    RunnableBranch,
    RunnableLambda
)

# LangChain OpenAI
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

# LangChain Community
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import (
    PyPDFLoader,
    WebBaseLoader,
    TextLoader
)
from langchain.text_splitter import RecursiveCharacterTextSplitter

# CrewAI
from crewai import Agent, Task, Crew, Process
from crewai.tools import tool, BaseTool
from crewai.flow.flow import Flow, listen, start
from crewai_tools import SerperDevTool, WebsiteSearchTool

# Pydantic
from pydantic import BaseModel, Field
from typing import List, Dict, Any
```

---

## 환경 변수

```bash
# 필수
OPENAI_API_KEY=sk-...

# LangSmith (선택)
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=...
LANGCHAIN_PROJECT=my-project

# CrewAI 도구 (선택)
SERPER_API_KEY=...
```

---

## 디버깅

### LangSmith

```python
import os
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = "..."
# 이후 모든 체인 자동 추적
```

### 중간 값 출력

```python
from langchain_core.runnables import RunnableLambda

def debug(x):
    print(f"Debug: {x}")
    return x

chain = prompt | RunnableLambda(debug) | llm | RunnableLambda(debug) | parser
```

### 토큰 사용량

```python
from langchain.callbacks import get_openai_callback

with get_openai_callback() as cb:
    result = chain.invoke(input)
    print(f"Tokens: {cb.total_tokens}, Cost: ${cb.total_cost}")
```

---

## 모델 비교

| 모델 | 용도 | 비용 |
|------|------|------|
| gpt-4o | 복잡한 추론 | 높음 |
| gpt-4o-mini | 일반 작업 | 저렴 |
| text-embedding-3-small | 임베딩 | 저렴 |
| text-embedding-3-large | 고품질 임베딩 | 중간 |

---

## 빠른 시작 템플릿

### 간단한 QA 봇

```python
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

# 로드 & 인덱싱
docs = WebBaseLoader("https://...").load()
chunks = RecursiveCharacterTextSplitter(chunk_size=1000).split_documents(docs)
vectorstore = Chroma.from_documents(chunks, OpenAIEmbeddings())
retriever = vectorstore.as_retriever()

# 체인
llm = ChatOpenAI(model="gpt-4o-mini")
prompt = ChatPromptTemplate.from_template("Context: {context}\n\nQ: {question}")

chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt | llm | StrOutputParser()
)

# 실행
answer = chain.invoke("질문")
```

### 간단한 크루

```python
from crewai import Agent, Task, Crew

agent = Agent(role="작가", goal="글 작성", backstory="작가입니다")
task = Task(description="{topic}에 대해 써주세요", expected_output="글", agent=agent)
crew = Crew(agents=[agent], tasks=[task])
result = crew.kickoff(inputs={"topic": "AI"})
```

---

## 관련 링크

- [LangChain Docs](https://python.langchain.com)
- [CrewAI Docs](https://docs.crewai.com)
- [LangSmith](https://smith.langchain.com)
- [OpenAI API](https://platform.openai.com)
