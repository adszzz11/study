---
date: 2026-11-07
tags: [tech]
type: tech-tool-study
status: draft
---

# Instruction Ecosystem 비교

| 항목 | Instruction format / 동작 | Stale-doc 대응 포인트 |
|---|---|---|
| OpenAI Codex | `AGENTS.md`, `AGENTS.override.md`; root→working directory 순으로 merge | global rule에 code-precedence를 두고 active source를 session마다 audit |
| Claude Code | `CLAUDE.md`; root/user/subdirectory scope를 합성 | 짧고 signal-dense하게 유지하고 convention 변경 뒤 갱신·분기별 stale sweep |
| GitHub Copilot / VS Code | `AGENTS.md`, `.github/copilot-instructions.md`, scoped instruction files | 여러 format의 충돌을 피하고 필요한 rule은 적용 범위 안에 유지 |
| AGENTS.md ecosystem | 여러 agent가 공유하는 open format | discovery·precedence는 tool마다 다르므로 동일 동작을 가정하지 않음 |
| CI / hooks / linters | executable validation | 검증 가능한 rule을 Markdown이 아닌 enforcement로 이동 |

## Codex에서 볼 점

Codex는 global→project→nested path 순서로 instruction chain을 만들고, 더 가까운 directory guidance를 뒤에 합쳐 override한다. 따라서 repository root의 stale rule뿐 아니라 하위 directory의 `AGENTS.override.md`와 `AGENTS.md`도 함께 inventory해야 한다.

## 선택 기준

| Rule 성격 | 적절한 위치 |
|---|---|
| 현재 구조를 설명하는 짧은 convention | project instruction |
| format, type, test처럼 결정 가능한 조건 | formatter, linter, test, CI |
| credential·deploy·approval | permission policy, protected workflow |
| 현재 migration의 예외 | issue/PR 및 시간 제한된 instruction |

관련 실습: [[tech/devtools/stale-agent-instructions/04-learning/02-deep-dive|Deep Dive]] · [[tech/devtools/stale-agent-instructions/cheatsheet|Cheatsheet]]

## Sources

- https://learn.chatgpt.com/docs/agent-configuration/agents-md
- https://agents.md/
- https://code.visualstudio.com/docs/agents/reference/custom-instructions-reference
- https://support.claude.com/en/articles/14553240-give-claude-context-claude-md-and-better-prompts
