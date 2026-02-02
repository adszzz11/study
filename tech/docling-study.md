# Docling 심층 스터디 가이드

> **한 줄 정의**: PDF, DOCX 등 비정형 문서를 AI/LLM이 활용할 수 있는 구조화된 형식(Markdown, JSON)으로 변환하는 IBM의 오픈소스 문서 파싱 라이브러리

---

## Part 1: 개요

### 1.1 정의 및 핵심 개념

**3줄 요약**:
1. PDF, DOCX, PPTX, 이미지 등 다양한 문서 포맷을 Markdown/JSON으로 변환
2. 페이지 레이아웃, 테이블 구조, 수식, 코드 블록까지 정확하게 인식
3. LangChain, LlamaIndex 등 RAG 파이프라인과 쉽게 통합

**핵심 키워드**: `#문서파싱` `#PDF변환` `#RAG` `#LLM전처리` `#IBM` `#오픈소스`

**Docling이 해결하는 문제**:

```
Before Docling:
┌─────────────────┐     ┌─────────────────┐
│   PDF 문서      │ ──▶ │  텍스트만 추출   │ ──▶ 테이블 깨짐, 구조 손실
│ (테이블, 이미지) │     │  (PyPDF2 등)    │
└─────────────────┘     └─────────────────┘

After Docling:
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   PDF 문서      │ ──▶ │    Docling      │ ──▶ │ 구조화된 출력    │
│ (테이블, 이미지) │     │  (AI 기반 분석)  │     │ (MD, JSON, HTML) │
└─────────────────┘     └─────────────────┘     └─────────────────┘
```

### 1.2 Quick Start (30초 체험)

```bash
# 1. 설치 (Python 3.10+ 필요)
pip install docling

# 2. CLI로 바로 변환
docling https://arxiv.org/pdf/2408.09869 --output ./output

# 3. 결과 확인
cat ./output/*.md
```

**Python 코드로 변환**:
```python
from docling.document_converter import DocumentConverter

# PDF URL 또는 로컬 경로
source = "https://arxiv.org/pdf/2408.09869"

converter = DocumentConverter()
result = converter.convert(source)

# Markdown으로 출력
print(result.document.export_to_markdown())
```

### 1.3 왜 Docling인가?

**장점**:
- **높은 정확도**: DocLayNet(레이아웃), TableFormer(테이블) 등 특화된 AI 모델 사용
- **다양한 포맷 지원**: PDF, DOCX, PPTX, XLSX, HTML, 이미지, 오디오까지
- **LLM 친화적 출력**: Markdown, JSON, DocTags 등 RAG에 최적화
- **MIT 라이선스**: 상업적 사용 가능
- **경량 실행**: GPU 없이도 일반 하드웨어에서 실행 가능

**단점**:
- CPU에서는 처리 속도가 느릴 수 있음 (GPU 권장)
- 복잡한 레이아웃은 여전히 100% 완벽하지 않음
- Python 3.10+ 필수 (3.9 지원 중단됨)

**주요 사용 사례**:
- RAG(Retrieval-Augmented Generation) 파이프라인 문서 전처리
- 학술 논문 자동 분석
- 기업 문서 디지털화
- 지식 베이스 구축

---

## Part 2: 생태계 파악

### 2.1 관련 기술/용어 맵

```
┌─────────────────────────────────────────────────────────────┐
│                    Docling 생태계                            │
├─────────────────────────────────────────────────────────────┤
│  [Core Components]                                          │
│  ├── docling: 메인 변환 라이브러리                            │
│  ├── docling-core: 핵심 데이터 타입 (DoclingDocument)         │
│  ├── docling-parse: 저수준 PDF 파싱                          │
│  └── docling-ibm-models: IBM AI 모델 (DocLayNet, TableFormer)│
│                                                              │
│  [AI Models]                                                 │
│  ├── DocLayNet: 문서 레이아웃 분석                            │
│  ├── TableFormer: 테이블 구조 인식                            │
│  └── Granite-Docling: 258M 파라미터 VLM (2025년 출시)         │
│                                                              │
│  [Output Formats]                                            │
│  ├── Markdown: 가장 많이 사용                                 │
│  ├── JSON (DoclingDocument): 완전한 구조 보존                 │
│  ├── HTML: 웹 표시용                                         │
│  └── DocTags: 특수 토큰 형식                                  │
│                                                              │
│  [Integrations]                                              │
│  ├── LangChain: DoclingLoader                                │
│  ├── LlamaIndex: DoclingReader                               │
│  └── spaCy: NLP 파이프라인                                   │
└─────────────────────────────────────────────────────────────┘
```

