# RAG - Retrieval-Augmented Generation

## 개요

RAG(Retrieval-Augmented Generation)는 외부 문서를 검색하여 LLM의 답변에 활용하는 기법이다. LLM의 지식 한계를 극복하고 최신 정보, 도메인 특화 지식을 제공할 수 있다.

---

## 1. RAG 아키텍처

### 기본 구조

```
┌─────────────────────────────────────────────────────────────┐
│                      RAG 파이프라인                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  [인덱싱 단계]                                              │
│  문서 → 로더 → 분할 → 임베딩 → 벡터 DB                      │
│                                                             │
│  [검색 단계]                                                │
│  질문 → 임베딩 → 유사도 검색 → 관련 문서                    │
│                                                             │
│  [생성 단계]                                                │
│  질문 + 관련 문서 → 프롬프트 → LLM → 답변                   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 핵심 컴포넌트

| 컴포넌트 | 역할 | LangChain 클래스 |
|----------|------|------------------|
| Document Loader | 문서 로드 | PyPDFLoader, WebBaseLoader |
| Text Splitter | 문서 분할 | RecursiveCharacterTextSplitter |
| Embeddings | 텍스트 → 벡터 | OpenAIEmbeddings |
| Vector Store | 벡터 저장/검색 | Chroma, Pinecone |
| Retriever | 관련 문서 검색 | VectorStoreRetriever |

---

## 2. 환경 설정

### 패키지 설치

```bash
pip install langchain langchain-openai langchain-community
pip install chromadb          # 벡터 DB
pip install pypdf             # PDF 처리
pip install beautifulsoup4    # 웹 크롤링
```

### 기본 import

```python
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import PyPDFLoader, WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
```

---

## 3. 인덱싱 단계

### 3.1 Document Loader

```python
# PDF 로더
from langchain_community.document_loaders import PyPDFLoader

loader = PyPDFLoader("document.pdf")
documents = loader.load()

# 웹 페이지 로더
from langchain_community.document_loaders import WebBaseLoader

loader = WebBaseLoader("https://example.com")
documents = loader.load()

# 디렉토리 로더
from langchain_community.document_loaders import DirectoryLoader

loader = DirectoryLoader("./docs", glob="**/*.txt")
documents = loader.load()
```

### 주요 로더 종류

| 로더 | 소스 | 패키지 |
|------|------|--------|
| PyPDFLoader | PDF 파일 | pypdf |
| WebBaseLoader | 웹 페이지 | beautifulsoup4 |
| TextLoader | 텍스트 파일 | - |
| CSVLoader | CSV 파일 | - |
| NotionDBLoader | Notion | notion-client |
| GitHubLoader | GitHub | pygithub |

### 3.2 Text Splitter

```python
from langchain.text_splitter import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,      # 청크 크기
    chunk_overlap=200,    # 청크 간 중복
    separators=["\n\n", "\n", " ", ""]  # 분할 기준
)

chunks = splitter.split_documents(documents)
print(f"총 {len(chunks)}개 청크 생성")
```

### 청크 크기 가이드라인

| 용도 | chunk_size | chunk_overlap |
|------|------------|---------------|
| 일반 문서 | 500-1000 | 50-200 |
| 기술 문서 | 1000-1500 | 200-300 |
| 코드 | 1500-2000 | 100-200 |
| Q&A | 300-500 | 50-100 |

### 3.3 Embeddings

```python
from langchain_openai import OpenAIEmbeddings

# OpenAI 임베딩
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

# 단일 텍스트 임베딩
vector = embeddings.embed_query("안녕하세요")
print(f"벡터 차원: {len(vector)}")  # 1536

# 여러 텍스트 임베딩
vectors = embeddings.embed_documents(["텍스트1", "텍스트2"])
```

### 임베딩 모델 비교

| 모델 | 차원 | 비용 | 성능 |
|------|------|------|------|
| text-embedding-3-small | 1536 | 저렴 | 좋음 |
| text-embedding-3-large | 3072 | 중간 | 매우 좋음 |
| text-embedding-ada-002 | 1536 | 저렴 | 좋음 (레거시) |

### 3.4 Vector Store

```python
from langchain_community.vectorstores import Chroma

