---
date: 2026-10-21
tags: [tech]
type: tech-tool-study
status: draft
---

# Getting started

## 1. 필요한 converter만 설치

```bash
pip install 'markitdown[pdf,docx,pptx]'
```

모든 입력 유형이 필요한 경우에만 `[all]`을 선택한다. 프로젝트 환경을 분리해 설치하고, 실제 처리할 파일 유형으로 smoke test한다.

## 2. CLI 변환

```bash
markitdown report.pdf -o report.md
```

생성된 `report.md`에서 다음을 직접 확인한다.

- 문서 제목과 section heading이 계층을 유지하는가?
- 표가 Markdown table로 읽을 수 있게 변환되었는가?
- 링크의 label과 URL이 유지되는가?
- 페이지 번호·반복 header/footer 같은 노이즈가 retrieval을 방해하는가?

## 3. Python API

```python
from markitdown import MarkItDown

result = MarkItDown().convert("report.xlsx")
print(result.markdown)
```

`result.markdown`을 파일로 저장하기 전, 원본과 대조해 구조 손실을 기록한다. 변환 실패를 무시해 빈 문서를 index하지 않도록 호출부에 실패 처리와 입력 파일 식별자를 둔다.

## 4. 첫 RAG 실험

1. Markdown을 heading 경계로 나눈다.
2. chunk마다 source path, 변환 시각, section heading 같은 metadata를 부여한다.
3. embedding/index 뒤, 표·링크·하위 section을 묻는 질문으로 retrieval을 평가한다.

## Sources

- https://github.com/microsoft/markitdown
- https://pypi.org/project/markitdown/