### 2.2 함께 자주 쓰이는 기술 스택

| 영역 | 기술 | 용도 |
|------|------|------|
| **RAG 프레임워크** | LangChain, LlamaIndex | 문서 임베딩 및 검색 |
| **벡터 DB** | Pinecone, Qdrant, Chroma | 임베딩 저장 |
| **LLM** | OpenAI, Claude, Llama | 질의응답 |
| **OCR** | Tesseract | 스캔 문서용 |
| **워크플로우** | Prefect, Airflow | 배치 처리 |

### 2.3 경쟁/대안 기술 비교

| 기준 | Docling | Unstructured | PyPDF | pdf2image + OCR |
|------|---------|--------------|-------|-----------------|
| **레이아웃 분석** | AI 기반 (강력) | AI 기반 | 없음 | OCR만 |
| **테이블 추출** | TableFormer (우수) | 지원 | 기본적 | 불가 |
| **라이선스** | MIT | Apache 2.0 | BSD | 다양 |
| **속도** | 중간 | 빠름 | 매우 빠름 | 느림 |
| **설치** | pip | pip + 의존성 | pip | 복잡 |
| **LLM 통합** | 내장 | 내장 | 없음 | 없음 |

**선택 가이드**:
- **Docling**: 테이블/수식이 많은 학술 문서, 높은 정확도 필요
- **Unstructured**: 다양한 문서 타입, 빠른 처리
- **PyPDF**: 단순 텍스트 추출, 속도 우선

### 2.4 최신 트렌드 및 동향 (2025)

- **Granite-Docling-258M 출시 (2025)**: 단일 VLM으로 문서를 한 번에 파싱, 기존 앙상블 파이프라인 대비 간소화
- **AAAI 2025 발표**: 학술 컨퍼런스에서 공식 발표
- **LF AI & Data Foundation 가입**: Linux Foundation 산하 프로젝트로 편입
- **Hugging Face 모델 공개**: Apache 2.0 라이선스로 무료 사용

---

## Part 3: 레퍼런스

### 3.1 공식 문서 및 필수 링크

