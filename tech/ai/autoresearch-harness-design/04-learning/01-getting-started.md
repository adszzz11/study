---
date: 2026-11-25
tags: [tech]
type: tech-tool-study
status: draft
---

# 시작하기: 기록과 lesson부터 분리하기

## 목표와 전제

하나의 작은 coding 또는 optimization task에서 실험 기록과 교훈을 분리한다. 제공 자료에는 설치·실행 절차가 없으므로 아래는 **실습용 schema와 절차 제안**이다. MLEvolver 재현이 아니다.

## 1. 고정할 조건

- 같은 task, evaluator, model/version, inference budget, 실험 실행 한도를 사용한다.
- 성공 기준과 종료 조건을 실행 전에 정한다.
- 초기 코드·실행 환경·seed를 남겨 조건 차이를 추적한다.

## 2. 두 종류의 자산 표현

```json
{
  "experiment": {
    "id": "exp-001",
    "hypothesis": "반복 계산을 줄이면 실행 시간이 감소한다",
    "change": "중복 계산 결과 캐싱",
    "conditions": {"seed": 42, "input_set": "fixed-v1"},
    "result": {"correct": true, "runtime_ms": 120},
    "artifact": "runs/exp-001/output.json"
  },
  "lesson": {
    "id": "lesson-001",
    "applies_when": "같은 입력의 계산이 반복되고 상태가 변하지 않을 때",
    "guidance": "캐싱의 메모리 비용과 실행 시간 변화를 함께 측정한다",
    "evidence": ["exp-001"],
    "use_events": [],
    "state": "active"
  }
}
```

값은 설명용 예시이며 논문 실험 결과가 아니다. 단일 실험에 근거한 lesson은 잠정적 지침으로 취급한다. Evidence ID로 원래 조건과 결과를 다시 확인할 수 있게 한다.

## 3. Context 정책만 비교

1. Recency truncation: 최근 기록만 설정된 한도 안에서 제공한다.
2. Rolling summary: 누적 이력을 갱신 요약으로 제공한다.
3. 개별 기록 접근: 각 실험을 ID로 다시 조회할 수 있게 한다.

Lesson 정책을 고정하고 각 조건을 반복 실행한다. 세 번째 조건은 연구 방향을 탐색하는 실습이며 context folding의 재현이 아니다. 기록 조회에 든 inference도 공통 budget에 포함한다.

## 4. 관측과 완료 기준

| 관측 | 목적 |
|---|---|
| Task score와 반복별 결과 | 성과와 변동 확인 |
| 반복 실험 수·inference 사용량 | 같은 한도에서 비교 |
| 조회한 기록 ID·조회량 | 실패 이력 접근 여부 추적 |
| Lesson 사용 빈도 | 이후 skill 실험의 관측 기반 |

이 지표는 실습 권장안이며 논문의 측정 항목 목록이 아니다.

- [ ] 한 lesson의 근거 실험을 찾을 수 있다.
- [ ] 정책 외 조건이 같았는지 확인할 수 있다.
- [ ] 평균값뿐 아니라 반복별 결과와 실패 사례를 설명할 수 있다.

다음 단계: [[tech/ai/autoresearch-harness-design/04-learning/02-deep-dive|Skill 정책을 분리해 평가하기]]

## Navigation

- [[tech/ai/autoresearch-harness-design/README|학습 진입점]]

## Sources

- https://arxiv.org/abs/2611.28244
- https://doi.org/10.48550/arXiv.2611.28244
