---
date: 2026-10-21
tags: [tech]
type: tech-tool-study
status: draft
---

# MarkItDown tool study

> **한 줄 정의**: MarkItDown은 여러 문서와 미디어를 LLM/RAG에 적합한 구조화 Markdown으로 정규화하는 Microsoft의 Python 도구다.

## Overview

PDF·Office 문서·웹 페이지·이미지·음성을 단순 텍스트가 아닌 heading, list, table, link의 의미 구조를 유지한 Markdown으로 바꾼다. 목표는 출판 품질의 문서 재현이 아니라, 읽기 쉽고 token-efficient한 AI ingestion layer다.

- 실행 경로: CLI, Python API, Docker, MCP server
- 입력 예: PDF, DOCX, PPTX, XLSX, HTML, CSV/JSON/XML, EPUB, ZIP, 이미지, 오디오, YouTube URL
- 설치는 필요한 converter만 선택할 수 있으며, 기본 변환은 로컬에서 실행된다.

## Learning Path

- [ ] [01-overview](./01-overview.md)에서 목적과 구조 보존의 의미를 이해한다.
- [ ] [04-learning/01-getting-started](./04-learning/01-getting-started.md)의 CLI와 Python API를 실행한다.
- [ ] 같은 문서의 heading/table/link 보존 결과를 검사하고 heading 기반 chunking을 시도한다.
- [ ] [02-ecosystem](./02-ecosystem.md)으로 Docling·Unstructured·Azure 계열의 선택 기준을 비교한다.
- [ ] [04-learning/02-deep-dive](./04-learning/02-deep-dive.md)에서 OCR, cloud tier, MCP 보안을 검토한다.
- [ ] [05-projects](./05-projects.md)의 작은 ingestion 프로젝트를 구현한다.

## When To Use

- 다양한 사내 문서를 빠르게 Markdown corpus로 정규화해 RAG/agent에 넣을 때
- Office·URL·미디어를 하나의 Python/CLI/MCP 진입점으로 처리할 때
- 로컬 기본 변환으로 비용과 운영 복잡도를 낮춘 MVP를 만들 때

## When Not To Use

- 복잡한 PDF의 reading order, 표, 수식에 최고 정확도가 필수일 때: Docling을 함께 평가한다.
- invoice/contract의 신뢰도와 정형 field 추출, SLA가 핵심일 때: Azure Content Understanding 또는 Document Intelligence를 우선 검토한다.
- PDF 한 종류만 대상으로 낮은 수준의 렌더링·이미지 제어를 직접 구현할 때: PyMuPDF가 더 직접적일 수 있다.

## Related Notes

- [[MOCs/Index]]
- [[MOCs/AI]]
- [[tech/ai/docling/README|Docling]]

## Sources

- https://github.com/microsoft/markitdown
- https://pypi.org/project/markitdown/
- https://github.com/microsoft/markitdown/releases
- https://github.com/microsoft/markitdown/blob/main/packages/markitdown-mcp/README.md
