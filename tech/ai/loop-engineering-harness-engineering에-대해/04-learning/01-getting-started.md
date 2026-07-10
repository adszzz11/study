---
date: 2026-06-23
tags: [tech, ai, getting-started, agent-harness, agents-md]
status: learning
type: tech-tool-study
---

# 04-1. Getting Started — 작은 Repo에 Harness 만들기

## 목표

처음부터 LangGraph나 복잡한 platform을 만들 필요는 없다. 작은 repo에서는 `AGENTS.md`, 명확한 테스트 명령, 완료 보고 양식만으로도 harness의 절반은 시작된다.

## 1. 최소 Harness 구조

```text
repo/
├── AGENTS.md          # agent instruction
├── package.json       # test/build command
├── src/
└── tests/
```

`AGENTS.md`는 coding agent용 README처럼 쓴다.

```md
# AGENTS.md

## Setup
- Install dependencies with `npm install`.

## Test
- Run `npm test` before reporting completion.
- Run `npm run lint` when editing TypeScript files.

## Code Style
- Keep changes small and local.
- Follow existing file structure.

## Forbidden Actions
- Do not run production deploy commands.
- Do not rewrite lockfiles unless dependency changes are requested.
- Do not delete user data or migration files without explicit approval.

## Completion Report
- List changed files.
- Explain why each change was needed.
- Include exact verification command and result.
```

## 2. 간단한 Agent Loop를 문서화하기

```text
1. 목표를 checklist로 바꾼다.
2. 관련 파일을 찾는다.
3. 최소 변경을 만든다.
4. 테스트를 실행한다.
5. 실패하면 log를 읽고 원인을 분류한다.
6. 다시 수정한다.
7. 성공 증거와 변경 요약을 남긴다.
```

agent에게는 아래처럼 시킨다.

```text
이 작업은 아래 loop로 진행해줘.
- 먼저 요구사항을 checklist로 정리
- 관련 파일을 찾아 최소 범위로 수정
- `npm test`로 검증
- 실패하면 로그 기반으로 원인을 분류하고 재시도
- 완료 보고에는 변경 파일, 이유, 검증 명령을 포함
```

## 3. Verification Protocol 만들기

| 작업 유형 | 완료 증거 |
|-----------|-----------|
| 버그 수정 | 재현 테스트 추가/수정 + 관련 test pass |
| UI 수정 | 스크린샷 또는 Playwright 확인 |
| API 수정 | unit/integration test + 응답 예시 |
| 리팩터링 | 기존 test pass + public behavior 변화 없음 |
| 문서 작업 | 링크, frontmatter, 파일 구조 확인 |

```bash
# 검증 명령 예시
npm test
npm run lint
pytest
go test ./...
```

## 4. Failure Attribution 연습

실패를 "안 됨"으로 두지 말고 분류한다.

| 실패 유형 | 질문 | 다음 행동 |
|-----------|------|-----------|
| `context failure` | 잘못된 파일을 봤나? | search 범위 재설정 |
| `tool failure` | 명령이 없거나 환경이 다른가? | setup 확인, 대체 명령 찾기 |
| `test failure` | 코드 변경이 regression을 만들었나? | 실패 test 중심으로 patch |
| `requirement failure` | 요구사항을 잘못 해석했나? | task checklist 재작성 |
| `permission failure` | 하면 안 되는 작업이 필요한가? | 사람 승인 요청 |

## 5. 첫 실습

```text
실습: 작은 Todo 앱 repo에 harness 추가

1. AGENTS.md 작성
2. test/lint/build 명령 확인
3. "완료 보고 양식" 추가
4. agent에게 사소한 버그를 맡김
5. 변경 보고와 실제 test result가 맞는지 확인
```

## 6. 좋은 시작점 체크리스트

- [ ] `AGENTS.md`가 있다.
- [ ] setup/test/build 명령이 명시되어 있다.
- [ ] 금지 명령과 승인 필요 작업이 적혀 있다.
- [ ] 완료 조건이 "느낌"이 아니라 test/log/report로 표현된다.
- [ ] 실패 시 재시도 방식이 있다.
- [ ] 사람이 리뷰할 지점이 정해져 있다.

## 추가 조사: Claude Code에 적용하는 최소 Loop Harness

Claude에 적용할 때는 `AGENTS.md`보다 Claude Code가 직접 읽는 `CLAUDE.md`와 `.claude/settings.json`을 중심으로 잡는 것이 실용적이다. 공식 문서 기준으로 Claude Code는 user/project/local/managed scope를 나누고, project 설정은 `.claude/settings.json`, local 개인 설정은 `.claude/settings.local.json`, project memory는 `CLAUDE.md` 또는 `.claude/CLAUDE.md`를 사용한다.

