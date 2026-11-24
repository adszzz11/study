---
date: 2026-11-25
tags: [tech]
type: tech-tool-study
status: draft
---

# Overview: 무엇을 기억하고 어떤 교훈을 남길까

## What

Autoresearch agent는 실험을 설계하고 실행 결과를 다음 시도에 반영한다. Harness는 이 반복을 지원하는 실행 체계이며, 기반 모델 외에 **과거 정보가 다음 행동에 전달되는 방식**도 성능에 영향을 준다.

| 관리 축 | 대상 | 질문 |
|---|---|---|
| Context management | 실험 이력 | 어떤 시도의 조건·변경·결과를 다시 볼 수 있는가? |
| Skill management | 재사용 가능한 lessons | 어떤 조건에서 어떤 교훈을 적용할 것인가? |

실험 기록은 특정 사건의 근거이고, lesson은 이후 행동에 적용할 지침이다. 둘을 별도로 최적화하는 것이 핵심이다.

## Why

기존 harness는 여러 mechanism을 함께 사용한다. 이력 보존 방식과 lesson 정책을 동시에 바꾸면 성능 개선의 원인을 분리하기 어렵다. 논문은 shared agent framework에서 각 설계 선택을 recency-truncation baseline과 비교한다.

## 특징과 평가 범위

| 항목 | Dossier에서 확인되는 내용 |
|---|---|
| Benchmark | MLE-Bench, KernelBench |
| Model | gpt-oss-120b, gpt-6-luna, gpt-6-sol |
| Setting | 2 benchmark × 3 model = 6 |
| Baseline | Recency truncation |
| 연구 축 | Context management, skill management |

### Context folding

개별적으로 접근 가능한 과거 시도 기록을 보존하는 방식이 rolling summary보다 효과적이었다. Context folding은 여섯 setting 모두 최상위였고 baseline 대비 최대 19.2% 개선이 보고됐다.

- Rolling summary는 여러 시도를 하나의 갱신되는 요약으로 표현한다.
- 개별 기록은 이전 사건을 구분해 다시 살펴볼 수 있게 한다.
- **해석:** 결론뿐 아니라 결론이 나온 조건과 실패 이력을 확인하는 능력이 중요할 수 있다.

이 해석은 정보 손실의 원인 분석을 검증한 결과가 아니다. Context folding의 저장 형식·호출 방식·압축 및 복원 절차는 자료에 없다. 특정 retrieval architecture나 context-window 확장 기술과 동일시하지 않는다. 19.2%는 최대값이며 상대 개선율인지 percentage point 차이인지 확정할 수 없다.

### Skill deletion

지속적으로 미사용인 lessons를 선택적으로 삭제하는 정책이 consolidation과 standing-rule promotion보다 평균적으로 효과적이었다. 이는 “skill이 적을수록 좋다”라는 일반 법칙이 아니다. 미사용 정의·threshold·판정 방식·복구 정책은 확인되지 않았다.

### MLEvolver

Context folding과 skill deletion을 결합한다. 아래는 abstract를 정리한 개념 흐름이며 실제 module이나 실행 순서를 재현한 것이 아니다.

```text
실험 설계 → 실행 → 결과 관찰 → 개별 실험 이력 보존
         → lessons 저장·재사용·선별 → 다음 실험 개선
```

| 평가 | 보고된 성과 |
|---|---|
| MLE-Bench Lite | Medal rate 72.7% |
| KernelBench Level 3 | `fast₁` score 94% |
| AIDE·OpenEvolve와 비교 | 동일 inference budget에서 상당한 우위 |

상대 시스템의 개별 점수와 격차, `fast₁`의 정의는 제공되지 않았다. 두 수치는 다른 지표여서 직접 비교할 수 없다. 동일 inference budget은 wall-clock time·hardware cost·실험 실행 비용까지 같다는 뜻이 아니다. 결합 결과만으로 synergy나 각 정책의 기여율을 계산할 수 없다.

## Navigation

- [[tech/ai/autoresearch-harness-design/README|학습 진입점]]

## Sources

- https://arxiv.org/abs/2611.28244
- https://doi.org/10.48550/arXiv.2611.28244