# 벡터 저장소 생성
vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory="./chroma_db"  # 영구 저장
)

# 이미 있는 저장소 로드
vectorstore = Chroma(
    persist_directory="./chroma_db",
    embedding_function=embeddings
)
```

### 주요 벡터 DB

| DB | 타입 | 특징 |
|----|------|------|
| Chroma | 임베디드 | 로컬 개발에 적합 |
| Pinecone | 클라우드 | 관리형, 확장성 |
| Weaviate | 하이브리드 | 멀티모달 지원 |
| pgvector | PostgreSQL | SQL 통합 |

---

## 4. 검색 단계

### 기본 Retriever

```python
# 벡터 스토어에서 retriever 생성
retriever = vectorstore.as_retriever(
    search_type="similarity",  # 검색 타입
    search_kwargs={"k": 4}     # 반환할 문서 수
)

# 검색 실행
docs = retriever.invoke("LangChain이 뭐야?")
for doc in docs:
    print(doc.page_content[:100])
```

### 검색 타입

| 타입 | 설명 | 사용 시점 |
|------|------|-----------|
| similarity | 유사도 기반 | 기본 검색 |
| mmr | 다양성 고려 (Maximum Marginal Relevance) | 중복 방지 |
| similarity_score_threshold | 점수 임계값 | 품질 필터링 |

```python
# MMR 검색 (다양성 확보)
retriever = vectorstore.as_retriever(
    search_type="mmr",
    search_kwargs={
        "k": 4,
        "fetch_k": 10,     # 후보군 크기
        "lambda_mult": 0.5  # 다양성 가중치 (0-1)
    }
)

# 점수 기반 필터링
retriever = vectorstore.as_retriever(
    search_type="similarity_score_threshold",
    search_kwargs={
        "score_threshold": 0.8,
        "k": 4
    }
)
```

### 메타데이터 필터링

```python
# 메타데이터가 포함된 문서
from langchain_core.documents import Document

docs = [
    Document(
        page_content="LangChain 소개...",
        metadata={"source": "docs", "category": "tutorial"}
    ),
    Document(
        page_content="RAG 구현하기...",
        metadata={"source": "blog", "category": "advanced"}
    )
]

# 메타데이터 필터 검색
retriever = vectorstore.as_retriever(
    search_kwargs={
        "k": 4,
        "filter": {"category": "tutorial"}
    }
)
```

---

## 5. 생성 단계

### 기본 RAG 체인

```python
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

llm = ChatOpenAI(model="gpt-4o-mini")

# RAG 프롬프트
prompt = ChatPromptTemplate.from_template("""
다음 컨텍스트를 참고하여 질문에 답변하세요.
컨텍스트에 답이 없으면 "모르겠습니다"라고 답하세요.

컨텍스트:
{context}

질문: {question}

답변:
""")

# 문서 포맷팅 함수
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

# RAG 체인
rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

# 실행
answer = rag_chain.invoke("LangChain이 뭐야?")
print(answer)
```

### 출처 포함 RAG

```python
from langchain_core.runnables import RunnableParallel

# 문서와 함께 출처 반환
def format_docs_with_source(docs):
    formatted = []
    for doc in docs:
        source = doc.metadata.get('source', 'Unknown')
        formatted.append(f"[출처: {source}]\n{doc.page_content}")
    return "\n\n".join(formatted)

rag_chain_with_source = (
    RunnableParallel(
        context=retriever | format_docs_with_source,
        question=RunnablePassthrough()
    )
    | prompt
    | llm
    | StrOutputParser()
)
```

---

## 6. 전체 RAG 파이프라인

### 완전한 예제

```python
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

# 1. 문서 로드
loader = WebBaseLoader("https://python.langchain.com/docs/concepts/")
documents = loader.load()

# 2. 문서 분할
splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)
chunks = splitter.split_documents(documents)

# 3. 임베딩 및 벡터 저장소 생성
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings
)

# 4. Retriever 생성
retriever = vectorstore.as_retriever(search_kwargs={"k": 4})

# 5. LLM 및 프롬프트
llm = ChatOpenAI(model="gpt-4o-mini")

