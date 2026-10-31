---
date: 2026-10-24
tags: [tech]
type: tech-tool-study
status: draft
---

# Projects

## 1. 장소·상품 hybrid search

**목표**: 200~1,000개의 공개 문서에 대해 BM25 + vector retrieval + Cross Encoder reranking을 만든다.

- query 유형: 정확한 상호명, 조건형 자연어, 동의어, 오탈자
- 산출물: query별 top-K, source, component별 latency, Recall@10/NDCG@10
- 검증: lexical-only, dense-only, hybrid를 같은 relevance set에서 비교한다.

## 2. 근거 기반 tool-calling Agent

**목표**: search와 detail API라는 두 tool을 schema로 정의하고, 답변마다 evidence id를 남긴다.

```text
plan → search(query) → inspect(document_id) → answer(evidence_ids)
```

- 최대 tool call 수, timeout, 허용 도메인을 정한다.
- evidence가 없으면 추측하지 않고 “확인할 수 없음”을 반환한다.
- 성공률뿐 아니라 잘못된 tool 순서, 무근거 답변, timeout을 failure taxonomy로 기록한다.

## 3. data quality feedback loop

**목표**: 중복·누락 속성·spam 후보를 labeling하고 retrieval 품질 변화까지 측정한다.

- `Deduplication`: canonical id와 near-duplicate 그룹을 분리한다.
- `Attribute Extraction`과 `Normalization`: 추출값, 원문, confidence를 모두 보관한다.
- before/after로 index size, Recall@K, 다양성, false positive를 비교한다.

## 완료 기준

offline score 하나만으로 완료하지 않는다. representative query set, p95 latency, 사람의 error review, 안전 fallback을 모두 통과해야 다음 단계의 production 실험 후보가 된다.

## Sources

- https://www.sbert.net/examples/sentence_transformer/applications/retrieve_rerank/README.html
- https://openreview.net/forum?id=Oljnxmf4pc
