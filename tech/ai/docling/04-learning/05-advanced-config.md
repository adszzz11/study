# 고급 설정 및 커스터마이징

## 📌 핵심 개념

PipelineOptions를 통해 OCR, 테이블 인식, 이미지 처리 등을 세밀하게 제어할 수 있습니다.

---

## 💻 고급 파이프라인 설정

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

---

## 💻 저수준 파싱 (docling-parse)

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

---

## ✅ 체크포인트

- [ ] OCR을 활성화하여 스캔 문서를 처리할 수 있는가?
- [ ] TableFormer 모드의 차이를 이해하는가?
- [ ] docling-parse로 저수준 접근을 할 수 있는가?

---

## ⚠️ 흔한 실수

| 실수 | 해결책 |
|------|--------|
| OCR 항상 활성화 | 처리 시간 증가, 필요시만 |
| ACCURATE 모드 느림 | FAST 대비 3-5배 느림 |

---

## 🔗 더 알아보기

- [Pipeline Options](https://docling-project.github.io/docling/concepts/pipeline/)
