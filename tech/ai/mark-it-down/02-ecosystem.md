---
date: 2026-10-21
tags: [tech]
type: tech-tool-study
status: draft
---

# Ecosystem and comparison

| 도구 | 강점 | MarkItDown보다 적합한 경우 |
|---|---|---|
| **MarkItDown** | 가볍고 범용적, Markdown output, Office·URL·MCP, Azure 연계 | 빠른 RAG ingestion 및 agent tool |
| **Docling** | PDF layout, reading order, table/formula/image 이해, OCR/VLM, lossless JSON·MCP·API server | 복잡한 PDF 구조 정확도와 후처리 모델이 중요할 때 |
| **Unstructured** | partitioning/chunking과 connector 중심 ingestion | 다양한 connector 및 enterprise pipeline이 필요할 때 |
| **PyMuPDF** | 빠른 저수준 PDF 처리, 텍스트·이미지·렌더링 제어 | PDF 전용 bespoke extraction을 구현할 때 |
| **Azure Document Intelligence / Content Understanding** | 관리형 OCR·layout·domain field extraction·confidence | 스캔 업무 문서, SLA, 신뢰도 기반 자동화가 필요할 때 |

## 선택 가이드

- **범용 Markdown 변환**: 여러 파일 유형을 간단히 수집하고 Markdown을 공통 계약으로 삼는다면 MarkItDown부터 시작한다.
- **정교한 PDF 이해**: reading order나 복잡한 table·formula가 search 품질을 좌우하면 Docling benchmark를 추가한다.
- **pipeline/connectors**: 변환 이후 partitioning, chunking, 외부 data source 연결이 중심이면 Unstructured를 평가한다.
- **업무 field 추출**: invoice number처럼 검증 가능한 필드와 confidence가 필요하면 Azure managed service를 설계에 넣는다.

## 평가 방법

동일한 대표 문서 묶음에 대해 (1) heading/table/link 보존, (2) OCR 오류, (3) chunk 수와 token 수, (4) retrieval 정답률, (5) 처리 시간·비용을 기록한다. 단일 샘플의 보기 좋은 Markdown만으로 선택하지 않는다.

## Sources

- https://github.com/docling-project/docling
- https://docs.unstructured.io/open-source/introduction/overview
- https://github.com/microsoft/markitdown
- https://learn.microsoft.com/en-us/azure/ai-services/document-intelligence/overview
