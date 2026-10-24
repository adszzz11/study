---
date: 2026-10-24
tags: [tech]
type: tech-tool-study
status: draft
---

# Cheatsheet

## 검색 pipeline

```text
Query → planning/tool selection → retrieval → reranking → grounded answer → evaluation
```

| 용어 | 짧은 해석 |
|---|---|
| `Agentic Search` | LLM이 계획·도구 호출로 근거를 찾아 답하는 검색 |
| `Tool Calling` | schema에 맞춰 외부 search/API를 호출 |
| `Search Index` | token/vector/metadata 기반의 빠른 후보 검색 구조 |
| `Dense Retrieval` | embedding similarity로 후보를 검색 |
| `Hybrid Search` | lexical + dense retrieval 결합 |
| `Bi-Encoder` | 빠른 1차 후보 생성 모델 |
| `Cross Encoder` | 느리지만 정밀한 top-K reranker |
| `Reranking` | 1차 후보의 순위를 정밀 재정렬 |
| `Recall@K` | 정답이 상위 K에 포함되는 비율 |
| `NDCG` | 관련도 등급을 반영한 순위 품질 |

## 학습과 데이터

| 용어 | 짧은 해석 |
|---|---|
| `PPO` | 이전 policy와의 거리를 제한하는 안정적 RL update |
| `GRPO` | group 내 상대 reward로 advantage를 만드는 PPO 계열 방법 |
| `Hard Negative` | 모델은 비슷하다고 보지만 실제 정답은 아닌 학습 후보 |
| `Contrastive Learning` | positive는 가깝게, negative는 멀게 학습 |
| `Distillation` | teacher의 지식을 작은 student로 이전 |
| `Click Data` | 노출·클릭·체류·전환의 행동 로그 |
| `Data Quality Model` | 신뢰성·중복·정합성·완전성을 판정 |
| `Deduplication` | 중복/유사 항목 탐지·통합·제거 |
| `Normalization` | 같은 의미의 값을 표준 표현으로 통일 |

## 운영 체크

- `Offline Metric` 상승은 `Online Quality` 상승을 보장하지 않는다.
- `LLM-as-a-Judge`는 human eval calibration 없이 최종 기준이 될 수 없다.
- `Serving`에서는 accuracy뿐 아니라 p95 latency, throughput, GPU cost, fallback을 측정한다.
- `Workflow Graph`는 재시도·guardrail·trace를 명시하지만 자유형 Agent보다 덜 유연할 수 있다.

## Sources

- https://careers.kakao.com/jobs/P-14519
- https://arxiv.org/abs/1707.06347
- https://www.sbert.net/examples/sentence_transformer/applications/retrieve_rerank/README.html