### 1. `CLAUDE.md`에 loop를 박아두기

```md
# CLAUDE.md

## Working Loop
- Restate the user request as a checklist before editing.
- Read the smallest relevant set of files first.
- Make scoped changes that follow existing patterns.
- Run the most relevant focused test first, then broader tests when needed.
- If a command fails, classify it as `context`, `tool`, `test`, `requirement`, or `permission` failure before retrying.
- Stop after 3 repeated failures with the same cause and ask for human direction.

## Verification Protocol
- Do not claim completion without command output, test result, screenshot, or diff-based evidence.
- Bug fix: add or update a regression test when feasible.
- Refactor: show that public behavior is unchanged.
- Docs-only: verify links, filenames, and frontmatter.

## Permission Boundary
- Allowed: read files, edit workspace files, run test/lint/build commands.
- Ask first: dependency changes, migrations, auth/payment/security changes.
- Forbidden: production deploy, secret access, destructive data commands.

## Completion Report
- Changed files
- Why each change was needed
- Verification commands and results
- Remaining risks or skipped checks
```

### 2. `.claude/settings.json`으로 권한을 harness화하기

공식 settings 문서는 permission rule을 `allow`, `ask`, `deny`로 둘 수 있고, project scope의 `.claude/settings.json`은 팀과 공유할 수 있다고 설명한다. 개인 실험은 `.claude/settings.local.json`에 둔다.

```json
{
  "$schema": "https://json.schemastore.org/claude-code-settings.json",
  "permissions": {
    "allow": [
      "Bash(npm test)",
      "Bash(npm run test *)",
      "Bash(npm run lint)",
      "Bash(pytest *)",
      "Bash(go test ./...)"
    ],
    "ask": [
      "Bash(npm install *)",
      "Bash(pnpm add *)",
      "Bash(rails db:migrate *)"
    ],
    "deny": [
      "Bash(rm -rf *)",
      "Bash(curl * | sh)",
      "Bash(kubectl delete *)",
      "Bash(terraform apply *)",
      "Read(./.env)",
      "Read(./.env.*)",
      "Read(./secrets/**)"
    ]
  }
}
```

| Harness 요소 | Claude Code 매핑 | 먼저 할 일 |
|---|---|---|
| `Project memory` | `CLAUDE.md`, `.claude/CLAUDE.md` | repo 구조, 테스트 규칙, loop 작성 |
| `Permission boundary` | `.claude/settings.json` permissions | 허용/질문/금지 명령 분리 |
| `Verification protocol` | `CLAUDE.md` + hooks | 완료 보고와 test command 강제 |
| `Tool registry` | MCP, plugins, allowed tools | read-only tool부터 연결 |
| `Failure attribution` | prompt/skill/report template | 실패 원인 분류를 보고 양식에 포함 |

### 3. 바로 쓸 수 있는 작업 프롬프트

```text
이 repo의 CLAUDE.md 규칙을 따라 loop engineering 방식으로 진행해줘.

목표:
- <해야 할 일>

절차:
- 먼저 요구사항을 checklist로 바꿔라.
- 관련 파일을 찾고, 왜 그 파일을 보는지 짧게 설명해라.
- 변경은 최소 범위로 해라.
- 검증 명령을 실행하고, 실패하면 failure attribution을 작성한 뒤 재시도해라.
- 같은 원인으로 3회 실패하면 멈추고 사람에게 필요한 결정을 요청해라.

완료 보고:
- 변경 파일
- 요구사항별 충족 여부
- 실행한 검증 명령과 결과
- 남은 위험
```

### 4. `/loop`로 반복 업무 만들기

Claude Code의 scheduled task 문서는 `/loop`로 prompt를 주기적으로 실행하는 방식을 제공한다. 운영 감시나 정기 점검에는 "무조건 고쳐라"보다 "관찰하고 report하라, 위험 작업은 승인받아라"가 안전하다.

```text
/loop every 30 minutes
Check CI status and recent error logs.
If failures exist:
- summarize failing job/log lines
- identify likely owner/component
- suggest the smallest next action
- do not deploy, rollback, delete data, or change secrets
```

참고:

- Claude Code settings: https://code.claude.com/docs/en/settings
- Claude Code memory: https://code.claude.com/docs/en/memory
- Claude Code scheduled tasks `/loop`: https://code.claude.com/docs/en/scheduled-tasks

## 관련 노트

- [[study/tech/ai/codex]]
- [[study/tech/ai/lazy-codex]]
- [[study/tech/ai/model-context-protocol-mcp]]
