---
date: 2026-10-21
tags: [tech]
type: tech-tool-study
status: draft
---

# Projects

## 1. Knowledge RAG ingestion

SharePoint에서 export한 DOCX·PPTX·PDF를 Markdown으로 변환하고, source path·문서 유형·변환 시각 metadata를 추가한다. heading 기준 chunk → embed → vector DB index 순서로 연결한다. 대표 질의의 retrieval 정답률과 변환 오류율을 release 기준으로 둔다.

## 2. 회의·교육 아카이브

녹음 전사와 발표자료를 같은 Markdown corpus로 정규화한다. 발표자료의 slide heading과 전사 시점을 metadata로 연결해 회의 검색과 Q&A의 인용 근거를 개선한다.

## 3. Document-to-agent MCP tool

신뢰된 local agent가 사용자가 선택한 파일만 필요할 때 Markdown으로 변환하게 한다. MCP server는 localhost/container에 한정하고, directory는 최소 read-only mount하며 URI allowlist를 둔다.

## 4. Invoice/contract automation

일반 텍스트 검색·요약은 MarkItDown path로 처리한다. 금액·거래처·계약일처럼 confidence와 정형 field가 필요한 단계는 Azure Content Understanding custom analyzer를 병행한다. 자동 확정 전에 human review 기준을 설계한다.

## 5. CI 문서 품질 검사

repository의 Office 문서를 Markdown으로 변환하고 heading/link/table 결과를 snapshot test로 감시한다. converter upgrade 시에는 snapshot diff를 사람이 승인해 의미 있는 구조 변화와 단순 formatting 변화를 구분한다.

## Sources

- https://github.com/microsoft/markitdown
- https://learn.microsoft.com/en-us/azure/ai-services/content-understanding/overview
