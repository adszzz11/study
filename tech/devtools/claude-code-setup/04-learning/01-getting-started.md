---
date: 2026-09-20
tags: [tech]
type: tech-tool-study
status: draft
---

# Claude Code Setup — Getting Started

> [[../03-references|이전: References]] · [[../README|목차로 돌아가기]] · [[02-deep-dive|다음: Deep Dive]]

## 1. 실행 환경 선택

처음에는 local repository에서 CLI로 시작하는 것이 가장 단순하다. Native Windows에서도 실행할 수 있지만 Bash sandbox가 필요하면 WSL2를 사용한다.

| 환경 | 권장 상황 | 주의 |
|---|---|---|
| macOS/Linux CLI | 일반 local development | native installer 또는 package manager 선택 |
| Native Windows | Windows toolchain과 PowerShell 중심 | sandbox 미지원, Git Bash는 선택 사항 |
| WSL2 | Linux toolchain, sandbox 필요 | project와 CLI를 WSL filesystem에 두는 편이 안정적 |
| Desktop/IDE | graphical diff와 editor context 선호 | CLI와 기능·설정 적용 범위가 다를 수 있음 |

## 2. 설치

공식 repository는 native installer를 권장하며 npm global 설치는 deprecated로 표시한다.

### macOS / Linux / WSL

```bash
# Native installer — 권장
curl -fsSL https://claude.ai/install.sh | bash

# Homebrew 대안
brew install --cask claude-code
```

### Windows PowerShell

```powershell
# Native installer — 권장
irm https://claude.ai/install.ps1 | iex

# WinGet 대안
winget install Anthropic.ClaudeCode
```

`curl | bash` 또는 `irm | iex`가 조직 보안정책에 맞지 않으면 Homebrew, WinGet, apt, dnf, apk를 사용하거나 installer 내용을 검토한다. Native installation은 background auto-update를 지원하지만 Homebrew와 WinGet은 직접 upgrade해야 한다.

```bash
brew upgrade claude-code
```

```powershell
winget upgrade Anthropic.ClaudeCode
```

## 3. 설치 검증

```bash
claude --version
claude doctor
```

`claude doctor`는 session을 시작하거나 파일을 바꾸지 않고 installation health, settings validation error, update warning을 진단한다.

## 4. 인증

Project directory에서 첫 session을 시작한다.

```bash
cd /path/to/project
claude
```

Browser login에서 다음 경로를 사용할 수 있다.

- Claude Pro, Max, Team, Enterprise
- Claude Console/API billing
- Amazon Bedrock
- Google Cloud Agent Platform
- Microsoft Foundry
- 조직의 self-hosted Claude apps gateway와 corporate SSO

`ANTHROPIC_API_KEY`가 설정되어 있으면 browser login 대신 key 사용 승인을 요청한다. SSH, WSL, container처럼 callback server가 browser에서 보이지 않는 환경에서는 화면의 URL/code를 browser로 옮겨 인증한다. Secret을 `CLAUDE.md`나 repository settings에 기록하지 않는다.

## 5. 첫 read-only session

처음부터 edit를 요청하기보다 현재 context와 repository 이해도를 확인한다.

```text
/status
/context
/permissions

이 repository의 목적, entry point, build/test command를 찾아서 설명해줘.
아직 파일은 수정하지 마.
```

확인할 것:

- working directory가 예상한 repository인가?
- 어떤 `CLAUDE.md` 또는 `AGENTS.md`가 load되었는가?
- model, account, settings source가 예상과 같은가?
- permission mode와 sandbox 상태가 적절한가?
- Claude가 제시한 build/test command가 실제 config와 일치하는가?

## 6. 최소 `CLAUDE.md` 만들기

Session에서 `/init`을 실행하면 repository를 분석해 시작 파일을 만든다. 기존 `CLAUDE.md`가 있으면 덮어쓰지 않고 개선안을 제시한다.

```text
/init
```

직접 작성한다면 discover하기 어렵고 자주 필요한 정보만 넣는다.

```markdown
# Project commands

- Install: `pnpm install`
- Test: `pnpm test`
- Lint: `pnpm lint`
- Typecheck: `pnpm typecheck`

# Architecture

- API routes live in `src/server/routes/`.
- Domain logic must not import UI modules.

# Working rules

- Preserve existing public APIs unless explicitly requested.
- Add regression tests for bug fixes.
- Show test output before claiming completion.
```

`/context`에서 실제 load 여부와 context 사용량을 확인한다.

> [!tip] Context 배치 원칙
> 모든 session에 필요한 짧고 안정적인 사실은 `CLAUDE.md`, 특정 path 규칙은 `.claude/rules/`, 긴 runbook과 반복 절차는 `.claude/skills/`로 분리한다.

## 7. 첫 변경 workflow

작고 검증 가능한 task를 선택한다.

```text
README의 잘못된 설치 명령 하나를 공식 문서와 맞게 고쳐줘.
먼저 대상 줄과 변경 계획을 보여주고, 수정 후 diff를 검토해줘.
```

변경 뒤 직접 확인한다.

```bash
git diff --check
git diff -- README.md
git status --short
```

Code task라면 repository의 test를 실행하고, exit code와 failure를 숨기지 않도록 요청한다.

## 8. 기본 문제 해결

| 증상 | 확인 |
|---|---|
| `claude: command not found` | terminal 재시작, `PATH`, `claude doctor` |
| login browser callback 실패 | 표시된 URL/code를 다른 browser에서 사용 |
| instruction 미적용 | `/context`, 현재 directory, filename과 scope 확인 |
| settings parsing 실패 | strict JSON, comment/trailing comma 제거 |
| command가 sandbox에서 실패 | `/sandbox`, dependency, filesystem/network rule 확인 |
| 원치 않는 permission prompt | `/permissions`와 rule specifier를 좁게 조정 |

## Sources

- [Claude Code Quickstart](https://code.claude.com/docs/en/quickstart)
- [Advanced setup](https://code.claude.com/docs/en/setup)
- [Authentication](https://code.claude.com/docs/en/authentication)
- [How Claude remembers your project](https://code.claude.com/docs/en/memory)
- [Troubleshooting](https://code.claude.com/docs/en/troubleshooting)

