# 이미지 및 수식 처리

## 📌 핵심 개념

Docling은 문서 내 이미지를 추출하고, LaTeX 수식을 인식할 수 있습니다.

---

## 💻 코드 예제

### 이미지 추출

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

### 수식 추출

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

---

## ✅ 체크포인트

- [ ] 문서에서 이미지를 추출하여 저장할 수 있는가?
- [ ] 수식이 LaTeX로 변환되는지 확인할 수 있는가?

---

## ⚠️ 흔한 실수

| 실수 | 해결책 |
|------|--------|
| 이미지 추출 메모리 사용 | 필요할 때만 활성화 |
| 스캔 문서 수식 인식 | OCR 정확도에 의존 |

---

## 🔗 더 알아보기

- [Image Export](https://docling-project.github.io/docling/examples/export_figures/)
