# Part 2: 생태계 파악

## 2.1 관련 기술/용어 맵

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
│  └── Granite-Docling: 258M 파라미터 VLM (2025년)             │
│                                                              │
│  [Integrations]                                              │
│  ├── LangChain: DoclingLoader                                │
│  ├── LlamaIndex: DoclingReader                               │
│  └── spaCy: NLP 파이프라인                                   │
└─────────────────────────────────────────────────────────────┘
```

---

## 2.2 함께 자주 쓰이는 기술 스택

| 영역 | 기술 | 용도 |
|------|------|------|
| **RAG 프레임워크** | LangChain, LlamaIndex | 문서 임베딩 및 검색 |
| **벡터 DB** | Pinecone, Qdrant, Chroma | 임베딩 저장 |
| **LLM** | OpenAI, Claude, Llama | 질의응답 |
| **OCR** | Tesseract | 스캔 문서용 |
| **워크플로우** | Prefect, Airflow | 배치 처리 |

---

## 2.3 경쟁/대안 기술 비교

| 기준 | Docling | Unstructured | PyPDF | pdf2image + OCR |
|------|---------|--------------|-------|-----------------|
| **레이아웃 분석** | AI 기반 (강력) | AI 기반 | 없음 | OCR만 |
| **테이블 추출** | TableFormer (우수) | 지원 | 기본적 | 불가 |
| **라이선스** | MIT | Apache 2.0 | BSD | 다양 |
| **속도** | 중간 | 빠름 | 매우 빠름 | 느림 |
| **LLM 통합** | 내장 | 내장 | 없음 | 없음 |

### 선택 가이드

| 상황 | 추천 |
|------|------|
| 테이블/수식이 많은 학술 문서 | **Docling** |
| 다양한 문서 타입, 빠른 처리 | Unstructured |
| 단순 텍스트 추출, 속도 우선 | PyPDF |

---

## 2.4 최신 트렌드 (2025)

- **Granite-Docling-258M**: 단일 VLM으로 문서 파싱
- **AAAI 2025 발표**: 학술 컨퍼런스 공식 발표
- **LF AI & Data Foundation**: Linux Foundation 프로젝트
- **Hugging Face 공개**: Apache 2.0 라이선스
