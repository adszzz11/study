---
date: 2026-10-22
tags: [tech]
type: tech-tool-study
status: draft
---

# CLI-Anything tool study

> **한 줄 정의**: CLI-Anything는 GUI 앱·codebase·Web API의 실제 backend를 AI agent가 안정적으로 조작하도록 상태, 명령, JSON output, 테스트를 갖춘 agent-native CLI harness로 바꾸는 오픈소스 방법론 및 생태계다.

## Overview

GUI automation은 screenshot 해석, 좌표, 로딩 타이밍에 의존하므로 UI 변경에 취약하다. CLI-Anything는 이를 화면 모방이 아니라 machine-readable contract의 문제로 바꾼다. 사람에게는 기존 GUI를 남기고, agent에는 deterministic command와 structured JSON을 제공한다.

- 대상: source/API가 있는 desktop app, codebase, REST API
- 실행: script·CI용 subcommand mode와 장기 작업용 stateful REPL
- 산출물: Click CLI, `--json` output, `SKILL.md`, unit/E2E test, 배포 가능한 package

## Learning Path

- [ ] [01-overview](./01-overview.md)에서 backend-first 접근과 핵심 특징을 이해한다.
- [ ] [04-learning/01-getting-started](./04-learning/01-getting-started.md)에서 CLI-Hub 탐색과 설치 후 smoke test를 수행한다.
- [ ] `--help`, `--json`, REPL을 각각 실행해 discoverability와 state 변화를 확인한다.
- [ ] [04-learning/02-deep-dive](./04-learning/02-deep-dive.md)에서 7-phase pipeline, artifact E2E, 보안 경계를 검토한다.
- [ ] [02-ecosystem](./02-ecosystem.md)으로 native API CLI, MCP, Playwright, UFO²의 선택 기준을 비교한다.
- [ ] [05-projects](./05-projects.md) 중 하나를 작은 native-artifact 검증 프로젝트로 구현한다.

## When To Use

- source/API가 있는 소프트웨어를 agent가 반복 가능하고 검증 가능하게 조작해야 할 때
- GUI workflow를 CI, batch job, evaluation harness로 옮길 때
- domain command를 정리해 tool discovery와 JSON parsing 비용을 낮추고 싶을 때

## When Not To Use

- 공식 API contract와 SDK/CLI가 이미 충분히 좋은 서비스: native API + 자체 CLI가 더 단순하다.
- source/API 없이 여러 Windows GUI를 즉시 넘나들어야 할 때: UFO² 같은 GUI automation system을 평가한다.
- 대상이 순수 Web app이고 DOM interaction이 핵심일 때: Playwright CLI가 더 직접적이다.

## Related Notes

- [[MOCs/Index]]
- [[MOCs/AI]]
- [[tech/ai/mark-it-down/README|MarkItDown]]

## Sources

- https://github.com/HKUDS/CLI-Anything
- https://arxiv.org/abs/2606.03854
- https://clianything.cc/
- https://github.com/HKUDS/CLI-Anything/releases
