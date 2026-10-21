---
date: 2026-10-21
tags: [tech]
type: tech-tool-study
status: draft
---

# MarkItDown cheatsheet

## Install

```bash
# 필요한 converter만
pip install 'markitdown[pdf,docx,pptx]'

# 전체 optional dependency
pip install 'markitdown[all]'
```

## CLI

```bash
# 파일을 Markdown으로 변환
markitdown report.pdf -o report.md

# 신뢰한 third-party plugin을 명시 활성화
markitdown --use-plugins report.pdf -o report.md
```

## Python API

```python
from markitdown import MarkItDown

converter = MarkItDown()
result = converter.convert("report.xlsx")
markdown = result.markdown
print(markdown)
```

## Quality checklist

- [ ] heading 계층이 보존되었는가?
- [ ] table과 list가 의미 있게 읽히는가?
- [ ] link label과 URL이 남아 있는가?
- [ ] header/footer·페이지 번호 노이즈를 처리했는가?
- [ ] 대표 질의로 retrieval 성능을 측정했는가?

## MCP checklist

- [ ] STDIO를 우선하고, HTTP/SSE는 localhost 또는 sandbox로 제한했는가?
- [ ] 최소 directory만 read-only mount했는가?
- [ ] `file:` URI 경로 범위와 network access를 제한했는가?
- [ ] untrusted input에 좁은 API와 크기·시간 제한을 적용했는가?

## Sources

- https://github.com/microsoft/markitdown
- https://github.com/microsoft/markitdown/blob/main/packages/markitdown-mcp/README.md
