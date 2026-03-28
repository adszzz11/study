# 성능 최적화

## 📌 핵심 개념

대량 문서 처리 시 병렬화와 캐싱으로 성능을 개선할 수 있습니다.

---

## 💻 병렬 처리

```python
from docling.document_converter import DocumentConverter
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor, as_completed

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

if __name__ == "__main__":
    results = batch_convert("./documents", max_workers=4)
    print(f"Processed {len(results)} documents")
```

---

## 💻 GPU 가속

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

---

## ✅ 체크포인트

- [ ] 병렬 처리로 대량 문서를 처리할 수 있는가?
- [ ] GPU 가속을 활용할 수 있는가?

---

## ⚠️ 흔한 실수

| 실수 | 해결책 |
|------|--------|
| ProcessPoolExecutor에서 Converter 공유 | 프로세스 내에서 생성 |
| GPU 메모리 부족 | 배치 크기 조절 |

---

## 🔗 더 알아보기

- [Performance Tips](https://docling-project.github.io/docling/)
