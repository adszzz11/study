# Docling 심층 스터디

> **한 줄 정의**: PDF, DOCX 등 비정형 문서를 AI/LLM이 활용할 수 있는 구조화된 형식(Markdown, JSON)으로 변환하는 IBM의 오픈소스 문서 파싱 라이브러리

## 3줄 요약

1. PDF, DOCX, PPTX, 이미지 등 다양한 문서 포맷을 Markdown/JSON으로 변환
2. 페이지 레이아웃, 테이블 구조, 수식, 코드 블록까지 정확하게 인식
3. LangChain, LlamaIndex 등 RAG 파이프라인과 쉽게 통합

## 핵심 키워드

`#문서파싱` `#PDF변환` `#RAG` `#LLM전처리` `#IBM` `#오픈소스`

---

## Quick Start (30초 체험)

```bash
# 1. 설치 (Python 3.10+ 필요)
pip install docling

# 2. CLI로 바로 변환
docling https://arxiv.org/pdf/2408.09869 --output ./output

# 3. 결과 확인
cat ./output/*.md
```

```python
from docling.document_converter import DocumentConverter

source = "https://arxiv.org/pdf/2408.09869"
converter = DocumentConverter()
result = converter.convert(source)

print(result.document.export_to_markdown())
```

---

## 목차

| 파일 | 내용 |
|------|------|
| [01-overview.md](./01-overview.md) | 핵심 개념, 장단점, 주요 사용 사례 |
| [02-ecosystem.md](./02-ecosystem.md) | 관련 기술, 경쟁 비교, 최신 동향 |
| [03-references.md](./03-references.md) | 공식 문서, 학습 자료, 커뮤니티 |
| [04-learning/](./04-learning/) | 상세 학습 로드맵 (주제별) |
| [05-projects.md](./05-projects.md) | 실전 프로젝트 및 Best Practices |
| [cheatsheet.md](./cheatsheet.md) | 자주 쓰는 명령어/코드 빠른 참조 |

### 04-learning/ 상세

| 파일 | 주제 |
|------|------|
| [01-basic-conversion.md](./04-learning/01-basic-conversion.md) | 기본 문서 변환 |
| [02-table-extraction.md](./04-learning/02-table-extraction.md) | 테이블 추출 |
| [03-image-formula.md](./04-learning/03-image-formula.md) | 이미지 및 수식 처리 |
| [04-langchain-integration.md](./04-learning/04-langchain-integration.md) | LangChain/LlamaIndex 통합 |
| [05-advanced-config.md](./04-learning/05-advanced-config.md) | 고급 설정 및 커스터마이징 |
| [06-performance.md](./04-learning/06-performance.md) | 성능 최적화 |

---

## 학습 플랜

### Day 1: 기초 (2시간)
- [ ] Quick Start 따라하기
- [ ] [01-overview.md](./01-overview.md) 읽기
- [ ] 다양한 문서 포맷 변환 테스트

### Day 2: 테이블/이미지 (2-3시간)
- [ ] [04-learning/01-basic-conversion.md](./04-learning/01-basic-conversion.md)
- [ ] [04-learning/02-table-extraction.md](./04-learning/02-table-extraction.md)
- [ ] PDF에서 테이블 추출 실습

### Day 3: RAG 통합 (3시간)
- [ ] [04-learning/04-langchain-integration.md](./04-learning/04-langchain-integration.md)
- [ ] LangChain으로 문서 QA 구축

### Day 4: 프로젝트 (4시간+)
- [ ] [05-projects.md](./05-projects.md)
- [ ] 논문 QA 시스템 구현
