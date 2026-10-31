---
date: 2026-10-24
tags: [tech]
type: tech-tool-study
status: draft
---

# Deep dive: 학습, 데이터 품질, production 평가

## Ranking 학습 용어

| 용어 | 해석 |
|---|---|
| `Loss` | 예측과 목표 차이를 수치화한 학습 목적함수 |
| `Optimization` | loss를 낮추도록 parameter를 update하는 과정 |
| `Sampling` | 응답·negative·trajectory 후보를 선택·생성하는 방식 |
| `Negative Sampling` | 관련 없는 문서 또는 비클릭 후보를 negative example로 뽑는 과정 |
| `Hard Negative Mining` | 모델이 헷갈리지만 정답은 아닌 후보를 골라 학습 난도를 높이는 기법 |
| `Contrastive Learning` | positive query-document는 가깝게, negative는 멀게 embedding space를 학습하는 방법 |
| `Knowledge Distillation` | 강한 teacher의 점수·분포를 작은 student가 배워 serving 비용을 줄이는 방법 |

## Agent policy 학습

`Policy Optimization`은 더 높은 reward를 얻도록 행동 확률 분포(policy)를 강화학습으로 갱신하는 방법이다. `PPO`는 새 policy가 이전 policy에서 지나치게 멀어지지 않도록 clipping해 안정성을 높인다. `GRPO`는 같은 문제에서 여러 sample의 보상을 상대 비교해 advantage를 만들고, 별도 critic 부담을 줄이려는 PPO 계열 방법이다.

둘 다 “보상이 높다 = 유용한 답”이라는 가정에 의존한다. 따라서 tool call 횟수만 줄이는 reward는 필요한 탐색도 억제할 수 있고, 정답 문자열 보상은 출처 없는 우연한 답을 과대평가할 수 있다. reward hacking을 막으려면 tool trace, evidence correctness, 안전 정책 위반, 사람 평가를 함께 본다.

## Search data modeling

| 용어 | 해석 | downstream 영향 |
|---|---|---|
| `Data Quality Model` | 신뢰성·중복·정합성·완전성을 점수화/분류하는 모델 | 후보 품질과 answer grounding 향상 |
| `Abuse` / `Spam` | 부정 노출 조작·광고성 저품질 콘텐츠 | ranking과 사용자 신뢰를 훼손 |
| `Deduplication` | 동일·유사 문서/상품을 탐지, 통합, 제거 | 다양성과 click 분산 개선 |
| `Attribute Extraction` | 브랜드·가격·위치·규격 같은 구조화 속성 추출 | filter와 API answer 정확도 향상 |
| `Normalization` | 동의 표현을 표준값으로 통일 | filter miss와 fragmentation 감소 |

## 평가와 서빙

`Dataset`은 학습·평가 데이터 모음이고, `Benchmark`는 재현 가능한 비교 규약이다. `MTEB`는 embedding model의 retrieval·reranking·clustering 등을, `RTEB`는 production retrieval에 가까운 전문 도메인·다국어 retrieval을 평가하려는 benchmark다. `BrowseComp`는 단순 검색으로 찾기 어려운 웹 사실을 계속 browse하며 찾는 Agent를 측정한다.

`LLM-as-a-Judge`는 rubric에 따라 결과를 자동 채점해 빠르지만 bias와 prompt sensitivity가 있다. `Human Eval / Alignment`는 사람 평가와 자동 평가가 얼마나 맞는지 확인한다. 따라서 `Offline Metric`의 Recall@K/NDCG가 올라도 `Online Quality`의 CTR, conversion, 만족도, 안전성이 함께 오르는지는 A/B test와 error analysis로 검증해야 한다.

`Serving` / `Inference Optimization`은 모델을 API로 배포하면서 latency, throughput, GPU 비용을 맞추는 일이다. `Distributed Training`은 여러 GPU/node에 model·data·gradient를 나누는 학습이며, `InfiniBand GPU Cluster`는 node 사이의 고대역폭·저지연 통신을 제공하는 인프라다. 인프라 규모보다 먼저 병목이 retrieval인지 reranking인지 generation인지 측정한다.

## Sources

- https://arxiv.org/abs/1707.06347
- https://github.com/deepseek-ai/DeepSeekMath
- https://github.com/embeddings-benchmark/mteb
- https://browsecomp.github.io/
