---
date: 2026-10-21
tags: [tech]
type: tech-tool-study
status: draft
---

# MarkItDown overview

## What

**MarkItDown**은 Microsoft가 개발한 Python 기반 document-to-Markdown converter다. 서로 다른 문서 포맷의 콘텐츠를 AI가 다루기 쉬운 Markdown으로 통일한다.

## Why

RAG나 agent는 원본 PDF·Office 문서를 그대로 안정적으로 chunking하기 어렵다. 평문 추출은 제목, 표, 목록, 링크의 관계를 잃기 쉽고 retrieval 품질도 흔들린다. MarkItDown은 이 구조를 Markdown으로 표현해 사람이 검토할 수 있고 후속 chunker가 이용할 수 있는 중간 산출물을 만든다.

## 핵심 특징

| 영역 | 내용 |
|---|---|
| 지원 입력 | PDF, Word, PowerPoint, Excel, HTML, CSV/JSON/XML, EPUB, ZIP, 이미지, 오디오, YouTube URL |
| 구조 | headings, lists, tables, links 보존을 지향 |
| 실행 | CLI, Python API, Docker, MCP server |
| 의존성 | `markitdown[pdf,docx,pptx]`처럼 선택 설치, `[all]`로 전체 설치 |
| 확장 | third-party plugin은 기본 비활성화, `--use-plugins`로 명시 활성화 |

## 처리 계층

1. 기본 converter는 format별 로컬 추출을 수행한다.
2. `markitdown-ocr`는 OpenAI-compatible Vision client로 문서 안 이미지 OCR을 보강할 수 있다.
3. Azure Document Intelligence는 cloud OCR/layout 추출을 제공한다.
4. Azure Content Understanding은 문서·이미지·음성·영상 분석과 custom/prebuilt analyzer, YAML front matter 기반 field extraction을 제공하며 호출 과금이 발생한다.

## 한계와 선택 기준

MarkItDown은 text analysis와 LLM pipeline용이다. 따라서 원본의 정밀한 출판 레이아웃을 보존하는 도구로 기대하면 안 된다. 스캔본, 다단 레이아웃, 복잡한 표는 실제 대표 문서로 품질을 확인한 뒤 OCR 또는 Azure tier-up 여부를 정한다.

## Sources

- https://github.com/microsoft/markitdown
- https://pypi.org/project/markitdown/
- https://learn.microsoft.com/en-us/azure/ai-services/content-understanding/overview
- https://learn.microsoft.com/en-us/azure/ai-services/document-intelligence/overview
