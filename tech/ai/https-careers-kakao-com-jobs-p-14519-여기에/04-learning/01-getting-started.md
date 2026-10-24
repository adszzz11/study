---
date: 2026-10-24
tags: [tech]
type: tech-tool-study
status: draft
---

# Getting started: 작은 retrieve-rerank pipeline

## 목표

작은 문서 집합에서 lexical과 dense 후보를 합치고, 상위 후보만 정밀 rerank하는 흐름을 이해한다. 실제 production index·GPU cluster가 아니라 개념 검증용 실습이다.

```python
query = "강남역 근처 늦게까지 하는 카페"

lexical = bm25.search(query, top_k=50)
dense = vector_index.search(embed(query), top_k=50)
candidates = reciprocal_rank_fusion(lexical, dense)[:30]
ranked = cross_encoder.rank([(query, doc.text) for doc in candidates])
answer = llm.answer(query=query, evidence=ranked[:5])
```

## 단계

1. 문서마다 `id`, `text`, `metadata`, `source`를 저장한다. metadata에는 장소·상품 같은 structured filter를 넣는다.
2. `BM25`로 exact match 후보를, embedding으로 semantic 후보를 각각 얻는다.
3. 동일 문서를 id로 deduplicate하고 fusion 후 top-K만 `Cross Encoder`에 전달한다.
4. 답변에는 인용할 evidence와 “정보 부족” fallback을 포함한다.
5. query별 latency를 retrieval, reranking, LLM synthesis로 나누어 기록한다.

## 첫 평가

| 지표 | 질문 |
|---|---|
| `Recall@K` | 정답 문서가 상위 K 후보 안에 들어왔는가? |
| `MRR` | 첫 관련 문서가 얼마나 앞에 있는가? |
| `NDCG` | 여러 관련도 등급을 고려할 때 순위가 좋은가? |
| latency | p50/p95가 서비스 budget을 만족하는가? |

`Search Log`는 query, 노출 순위, 후보, 클릭, 체류, 전환처럼 검색 세션에서 생기는 기록이고, `Click Data`는 그중 사용자 반응 신호다. 클릭 없음은 항상 negative가 아니다. 이미 답을 보았거나 노출 위치가 나빴을 수 있으므로 position bias와 query intent를 함께 고려한다.

## Sources

- https://www.sbert.net/examples/sentence_transformer/applications/retrieve_rerank/README.html
- https://github.com/embeddings-benchmark/mteb
