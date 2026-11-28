---
date: 2026-11-28
tags: [tech]
type: tech-tool-study
status: draft
---

# 심화 학습: Selection과 routing 분리하기

## 실습 범위

아래 절차와 숫자는 개념 이해를 위해 만든 예시다. P-FedSkill의 공식 알고리즘·목적함수·실험 결과가 아니다.

## Task heterogeneity 통제

두 종류의 합성 task와 같은 skill 후보군을 준비한다. Client A는 표 계산 80%·문서 요약 20%, Client B는 표 계산 20%·문서 요약 80%로 구성한다. Skill마다 task 유형별 성공률을 별도 평가 task에서 측정한다.

| 가상 patch | 표 계산 성공률 | 문서 요약 성공률 | A의 가중 평균 | B의 가중 평균 |
|---|---:|---:|---:|---:|
| 계산 검증 전략 | 0.90 | 0.20 | 0.76 | 0.34 |
| 요약 구조화 전략 | 0.30 | 0.85 | 0.41 | 0.74 |

가중 평균은 `Σ(task 비중 × 해당 유형 성공률)`이다. 같은 skill도 client의 task 구성에 따라 유용성이 달라질 수 있음을 보여준다. 이 식을 논문의 PSS score로 해석해서는 안 된다.

## Ablation 설계

| 구성 | 확인할 질문 |
|---|---|
| 모든 client에 동일 skill set, routing 없음 | 전체 공유의 기준 성과는? |
| Client별 selection만 적용 | Client별 후보군 조정 효과는? |
| 공통 skill set에 routing만 적용 | 현재 task 적합성만 고려한 효과는? |
| Client별 selection + routing | 두 단계 조합의 추가 효과는? |

후보 skill 수, context budget, agent 모델과 평가 task를 동일하게 유지한다. 임의의 간단한 condition 매칭을 사용했다면 TASR 재현이 아니라 학습용 proxy라고 기록한다.

## 측정과 해석

- **성과:** 전체 평균, client별 성공률, 가장 낮은 client 성과를 함께 기록한다.
- **비용:** Selection 평가 호출, routing 시간, 입력 토큰, 저장·전송 크기를 기록한다.
- **분리:** Selection용 평가 task와 최종 평가 task를 나누어 결과 누출을 줄인다.
- **반복:** 실행 변동이 있다면 여러 번 수행하고 횟수와 분산을 기록한다.
- **실패:** Condition 오판, 평가 결과 부족, task 분포 변화 시 skill 선택이 어떻게 흔들리는지 관찰한다.

## 이론·privacy 검토

Theoretical guarantee는 존재 주장만 확인된다. 가정과 theorem을 읽기 전에는 최적성·수렴성을 단정하지 않는다.

Privacy 검토에서는 condition과 strategy에 원본 식별자·고유 문장·민감한 작업 내용이 남는지 살펴본다. 원본 trajectory를 공유하지 않는다는 설계만으로 privacy가 보장되지는 않는다. Differential Privacy나 공격 평가가 논문에 포함된 것으로 가정하지 않는다.

## Related Notes

- [[tech/ai/personalized-federated-skill-learning/README|학습 진입점]]

## Sources

- https://arxiv.org/abs/2611.33707 — 제공된 dossier의 서지 정보·초록 설명을 근거로 정리. 전문·코드·실험 수치는 확인하지 않음.
