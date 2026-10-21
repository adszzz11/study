---
date: 2026-10-22
tags: [tech]
type: tech-tool-study
status: draft
---

# Harness² cheatsheet

## Mental model

```text
fixed model weights
  + editable harness
  → propose candidates
  → probe on task
  → compose from behavioral contrast
  → store adopted harness + lessons
```

## Key terms

| 용어 | 뜻 |
|---|---|
| harness | 모델을 둘러싼 prompt, tool, memory, skill, orchestration 구성 |
| Propose–Probe–Compose | 후보 제안 → 같은 task에서 실행 → trace 대비로 합성 |
| task-level recursion | 현재 task 안에서 harness를 개선 |
| harnessing-level recursion | 채택한 lesson을 이후 task에 재사용 |
| `parallel` | 후보 탐색 폭을 넓히는 mode |
| `sequential` | 이전 refinement를 이어 깊게 다듬는 mode |
| substrate | executor integration; 기본 OpenCode, 선택 Codex (`--substrate cx`) |

## Demo

```bash
uv venv --python 3.12 .venv
source .venv/bin/activate
uv pip install -e '.[render]'
harness2-demo --output runs/demo-k1 --k 1
```

## Benchmark sequence

```text
harness2-setup → harness2-check → harness2 → harness2-judge → harness2-report
```

비교 시 benchmark·executor·subset·`k`·mode·seed를 맞춘다.

## Safe starting flags

```bash
harness2 --dry-run --only-domains <domain> --max-tasks 1
```

현재 release의 flag와 문법을 공식 CLI 문서에서 확인한 뒤 사용한다.

## Before promotion

- [ ] baseline과 candidate를 같은 budget에서 비교했다.
- [ ] sealed eval set, CI, human review를 통과했다.
- [ ] executor egress/DNS policy와 dataset revision을 기록했다.
- [ ] reflection/lesson에서 PII와 secret을 redaction했다.
- [ ] production write 권한 없이 격리 workspace에서 검토했다.

Source: https://github.com/google-research/harness2
