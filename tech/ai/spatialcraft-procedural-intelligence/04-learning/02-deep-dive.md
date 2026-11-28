---
date: 2026-11-26
tags: [tech]
type: tech-tool-study
status: draft
---

# Deep Dive: Experience의 효용과 통합

## Skill-anchored 제공

Experience를 task 시작 시 한 번 주는 방식과, 연결된 Skill의 활성 구간에 제공하는 방식을 구분한다. 비교 시 지침 내용과 task 조건을 맞추어 제공 시점의 차이를 관찰한다. Context 절약 효과는 별도 측정 없이는 주장하지 않는다.

## Withholding 실습

1. 같은 task에 대해 반복 rollout을 준비한다.
2. 후보 Experience를 무작위로 제공하거나 제외한다.
3. 정답 여부, 호출 횟수, 실행 비용을 기록한다.
4. task별 차이를 살핀 후 여러 task에서 경향이 반복되는지 본다.

| task | Experience | 제공 여부 | 정답 여부 | 호출 수 | 비용 |
|---|---|---|---|---|---|
| 동일 task ID | 후보 ID | 제공 / withholding | 관측값 | 관측값 | 관측값 |

학습용 요약 지표는 다음처럼 둘 수 있다.

```text
Δaccuracy(task) = 해당 task의 제공군 정답률 − 제외군 정답률
```

**이 식은 논문의 Contrastive Utility Score가 아니다.** 정확한 논문 수식과 제외 확률·rollout 수는 제공 자료에 없다. 표본 수와 변동성을 함께 기록하고 적은 실행만으로 규칙을 확정하지 않는다.

같은 task 안에서 무작위 제외하는 설계는 task difficulty와 Experience 기여를 분리하려는 장치다. 여러 Experience를 함께 바꾸면 상호작용 때문에 개별 기여를 해석하기 어려울 수 있다. 엄밀한 개별 causal effect가 보장된다고 말하지 않는다.

## Consolidation 실습

반복적으로 유용했던 Experience를 Skill 절차에 반영하고 세 상태를 비교한다.

| 상태 | 목적 |
|---|---|
| 통합 전 Skill | 기준 성능 확인 |
| Skill + 외부 Experience | 전술 제공의 효과 확인 |
| Experience를 통합한 Skill | 절차 변경 후 효과 유지 여부 확인 |

통합에 쓰지 않은 task도 평가한다. Skill 버전과 변경 이유를 기록하고, 실습에서는 성능이 떨어지면 이전 버전으로 돌아갈 수 있게 보관한다. 이는 실습 운영 제안이며 논문의 퇴행 처리 정책으로 확인된 것은 아니다.

## 해석 체크리스트

- [ ] 기억 개수보다 적절한 시점의 행동 변화가 관측되는가?
- [ ] 도구 품질·모델 설정 변화가 효과에 섞이지 않았는가?
- [ ] 정확도 개선에 필요한 추가 호출·비용을 함께 기록했는가?
- [ ] 통합에 사용하지 않은 task에서도 경향이 유지되는가?
- [ ] 실패 사례와 불확실성을 숨기지 않았는가?

## 연결

- [[tech/ai/spatialcraft-procedural-intelligence/README|학습 경로]]
- [[tech/ai/spatialcraft-procedural-intelligence/05-projects|실전 프로젝트]]
- [[tech/ai/spatialcraft-procedural-intelligence/03-references|전문에서 확인할 질문]]

## Sources

- https://arxiv.org/abs/2611.31475 — SpatialCraft 논문. 이 노트는 제공된 초록·서지 정보 dossier에 근거하며, 전문이나 공식 코드를 검증한 결과가 아니다.
