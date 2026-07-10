---
date: 2026-06-19
tags:
  - tech
  - devtools
  - ai
  - coding-agent
  - learning
type: tech-tool-study
parent: "[[../README]]"
---

# 시작하기 - 작은 Repo에서 Agent Workflow 체험

> [[../README|목차로 돌아가기]] | [[02-deep-dive|다음: 딥다이브]]

---

## 목표

AI coding agent를 처음 배울 때는 큰 기능 개발보다 **작고 검증 가능한 작업**으로 시작한다.

추천 과제:

- 테스트 없는 pure function에 unit test 추가
- lint error 1-3개 수정
- 작은 bug를 reproduction test로 고정한 뒤 patch
- README의 실행 명령을 실제 repo 기준으로 정리

---

## 1. 도구 하나 선택

| 선호 | 선택지 |
|------|--------|
| OpenAI/ChatGPT 생태계 | Codex |
| terminal 기반 agent workflow | Claude Code, Codex, OpenCode |
| GitHub issue/PR 중심 | GitHub Copilot coding agent |
| VS Code 계열 IDE UX | Cursor, Windsurf |
| git pair programming | Aider |

처음에는 하나만 고른다. 여러 도구를 동시에 쓰면 agent behavior, permission, memory 차이를 구분하기 어렵다.

---

## 2. 작은 Repo 준비

```bash
git status
git branch
npm test
npm run lint
```

확인할 것:

| 항목 | 이유 |
|------|------|
| clean working tree | agent 변경분을 구분하기 쉬움 |
| test command | 결과 검증 기준 |
| lint/typecheck command | 반복 수정 기준 |
| package manager | `npm`, `pnpm`, `yarn`, `uv`, `go test` 등 |

---

## 3. Project Instruction 작성

예시 `AGENTS.md`:

```md
# Agent Instructions

## Commands

- Install: npm install
- Test: npm test
- Lint: npm run lint
- Typecheck: npm run typecheck

## Rules

- Keep changes minimal and scoped to the task.
- Do not modify unrelated files.
- Add or update tests for behavior changes.
- Before finalizing, run the smallest relevant verification command.

## Architecture Notes

- API code lives in src/api.
- Shared utilities live in src/lib.
- Tests use Vitest and are colocated as *.test.ts.
```

핵심은 agent가 매번 물어보지 않아도 되는 정보를 파일로 고정하는 것이다.

---

## 4. Plan 먼저 요구

바로 수정시키지 말고 먼저 탐색과 계획만 요청한다.

```text
이 repo에서 src/lib/formatDate.ts에 대한 테스트를 추가하려고 한다.
먼저 관련 파일을 탐색하고, 수정할 파일 목록과 test plan만 제안해줘.
아직 파일은 수정하지 마.
```

좋은 plan의 조건:

- 관련 파일과 이유를 말한다.
- 변경 범위가 작다.
- 검증 명령이 구체적이다.
- 불확실한 부분을 질문하거나 가정으로 표시한다.

---

## 5. 수정과 검증

수정 요청 예시:

```text
제안한 plan대로 진행해줘.
변경 범위를 테스트 추가에 한정하고, 마지막에 관련 테스트만 실행해줘.
```

검증:

```bash
git diff
npm test -- formatDate
npm run lint
```

확인 기준:

| 체크 | 질문 |
|------|------|
| Scope | 요청한 파일/행동만 바뀌었는가? |
| Behavior | 테스트가 실제 behavior를 고정하는가? |
| Style | 기존 convention을 따르는가? |
| Verification | agent가 실행한 command가 충분한가? |
| Risk | secret, destructive command, broad refactor가 없었는가? |

---

## 6. 첫 회고

작업이 끝나면 다음을 기록한다.

- agent가 잘 찾은 context
- agent가 놓친 convention
- 추가해야 할 project instruction
- 다음부터 먼저 금지할 command
- 반복해서 쓸 prompt pattern

---

## 관련 노트

- [[study/tech/ai/codex/cheatsheet]] - Codex 빠른 참조
- [[study/tech/ai/claude/03-claude-code]] - Claude Code 기본 사용
- [[study/tech/ai/model-context-protocol-mcp]] - 외부 도구 연결
