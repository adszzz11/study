---
date: 2026-09-25
tags: [tech]
type: tech-tool-study
status: draft
---

# Clodex loop — Getting started

## 목표: 작은 repository에서 state machine 보기

처음 실습은 production repository가 아닌 작은 Git repository에서 한다. 목표는 agent가 코드를 많이 쓰게 하는 것이 아니라 worktree, artifact, diff hash, approval, apply의 연결을 관찰하는 것이다.

## 1. 사전 점검

Clodex README 기준 기본 요구사항은 Python 3.12+, Git, Claude Code CLI, Codex CLI다. CLI 로그인과 repository 상태를 먼저 확인한다.

```bash
python --version
git --version
claude auth login
codex login

# npm 설치를 택한 경우
npm install -g clodex
clodex doctor
```

source checkout에서 먼저 예정된 변경만 확인한다.

```bash
clodex init --dry-run
clodex native doctor
```

`init`은 managed Clodex block과 MCP 설정을 추가할 수 있다. dry-run 출력에서 `AGENTS.md`, `CLAUDE.md`, `CLODEX.md`, `.mcp.json`, `.codex/config.toml`의 예정 변경과 기존 설정 충돌을 검토한다.

## 2. 작은 policy로 시작

처음에는 repository의 `CLODEX.md`에서 다음 원칙을 택한다.

```yaml
workspace:
  backend: git-worktree
  apply_mode: manual
max_fix_loops: 1
```

한 번의 fix loop만 허용하면 failure를 숨기지 않고 reviewer finding, test failure, timeout을 사람이 읽게 된다. model 이름은 이 예제가 아니라 현재 CLI가 지원하는 값을 공식 문서와 `doctor`로 확인한다.

## 3. plan과 dry-run을 분리해 읽기

```bash
clodex plan "Add a small, testable feature"
clodex build --dry-run "Add a small, testable feature"
```

plan에는 최소한 scope, acceptance criteria, test strategy, 변경하지 않을 영역이 있어야 한다. dry-run에서는 다음 연결을 확인한다.

```text
01-claude-plan.json
  → 02-codex-implementation.md
  → 03-claude-audit.json + 04-codex-audit.json
  → 05-agreement.json
  → changes.diff / apply.patch / trace.jsonl / workspace.json
```

## 4. 실제 run 후 사람이 확인할 것

`clodex apply <run-id>` 전에 worktree의 `changes.diff`, 실행한 test와 결과, unresolved finding, final diff hash, `05-agreement.json`의 `approved`를 확인한다. 승인됐더라도 migration, secret, destructive operation, production deployment는 별도 review와 승인 범위에 둔다.

## Sources

- https://github.com/9thLevelSoftware/Clodex/blob/main/README.md
- https://github.com/9thLevelSoftware/Clodex/blob/main/install.sh
- https://github.com/9thLevelSoftware/Clodex/blob/main/CLODEX.md
