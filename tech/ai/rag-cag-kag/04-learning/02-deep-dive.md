---
date: 2026-10-21
tags: [tech]
type: tech-tool-study
status: draft
---

# Deep dive: CAG and graph reasoning

## CAG benchmark

동일한 정적 corpus와 evaluation set으로 RAG, long-context prompting, CAG를 비교한다. CAG의 prompt는 공유 corpus를 앞에 고정하고 질문을 뒤에 둔다.

```text
[stable system instruction][canonical corpus, unchanged]  ← cached prefix
[user question][answer/citation instruction]              ← per-request suffix
```

| 측정 | 확인할 질문 |
|---|---|
| cold/warm latency | prefill과 cache-hit path가 각각 얼마나 빠른가? |
| token cost | 반복 prefix의 비용이 실제로 줄었는가? |
| accuracy | long context에서 필요한 근거를 계속 찾는가? |
| refresh | 문서 변경 때 cache를 어떤 단위로 무효화·재생성하는가? |
| capacity | context window, GPU memory, eviction이 peak load에서 충분한가? |

provider의 prompt caching은 cache key, 최소 prefix 길이, retention, 요금 정책이 다를 수 있다. 운영 전에 공식 문서와 실제 request trace를 확인한다.

## KAG/GraphRAG prototype

multi-hop set에서 RAG가 반복적으로 실패할 때만 아래 최소 모델을 만든다.

1. domain schema에 entity, relation, claim, source span, document version을 정의한다.
2. extraction 결과를 샘플링 검수해 entity resolution과 relation 오류를 기록한다.
3. 질문을 graph traversal 또는 logical form/plan으로 변환하고, graph 결과와 원문 chunk를 함께 가져온다.
4. answer마다 raw source clause와 reasoning trace를 보존한다.
5. local fact QA와 global theme QA를 분리해 GraphRAG community summary의 효과를 평가한다.

graph를 정답의 유일한 근거로 취급하지 않는다. graph edge는 추출 오류를 가질 수 있으므로 생성 prompt에는 원문 위치와 버전을 함께 전달한다.

## 운영 guardrails

- ACL은 graph traversal과 chunk retrieval 모두에 적용한다.
- index/corpus version, query rewrite, retrieved IDs, reranker score, cache hit 여부를 trace로 남긴다.
- 데이터 변경은 re-index 및 cache invalidation의 명시적 trigger가 되게 한다.
- graph indexing 비용, LLM structured-output failure, stale summary를 별도 monitor한다.

## Sources

- https://arxiv.org/abs/2412.15605
- https://developers.openai.com/api/docs/guides/prompt-caching
- https://docs.vllm.ai/en/latest/features/automatic_prefix_caching/
- https://microsoft.github.io/graphrag/index/overview/
- https://arxiv.org/abs/2409.13731
