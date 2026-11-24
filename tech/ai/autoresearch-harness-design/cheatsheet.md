---
date: 2026-11-25
tags: [tech]
type: tech-tool-study
status: draft
---

# Cheatsheet: Context·Skill 관리

## 핵심 구분

| 용어 | 기억할 점 |
|---|---|
| Context management | 과거 실험 이력에서 무엇을 유지할지 |
| Skill management | 재사용 lesson의 저장·활용·선별 |
| Recency truncation | 최근 이력을 남기는 baseline |
| Rolling summary | 여러 시도를 갱신되는 요약으로 표현 |
| Context folding | 여섯 setting 최상위; 구체 알고리즘 미확인 |
| Skill deletion | 지속적 미사용 lesson의 선택적 삭제 |
| MLEvolver | Context folding + skill deletion |

## 숫자 읽기

| 보고값 | 피해야 할 해석 |
|---|---|
| 최대 19.2% 개선 | 평균 19.2% 또는 19.2 percentage points라고 확정 |
| MLE-Bench Lite medal rate 72.7% | MLE-Bench 전체나 임의 task의 성과로 일반화 |
| KernelBench Level 3 `fast₁` score 94% | 일반 성공률 94%로 변경 |
| 동일 inference budget에서 AIDE·OpenEvolve 대비 우위 | 실행 시간·hardware·전체 비용까지 동일하다고 주장 |

## 실습 순서

1. 실험 기록과 lesson schema를 분리한다.
2. Task·model·evaluator·budget을 고정한다.
3. Context 정책만 바꿔 비교한다.
4. Context를 고정하고 skill 정책을 비교한다.
5. 성과와 관리 비용, 반복별 변동을 함께 기록한다.

## 빠른 점검

- [ ] 원래 실험의 조건·실패를 다시 조회할 수 있는가?
- [ ] Lesson의 적용 조건과 근거 ID가 있는가?
- [ ] 미사용·미조회·무효를 구분했는가?
- [ ] 삭제의 threshold·window·복구 방식을 기록했는가? (실습 설정)
- [ ] 보고 사실·해석·실습 제안을 구분했는가?

**기억할 문장:** 실험 기록은 접근 가능하게 보존하고, 재사용 교훈은 사용 이력에 따라 선별한다. 이것은 무조건적인 memory 확대나 skill 축소를 뜻하지 않는다.

## Navigation

- [[tech/ai/autoresearch-harness-design/README|학습 진입점]]

## Sources

- https://arxiv.org/abs/2611.28244
- https://doi.org/10.48550/arXiv.2611.28244
