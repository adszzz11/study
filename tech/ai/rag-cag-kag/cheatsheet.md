---
date: 2026-10-21
tags: [tech]
type: tech-tool-study
status: draft
---

# RAG · CAG · KAG cheatsheet

## 빠른 선택

| 신호 | 기본 선택 |
|---|---|
| corpus가 크고 자주 바뀜 | RAG |
| corpus가 작거나 중간 크기, 정적, 질문 prefix 반복 | CAG를 RAG와 benchmark |
| multi-hop·규칙·entity constraint가 반복 실패 | KAG/GraphRAG prototype |
| 소량 원문을 한 번만 분석 | long-context prompting |
| 지식 갱신보다 고정 작업 행동/형식이 중요 | fine-tuning 검토 |

## RAG checklist

- [ ] parsing과 chunking 결과를 원문과 대조했다.
- [ ] ACL과 metadata filter를 retrieval 전에 적용한다.
- [ ] hybrid retrieval/reranker는 baseline 대비 평가셋으로 검증했다.
- [ ] answer correctness, context recall, citation correctness, latency, cost를 기록한다.
- [ ] source location·document version·retrieval trace를 보존한다.

## CAG checklist

- [ ] canonical corpus가 context window에 안정적으로 들어간다.
- [ ] 공유·불변 prefix를 앞, 질문을 뒤에 둔다.
- [ ] cold/warm path 모두 측정했다.
- [ ] cache hit, eviction, GPU memory, refresh/invalidation을 monitor한다.
- [ ] prompt caching 기능과 knowledge-system 품질을 혼동하지 않는다.

## KAG/GraphRAG checklist

- [ ] multi-hop failure가 RAG evaluation set에서 확인됐다.
- [ ] schema와 entity/relation extraction을 샘플링 검수했다.
- [ ] graph edge뿐 아니라 원문 span·version을 provenance로 제공한다.
- [ ] ACL을 graph와 chunk 양쪽에 적용한다.
- [ ] indexing 비용, graph noise, stale summary를 모니터링한다.

## Sources

- https://arxiv.org/abs/2005.11401
- https://arxiv.org/abs/2412.15605
- https://arxiv.org/abs/2409.13731
- https://microsoft.github.io/graphrag/get_started/
