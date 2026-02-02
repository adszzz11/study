# LangChain/LlamaIndex 통합

## 개요

Firecrawl은 **LangChain**과 **LlamaIndex**에 네이티브로 통합되어 있어, RAG(Retrieval-Augmented Generation) 파이프라인을 쉽게 구축할 수 있다.

```
웹 데이터 → Firecrawl → LangChain/LlamaIndex → 벡터 DB → LLM 질의
```

---

## LangChain 통합

### 설치

```bash
pip install langchain langchain-community firecrawl-py
pip install langchain-openai chromadb  # RAG 구축 시
```

### FireCrawlLoader 기본 사용법

```python
from langchain_community.document_loaders import FireCrawlLoader

# Scrape 모드 (단일 페이지)
loader = FireCrawlLoader(
    url="https://docs.example.com/getting-started",
    api_key="fc-YOUR_API_KEY",
    mode="scrape"
)
docs = loader.load()

print(f"로드된 문서: {len(docs)}개")
print(docs[0].page_content[:500])
print(docs[0].metadata)
```

### Crawl 모드 (전체 사이트)

```python
from langchain_community.document_loaders import FireCrawlLoader

loader = FireCrawlLoader(
    url="https://docs.example.com",
    api_key="fc-YOUR_API_KEY",
    mode="crawl",
    params={
        "limit": 50,
        "scrapeOptions": {
            "formats": ["markdown"],
            "onlyMainContent": True
        }
    }
)
docs = loader.load()

print(f"크롤링된 문서: {len(docs)}개")
```

---

## LangChain RAG 파이프라인

### 전체 파이프라인

```python
from langchain_community.document_loaders import FireCrawlLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_chroma import Chroma
from langchain.chains import RetrievalQA

# 1. 웹 데이터 로드
loader = FireCrawlLoader(
    url="https://docs.langchain.com",
    api_key="fc-YOUR_API_KEY",
    mode="crawl",
    params={"limit": 100}
)
docs = loader.load()
print(f"로드된 문서: {len(docs)}개")

# 2. 청킹
splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)
chunks = splitter.split_documents(docs)
print(f"생성된 청크: {len(chunks)}개")

# 3. 벡터 저장소 생성
vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=OpenAIEmbeddings()
)

# 4. RAG 체인 구성
qa_chain = RetrievalQA.from_chain_type(
    llm=ChatOpenAI(model="gpt-4"),
    chain_type="stuff",
    retriever=vectorstore.as_retriever(search_kwargs={"k": 5})
)

# 5. 질의
response = qa_chain.invoke("LangChain에서 에이전트를 만드는 방법은?")
print(response["result"])
```

### 단계별 세부 구현

#### 데이터 로드 및 전처리

```python
def load_documentation(url, max_pages=100):
    """문서 사이트 로드 및 전처리"""
    loader = FireCrawlLoader(
        url=url,
        api_key="fc-YOUR_API_KEY",
        mode="crawl",
        params={
            "limit": max_pages,
            "scrapeOptions": {
                "formats": ["markdown"],
                "onlyMainContent": True,
                "excludeTags": ["nav", "footer", ".sidebar"]
            }
        }
    )

    docs = loader.load()

    # 빈 문서 필터링
    docs = [doc for doc in docs if len(doc.page_content.strip()) > 100]

    # 메타데이터 정리
    for doc in docs:
        doc.metadata["source_type"] = "documentation"
        doc.metadata["loaded_at"] = datetime.now().isoformat()

    return docs
```

#### 스마트 청킹

```python
from langchain.text_splitter import MarkdownHeaderTextSplitter

def smart_chunk(docs):
    """마크다운 구조를 고려한 청킹"""
    # 헤더 기반 분할
    headers_to_split_on = [
        ("#", "Header 1"),
        ("##", "Header 2"),
        ("###", "Header 3"),
    ]

    markdown_splitter = MarkdownHeaderTextSplitter(
        headers_to_split_on=headers_to_split_on
    )

    # 추가 분할 (너무 긴 청크 처리)
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    all_chunks = []
    for doc in docs:
        # 마크다운 헤더로 1차 분할
        md_chunks = markdown_splitter.split_text(doc.page_content)

        for chunk in md_chunks:
            # 메타데이터 상속
            chunk.metadata.update(doc.metadata)

        # 긴 청크 추가 분할
        final_chunks = text_splitter.split_documents(md_chunks)
        all_chunks.extend(final_chunks)

    return all_chunks
```

