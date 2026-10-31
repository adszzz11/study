---
date: 2026-10-24
tags: [tech]
type: tech-tool-study
status: draft
---

# Agentic Search Platform overview

## What

`Agentic Search Platform`은 LLM이 즉시 답을 생성하는 대신, 질의를 이해하고 계획을 세워 검색 index·API·browse 같은 도구에서 근거를 모은 뒤 답을 만드는 시스템이다. 공고의 적용 예시는 카카오맵 검색, 톡딜 상품 검색, 카나나 in 카카오톡, 카나나 검색이다.

```text
User query
  → Query understanding / Agent Planning
  → Tool Calling (search index, API, browse, service tools)
  → Candidate retrieval (dense + lexical)
  → Reranking (cross encoder)
  → LLM synthesis / answer
  → Offline + online evaluation → feedback / retraining
```

## Why

`keyword match`만으로는 “무엇을, 어느 순서로, 어떤 도구로” 찾아야 하는 복합 질의를 풀기 어렵다. 예를 들어 장소의 영업 상태와 상품 속성을 동시에 확인하는 답은 retrieval, structured API, 출처 검증을 조합해야 한다. 좋은 시스템은 결과를 찾는 것뿐 아니라 중복·spam·잘못된 metadata를 줄여 그 다음 단계의 오류도 낮춘다.

## 핵심 특징

| 축 | 역할 | 성공 조건 |
|---|---|---|
| Agentic Search LLM | planning, tool use, answer synthesis | 필요한 근거를 적은 단계와 안전한 도구 호출로 확보 |
| Search Ranking Model | retrieval 및 candidate 순위화 | 관련 결과를 latency budget 안에서 상위에 배치 |
| Search Data Modeling | 품질 점수, 속성 추출, 정규화 | 신뢰성 있고 중복 없는 검색 corpus 유지 |
| Evaluation | offline·online·human evaluation | 모델 지표와 실제 만족도 사이의 차이를 감시 |

## 용어 지도

| 계층 | 용어 | 해석 |
|---|---|---|
| Agent | `LLM` | 텍스트 이해·생성·추론과 도구 호출 정책을 맡는 Large Language Model |
| Agent | `Planning` | 목표를 하위 작업으로 나누고 필요한 정보·도구의 순서를 정하는 과정 |
| Agent | `Tool Use` / `Tool Calling` | 검색, DB, 지도, 상품 API를 정해진 schema로 호출하는 능력 |
| Agent | `Agent Orchestration` | Agent·도구·상태·재시도·안전 규칙을 workflow로 조정하는 계층 |
| Agent | `Long-Horizon Reasoning` | 여러 탐색·검증 단계를 누적해 답에 도달하는 추론 |
| Agent | `Dynamic Environment` | 시간과 행동에 따라 index/API 관측값이 바뀌는 상호작용 환경 |
| Retrieval | `Search Index` | token, vector, metadata를 저장해 빠른 retrieval을 지원하는 자료구조 |
| Retrieval | `Embedding Model` | query·문서·상품을 dense vector로 바꿔 의미 유사도를 계산하는 모델 |
| Retrieval | `Dense Retrieval` | embedding vector similarity로 후보를 찾는 검색 |
| Retrieval | `Hybrid Search` | BM25 같은 lexical retrieval과 dense retrieval을 결합하는 방법 |
| Ranking | `Reranking` | 1차 후보의 순위를 강한 모델로 다시 매기는 단계 |
| Ranking | `Bi-Encoder` | query와 document를 각각 encode하여 대규모 vector index를 빠르게 검색하는 구조 |
| Ranking | `Cross Encoder` | query-document를 함께 넣어 관련성을 정밀 판정하는 구조; 보통 top-K reranking에 사용 |

## Sources

- https://careers.kakao.com/jobs/P-14519
- https://www.sbert.net/examples/sentence_transformer/applications/retrieve_rerank/README.html
- https://arxiv.org/abs/1706.03762
