---
date: 2026-09-25
tags: [tech]
type: tech-tool-study
status: draft
---

# Clodex loop — What / Why / 핵심 특징

## What: dual-CLI workflow contract

**9thLevelSoftware/Clodex**는 Claude Code CLI와 Codex CLI의 native collaboration layer다. Claude가 구현 가능한 plan을 먼저 만들고, Codex가 accepted plan만 구현한다. 이후 두 agent는 동일한 최종 diff hash를 adversarial audit하며, 둘 다 승인할 때만 run을 완료로 취급한다.

```text
Task
  → Claude plan (Plan mode)
  → accepted plan
  → isolated Git worktree
  → Codex implementation
  → same final diff hash
  → Claude audit + Codex audit
  → approved? ─ Yes → manual `clodex apply <run-id>`
              └ No  → fix (max_fix_loops 안에서) → re-audit
```

## Why: 자기확증과 handoff 손실을 줄이기

단일 coding agent는 계획, 구현, self-review가 같은 context와 model 안에 묶이기 쉽다. 그러면 plan과 code의 불일치, self-review의 확증 편향, 긴 작업의 handoff 손실, source checkout의 조기 변경이 발생할 수 있다.

Clodex는 역할과 증거를 분리한다.

- **Claude Code**는 product/design 관점의 plan을 구조화한다.
- **Codex CLI**는 plan을 구현하고 changed files, 실행 test, unresolved item을 기록한다.
- **Dual audit**는 구현 session의 가정을 다른 역할에서 재검토한다.
- **Manual apply**는 approved patch와 source checkout 변경을 분리한다.

## 핵심 특징

| 영역 | 내용 | 운영상 의미 |
|---|---|---|
| Isolation first | 기본 build는 `.clodex/workspaces/<run-id>/` Git worktree에서 실행 | source checkout은 `apply` 성공 전 변경되지 않는다. |
| Durable artifacts | plan, implementation report, audit, agreement, diff/patch, trace, workspace metadata | 재개·감사·CI 보관에 필요한 증거가 남는다. |
| Durable state | `.clodex/state.sqlite3`와 task/run lifecycle | interrupted run의 상태를 CLI/MCP에서 조회한다. |
| MCP handoff | `clodex_handoff_create/update/get/decide` 및 task lifecycle tools | MCP가 없을 때는 CLI fallback을 쓴다. |
| Policy as code | repo-owned `CLODEX.md` | model, sandbox, backend, reviewer, timeout, loop cap을 version control한다. |
| Bounded autonomy | 기본 `max_fix_loops: 2`, final agreement 필요 | 끝없는 agent 수정 대신 escalation 지점을 만든다. |

## 안전 기본값과 한계

기본 contract는 Claude의 Plan mode, Codex의 `workspace-write`, Git worktree, manual apply를 사용한다. `workspace-write`는 workspace 쓰기 범위를 제한하는 sandbox policy다.

`05-agreement.json`의 `approved: true`는 **최종 diff hash**에 대응해야 한다. 하지만 dual audit는 test, lint, dependency scan, SAST나 사람이 하는 release approval을 대체하지 않는다. 또한 README에 보이는 `opus`, `gpt-5.5` 같은 모델 값은 해당 repository contract의 기본 예시이지, 현재 CLI에서 항상 선택 가능한 모델이라는 제품 사양은 아니다.

## Sources

- https://github.com/9thLevelSoftware/Clodex/blob/main/README.md
- https://github.com/9thLevelSoftware/Clodex/blob/main/CLODEX.md
- https://developers.openai.com/docs/config-file/config-reference
- https://docs.anthropic.com/en/docs/mcp
