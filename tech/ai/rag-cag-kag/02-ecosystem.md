---
date: 2026-10-21
tags: [tech]
type: tech-tool-study
status: draft
---

# Ecosystem and comparison

| 접근 | 지식 접근 방식 | 적합한 경우 | 핵심 장점 | 주요 한계 |
|---|---|---|---|---|
| Naive/Advanced RAG | query-time vector/BM25/hybrid retrieval | 크고 자주 바뀌는 문서, enterprise search | 증분 갱신, 비교적 예측 가능한 비용/context | retrieval miss, chunk 경계, reranking 튜닝 |
| CAG | 전체 또는 공유 corpus의 prefilled KV cache | 작은/중간 정적 corpus, 반복 질의 | retrieval 제거, warm-cache latency 절감 | long-context 품질, memory 압박, cache invalidation |
| KAG | Knowledge Graph + chunk/vector + logical reasoning | 관계·규칙이 중요한 전문 도메인 | multi-hop, 제약 기반 답변, 설명 가능성 | ontology·graph 구축/운영, extraction 오류 |
| GraphRAG | entity graph + community summary + local/global retrieval | corpus 전체 관계·theme·sensemaking | global 질문과 관계 탐색 | indexing LLM 비용, graph noise |
| Fine-tuning | 모델 파라미터에 지식/행동 흡수 | 안정된 반복 업무, 출력 형식/행동 | inference context 절약, 스타일 일관성 | 최신 지식·출처 보장 부적합, 재학습 비용 |
| Long-context prompting | 원문을 매 질의 직접 주입 | 소량의 단발성 분석 | 가장 단순한 구현 | 반복 prefill 비용, 근거 선택 문제 |

## 선택 순서

1. **RAG baseline**: 대표 corpus와 질문으로 retrieval·citation·latency 평가를 먼저 만든다.
2. **CAG 비교**: corpus가 작고 정적이며 prefix가 공유될 때 cold/warm latency, token cost, 정답률을 같은 evaluation set으로 비교한다.
3. **KAG/GraphRAG 확장**: multi-hop, entity constraint, 규칙/예외가 반복 실패 원인일 때만 schema와 provenance를 도입한다.

## 구성 요소

| 계층 | RAG | CAG 추가 요소 | KAG/GraphRAG 추가 요소 |
|---|---|---|---|
| ingestion | parser, chunker, metadata | cacheable canonical corpus | entity/relation/claim extraction |
| storage | vector DB 또는 search engine | KV/prefix cache 정책 | graph store, ontology/schema |
| query | rewrite, filter, hybrid retrieval, reranker | stable prefix + request suffix | graph query, symbolic executor, hybrid retrieval |
| 운영 | evaluation, tracing, ACL | cache hit/eviction, refresh | provenance, graph quality, index cost |

## Sources

- https://github.com/OpenSPG/KAG
- https://openspg.github.io/v2/
- https://microsoft.github.io/graphrag/get_started/
- https://docs.langchain.com/oss/python/learn
