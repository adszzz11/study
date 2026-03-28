# 기본 문서 변환

## 📌 핵심 개념

DocumentConverter는 Docling의 핵심 클래스입니다. 파일 경로나 URL을 입력받아 DoclingDocument 객체로 변환합니다.

---

## 💻 코드 예제

### 다양한 입력 소스

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

### 출력 포맷 선택

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

---

## ✅ 체크포인트

- [ ] DocumentConverter로 PDF를 변환할 수 있는가?
- [ ] 4가지 출력 포맷의 차이를 이해하는가?
- [ ] `convert_all()`로 일괄 처리할 수 있는가?

---

## ⚠️ 흔한 실수

| 실수 | 해결책 |
|------|--------|
| 대용량 PDF 메모리 부족 | 페이지별 처리 고려 |
| HTTPS 인증서 오류 | 로컬 다운로드 후 처리 |

---

## 🔗 더 알아보기

- [Basic Usage](https://docling-project.github.io/docling/)
