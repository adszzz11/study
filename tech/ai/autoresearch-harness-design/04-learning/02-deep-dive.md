---
date: 2026-11-25
tags: [tech]
type: tech-tool-study
status: draft
---

# Deep Dive: 보존·조회·일반화·삭제 분리하기

## 1. Skill 정책을 독립적으로 비교

Context 정책을 고정한 다음 동일 초기 lesson 집합에서 아래 정책을 비교한다. 모든 정책의 생성·검색·관리 비용을 같은 inference 한도에 포함하는 것은 실습 설계 제안이다.

| 정책 | 실습 조작 | 확인할 실패 가능성 |
|---|---|---|
| 유지 | Lesson을 계속 보관 | 불필요한 지침 누적 |
| 통합 | 유사 lessons를 합침 | 조건·예외 소실 |
| 상시 규칙화 | 선택 lesson을 매번 제공 | 과도한 일반화 |
| 미사용 삭제 | 지속적 미사용 후보를 비활성화 | 희귀하지만 유용한 교훈 손실 |

논문은 선택적 삭제의 평균적 우위를 보고하지만, 위 실패 가능성을 원인으로 검증한 것은 아니다.

## 2. 미사용과 무효 구별

```text
관련 상황이 발생했는가?
  아니오 → 사용 기회가 없었음
  예 → lesson이 조회되었는가?
         아니오 → 검색·노출 문제 후보
         예 → 적용되었는가?
                아니오 → 적용 조건·선택 이유 기록
                예 → 도움이 되었는가? 결과와 근거 기록
```

사용되지 않았다는 사실만으로 틀린 lesson이라고 판단하지 않는다. 조회·적용·효과를 분리해 event로 기록한다. 효과의 인과 판단에는 추가 비교가 필요하다.

## 3. 삭제 실험의 관측 가능성

다음은 공식 deletion 알고리즘이 아닌 실습용 의사코드다. 임계값은 실험자가 사전에 정하고 기록한다.

```python
for lesson in lessons:
    if eligible_opportunities(lesson) >= min_opportunities:
        if uses_in_window(lesson) == 0:
            archive_candidate(lesson, reason="persistent_non_use")
```

- Archive는 복구와 사후 분석을 위한 실습 선택이다. 논문의 복구 정책은 미확인이다.
- 기회 수와 관측 window를 바꾸는 sensitivity 실험은 기본 비교 이후 별도로 수행한다.
- 삭제 후보가 다시 필요한 상황을 별도 평가하여 드문 lesson의 손실을 확인한다.

## 4. 결합 효과 검토

가능하다면 개별 기록 접근 유무 × 선택적 삭제 유무의 2×2 비교를 구성한다. 같은 evaluator와 budget에서 각 조건을 반복하고 성과·조회량·관리 비용을 함께 본다. 이 설계 역시 논문 ablation을 재현한 것이 아니다.

결합 조건의 점수가 높다는 사실만으로 synergy를 주장하지 않는다. 각 단독 조건과 상호작용을 평가할 충분한 반복과 분석이 필요하다.

## 이해도 점검

- [ ] 실험 이력의 보존과 lesson 일반화를 별도로 설명할 수 있다.
- [ ] 조회되지 않은 lesson과 적용했으나 무효인 lesson을 구분한다.
- [ ] `fast₁` 94%를 성공률이라고 바꾸지 않는다.
- [ ] 같은 inference budget과 같은 전체 비용의 차이를 설명한다.

## Navigation

- [[tech/ai/autoresearch-harness-design/README|학습 진입점]]

## Sources

- https://arxiv.org/abs/2611.28244
- https://doi.org/10.48550/arXiv.2611.28244