prompt = ChatPromptTemplate.from_template("""
당신은 LangChain 전문가입니다.
주어진 컨텍스트를 바탕으로 질문에 상세히 답변하세요.

컨텍스트:
{context}

질문: {question}

답변:
""")

# 6. RAG 체인 구성
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

# 7. 실행
question = "LCEL이란 무엇인가요?"
answer = rag_chain.invoke(question)
print(answer)
```

---

## 7. 고급 RAG 기법

### 7.1 하이브리드 검색

키워드 검색과 벡터 검색을 결합

```python
from langchain.retrievers import EnsembleRetriever
from langchain_community.retrievers import BM25Retriever

# 키워드 검색 (BM25)
bm25_retriever = BM25Retriever.from_documents(chunks)
bm25_retriever.k = 4

# 벡터 검색
vector_retriever = vectorstore.as_retriever(search_kwargs={"k": 4})

# 앙상블 (하이브리드)
ensemble_retriever = EnsembleRetriever(
    retrievers=[bm25_retriever, vector_retriever],
    weights=[0.5, 0.5]
)
```

### 7.2 Re-ranking

검색 결과를 재정렬하여 품질 향상

```python
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import CrossEncoderReranker
from langchain_community.cross_encoders import HuggingFaceCrossEncoder

# 크로스 인코더 리랭커
model = HuggingFaceCrossEncoder(model_name="BAAI/bge-reranker-base")
compressor = CrossEncoderReranker(model=model, top_n=3)

# 압축 리트리버
compression_retriever = ContextualCompressionRetriever(
    base_compressor=compressor,
    base_retriever=retriever
)
```

### 7.3 Multi-Query

다양한 쿼리로 검색 범위 확대

```python
from langchain.retrievers.multi_query import MultiQueryRetriever

# 다중 쿼리 생성
multi_query_retriever = MultiQueryRetriever.from_llm(
    retriever=retriever,
    llm=llm
)

# 원래 질문을 여러 관점으로 변환하여 검색
docs = multi_query_retriever.invoke("LangChain 사용법")
```

### 7.4 Self-Query

자연어 쿼리를 구조화된 필터로 변환

```python
from langchain.retrievers.self_query.base import SelfQueryRetriever
from langchain.chains.query_constructor.base import AttributeInfo

# 메타데이터 속성 정의
metadata_field_info = [
    AttributeInfo(
        name="category",
        description="문서 카테고리 (tutorial, reference, guide)",
        type="string"
    ),
    AttributeInfo(
        name="date",
        description="문서 작성일",
        type="string"
    )
]

self_query_retriever = SelfQueryRetriever.from_llm(
    llm=llm,
    vectorstore=vectorstore,
    document_contents="LangChain 관련 문서",
    metadata_field_info=metadata_field_info
)

# "최근 튜토리얼 문서" → category="tutorial" 필터 자동 적용
docs = self_query_retriever.invoke("최근 튜토리얼 문서 찾아줘")
```

---

## 8. 대화형 RAG (Chat History)

### 대화 기록을 포함한 RAG

```python
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain.chains import create_history_aware_retriever

# 대화 기록을 고려한 검색 프롬프트
contextualize_prompt = ChatPromptTemplate.from_messages([
    ("system", "대화 기록을 참고하여 독립적인 질문을 생성하세요."),
    MessagesPlaceholder("chat_history"),
    ("human", "{input}")
])

# 히스토리 인식 리트리버
history_aware_retriever = create_history_aware_retriever(
    llm, retriever, contextualize_prompt
)

# 답변 생성 프롬프트
qa_prompt = ChatPromptTemplate.from_messages([
    ("system", "컨텍스트를 참고하여 답변하세요:\n\n{context}"),
    MessagesPlaceholder("chat_history"),
    ("human", "{input}")
])

# 체인 구성
question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)
rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)

# 대화 기록과 함께 사용
chat_history = [
    HumanMessage(content="LangChain이 뭐야?"),
    AIMessage(content="LangChain은 LLM 애플리케이션 프레임워크입니다.")
]

result = rag_chain.invoke({
    "chat_history": chat_history,
    "input": "그것의 주요 기능은?"  # "그것" = LangChain
})

