---
date: 2026-11-27
tags: [tech]
type: tech-tool-study
status: draft
---

# 시작하기: State·Metric·Progress 분리

## 실습 목표

별도 제품 설치 없이 작은 작업 목록을 만든다. 여기서 완료는 **실행 종료 후 결과 검증까지 통과한 작업**으로 정의한다. `succeeded`도 이 조건을 충족한 상태로 사용한다. 영상의 계산식이 아니다.

| task_id | state | 검증 결과 |
|---|---|---|
| T1 | succeeded | 통과 |
| T2 | running | 미확정 |
| T3 | failed | 실패 |
| T4 | queued | 미실행 |

## 계산해 보기

```python
tasks = [
    {"id": "T1", "state": "succeeded"},
    {"id": "T2", "state": "running"},
    {"id": "T3", "state": "failed"},
    {"id": "T4", "state": "queued"},
]
completed_tasks = sum(t["state"] == "succeeded" for t in tasks)
total_tasks = len(tasks)
progress = completed_tasks / total_tasks if total_tasks else None
print(completed_tasks, progress)  # 1, 0.25
```

- State는 개별 작업의 현재 상태다.
- Metric은 상태 집합을 집계한 값이다. `completed_tasks`의 단위는 작업 건수다.
- Progress는 선택한 전체 범위 대비 완료 비율이다. 이 모델에서 실패도 분모에 남는다.
- 전체 작업이 0이면 비율을 `N/A`로 표시한다. 임의로 완료 100%로 간주하지 않는다.

## 분모 바꾸기

T2가 검증까지 통과하면 `2/4 = 50%`다. 이후 작업 6개를 추가하면 완료 수는 그대로여도 `2/10 = 20%`가 된다. 이는 회귀가 아니라 범위 확대일 수 있다. UI에 완료 수·전체 수·범위 변경 시점을 함께 표시한다.

## 완료 점검

- [ ] 실행 종료와 검증 통과를 구분했는가?
- [ ] 막대 옆에 `1/4 tasks · 25%`를 표시했는가?
- [ ] 각 집계값에서 해당 task ID 목록을 확인할 수 있는가?
- [ ] running 작업 수를 실행 중인 Agent 수로 오인하지 않는가?

다음: [[tech/devtools/agent-dashboard-progress/04-learning/02-deep-dive|이벤트와 집계 심화]]

## Related Notes

- [[tech/devtools/agent-dashboard-progress/README|학습 진입점]]

## Sources

- 사용자 제공 dossier: 영상 00:00·00:05 장면 요약. 원본 URL은 제공되지 않아 기재할 수 없다.
- 아래 실습·모델·설계 제안은 학습용이며 영상에서 확인된 구현을 뜻하지 않는다.
