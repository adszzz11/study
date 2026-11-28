---
date: 2026-11-27
tags: [tech]
type: tech-tool-study
status: draft
---

# Ecosystem: 설계 대안 비교

경쟁 서비스·비교 논문 정보가 없으므로 제품별 우열을 판단하지 않는다. 아래는 구현 전에 비교할 **설계 대안**이다.

| 접근 | 검색 근거 | 비교할 질문 | 해석 한계 |
|---|---|---|---|
| Metadata 검색 | annotation·조건 | 조건 필터만으로 얼마나 좁혀지는가? | signature 패턴은 사용하지 않음 |
| 직접 signature 비교 | 관측 특징·변화량 | 단순 거리·유사도의 baseline은? | scale·전처리에 의존 |
| Embedding 검색 | 학습 표현 | 미관측 조건에서 baseline보다 나은가? | 학습 구성·누수 검토 필요 |
| 관계 기반 검색 | signature–target–compound 연결 | 어떤 경로가 후보를 지지하는가? | 연결은 인과를 보장하지 않음 |
| Context 반영 검색 | signature와 조건 | 조건 내·조건 간 성능 차이는? | 결측·비교 가능성 처리 필요 |

## 조합과 선택

1. Query와 candidate 단위를 정한다.
2. 비교 가능한 조건으로 후보를 필터링한다.
3. 직접 벡터 검색을 baseline으로 둔다.
4. 데이터와 relevance label이 있을 때 embedding이나 관계 정보를 추가해 비교한다.
5. 검색 품질 외에 근거 추적성과 순위 안정성도 확인한다.

Metadata 필터와 벡터 순위화는 함께 쓸 수 있다. 알려진 관계가 없는 후보는 ‘미확인’으로 표시한다. 사용 도구·라이브러리·공개 데이터셋은 dossier에서 확인되지 않았다.

## 연결

[[tech/ai/perturbation-signature-retrieval/01-overview|검색 계약]] · [[tech/ai/perturbation-signature-retrieval/04-learning/02-deep-dive|평가 설계]] · [[tech/ai/perturbation-signature-retrieval/README|학습 지도]]

## Sources

- 사용자 제공 dossier: 영상 00:47에 주제의 논문 제목이 표시되었다는 설명. 영상 및 논문 URL은 제공되지 않아 기재할 수 없다.
- 아래 설계·실습은 dossier를 바탕으로 만든 학습용 제안이며, 원 논문의 구현 또는 검증 결과가 아니다.