print(result["answer"])
```

---

## 9. 평가 및 모니터링

### RAG 평가 지표

| 지표 | 설명 |
|------|------|
| **Faithfulness** | 답변이 컨텍스트에 충실한가 |
| **Answer Relevance** | 답변이 질문에 관련 있는가 |
| **Context Relevance** | 검색된 문서가 관련 있는가 |
| **Context Recall** | 필요한 정보가 모두 검색되었는가 |

### RAGAS로 평가

```python
from ragas import evaluate
from ragas.metrics import (
    faithfulness,
    answer_relevancy,
    context_precision,
    context_recall
)
from datasets import Dataset

# 평가 데이터 준비
data = {
    "question": ["LangChain이 뭐야?"],
    "answer": ["LangChain은 LLM 애플리케이션 개발 프레임워크입니다."],
    "contexts": [["LangChain은 LLM 기반 앱을 쉽게 개발..."]],
    "ground_truth": ["LangChain은 LLM 앱 프레임워크이다."]
}

dataset = Dataset.from_dict(data)

# 평가 실행
results = evaluate(
    dataset,
    metrics=[faithfulness, answer_relevancy, context_precision, context_recall]
)

print(results)
```

---

## 10. 실습 프로젝트

### 미니 프로젝트: 문서 QA 봇

```python
import os
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

class DocumentQA:
    def __init__(self, docs_dir: str, persist_dir: str = "./chroma_db"):
        self.embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
        self.llm = ChatOpenAI(model="gpt-4o-mini")
        self.persist_dir = persist_dir

        # 벡터 저장소 로드 또는 생성
        if os.path.exists(persist_dir):
            self.vectorstore = Chroma(
                persist_directory=persist_dir,
                embedding_function=self.embeddings
            )
        else:
            self._index_documents(docs_dir)

        self._setup_chain()

    def _index_documents(self, docs_dir: str):
        # 문서 로드
        loader = DirectoryLoader(docs_dir, glob="**/*.txt", loader_cls=TextLoader)
        documents = loader.load()

        # 분할
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        chunks = splitter.split_documents(documents)

        # 벡터 저장소 생성
        self.vectorstore = Chroma.from_documents(
            documents=chunks,
            embedding=self.embeddings,
            persist_directory=self.persist_dir
        )

    def _setup_chain(self):
        retriever = self.vectorstore.as_retriever(search_kwargs={"k": 4})

        prompt = ChatPromptTemplate.from_template("""
        다음 컨텍스트를 참고하여 질문에 답변하세요.

        컨텍스트:
        {context}

        질문: {question}

        답변:
        """)

        def format_docs(docs):
            return "\n\n".join(doc.page_content for doc in docs)

        self.chain = (
            {"context": retriever | format_docs, "question": RunnablePassthrough()}
            | prompt
            | self.llm
            | StrOutputParser()
        )

    def ask(self, question: str) -> str:
        return self.chain.invoke(question)

# 사용
qa = DocumentQA("./my_docs")
answer = qa.ask("프로젝트 개요가 뭐야?")
print(answer)
```

---

## 핵심 요약

```
┌─────────────────────────────────────────────────┐
│ RAG 핵심 요약                                    │
├─────────────────────────────────────────────────┤
│ 인덱싱: 로드 → 분할 → 임베딩 → 벡터 저장        │
│ 검색: 질문 임베딩 → 유사도 검색 → 문서 반환     │
│ 생성: 질문 + 문서 → 프롬프트 → LLM → 답변       │
├─────────────────────────────────────────────────┤
│ 핵심 컴포넌트:                                   │
│ - Loader: PyPDFLoader, WebBaseLoader            │
│ - Splitter: RecursiveCharacterTextSplitter      │
│ - Embeddings: OpenAIEmbeddings                  │
│ - VectorStore: Chroma, Pinecone                 │
│ - Retriever: as_retriever(search_kwargs={"k":4})│
└─────────────────────────────────────────────────┘
```

## 다음 단계

- [[04-crewai-basics|CrewAI 기초]] - 에이전트 시스템
- [[06-integration|LangChain + CrewAI 통합]] - RAG와 에이전트 결합
