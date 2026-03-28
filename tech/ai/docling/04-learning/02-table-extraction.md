# 테이블 추출

## 📌 핵심 개념

Docling은 TableFormer 모델을 사용해 복잡한 테이블도 정확하게 인식합니다. 추출된 테이블은 DataFrame으로 변환하거나 HTML/CSV로 내보낼 수 있습니다.

---

## 💻 코드 예제

### 테이블 추출 및 저장

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

### 테이블 구조 분석

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

---

## ✅ 체크포인트

- [ ] `result.document.tables`로 테이블에 접근할 수 있는가?
- [ ] DataFrame으로 변환하여 분석할 수 있는가?
- [ ] 병합된 셀이 있는 테이블도 처리할 수 있는가?

---

## ⚠️ 흔한 실수

| 실수 | 해결책 |
|------|--------|
| 테이블이 이미지로 삽입됨 | OCR 활성화 필요 |
| 복잡한 중첩 테이블 | 정확도 저하 가능 |

---

## 🔗 더 알아보기

- [Table Extraction](https://docling-project.github.io/docling/examples/export_tables/)