| 리소스 | URL | 설명 |
|--------|-----|------|
| 🟢 공식 문서 | [docling-project.github.io/docling](https://docling-project.github.io/docling/) | 메인 문서 |
| 🟢 GitHub | [github.com/docling-project/docling](https://github.com/docling-project/docling) | 소스 코드 |
| 🟢 PyPI | [pypi.org/project/docling](https://pypi.org/project/docling/) | 패키지 설치 |
| 🟡 IBM 블로그 | [IBM Research Blog](https://research.ibm.com/blog/docling-generative-AI) | 배경 설명 |
| 🟡 Hugging Face | Granite-Docling-258M | VLM 모델 |

### 3.2 추천 학습 자료

**🟢 입문**:
- [Docling GitHub README](https://github.com/docling-project/docling) - 설치 및 기본 사용법
- [Codecademy: Docling AI Guide](https://www.codecademy.com/article/docling-ai-a-complete-guide-to-parsing) - 전체 개요

**🟡 중급**:
- [Building Document Parsing Pipelines](https://lasha-dolenjashvili.medium.com/building-document-parsing-pipelines-with-python-3c06f62569ad) - 실전 파이프라인 구축
- [Towards Data Science: Docling Deep Dive](https://towardsdatascience.com/docling-the-document-alchemist/) - 상세 분석

**🔴 고급**:
- [docling-parse 저수준 API](https://github.com/docling-project/docling-parse) - 커스텀 파싱
- [AAAI 2025 Paper](https://research.ibm.com/publications/docling-an-efficient-open-source-toolkit-for-ai-driven-document-conversion) - 학술 논문

### 3.3 커뮤니티 및 질문할 곳

- **GitHub Issues**: [docling-project/docling/issues](https://github.com/docling-project/docling/issues)
- **GitHub Discussions**: 기능 요청 및 토론
- **IBM Research Blog**: 공식 발표 및 업데이트

### 3.4 실무 예제/오픈소스 프로젝트

- [LangChain DoclingLoader](https://python.langchain.com/docs/integrations/document_loaders/docling/) - LangChain 통합 예제
- [LlamaIndex DoclingReader](https://docs.llamaindex.ai/) - LlamaIndex 통합
- [Docling Examples](https://github.com/docling-project/docling/tree/main/examples) - 공식 예제

---

## Part 4: 상세 학습 로드맵

### 4.1 기본 문서 변환

📌 **핵심 개념**

DocumentConverter는 Docling의 핵심 클래스입니다. 파일 경로나 URL을 입력받아 DoclingDocument 객체로 변환합니다.

💻 **코드 예제: 다양한 입력 소스**

```python
from docling.document_converter import DocumentConverter

converter = DocumentConverter()

# 1. URL에서 직접 변환
url_result = converter.convert("https://arxiv.org/pdf/2408.09869")

# 2. 로컬 파일 변환
local_result = converter.convert("/path/to/document.pdf")

# 3. 여러 파일 일괄 변환
from pathlib import Path

input_files = list(Path("./documents").glob("*.pdf"))
results = converter.convert_all(input_files)

for result in results:
    print(f"Converted: {result.input.file}")
    print(result.document.export_to_markdown()[:500])
    print("---")
```

**출력 포맷 선택**:
```python
result = converter.convert("document.pdf")

# Markdown (가장 많이 사용)
markdown = result.document.export_to_markdown()

# HTML
html = result.document.export_to_html()

# JSON (완전한 구조 보존)
json_doc = result.document.export_to_dict()

# DocTags (특수 토큰 형식)
doctags = result.document.export_to_doctags()
```

✅ **체크포인트**
- [ ] DocumentConverter로 PDF를 변환할 수 있는가?
- [ ] 4가지 출력 포맷의 차이를 이해하는가?
- [ ] `convert_all()`로 일괄 처리할 수 있는가?

⚠️ **흔한 실수**
- 대용량 PDF는 메모리 부족 발생 가능 → 페이지별 처리 고려
- HTTPS 인증서 오류 시 로컬 다운로드 후 처리

🔗 **더 알아보기**: [Basic Usage](https://docling-project.github.io/docling/)

---

### 4.2 테이블 추출

📌 **핵심 개념**

Docling은 TableFormer 모델을 사용해 복잡한 테이블도 정확하게 인식합니다. 추출된 테이블은 DataFrame으로 변환하거나 HTML/CSV로 내보낼 수 있습니다.

💻 **코드 예제: 테이블 추출 및 저장**

```python
from docling.document_converter import DocumentConverter
import pandas as pd
from pathlib import Path

converter = DocumentConverter()
result = converter.convert("report_with_tables.pdf")

# 문서 내 모든 테이블 순회
for idx, table in enumerate(result.document.tables):
    print(f"\n=== Table {idx + 1} ===")

    # Pandas DataFrame으로 변환
    df = table.export_to_dataframe()
    print(df.head())

    # CSV로 저장
    df.to_csv(f"table_{idx + 1}.csv", index=False)

    # HTML로 저장
    html_content = table.export_to_html()
    Path(f"table_{idx + 1}.html").write_text(html_content)

    # Markdown으로 출력
    print(table.export_to_markdown())
```

**테이블 구조 분석**:
```python
for table in result.document.tables:
    # 테이블 메타데이터
    print(f"Rows: {table.num_rows}")
    print(f"Columns: {table.num_cols}")

    # 셀 단위 접근
    for row_idx, row in enumerate(table.data):
        for col_idx, cell in enumerate(row):
            print(f"[{row_idx},{col_idx}]: {cell.text}")
```

✅ **체크포인트**
- [ ] `result.document.tables`로 테이블에 접근할 수 있는가?
- [ ] DataFrame으로 변환하여 분석할 수 있는가?
- [ ] 병합된 셀이 있는 테이블도 처리할 수 있는가?

⚠️ **흔한 실수**
- 테이블이 이미지로 삽입된 경우 OCR 필요 (별도 설정)
- 매우 복잡한 중첩 테이블은 정확도 저하 가능

🔗 **더 알아보기**: [Table Extraction](https://docling-project.github.io/docling/examples/export_tables/)

---

### 4.3 이미지 및 수식 처리

📌 **핵심 개념**

Docling은 문서 내 이미지를 추출하고, LaTeX 수식을 인식할 수 있습니다.

💻 **코드 예제: 이미지 추출**

```python
from docling.document_converter import DocumentConverter
from docling.datamodel.pipeline_options import PdfPipelineOptions
from pathlib import Path

# 이미지 추출 활성화
pipeline_options = PdfPipelineOptions()
pipeline_options.images_scale = 2.0  # 해상도 조절
pipeline_options.generate_picture_images = True

converter = DocumentConverter(
    allowed_formats=["pdf"],
    format_options={"pdf": {"pipeline_options": pipeline_options}}
)

result = converter.convert("paper_with_figures.pdf")

# 이미지 저장
output_dir = Path("./extracted_images")
output_dir.mkdir(exist_ok=True)

for idx, picture in enumerate(result.document.pictures):
    if picture.image:
        image_path = output_dir / f"figure_{idx + 1}.png"
        picture.image.save(image_path)
        print(f"Saved: {image_path}")
```

**수식 추출**:
```python
# Markdown에서 수식은 LaTeX 형식으로 출력됨
markdown = result.document.export_to_markdown()

# 예시 출력:
# The equation is: $E = mc^2$
# Or as a block:
# $$
# \int_{0}^{\infty} e^{-x^2} dx = \frac{\sqrt{\pi}}{2}
# $$
```

✅ **체크포인트**
- [ ] 문서에서 이미지를 추출하여 저장할 수 있는가?
- [ ] 수식이 LaTeX로 변환되는지 확인할 수 있는가?

⚠️ **흔한 실수**
- 이미지 추출은 추가 메모리 사용 → 필요할 때만 활성화
- 스캔 문서의 수식은 OCR 정확도에 의존

🔗 **더 알아보기**: [Image Export](https://docling-project.github.io/docling/examples/export_figures/)

---

### 4.4 LangChain/LlamaIndex 통합

📌 **핵심 개념**

RAG 파이프라인에서 Docling을 문서 로더로 사용하여 정확한 청킹과 임베딩이 가능합니다.

💻 **코드 예제: LangChain 통합**

```python
# pip install langchain-docling

from langchain_docling import DoclingLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma

# 1. Docling으로 문서 로드
loader = DoclingLoader(
    file_path="research_paper.pdf",
    # export_type=ExportType.MARKDOWN  # 기본값
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
results = retriever.invoke("What is the main contribution of this paper?")

for doc in results:
    print(doc.page_content[:200])
```

**LlamaIndex 통합**:
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

✅ **체크포인트**
- [ ] LangChain DoclingLoader를 사용할 수 있는가?
- [ ] 청킹 전략을 이해하는가?
- [ ] RAG 파이프라인에 Docling을 통합할 수 있는가?

⚠️ **흔한 실수**
- 청크 크기가 너무 크면 검색 정확도 저하
- 테이블은 청킹 시 분리될 수 있음 → 테이블별 별도 처리 고려

🔗 **더 알아보기**: [LangChain Integration](https://python.langchain.com/docs/integrations/document_loaders/docling/)

---

### 4.5 고급 설정 및 커스터마이징

📌 **핵심 개념**

PipelineOptions를 통해 OCR, 테이블 인식, 이미지 처리 등을 세밀하게 제어할 수 있습니다.

💻 **코드 예제: 고급 파이프라인 설정**

```python
from docling.document_converter import DocumentConverter
from docling.datamodel.pipeline_options import (
    PdfPipelineOptions,
    TableFormerMode,
)
from docling.datamodel.base_models import InputFormat

# 고급 옵션 설정
pipeline_options = PdfPipelineOptions()

# 테이블 인식 모드 (ACCURATE vs FAST)
pipeline_options.table_structure_options.mode = TableFormerMode.ACCURATE

# OCR 활성화 (스캔 문서용)
pipeline_options.do_ocr = True
pipeline_options.ocr_options.lang = ["en", "ko"]  # 영어 + 한국어

# 이미지 추출 설정
pipeline_options.generate_picture_images = True
pipeline_options.images_scale = 1.5

# 포맷별 옵션 지정
converter = DocumentConverter(
    allowed_formats=[InputFormat.PDF, InputFormat.DOCX],
    format_options={
        InputFormat.PDF: {"pipeline_options": pipeline_options}
    }
)

result = converter.convert("scanned_document.pdf")
```

**저수준 파싱 (docling-parse)**:
```python
# pip install docling-parse

from docling_parse.pdf_parser import DoclingPdfParser, PdfDocument
from docling_core.types.doc.page import TextCellUnit

parser = DoclingPdfParser()
pdf_doc: PdfDocument = parser.load("document.pdf")

for page_no, page in pdf_doc.iterate_pages():
    print(f"\n=== Page {page_no} ===")

    # 단어 단위 추출
    for word in page.iterate_cells(unit_type=TextCellUnit.WORD):
        print(f"Position: {word.rect}, Text: {word.text}")

    # 페이지를 이미지로 렌더링
    img = page.render_as_image(cell_unit=TextCellUnit.CHAR)
    img.save(f"page_{page_no}.png")
```

✅ **체크포인트**
- [ ] OCR을 활성화하여 스캔 문서를 처리할 수 있는가?
- [ ] TableFormer 모드의 차이를 이해하는가?
- [ ] docling-parse로 저수준 접근을 할 수 있는가?

⚠️ **흔한 실수**
- OCR 활성화는 처리 시간 증가 → 필요할 때만 사용
- ACCURATE 모드는 FAST 대비 3-5배 느림

🔗 **더 알아보기**: [Pipeline Options](https://docling-project.github.io/docling/concepts/pipeline/)

---

### 4.6 성능 최적화

📌 **핵심 개념**

대량 문서 처리 시 병렬화와 캐싱으로 성능을 개선할 수 있습니다.

💻 **코드 예제: 병렬 처리**

```python
from docling.document_converter import DocumentConverter
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor, as_completed
import multiprocessing

def convert_single_file(file_path: str) -> dict:
    """단일 파일 변환 (프로세스별 실행)"""
    converter = DocumentConverter()  # 프로세스마다 새로 생성
    result = converter.convert(file_path)
    return {
        "file": file_path,
        "markdown": result.document.export_to_markdown()[:500]
    }

def batch_convert(input_dir: str, max_workers: int = 4):
    """디렉토리 내 모든 PDF 병렬 변환"""
    pdf_files = list(Path(input_dir).glob("*.pdf"))
    results = []

    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        futures = {
            executor.submit(convert_single_file, str(f)): f
            for f in pdf_files
        }

        for future in as_completed(futures):
            file_path = futures[future]
            try:
                result = future.result()
                results.append(result)
                print(f"✅ Completed: {file_path}")
            except Exception as e:
                print(f"❌ Failed: {file_path} - {e}")

    return results

# 실행
if __name__ == "__main__":
    results = batch_convert("./documents", max_workers=4)
    print(f"Processed {len(results)} documents")
```

**GPU 가속 (CUDA)**:
```python
import torch

# GPU 사용 가능 여부 확인
if torch.cuda.is_available():
    print(f"GPU available: {torch.cuda.get_device_name(0)}")
    # Docling은 자동으로 GPU 감지하여 사용
else:
    print("Running on CPU (slower)")

# 환경 변수로 GPU 지정
import os
os.environ["CUDA_VISIBLE_DEVICES"] = "0"
```

✅ **체크포인트**
- [ ] 병렬 처리로 대량 문서를 처리할 수 있는가?
- [ ] GPU 가속을 활용할 수 있는가?

⚠️ **흔한 실수**
- ProcessPoolExecutor 사용 시 DocumentConverter를 프로세스 내에서 생성
- GPU 메모리 부족 시 배치 크기 조절 필요

🔗 **더 알아보기**: [Performance Tips](https://docling-project.github.io/docling/)

---

## Part 5: 실전 프로젝트

### 5.1 미니 프로젝트 아이디어

| 난이도 | 프로젝트 | 학습 포인트 |
|--------|---------|------------|
| 🟢 | PDF 논문 → Markdown 변환기 | 기본 변환, CLI |
| 🟢 | 청구서 테이블 추출기 | 테이블 → CSV |
| 🟡 | 학술 논문 RAG 챗봇 | LangChain 통합 |
| 🟡 | 문서 비교 도구 | JSON 출력 활용 |
| 🔴 | 대규모 문서 인덱싱 시스템 | 병렬 처리, 벡터 DB |

### 5.2 단계별 구현 가이드: 논문 QA 시스템

**목표**: PDF 논문을 업로드하면 질문에 답변하는 RAG 시스템

```python
# paper_qa.py
from docling.document_converter import DocumentConverter
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from pathlib import Path
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

        # RAG 체인 구성
        retriever = self.vectorstore.as_retriever(
            search_kwargs={"k": k}
        )

        prompt = ChatPromptTemplate.from_template("""
        Based on the following context from a research paper, answer the question.
        If you cannot find the answer in the context, say "I couldn't find this information in the paper."

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

    # 논문 로드
    qa.load_paper("attention_is_all_you_need.pdf")

    # 질문하기
    questions = [
        "What is the main contribution of this paper?",
        "How does the attention mechanism work?",
        "What datasets were used for evaluation?"
    ]

    for q in questions:
        print(f"\nQ: {q}")
        answer = qa.ask(q)
        print(f"A: {answer}")
```

### 5.3 Best Practices

**문서 전처리 파이프라인**:
```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  PDF 수집   │ ──▶ │   Docling   │ ──▶ │  품질 검증   │
│  (S3 등)    │     │   변환      │     │  (길이 체크) │
└─────────────┘     └─────────────┘     └─────────────┘
                                              │
      ┌───────────────────────────────────────┘
      ▼
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   청킹     │ ──▶ │  임베딩     │ ──▶ │  벡터 DB    │
│ (문맥 유지) │     │ (OpenAI 등) │     │  (Pinecone) │
└─────────────┘     └─────────────┘     └─────────────┘
```

**운영 권장사항**:

1. **입력 검증**: 파일 크기, 페이지 수 제한
2. **에러 처리**: 변환 실패 시 폴백 (PyPDF 등)
3. **캐싱**: 동일 문서 재변환 방지
4. **모니터링**: 변환 시간, 성공률 추적
5. **청킹 전략**: 테이블/이미지 캡션은 별도 처리

```python
# 캐싱 예시
import hashlib
from pathlib import Path
import json

def get_cached_or_convert(pdf_path: str, cache_dir: str = "./cache"):
    """캐시된 결과가 있으면 반환, 없으면 변환 후 캐시"""
    cache_dir = Path(cache_dir)
    cache_dir.mkdir(exist_ok=True)

    # 파일 해시로 캐시 키 생성
    with open(pdf_path, "rb") as f:
        file_hash = hashlib.md5(f.read()).hexdigest()

    cache_file = cache_dir / f"{file_hash}.json"

    if cache_file.exists():
        print("Using cached result")
        return json.loads(cache_file.read_text())

    # 변환
    converter = DocumentConverter()
    result = converter.convert(pdf_path)

    # 캐시 저장
    cached_data = {
        "markdown": result.document.export_to_markdown(),
        "tables": [t.export_to_markdown() for t in result.document.tables]
    }
    cache_file.write_text(json.dumps(cached_data, ensure_ascii=False))

    return cached_data
```

---

## 요약

Docling은 RAG 파이프라인을 위한 최고의 문서 변환 도구 중 하나입니다:

- **시작**: `pip install docling` → `DocumentConverter().convert()`
- **출력**: Markdown, JSON, HTML, DocTags 중 선택
- **통합**: LangChain/LlamaIndex와 원활한 연동
- **확장**: OCR, 테이블 추출, 이미지 처리까지

다음 단계:
1. [GitHub 예제](https://github.com/docling-project/docling/tree/main/examples) 따라하기
2. 자신의 PDF 문서로 변환 테스트
3. LangChain과 연동하여 간단한 RAG 챗봇 만들기
