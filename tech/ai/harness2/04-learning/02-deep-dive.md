---
date: 2026-10-22
tags: [tech]
type: tech-tool-study
status: draft
---

# Deep dive: modes, reproducibility, and isolation

## Parallel versus sequential

| Mode | 주된 장점 | 비교 시 통제할 것 |
|---|---|---|
| `parallel` | 넓은 candidate 탐색과 evidence 조합 | task selection, model, seed, `k` |
| `sequential` | 직전 refinement를 이어가는 깊은 개선 | task selection, model, seed, `k` |

두 mode 중 하나를 보편적으로 우월하다고 가정하지 않는다. domain과 budget에 따라 exploration breadth와 refinement depth의 가치가 달라진다.

## Benchmark workflow

실제 benchmark는 다음 순서로 실행한다.

```text
harness2-setup → harness2-check → harness2 → harness2-judge → harness2-report
```

`refine`, `judge`, `report`의 결과를 비교하려면 benchmark, executor, subset, `k`, mode, seed를 동일하게 맞춘다. dataset revision, code commit, model endpoint/version, 실행 시각도 결과 metadata에 기록한다.

## Cost controls

처음에는 전체 sweep 대신 작은 범위로 시작한다.

```bash
# 실제 지원 flag와 selection 문법은 현재 release 문서에서 확인한다.
harness2 --dry-run --only-domains <domain> --max-tasks 1
```

- model-backed rollout과 improver 호출은 모두 API 비용을 만든다.
- baseline과 improved harness를 같은 budget에서 비교한다.
- 실패·retry·timeout도 비용 및 품질 지표로 남긴다.

## Security boundary

release는 executor network를 제한하지 않으며, Codex executor는 sandbox-disabled로 동작한다. 공개 benchmark rubric 유출을 피하려면 application 설정만 믿지 말고 executor host에서 egress/DNS policy를 적용한다.

- Hugging Face, GitHub 등 benchmark 답안을 얻을 수 있는 destination을 평가 중 차단한다.
- 차단 정책, 예외, dataset revision을 run result에 함께 기록한다.
- reflection 및 lesson artifact에 PII·secret이 들어가지 않도록 redaction layer를 둔다.
- production agent에는 직접 write 권한을 주지 않고 격리 workspace에서 후보 patch를 검토한다.

자세한 조건: https://github.com/google-research/harness2/blob/main/docs/EXPERIMENTS.md
