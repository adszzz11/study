---
date: 2026-10-21
tags: [tech]
type: tech-tool-study
status: draft
---

# RAG · CAG · KAG overview

## What

**Retrieval-Augmented Generation (RAG)**는 query-time retrieval 결과를 LLM prompt에 넣는 방식이다. Lewis et al.은 pretrained seq2seq model의 parametric memory와 dense vector index의 non-parametric memory를 결합했다.

**Cache-Augmented Generation (CAG)**는 제한된 corpus를 long context에 prefill하고 그 **KV cache**를 보존한다. 이후 질문은 공유 prefix 뒤에 붙으므로 별도 retriever를 거치지 않는다.

**Knowledge-Augmented Generation (KAG)**는 Knowledge Graph, 원문 chunk/vector, domain schema와 logical reasoning을 함께 사용한다. OpenSPG KAG는 graph와 원문을 상호 인덱싱하고 logical-form-guided hybrid reasoning을 지향한다.

## Why

사내 문서와 최신 정보는 모델 재학습 없이 갱신되어야 하며, 답변이 어떤 원문을 근거로 했는지도 확인해야 한다. RAG는 이를 위한 실용적 기본값이지만 retrieval miss, 나쁜 chunk 경계, embedding/reranking 오류가 정답을 막는다. CAG는 작은 정적 corpus에서 이 retrieval 단계를 없앨 수 있고, KAG는 vector similarity만으로 부족한 관계·규칙 질의를 다룬다.

## 핵심 특징

| 접근 | 처리 흐름 | 강점 | 핵심 제약 |
|---|---|---|---|
| RAG | ingest → chunk → index → retrieve/rerank → grounded generation | 증분 갱신, 대규모 corpus | retrieval quality와 운영 복잡성 |
| CAG | corpus prefill → KV cache 보존 → 질문 append → generation | warm path latency와 retrieval error 감소 | context window, GPU memory, invalidation |
| KAG | entity/relation/schema → graph·chunk 검색 → logical plan/execution | multi-hop, constraint, 설명 가능성 | ontology·extraction·graph 운영 비용 |

## RAG architecture

```text
Documents → parsing/chunking → embedding + metadata index
Question → rewrite/filter → BM25/vector hybrid → reranker
        → grounded prompt → LLM → answer + citation + evaluation trace
```

metadata는 ACL, 문서 버전, source location, freshness를 담는다. access control은 retrieval **전에** 적용하고, citation이 실제 주장을 뒷받침하는지는 별도로 평가한다.

## CAG와 prompt caching

CAG의 전제는 “지식 전체가 context window에 들어가고, 대부분의 요청이 같은 prefix를 공유한다”이다. provider prompt caching 또는 vLLM Automatic Prefix Caching은 구현 기반이 될 수 있지만, cache eviction·knowledge refresh·문서 선택·정확성 평가를 자동으로 해결하지는 않는다. 공유되고 변하지 않는 corpus를 앞에, request별 질문을 뒤에 둔다.

## KAG와 GraphRAG

KAG는 하나의 제품명이 아니라 graph-informed knowledge system의 넓은 계열이다. Microsoft GraphRAG는 entity graph와 community detection/summary를 만들어 local fact 질문뿐 아니라 corpus 전체의 theme 같은 global 질문을 다룬다. graph indexing은 LLM 비용과 graph noise를 유발할 수 있으므로, raw chunk RAG가 실패한 multi-hop 평가셋으로 가치를 검증한다.

## Sources

- https://arxiv.org/abs/2005.11401
- https://arxiv.org/abs/2412.15605
- https://arxiv.org/abs/2409.13731
- https://microsoft.github.io/graphrag/index/overview/
- https://docs.vllm.ai/en/latest/features/automatic_prefix_caching/
