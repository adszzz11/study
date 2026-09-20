---
date: 2026-09-20
tags: [tech]
type: tech-tool-study
status: draft
---

# Claude Code Setup — Cheatsheet

> [[05-projects|이전: Projects]] · [[README|목차로 돌아가기]]

## 설치

```bash
# macOS / Linux / WSL — native installer
curl -fsSL https://claude.ai/install.sh | bash

# macOS / Linux — Homebrew
brew install --cask claude-code

# Windows PowerShell — native installer
irm https://claude.ai/install.ps1 | iex

# Windows — WinGet
winget install Anthropic.ClaudeCode
```

> `npm install -g @anthropic-ai/claude-code`는 2026-09-20 기준 official repository에서 deprecated로 표시된다.

## 진단과 실행

| 명령 | 용도 |
|---|---|
| `claude --version` | 설치 version 확인 |
| `claude doctor` | read-only installation/settings 진단 |
| `claude` | interactive session 시작 |
| `claude "fix the build error"` | initial prompt와 함께 시작 |
| `claude -p "explain this function"` | one-off print mode |
| `claude -c` | 현재 directory의 최근 conversation 계속 |
| `claude -r` | 이전 conversation 선택/재개 |
| `claude mcp list` | MCP server 목록 확인 |

## Session command

| 명령 | 용도 |
|---|---|
| `/help` | command help |
| `/status` | version, model, account, settings source |
| `/context` | context usage와 memory file 확인 |
| `/permissions` | effective permission 확인/관리 |
| `/sandbox` | sandbox 상태/설정 확인 |
| `/init` | repository 분석 후 `CLAUDE.md` 초안 생성 |
| `/login` | account 전환 또는 재인증 |
| `/clear` | conversation context 초기화 |
| `/resume` | conversation 재개 |
| `/exit` | session 종료 |

## 주요 경로

```text
~/.claude/CLAUDE.md               # user memory
~/.claude/settings.json           # user settings
~/.claude/skills/                 # personal skills

./CLAUDE.md                       # shared project memory
./CLAUDE.local.md                 # local project memory
./AGENTS.md                       # cross-agent instructions
.claude/settings.json             # shared project settings
.claude/settings.local.json       # personal project override
.claude/rules/*.md                # path-specific rules
.claude/skills/<name>/SKILL.md    # project skill
.mcp.json                         # project MCP configuration
```

## 최소 `CLAUDE.md`

```markdown
# Commands

- Test: `pnpm test`
- Lint: `pnpm lint`
- Typecheck: `pnpm typecheck`

# Architecture

- Domain logic must not import UI modules.

# Done criteria

- Add regression tests for bug fixes.
- Show test output before claiming completion.
```

## 최소 shared settings

```json
{
  "$schema": "https://json.schemastore.org/claude-code-settings.json",
  "permissions": {
    "allow": [
      "Bash(pnpm lint)",
      "Bash(pnpm test *)"
    ],
    "deny": [
      "Read(./.env)",
      "Read(./.env.*)"
    ]
  },
  "sandbox": {
    "enabled": true,
    "allowUnsandboxedCommands": false
  }
}
```

## Sandbox

```bash
# Ubuntu / Debian / WSL2 dependency
sudo apt-get install bubblewrap socat

# 일회성 강제 설정
claude --settings \
  '{"sandbox":{"enabled":true,"allowUnsandboxedCommands":false}}'
```

Security gate용 managed setting:

```json
{
  "sandbox": {
    "enabled": true,
    "failIfUnavailable": true,
    "allowUnsandboxedCommands": false
  }
}
```

| Platform | Sandbox |
|---|---|
| macOS | Seatbelt |
| Linux/WSL2 | bubblewrap + socat |
| Native Windows | 미지원 — WSL2 고려 |

## Permission rule 감각

| Rule | 범위 |
|---|---|
| `Bash(pnpm lint)` | 정확한 command |
| `Bash(pnpm test *)` | test command와 추가 argument |
| `Read(./.env)` | 한 secret file |
| `Read(./.env.*)` | `.env.*` pattern |
| `WebFetch(domain:docs.example.com)` | 한 domain |
| `Bash` | 모든 shell command — 대개 너무 넓음 |

## Context 배치

| 내용 | 위치 |
|---|---|
| 매 session에 필요한 짧은 사실 | `CLAUDE.md` |
| 여러 agent의 공통 규칙 | `AGENTS.md` + 명시적 import 고려 |
| 특정 path/file type 규칙 | `.claude/rules/` |
| 긴 runbook·반복 workflow | `.claude/skills/` |
| 개인 preference/승인 | local/user settings |
| 조직 보안 baseline | managed settings |

## 완료 전 30초 점검

```bash
git status --short
git diff --check
git diff
```

- [ ] 요청 범위 밖 파일이 바뀌지 않았는가?
- [ ] test/lint/typecheck의 최신 output이 있는가?
- [ ] 실패하거나 skip한 검증을 명시했는가?
- [ ] secret, credential, `.env`가 diff/context에 들어가지 않았는가?
- [ ] commit/push/PR 같은 external change는 명시적 승인을 받았는가?

## Sources

- [Claude Code Quickstart](https://code.claude.com/docs/en/quickstart)
- [Advanced setup](https://code.claude.com/docs/en/setup)
- [CLI reference](https://code.claude.com/docs/en/cli-reference)
- [How Claude remembers your project](https://code.claude.com/docs/en/memory)
- [Settings files and precedence](https://code.claude.com/docs/en/settings)
- [Configure permissions](https://code.claude.com/docs/en/permissions)
- [Configure the sandboxed Bash tool](https://code.claude.com/docs/en/sandboxing)

