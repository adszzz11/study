---
date: 2026-11-28
tags: [tech]
type: tech-tool-study
status: draft
---

# P-FedSkill Cheatsheet

## 핵심 용어

| 용어 | 기억할 의미 |
|---|---|
| FSL | Trajectory를 compact skill representation으로 증류해 server에 공유 |
| Task heterogeneity | Client마다 수행 task가 달라 같은 skill의 기여도도 달라짐 |
| LSE | Trajectory에서 condition·strategy·outcome 추출 |
| Skill patch | Applicability condition + execution strategy |
| PSS | Outcomes와 conditions로 client별 personalized skill set 구성 |
| TASR | Conditions를 활용해 현재 task와 관련된 patch subset 선택 |

## 빠른 흐름

```text
경험 → LSE → patch + 별도 outcome
     → PSS → client별 후보군
     → TASR → 현재 task용 subset → 실행 지원
```

기능 관계만 표시했다. 통신 순서·정확한 실행 위치는 미확인이다.

## 해석 체크

| 가능한 설명 | 피할 단정 |
|---|---|
| Client별 유용성과 실행 시 적합성을 구분 | Similarity가 높으면 항상 유용함 |
| Outcome을 selection 평가 근거로 사용 | Outcome이 patch 내부 구성요소 |
| 저자들이 theoretical guarantee를 제시한다고 밝힘 | PSS 최적성이 증명됨 |
| 저자들이 extensive experiments로 검증했다고 주장 | 특정 개선율·benchmark를 추정 |
| 원본 trajectory 공유를 피하는 접근 | Privacy가 자동 보장됨 |

## 실습 요령

- 합성 trajectory로 condition과 strategy를 분리한다.
- Client별 task 비중을 바꾸고 전체 평균·client별 성과를 함께 본다.
- Selection 유무 × routing 유무를 같은 budget에서 비교한다.
- 학습용 proxy를 논문의 공식 알고리즘으로 소개하지 않는다.
- 설치 명령·repository·성능 수치는 자료 확인 전까지 쓰지 않는다.

## Related Notes

- [[tech/ai/personalized-federated-skill-learning/README|학습 진입점]]

## Sources

- https://arxiv.org/abs/2611.33707 — 제공된 dossier의 서지 정보·초록 설명을 근거로 정리. 전문·코드·실험 수치는 확인하지 않음.
