---
date: 2026-10-24
tags: [tech]
type: tech-tool-study
status: draft
---

# Ecosystem and trade-offs

| 영역 | 주 접근 | 강점 | 한계 / 보완 시점 |
|---|---|---|---|
| Retrieval | `BM25` lexical search | 정확한 keyword, 상품 코드, 고유명사에 강함 | 의미 유사성은 약해 dense retrieval과 결합 |
| Retrieval | `Bi-Encoder` dense retrieval | ANN/vector index에서 빠르고 semantic match에 강함 | 세밀한 query-document 상호작용은 약함 |
| Ranking | `Cross Encoder` reranker | 상위 후보 관련성 판정이 정밀 | 비싸므로 모든 문서 대신 top-K에 적용 |
| Ranking | `Hybrid Search` | lexical·semantic recall을 함께 확보 | fusion weight, latency, 운영 복잡도 증가 |
| Agent 학습 | `PPO` | 검증된 안정적 policy-gradient 계열 | critic/value model이 memory·복잡도를 늘릴 수 있음 |
| Agent 학습 | `GRPO` | sample group의 상대 보상으로 critic 부담을 줄이는 PPO 계열 접근 | reward 설계, group size, reward hacking 검증이 중요 |
| Agent 실행 | 자유형 ReAct-style Agent | 탐색 유연성이 큼 | nondeterminism, 통제, 재현이 어려움 |
| Agent 실행 | `Workflow Graph` orchestration | 도구 순서, 재시도, guardrail, 관측성이 좋음 | 새로운 상황의 유연성은 줄 수 있음 |
| 평가 | `MTEB` / `RTEB` | embedding·retrieval의 표준화된 비교 | 도메인 로그와 실제 product KPI를 대체하지 못함 |
| 평가 | `BrowseComp` | browsing Agent의 지속 탐색 능력을 측정 | 일반 검색 UX 전체를 대표하지 않음 |
| 품질 평가 | `LLM-as-a-Judge` | 빠르고 확장 가능 | bias·prompt sensitivity 때문에 human eval calibration이 필요 |

## 선택 순서

1. **Retrieval recall**: BM25와 dense retrieval을 각각 측정하고, 놓치는 질의 유형을 확인한다.
2. **Ranking precision**: latency budget 안의 top-K에 Cross Encoder를 붙인다.
3. **Agent control**: 고위험 도구·재시도·fallback이 있으면 Workflow Graph로 명시한다.
4. **Evaluation**: 공개 benchmark는 출발점으로 쓰되 search log, CTR, conversion, latency와 사람 평가로 검증한다.

`Hybrid Search`의 결합은 단순 평균일 필요가 없다. reciprocal-rank fusion, learned fusion, query intent별 routing 중 어느 것이 적합한지는 query mix와 운영 비용을 측정해 정한다.

## Sources

- https://www.sbert.net/examples/sentence_transformer/applications/retrieve_rerank/README.html
- https://arxiv.org/abs/1707.06347
- https://github.com/embeddings-benchmark/mteb
- https://browsecomp.github.io/
