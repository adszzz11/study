---
date: 2026-11-25
tags: [tech]
type: tech-tool-study
status: draft
---

# Ecosystem: Harness 정책과 비교 시스템

## 비교 지도

이 자료의 ecosystem은 제품 목록보다 harness 설계 대안과 비교 대상 agent를 중심으로 읽는 것이 적절하다. 정책과 완성된 시스템은 비교 단위가 다르다.

| 대상 | 역할·접근 | 제공 자료의 비교 결과 | 미확인 사항 |
|---|---|---|---|
| Recency truncation | 최근 이력을 남기는 baseline | 설계 선택의 비교 기준 | 보존 길이·절단 규칙 |
| Rolling summary | 누적 이력을 갱신 요약으로 관리 | 개별 접근 가능한 기록 보존보다 불리 | Prompt·길이·갱신 주기 |
| Context folding | 과거 시도 기록 관리 | 여섯 setting 최상위, 최대 19.2% 개선 | 알고리즘·추가 비용 |
| Skill deletion | 지속적 미사용 lesson 선별 삭제 | 통합·상시 규칙 승격보다 평균적으로 우세 | 미사용 정의·threshold·복구 |
| Skill consolidation | 여러 lesson 통합 | 선택적 삭제가 평균적으로 우세 | 통합 기준·충돌 처리 |
| Standing-rule promotion | Lesson을 상시 규칙으로 승격 | 선택적 삭제가 평균적으로 우세 | 승격 조건·우선순위 |
| MLEvolver | Context folding + skill deletion | 명시된 benchmark subset에서 높은 성과 | 구현·재현 절차·세부 ablation |
| AIDE | 비교 autoresearch 시스템 | 동일 inference budget에서 MLEvolver 우세 | 구조·버전·개별 점수 |
| OpenEvolve | 비교 autoresearch 시스템 | 동일 inference budget에서 MLEvolver 우세 | 구조·버전·개별 점수 |

## 선택할 때의 질문

아래는 논문이 검증한 원인이 아니라 실습 설계를 위한 질문이다.

- **기록 보존:** 요약 후에도 특정 실패의 실행 조건을 다시 확인할 수 있는가?
- **통합:** 적용 조건과 예외가 사라지지 않는가?
- **규칙 승격:** 한 실험에서 나온 교훈을 모든 상황에 적용해도 되는가?
- **삭제:** 드물지만 유용한 lesson을 미사용이라는 이유만으로 제거하지 않는가?

실험 기록의 접근성을 유지하면서 교훈을 선별하는 비대칭성이 중요하다. “Memory를 늘리면 좋아진다”로 단순화하면 두 정책의 차이를 놓친다.

## 비교의 한계

보고된 순위를 다른 모델·연구 분야에 일반화하지 않는다. 동일 inference budget에서의 우위도 전체 운영 비용이나 실행 시간의 우위를 입증하지 않는다. AIDE와 OpenEvolve의 내부 구조는 제공 자료로 설명할 수 없다.

## Navigation

- [[tech/ai/autoresearch-harness-design/README|학습 진입점]]

## Sources

- https://arxiv.org/abs/2611.28244
- https://doi.org/10.48550/arXiv.2611.28244
