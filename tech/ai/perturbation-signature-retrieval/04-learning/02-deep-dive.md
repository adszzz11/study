---
date: 2026-11-27
tags: [tech]
type: tech-tool-study
status: draft
---

# Deep Dive: 평가·누수·근거

## 평가 계약

실험 행 검색인지 compound·target 검색인지 먼저 정한다. 같은 compound의 여러 실험 행이 Top-K를 채우면 후보 단위 성능과 행 단위 성능은 달라질 수 있다. 후보 집계 방식과 동점 규칙을 고정하고, 알려지지 않은 annotation을 자동으로 오답 처리하지 않는다.

| 지표 | 정의 | 전제 |
|---|---|---|
| Precision@K | 상위 K 중 relevant 후보 수 / K | K개 결과와 명확한 label |
| Recall@K | 상위 K의 relevant 후보 수 / 전체 relevant 후보 수 | 전체 relevant 집합을 알아야 함 |
| MRR | query별 첫 relevant 결과 순위의 역수 평균 | 미검색은 0, 평가 깊이 명시 |

Relevant 후보가 없는 query의 처리와 실제 반환 수가 K보다 작은 경우의 분모를 사전에 명시한다. 정답 정의 없이 지표만 계산하지 않는다.

## 분할별 질문

| 분할 | 답하려는 일반화 질문 | 주의점 |
|---|---|---|
| 실험 행 무작위 분할 | 기존 identity 주변의 새 관측을 찾는가? | 가까운 replicate 공유로 쉬워질 수 있음 |
| Perturbation identity 분할 | 보지 못한 개입으로 일반화하는가? | 같은 identity는 같은 split에 배치 |
| 조건 분할 | 새로운 cell type·농도·시간에 대응하는가? | 조건의 결측과 겹침을 보고 |
| Compound / target 분할 | 새로운 화합물 또는 표적을 다루는가? | 두 분할은 별도 질문이며 관계 중복도 확인 |

검색에서는 query·학습 데이터·검색 corpus의 역할을 구분한다. 새로운 identity의 후보를 corpus에 제공하는지, 학습에서만 제외하는지 적어야 평가 의미가 분명해진다. 전처리 통계와 학습 표현은 학습 split에서만 추정한다.

## 안정성 실험

1. 비교 가능한 control과 replicate만 사용해 기준 순위를 만든다.
2. Control 선택 또는 replicate 구성을 바꾸어 순위를 다시 계산한다.
3. Top-K 겹침과 후보별 순위 변화를 기록한다.
4. Context별 결과를 별도로 보고한다. 작은 표본의 단일 점수를 일반화하지 않는다.

## 근거 출력 계약

```text
candidate_id, candidate_type, rank, similarity_score,
evidence_experiment_ids, context, replicate_consistency,
known_target_annotation, annotation_source, uncertainty
```

유사도, 반복 관측의 일관성, 알려진 target 연결은 별도 근거다. 관계 정보의 출처가 없으면 ‘미확인’으로 남긴다. 검색 성공은 target identification이나 기능적 효과의 실험 검증을 대체하지 않는다. 이 평가가 원 논문에서 수행되었는지는 알 수 없다.

## 연결

[[tech/ai/perturbation-signature-retrieval/05-projects|평가 프로젝트]] · [[tech/ai/perturbation-signature-retrieval/cheatsheet|검토 체크리스트]] · [[tech/ai/perturbation-signature-retrieval/README|학습 지도]]

## Sources

- 사용자 제공 dossier: 영상 00:47에 주제의 논문 제목이 표시되었다는 설명. 영상 및 논문 URL은 제공되지 않아 기재할 수 없다.
- 아래 설계·실습은 dossier를 바탕으로 만든 학습용 제안이며, 원 논문의 구현 또는 검증 결과가 아니다.
