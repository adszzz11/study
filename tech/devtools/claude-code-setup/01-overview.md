---
date: 2026-09-20
tags: [tech]
type: tech-tool-study
status: draft
---

# Claude Code Setup — Overview

> [[README|목차로 돌아가기]] · [[02-ecosystem|다음: Ecosystem]]

## What — Claude Code란?

Claude Code는 자연어로 목표를 전달하면 codebase를 탐색하고, tool을 선택해 파일과 command를 다루며, 실행 결과를 관찰해 다음 행동을 결정하는 agentic coding environment다. Terminal CLI가 중심이지만 VS Code, JetBrains, Desktop, Web, Slack, GitHub Actions, GitLab CI/CD에서도 사용할 수 있다.

주요 built-in capability는 다음과 같다.

- repository file 읽기와 search
- 여러 파일 edit 및 새 파일 생성
- Bash 또는 PowerShell command 실행
- build, lint, typecheck, test 결과 분석
- Git diff, commit, branch, merge conflict workflow
- web 및 MCP server를 통한 외부 data/tool 연결

## Why — 왜 필요한가?

기존 AI coding assistant는 code completion이나 한 번의 질의응답에 강했지만, 실제 개발 작업은 다음처럼 연속된 feedback loop다.

1. repository 구조와 관련 symbol을 찾는다.
2. dependency와 기존 convention을 파악한다.
3. 변경 범위와 검증 계획을 정한다.
4. 여러 파일을 수정한다.
5. build·lint·test를 실행한다.
6. 실패 원인을 분석하고 수정한다.
7. diff와 evidence를 검토한 뒤 commit 또는 PR로 전달한다.

Claude Code는 이 loop 안에서 model과 local tool을 연결해, 개발자가 code를 chat으로 복사하고 결과를 다시 editor와 terminal로 옮기는 context switching을 줄인다.

## Agentic Loop

```text
User goal
   ↓
Repository / context 탐색
   ↓
Plan과 tool 선택
   ↓
Read · Search · Edit · Bash · Web · MCP
   ↓
Build · test · diagnostic 관찰
   ↓
수정 반복
   ↓
Diff · evidence · commit / PR
```

핵심은 model이 답변만 생성하지 않는다는 점이다. 각 tool result가 다음 판단의 observation이 된다. 따라서 품질은 model만이 아니라 context의 정확성, tool authority, test feedback, 사용자의 검토 방식에 의해 함께 결정된다.

## Setup의 네 층

### 1. Runtime

| 선택지 | 장점 | 주의점 |
|---|---|---|
| CLI | shell·Git workflow에 직접 연결 | terminal과 command 이해 필요 |
| IDE | 열린 file, selection, diagnostics와 자연스럽게 연결 | extension과 CLI version 확인 |
| Desktop/Web | graphical workflow, remote/cloud task | local-only 설정과 capability 차이 확인 |
| CI/CD | issue/PR event 기반 자동화 | secret, token, branch protection 설계 필요 |

### 2. Context

- `CLAUDE.md`: session에 지속적으로 제공할 짧고 안정적인 project instruction
- `AGENTS.md`: 여러 coding agent가 공유할 수 있는 instruction file. 현재 Claude Code에서는 설정과 실행 환경에 따라 fallback 또는 병행 로드됨
- `.claude/rules/*.md`: 특정 path나 file type에만 적용할 규칙
- `.claude/skills/<name>/SKILL.md`: 필요할 때 load하는 reusable workflow

### 3. Authority

- permissions: tool과 argument 단위 allow/ask/deny
- sandbox: Bash process의 filesystem·network boundary
- hooks: lifecycle event에 deterministic command를 실행
- managed settings: 조직이 override할 수 없는 security baseline 배포

### 4. Integration

- MCP: database, browser, issue tracker, internal API 같은 외부 system 연결
- plugins: skills, agents, hooks, MCP server를 묶어 배포
- GitHub Actions/GitLab CI/CD: repository event 기반 실행
- Bedrock, Google Cloud Agent Platform, Microsoft Foundry: enterprise cloud provider 경로

## 핵심 특징

| 특징 | 의미 |
|---|---|
| Repository-aware | 필요한 file을 직접 찾아 context를 구성한다. |
| Tool-using | edit, shell, search, MCP 등을 실행한다. |
| Iterative | test failure를 관찰하고 수정 loop를 반복한다. |
| Configurable | context, permission, sandbox, hook을 scope별로 설정한다. |
| Multi-surface | terminal, IDE, desktop, web, CI/CD를 지원한다. |
| Extensible | skills, subagents, plugins, MCP로 확장한다. |

## 한계와 위험

- prompt injection이나 악성 repository instruction이 tool 사용을 유도할 수 있다.
- 넓은 Bash permission과 network access는 credential 유출 범위를 키운다.
- test가 없으면 문법적으로 그럴듯하지만 동작이 틀린 변경을 놓치기 쉽다.
- 긴 `CLAUDE.md`는 모든 session의 context를 소비하고 중요한 지침을 희석한다.
- cloud/remote session은 local user settings나 personal skill을 그대로 읽지 않을 수 있다.
- `bypassPermissions`는 일반 workstation이 아니라 외부에서 격리된 container/VM에서만 고려해야 한다.

## Sources

- [Claude Code overview](https://code.claude.com/docs/en/overview)
- [Claude Code Quickstart](https://code.claude.com/docs/en/quickstart)
- [How Claude Code works](https://code.claude.com/docs/en/how-claude-code-works)
- [Claude Code security](https://code.claude.com/docs/en/security)

