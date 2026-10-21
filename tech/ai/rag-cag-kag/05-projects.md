---
date: 2026-10-21
tags: [tech]
type: tech-tool-study
status: draft
---

# Projects

## 1. 사내 정책 Copilot

**구성**: hybrid RAG + document ACL + 문단 단위 citation + freshness/SLA metadata.

**완료 기준**: 권한 없는 문서가 top-k에 나타나지 않고, 각 답변 주장이 해당 문단으로 검증되며, 정책 문서 갱신이 index version과 trace에 반영된다.

## 2. 고정 매뉴얼 지원 봇

**구성**: 작은 제품 매뉴얼을 canonical prefix로 만들고 CAG/provider prompt caching의 warm path를 RAG와 비교한다.

**완료 기준**: cold/warm latency·token cost·citation correctness를 같은 evaluation set으로 비교하고, 매뉴얼 release 시 cache refresh 절차를 문서화한다.

## 3. 규제·계약 검토 assistant

**구성**: 조항, 의무, 예외, 당사자 relation을 schema화한 KAG/GraphRAG와 raw clause retrieval.

**완료 기준**: multi-hop/exception 질문에서 baseline RAG보다 개선되고, 답변마다 source clause·document version·reasoning trace가 남는다.

## 4. Research intelligence

**구성**: ingest 시 entity/claim graph를 만들고 local fact QA와 global trend summary를 분리한다.

**완료 기준**: community summary가 global 질문에 기여하는지, index 비용과 graph noise가 허용 범위인지 평가한다.

## 5. RAG router

**구성**: 질의와 corpus 특성으로 direct answer / CAG / standard RAG / graph reasoning을 선택한다.

**완료 기준**: router도 동일한 evaluation set, latency, cost, citation metric으로 평가하며 복잡한 route가 baseline을 이기는 경우만 채택한다.

## Sources

- https://github.com/OpenSPG/KAG
- https://microsoft.github.io/graphrag/get_started/
- https://developers.openai.com/api/docs/guides/prompt-caching
