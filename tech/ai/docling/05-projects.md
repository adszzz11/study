# Part 5: 실전 프로젝트

## 5.1 미니 프로젝트 아이디어

| 난이도 | 프로젝트 | 학습 포인트 |
|--------|---------|------------|
| 🟢 | PDF 논문 → Markdown 변환기 | 기본 변환, CLI |
| 🟢 | 청구서 테이블 추출기 | 테이블 → CSV |
| 🟡 | 학술 논문 RAG 챗봇 | LangChain 통합 |
| 🟡 | 문서 비교 도구 | JSON 출력 활용 |
| 🔴 | 대규모 문서 인덱싱 시스템 | 병렬 처리, 벡터 DB |

---

## 5.2 단계별 구현 가이드: 논문 QA 시스템

```python
# paper_qa.py
from docling.document_converter import DocumentConverter
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
import os

class PaperQA:
    def __init__(self, openai_api_key: str):
        os.environ["OPENAI_API_KEY"] = openai_api_key
        self.converter = DocumentConverter()
        self.embeddings = OpenAIEmbeddings()
        self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
        self.vectorstore = None

    def load_paper(self, pdf_path: str) -> str:
        """PDF 논문 로드 및 인덱싱"""
        print(f"Loading: {pdf_path}")

        # 1. Docling으로 변환
        result = self.converter.convert(pdf_path)
        markdown = result.document.export_to_markdown()

        # 2. 청킹
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            separators=["\n## ", "\n### ", "\n\n", "\n", " "]
        )
        chunks = splitter.split_text(markdown)
        print(f"Created {len(chunks)} chunks")

        # 3. 벡터 스토어 생성
        self.vectorstore = Chroma.from_texts(
            texts=chunks,
            embedding=self.embeddings,
            collection_name="paper"
        )

        return f"Loaded {len(chunks)} chunks from {pdf_path}"

    def ask(self, question: str, k: int = 4) -> str:
        """질문에 답변"""
        if not self.vectorstore:
            return "Please load a paper first."

        retriever = self.vectorstore.as_retriever(search_kwargs={"k": k})

        prompt = ChatPromptTemplate.from_template("""
        Based on the following context, answer the question.
        If you cannot find the answer, say so.

        Context:
        {context}

        Question: {question}

        Answer:
        """)

        chain = (
            {"context": retriever, "question": RunnablePassthrough()}
            | prompt
            | self.llm
        )

        response = chain.invoke(question)
        return response.content


# 사용 예시
if __name__ == "__main__":
    qa = PaperQA(openai_api_key="your-api-key")
    qa.load_paper("attention_is_all_you_need.pdf")

    questions = [
        "What is the main contribution?",
        "How does attention work?",
    ]

    for q in questions:
        print(f"\nQ: {q}")
        print(f"A: {qa.ask(q)}")
```

---

## 5.3 Best Practices

### 문서 전처리 파이프라인

```
PDF 수집 → Docling 변환 → 품질 검증 → 청킹 → 임베딩 → 벡터 DB
```

### 운영 권장사항

| 항목 | 권장사항 |
|------|---------|
| **입력 검증** | 파일 크기, 페이지 수 제한 |
| **에러 처리** | 변환 실패 시 폴백 (PyPDF 등) |
| **캐싱** | 동일 문서 재변환 방지 |
| **모니터링** | 변환 시간, 성공률 추적 |
| **청킹 전략** | 테이블/이미지 캡션 별도 처리 |