#### 벡터 저장소 관리

```python
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
import os

def create_or_load_vectorstore(docs=None, persist_dir="./chroma_db"):
    """벡터 저장소 생성 또는 로드"""
    embeddings = OpenAIEmbeddings()

    if docs:
        # 새로 생성
        vectorstore = Chroma.from_documents(
            documents=docs,
            embedding=embeddings,
            persist_directory=persist_dir
        )
        print(f"새 벡터 저장소 생성: {len(docs)}개 문서")
    else:
        # 기존 로드
        vectorstore = Chroma(
            persist_directory=persist_dir,
            embedding_function=embeddings
        )
        print("기존 벡터 저장소 로드")

    return vectorstore
```

---

## LlamaIndex 통합

### 설치

```bash
pip install llama-index llama-index-readers-web firecrawl-py
```

### FireCrawlWebReader 기본 사용법

```python
from llama_index.readers.web import FireCrawlWebReader

# 리더 초기화
reader = FireCrawlWebReader(
    api_key="fc-YOUR_API_KEY",
    mode="scrape"  # 또는 "crawl"
)

# 단일 페이지 로드
documents = reader.load_data(url="https://docs.example.com/getting-started")

print(f"로드된 문서: {len(documents)}개")
print(documents[0].text[:500])
```

### Crawl 모드

```python
from llama_index.readers.web import FireCrawlWebReader

reader = FireCrawlWebReader(
    api_key="fc-YOUR_API_KEY",
    mode="crawl",
    params={
        "limit": 50,
        "scrapeOptions": {"formats": ["markdown"]}
    }
)

documents = reader.load_data(url="https://docs.example.com")
```

---

## LlamaIndex RAG 파이프라인

```python
from llama_index.core import VectorStoreIndex, Settings
from llama_index.readers.web import FireCrawlWebReader
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding

# 설정
Settings.llm = OpenAI(model="gpt-4")
Settings.embed_model = OpenAIEmbedding()

# 1. 데이터 로드
reader = FireCrawlWebReader(
    api_key="fc-YOUR_API_KEY",
    mode="crawl"
)
documents = reader.load_data(url="https://docs.example.com")

# 2. 인덱스 생성
index = VectorStoreIndex.from_documents(documents)

# 3. 쿼리 엔진 생성
query_engine = index.as_query_engine()

# 4. 질의
response = query_engine.query("이 문서에서 설명하는 주요 기능은 무엇인가요?")
print(response)
```

---

## 고급 활용

### 멀티 소스 RAG

```python
from langchain_community.document_loaders import FireCrawlLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings

def build_multi_source_rag(sources):
    """여러 웹사이트에서 데이터 수집하여 통합 RAG 구축"""
    all_docs = []

    for source in sources:
        loader = FireCrawlLoader(
            url=source["url"],
            api_key="fc-YOUR_API_KEY",
            mode="crawl",
            params={"limit": source.get("limit", 50)}
        )
        docs = loader.load()

        # 소스 정보 추가
        for doc in docs:
            doc.metadata["source_name"] = source["name"]

        all_docs.extend(docs)
        print(f"{source['name']}: {len(docs)}개 문서 로드")

    # 청킹
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    chunks = splitter.split_documents(all_docs)

    # 벡터 저장소
    vectorstore = Chroma.from_documents(
        chunks,
        OpenAIEmbeddings()
    )

    return vectorstore

# 사용
sources = [
    {"name": "LangChain Docs", "url": "https://docs.langchain.com", "limit": 100},
    {"name": "OpenAI Docs", "url": "https://platform.openai.com/docs", "limit": 50},
]

vectorstore = build_multi_source_rag(sources)
```

### 실시간 웹 검색 에이전트

