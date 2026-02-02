# LangChain/LlamaIndex 통합

## 📌 핵심 개념

RAG 파이프라인에서 Docling을 문서 로더로 사용하여 정확한 청킹과 임베딩이 가능합니다.

---

## 💻 LangChain 통합

```python
# pip install langchain-docling

from langchain_docling import DoclingLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma

# 1. Docling으로 문서 로드
loader = DoclingLoader(
    file_path="research_paper.pdf",
)
documents = loader.load()

# 2. 텍스트 분할 (청킹)
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)
splits = text_splitter.split_documents(documents)

# 3. 벡터 스토어 생성
embeddings = OpenAIEmbeddings()
vectorstore = Chroma.from_documents(
    documents=splits,
    embedding=embeddings,
    persist_directory="./chroma_db"
)

# 4. 검색
retriever = vectorstore.as_retriever()
results = retriever.invoke("What is the main contribution?")

for doc in results:
    print(doc.page_content[:200])
```

---

## 💻 LlamaIndex 통합

```python
# pip install llama-index-readers-docling

from llama_index.readers.docling import DoclingReader
from llama_index.core import VectorStoreIndex

# 문서 로드
reader = DoclingReader()
documents = reader.load_data(file_path="document.pdf")

# 인덱스 생성
index = VectorStoreIndex.from_documents(documents)

# 쿼리
query_engine = index.as_query_engine()
response = query_engine.query("Summarize the key findings")
print(response)
```

---

## ✅ 체크포인트

- [ ] LangChain DoclingLoader를 사용할 수 있는가?
- [ ] 청킹 전략을 이해하는가?
- [ ] RAG 파이프라인에 Docling을 통합할 수 있는가?

---

## ⚠️ 흔한 실수

| 실수 | 해결책 |
|------|--------|
| 청크 크기 너무 큼 | 검색 정확도 저하 |
| 테이블이 청킹 시 분리됨 | 테이블별 별도 처리 고려 |

---

## 🔗 더 알아보기

- [LangChain Integration](https://python.langchain.com/docs/integrations/document_loaders/docling/)
