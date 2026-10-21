---
date: 2026-10-21
tags: [tech]
type: tech-tool-study
status: draft
---

# Jcode — 치트시트

> [[README|목차로 돌아가기]]

## Quick Start

```sh
curl -fsSL https://jcode.sh/install | bash
cd <repository-root>
jcode login --provider openai
jcode
```

| 목적 | 명령/기능 | 확인할 것 |
|---|---|---|
| model 전환 | `/model` | provider와 model ID |
| reasoning 조절 | `/effort` | 비용·latency·품질 변화 |
| 검증 | `/test`, `/review`, `/diff` | 실행 로그와 exit code |
| 진행 확인 | `/todos` | unfinished work와 완료 기준 |
| 협업 | `/swarm` | agent ownership, 변경 알림 |
| 원격 사용 | `jcode serve` | socket forwarding과 host 권한 |

## Safe Defaults

- `AGENTS.md`에 build, test, format, scope 규칙을 적는다.
- agent마다 file/module ownership을 부여하고 충돌 가능 작업은 worktree로 분리한다.
- `.jcode/mcp.json`에는 최소 권한 MCP만 project-local로 둔다.
- model output, diff, test 결과를 사람이 검토한 뒤 merge/deploy한다.
- untrusted code/prompt는 container/VM에서 실행한다.
- SDK/CI의 `autoApprove`는 기본적으로 끄고 approval·audit을 둔다.

## Evaluation Record

| 지표 | 기록 예시 |
|---|---|
| 품질 | test pass rate, review finding, regression 수 |
| 속도 | wall-clock, first response, queue time |
| 자원 | session당 RAM, CPU, token/cost |
| 협업 | file conflict 수, coordinator rework |
| 안전 | 승인 우회, secret exposure, MCP 권한 범위 |

## Sources

- https://jcode.sh/docs
- https://jcode.sh/docs/commands
- https://jcode.sh/sdk