```python
from langchain.agents import create_openai_tools_agent, AgentExecutor
from langchain.tools import Tool
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

def search_and_scrape(query):
    """웹 검색 후 결과 페이지 스크래핑"""
    from firecrawl import FirecrawlApp

    app = FirecrawlApp(api_key="fc-YOUR_API_KEY")

    # Search API 사용 (검색 + 스크래핑)
    result = app.search(query, {"limit": 3})

    contents = []
    for item in result.get("data", []):
        contents.append(f"URL: {item['url']}\n{item['markdown'][:1000]}")

    return "\n\n---\n\n".join(contents)

# 도구 정의
web_search_tool = Tool(
    name="web_search",
    description="웹에서 정보를 검색하고 내용을 가져옵니다",
    func=search_and_scrape
)

# 에이전트 구성
llm = ChatOpenAI(model="gpt-4")
prompt = ChatPromptTemplate.from_messages([
    ("system", "당신은 웹 검색을 통해 최신 정보를 제공하는 도우미입니다."),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}")
])

agent = create_openai_tools_agent(llm, [web_search_tool], prompt)
executor = AgentExecutor(agent=agent, tools=[web_search_tool])

# 실행
response = executor.invoke({"input": "2024년 최신 AI 트렌드는?"})
print(response["output"])
```

### 증분 인덱싱

```python
def incremental_index(vectorstore, new_url):
    """기존 인덱스에 새 문서 추가"""
    loader = FireCrawlLoader(
        url=new_url,
        api_key="fc-YOUR_API_KEY",
        mode="crawl",
        params={"limit": 50}
    )
    new_docs = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    new_chunks = splitter.split_documents(new_docs)

    # 기존 벡터 저장소에 추가
    vectorstore.add_documents(new_chunks)

    print(f"{len(new_chunks)}개 청크 추가됨")
    return vectorstore
```

---

## 성능 최적화

### 배치 처리

```python
async def batch_load_urls(urls, batch_size=10):
    """URL 배치 로딩"""
    from firecrawl import FirecrawlApp
    import asyncio

    app = FirecrawlApp(api_key="fc-YOUR_API_KEY")
    all_docs = []

    for i in range(0, len(urls), batch_size):
        batch = urls[i:i+batch_size]

        # 병렬 스크래핑
        tasks = [
            asyncio.to_thread(
                app.scrape_url, url, {"formats": ["markdown"]}
            )
            for url in batch
        ]

        results = await asyncio.gather(*tasks, return_exceptions=True)

        for url, result in zip(batch, results):
            if isinstance(result, dict) and "markdown" in result:
                all_docs.append({
                    "url": url,
                    "content": result["markdown"]
                })

        print(f"진행: {min(i+batch_size, len(urls))}/{len(urls)}")

    return all_docs
```

### 캐싱

```python
from functools import lru_cache
import hashlib

@lru_cache(maxsize=100)
def cached_scrape(url):
    """스크래핑 결과 캐싱"""
    from firecrawl import FirecrawlApp

    app = FirecrawlApp(api_key="fc-YOUR_API_KEY")
    result = app.scrape_url(url, {"formats": ["markdown"]})
    return result["markdown"]
```

---

## 팁과 주의사항

### 1. 토큰 효율성

```python
# 본문만 추출하여 토큰 절약
loader = FireCrawlLoader(
    url=url,
    mode="scrape",
    params={
        "scrapeOptions": {
            "onlyMainContent": True,
            "excludeTags": ["nav", "footer", "aside"]
        }
    }
)
```

### 2. 메타데이터 활용

```python
# 검색 시 메타데이터로 필터링
retriever = vectorstore.as_retriever(
    search_kwargs={
        "k": 5,
        "filter": {"source_name": "LangChain Docs"}
    }
)
```

### 3. 에러 처리

```python
def safe_load(url):
    try:
        loader = FireCrawlLoader(url=url, mode="scrape")
        return loader.load()
    except Exception as e:
        print(f"로드 실패 {url}: {e}")
        return []
```

---

## 다음 단계

- [[06-optimization|캐싱과 비용 최적화]]
- [[../05-projects|실전 프로젝트]]
