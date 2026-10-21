---
date: 2026-10-22
tags: [tech]
type: tech-tool-study
status: draft
---

# Getting started: demo와 첫 trace

## Goal

credential-free demo로 한 번의 **Propose–Probe–Compose**가 어떤 artifact를 만들고, candidate 실행 trace가 harness adoption 근거로 어떻게 쓰이는지 확인한다.

## Prerequisites

- Linux
- Python 3.12
- `uv`

## Run the demo

```bash
uv venv --python 3.12 .venv
source .venv/bin/activate
uv pip install -e '.[render]'
harness2-demo --output runs/demo --k 2
```

첫 관찰은 `k=1`이 적합하다. 후보 수가 적으면 제안, probe, compose 간의 인과관계를 읽기 쉽다.

```bash
harness2-demo --output runs/demo-k1 --k 1
```

## Inspect the run

`runs/` 아래에서 다음을 확인한다.

- task summary와 deliverable
- 각 candidate의 harness 변경 내용
- executor trace와 candidate 간 행동 차이
- adopted/refined harness와 reflection
- evaluation result 및 재개(resume)에 필요한 run metadata

## First experiment log

| 질문 | 기록할 관찰 |
|---|---|
| 무엇이 바뀌었나? | prompt, guidance, memory 등 변경 surface |
| candidate가 어떻게 달랐나? | trace, tool use, output quality, failure mode |
| 왜 채택됐나? | compose 단계가 든 behavioral evidence |
| 비용은 얼마였나? | rollout/improver 호출 수와 실행 시간 |

## Next

- [[./02-deep-dive|Deep dive]]에서 실제 benchmark pipeline과 isolation 조건을 확인한다.
- 설치 세부 사항: https://github.com/google-research/harness2/blob/main/docs/SETUP.md
