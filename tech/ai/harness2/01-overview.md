---
date: 2026-10-22
tags: [tech]
type: tech-tool-study
status: draft
---

# Harness² overview

## What

Harness²는 agent의 **harness**—모델을 둘러싼 prompt, tool, memory, orchestration—를 탐색·검증·합성하는 research framework다. fine-tuning이나 RL처럼 model weight를 바꾸지 않고 runtime artifact를 바꾼다.

## Why

open-world 업무는 정답 label이나 verifier를 사전에 준비하기 어렵다. 또한 agent를 새 업무에 맞추려면 보통 사람이 `AGENTS.md`, tool guidance, memory rule, subagent topology를 손으로 조정한다. Harness²는 task의 실행 결과와 trace 차이를 개선 근거로 삼고, 채택된 교훈을 이후 task에 넘긴다.

## Two levels of recursion

| 수준 | 하는 일 | 남기는 것 |
|---|---|---|
| Task-level recursion | 현재 task의 여러 변경안을 실행·비교해 refined harness를 합성 | adopted harness와 task evidence |
| Harnessing-level recursion | 채택된 harness와 근거 있는 lesson을 domain library에 축적 | 이후 task의 초기 개선 맥락 |

## Propose–Probe–Compose

1. **Propose**: improver가 invariant와 domain-specific 변경안을 낸다.
2. **Probe**: executor가 같은 task에서 각 후보 harness를 실행한다.
3. **Compose**: execution trace의 behavioral contrast를 읽어 refined harness를 합성한다.

`parallel` mode는 여러 후보를 넓게 탐색하고 근거를 조합한다. `sequential` mode는 직전 refined harness와 누적 근거를 다음 단계에 이어 깊게 다듬는다.

## Editable harness surface

- system prompt와 guardrails
- memory와 tool guidance
- subagents와 skills
- scripts와 plugins

## Reported evidence and limit

논문 저자는 GLM-5·Gemini 3.5 Flash 실험에서 한 단계 개선으로 WorkBuddy-Bench 최대 +11.5점, JobBench +4.5점, LAB partial pass rate +11.8%p를 보고했다. 이는 저자 보고치이므로 도입 판단에는 자신의 workload, model, 비용 조건에서 재현 실험이 필요하다.

## Further reading

- [[./02-ecosystem|Ecosystem comparison]]
- [[./04-learning/02-deep-dive|Deep dive]]
- https://arxiv.org/abs/2610.14224
