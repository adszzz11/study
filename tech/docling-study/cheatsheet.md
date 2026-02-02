# Docling Cheat Sheet

## 설치

```bash
pip install docling

# LangChain 통합
pip install langchain-docling

# LlamaIndex 통합
pip install llama-index-readers-docling
```

## CLI 사용

```bash
# URL에서 변환
docling https://arxiv.org/pdf/2408.09869 --output ./output

# 로컬 파일 변환
docling document.pdf --output ./output

# 출력 포맷 지정
docling document.pdf --format markdown
docling document.pdf --format json
```

## Python 기본 사용

```python
from docling.document_converter import DocumentConverter

converter = DocumentConverter()
result = converter.convert("document.pdf")

# 출력 포맷
markdown = result.document.export_to_markdown()
html = result.document.export_to_html()
json_doc = result.document.export_to_dict()
```

## 테이블 추출

```python
for table in result.document.tables:
    df = table.export_to_dataframe()
    df.to_csv("table.csv")
```

## 이미지 추출

```python
for idx, picture in enumerate(result.document.pictures):
    if picture.image:
        picture.image.save(f"figure_{idx}.png")
```

## LangChain 통합

```python
from langchain_docling import DoclingLoader

loader = DoclingLoader(file_path="document.pdf")
documents = loader.load()
```

## LlamaIndex 통합

```python
from llama_index.readers.docling import DoclingReader

reader = DoclingReader()
documents = reader.load_data(file_path="document.pdf")
```

## 고급 옵션

```python
from docling.datamodel.pipeline_options import PdfPipelineOptions

options = PdfPipelineOptions()
options.do_ocr = True
options.ocr_options.lang = ["en", "ko"]
options.generate_picture_images = True
```

## 지원 포맷

| 입력 | 출력 |
|------|------|
| PDF | Markdown |
| DOCX | JSON |
| PPTX | HTML |
| XLSX | DocTags |
| HTML | - |
| 이미지 | - |

## 유용한 링크

- 공식 문서: https://docling-project.github.io/docling/
- GitHub: https://github.com/docling-project/docling
- PyPI: https://pypi.org/project/docling/
