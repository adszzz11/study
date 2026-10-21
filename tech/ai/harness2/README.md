---
date: 2026-10-22
tags: [tech]
type: tech-tool-study
status: draft
---

# Harness² tool study

> **한 줄 정의**: Harness²는 model weight를 고정한 채 prompt·tool·memory·skill·subagent 같은 agent harness를 반복적으로 개선하는 Google Research의 open-source framework다.

## Overview

LLM agent의 성능은 foundation model만으로 결정되지 않는다. system prompt, tool interface, context/memory, orchestration도 결과를 좌우한다. Harness²는 새 업무마다 사람이 이 층을 수작업으로 고치는 대신, task 실행 중 후보 harness를 제안·실행·비교하고 다음 task에 쓸 lesson을 축적한다.

- 편집 대상: system prompt, guardrails, memory, tool guidance, subagents, skills, scripts, plugins
- 핵심 loop: **Propose → Probe → Compose**
- 지속 학습: weight update가 아닌 harness/lesson library의 runtime-level update
- substrate: 기본 OpenCode, 선택 Codex (`--substrate cx`)
- 산출물: `runs/`에 task summary, deliverable, adopted harness, reflection, evaluation result를 남기며 resume할 수 있다.

## Learning Path

- [ ] [01-overview](./01-overview.md)에서 문제, 두 수준의 recursion, 8개 harness surface를 이해한다.
- [ ] [04-learning/01-getting-started](./04-learning/01-getting-started.md)의 credential-free demo를 `k=1`로 실행하고 trace를 읽는다.
- [ ] 같은 selection/model/seed로 `parallel`과 `sequential`을 비교한다.
- [ ] [04-learning/02-deep-dive](./04-learning/02-deep-dive.md)를 따라 benchmark pipeline과 재현성 조건을 확인한다.
- [ ] [02-ecosystem](./02-ecosystem.md)에서 DSPy, Reflexion, Meta-Harness, OpenAI agent evals와 역할을 구분한다.
- [ ] [05-projects](./05-projects.md)의 격리된 improvement workspace 프로젝트를 설계한다.

## When To Use

- 반복되는 coding, review, migration, support workflow에서 harness 품질을 체계적으로 개선할 때
- 정답 verifier를 미리 만들기 어려운 open-world task에서 실행 trace의 대비를 활용할 때
- domain별 lesson을 축적해 새 task의 개선 시작점을 재사용할 때
- production 변경 전, 후보 harness를 격리 환경에서 eval·security review·human approval으로 검증할 때

## When Not To Use

- 즉시 production agent가 스스로 설정을 바꾸고 배포해야 하는 경우: 별도 promotion gate가 없는 self-modification은 위험하다.
- 저비용의 단발성 task 또는 harness 변경의 가치가 rollout/API 비용보다 작은 경우
- executor host의 sandbox·network isolation을 보장할 수 없거나 공개 benchmark rubric 유출을 막을 수 없는 경우
- 명확한 metric 하나를 빠르게 최적화할 구조화된 LM pipeline만 필요한 경우: DSPy가 더 직접적일 수 있다.

## Related Notes

- [[MOCs/Index]]
- [[MOCs/AI]]
- [[tech/ai/agent-orchestration/README|Agent Orchestration]]

## Sources

- https://github.com/google-research/harness2
- https://arxiv.org/abs/2610.14224
- https://github.com/google-research/harness2/blob/main/docs/SETUP.md
- https://github.com/google-research/harness2/blob/main/docs/EXPERIMENTS.md
- https://github.com/google-research/harness2/blob/main/docs/BENCHMARKS.md
