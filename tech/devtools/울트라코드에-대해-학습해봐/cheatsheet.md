---
date: 2026-06-19
tags:
  - tech
  - devtools
  - ai
  - coding-agent
  - cheatsheet
type: tech-tool-study
parent: "[[README]]"
---

# 울트라코드 - 치트시트

> [[README|목차로 돌아가기]]

---

## 한 줄 기억

울트라코드는 특정 공식 제품명이라기보다 **AI coding agent devtools** 흐름으로 이해한다. 핵심은 LLM이 repo context와 도구 권한을 받아 file edit, terminal, test, git/PR workflow를 반복하는 것이다.

---

## 핵심 구성

| 구성 | 키워드 |
|------|--------|
| Model | LLM reasoning, coding model |
| Context | `AGENTS.md`, `CLAUDE.md`, rules, memory, repo map |
| Tools | file read/edit, shell, browser, API, MCP |
| Permission | sandbox, approval, least privilege |
| Verification | lint, typecheck, unit/integration test, screenshot |
| Handoff | git diff, commit, PR, review comment |

---

## 도구 선택

| 필요 | 후보 |
|------|------|
| OpenAI 기반 coding agent | Codex |
| terminal 중심 agent | Claude Code, Codex, OpenCode |
| GitHub issue/PR agent | GitHub Copilot coding agent |
| AI IDE | Cursor, Windsurf |
| git 중심 pair programming | Aider |
| provider-neutral open source | OpenCode, Aider |

---

## 좋은 요청 Pattern

### Plan-only

```text
파일을 수정하지 말고 먼저 관련 파일을 탐색해줘.
영향 범위, 변경 후보, test plan, 위험 요소만 정리해줘.
```

### Scoped implementation

```text
변경 범위를 이 bug fix에 한정해줘.
관련 없는 refactor는 하지 말고, 수정 후 가장 작은 관련 테스트만 실행해줘.
```

### Review

```text
이 diff를 review해줘.
버그, edge case, missing test, security risk를 우선순위 순으로 찾아줘.
```

### Debug loop

```text
이 테스트 실패 로그를 분석해줘.
원인을 좁히고, 최소 수정 후 같은 테스트를 다시 실행해줘.
```

---

## Project Instruction Checklist

```md
# Agent Instructions

## Commands
- Test:
- Lint:
- Typecheck:
- Build:

## Rules
- Keep changes scoped.
- Do not modify unrelated files.
- Add tests for behavior changes.
- Ask before destructive commands.

## Architecture
- Main modules:
- Test location:
- Naming/style:
```

---

## 권한 체크

| 위험 | 기본 대응 |
|------|----------|
| broad file rewrite | scope 제한 |
| destructive command | 승인 없이는 금지 |
| secret access | 차단 |
| production resource | 차단 |
| network install | 승인 기반 |
| generated large diff | 작은 step으로 분리 |

---

## 검증 체크

| 변경 | 검증 |
|------|------|
| docs | link/path 확인 |
| utility | unit test |
| API | unit + integration test |
| UI | browser/screenshot check |
| dependency | build + full test |
| security | regression + abuse case |

---

## Anti-pattern

- “전체 repo를 알아서 개선해줘”
- test/lint 없이 agent patch를 merge
- `AGENTS.md` 없이 매번 긴 prompt 반복
- secret과 production access를 agent에게 넓게 허용
- 실패 원인 확인 없이 큰 refactor로 덮기
- PR 설명에 검증 결과를 남기지 않기

---

## 관련 노트

- [[study/tech/ai/codex/cheatsheet]] - Codex 명령과 패턴
- [[study/tech/ai/claude/03-claude-code]] - Claude Code workflow
- [[study/tech/ai/model-context-protocol-mcp/cheatsheet]] - MCP tool 설계 빠른 참조
