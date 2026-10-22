---
date: 2026-10-22
tags: [tech]
type: tech-tool-study
status: draft
---

# CLI-Anything overview

## What

**CLI-Anything**는 기존 software의 실제 backend 위에 agent-native CLI harness를 생성하는 접근이다. Blender rendering, LibreOffice 변환, REST API처럼 이미 구현된 기능을 호출하며, mock GUI나 toy reimplementation을 만드는 것이 목적이 아니다.

## Why

Computer Use는 visual state, 좌표, timing에 영향을 받는다. 반면 CLI contract는 명령 이름, argument, exit status, JSON schema로 동작을 드러낸다. agent는 `--help`로 기능을 발견하고 `--json`으로 결과를 읽으며, test와 artifact assertion으로 성공을 판정할 수 있다.

## 핵심 특징

| 특징 | 의미 |
|---|---|
| backend-first | UI를 우회해 실제 source/API/backend 기능을 호출한다. |
| subcommand + REPL | script·CI에는 stateless command, undo/redo·장기 흐름에는 persistent state를 쓴다. |
| agent-friendly I/O | `--help`, `--json`, 예제와 error handling을 담은 `SKILL.md`를 제공한다. |
| 검증 중심 | unit test뿐 아니라 native artifact 생성·재오픈을 포함한 E2E test를 둔다. |
| distribution | CLI-Hub에서 harness를 탐색, 설치, update, uninstall할 수 있다. |

## 7-phase harness pipeline

1. target의 source/API와 실행 경로를 분석한다.
2. command, state, output schema를 설계한다.
3. Click 기반 CLI와 REPL을 구현한다.
4. test plan을 만든다.
5. unit/E2E test로 실제 backend 호출을 검증한다.
6. 사용법과 `SKILL.md`를 문서화한다.
7. package와 `PATH`를 통해 설치 가능하게 배포한다.

## 한계

source code 접근이 핵심이다. binary-only target은 command coverage와 품질이 낮아질 수 있다. 최초 생성물도 완료가 아니라 가설이므로, 실제 E2E 결과를 바탕으로 `/refine`하고 generated code와 shell invocation을 review해야 한다.

## Sources

- https://github.com/HKUDS/CLI-Anything
- https://github.com/HKUDS/CLI-Anything#-how-cli-anything-works
- https://github.com/HKUDS/CLI-Anything#limitations
