---
date: 2026-06-23
tags: [tech, ai, deep-dive, traces, evals, observability]
status: learning
type: tech-tool-study
---

# 04-2. Deep Dive — Trace, Eval, Permission, Memory

## 1. Trace-Based Evaluation

`trace-based evaluation`은 최종 답변만 보는 것이 아니라 agent의 실행 전체를 episode로 본다.

```text
episode
├── task prompt
├── retrieved context
├── tool calls
├── command outputs
├── patches
├── failures
├── verification report
└── final answer
```

최종 patch가 통과했더라도 trace를 보면 다음을 알 수 있다.

- 잘못된 파일을 오래 봤는가?
- 같은 실패를 반복했는가?
- 위험 명령을 실행하려 했는가?
- 테스트 없이 완료했다고 했는가?
- 사람 개입이 있었는데 자동화 성과로 오해하고 있는가?

## 2. Episode Package

`episode package`는 감사 가능한 실행 기록 묶음이다.

| 구성 | 예시 |
|------|------|
| `patch` | git diff |
| `tool trace` | file read, command execution, API call |
| `verification report` | test command, result, screenshot |
| `failure attribution` | context/tool/test/permission failure |
| `intervention log` | 사람이 알려준 힌트, 승인, 수동 수정 |

```text
좋은 episode package = 나중에 사람이 "왜 이렇게 바뀌었지?"를 재구성할 수 있는 기록
```

## 3. Eval Gate

`eval gate`는 agent 결과가 merge/deploy되기 전에 자동 평가를 통과하게 하는 문이다.

| gate | 검사 대상 |
|------|-----------|
| unit test gate | 기존 기능 regression |
| lint/type gate | code quality baseline |
| rubric judge gate | 요구사항 충족 여부 |
| security gate | secret, dangerous command, permission violation |
| entropy gate | 불필요한 dependency, residue, overengineering |

```yaml
# 개념 예시
eval_gate:
  required:
    - unit_tests_pass
    - lint_pass
    - no_secret_added
    - verification_report_present
  manual_review:
    - database_migration
    - auth_or_payment_change
    - production_deploy
```

## 4. Permission Boundary

`permission boundary`는 agent가 해도 되는 일과 금지된 일을 나누는 안전 경계다.

| 작업 | 권한 정책 |
|------|-----------|
| 파일 읽기 | 대부분 허용 |
| 코드 수정 | workspace 내부만 허용 |
| 테스트 실행 | 허용 |
| dependency 추가 | 승인 또는 명확한 이유 필요 |
| DB migration | 사람 승인 필요 |
| deploy | 보통 금지 또는 별도 gate 필요 |
| secret 접근 | 금지 |
| destructive command | 금지 또는 강한 승인 필요 |

좋은 boundary는 agent를 묶기만 하는 규칙이 아니다. 오히려 agent가 무엇을 해도 되는지 명확히 알려서 불필요한 질문과 위험 행동을 동시에 줄인다.

## 5. Context Manager와 Project Memory

긴 작업에서 가장 흔한 실패는 잘못된 context다.

```text
context manager:
  - 관련 파일 찾기
  - 오래된 정보 제거
  - 큰 로그 요약
  - 중요한 instruction 유지

project memory:
  - architecture note
  - test rule
  - deploy rule
  - known pitfalls
  - previous failure
```

한국 회사 예시:

- 신규 입사자에게 매번 "우리 API는 controller-service-repository 구조야"라고 말하면 낭비다.
- repo-level memory에 "API 변경 시 contract test를 같이 수정한다"가 있으면 agent도 같은 관습을 따른다.

## 6. Subagent와 Worktree Isolation

| 개념 | 설명 | 언제 쓰나 |
|------|------|-----------|
| `subagent` | 특정 역할만 맡는 specialist agent | review, test diagnosis, docs, security scan |
| `worktree isolation` | 병렬 agent가 서로 다른 git worktree에서 작업 | 여러 이슈를 동시에 처리할 때 |
| `human-in-the-loop` | 사람 승인·판단을 loop 중간에 삽입 | 모호한 요구사항, 위험 변경 |
| `MCP` | 외부 data/tools/workflows 연결 protocol | DB, SaaS, internal API 연결 |

## 7. Agent Improvement Loop

OpenAI Cookbook의 agent improvement loop는 harness 개선 자체를 loop로 만든다.

```text
traces
 -> human/LLM feedback
 -> evals
 -> ranked harness changes
 -> Codex implementation
 -> new traces
```

여기서 harness는 `instructions, tools, routing, output requirements, validation checks` 전체 contract다. 즉 prompt를 조금 바꾸는 수준이 아니라 실행 계약을 계속 개선한다.

## 8. Deep-Dive 체크리스트

- [ ] 최종 답변만이 아니라 trace를 저장한다.
- [ ] 실패 원인을 context/tool/test/permission/requirement로 분류한다.
- [ ] agent 결과를 eval gate로 막는다.
- [ ] 위험 명령과 승인 필요 작업을 permission boundary에 적는다.
- [ ] 반복 실패와 사람 개입을 episode package에 남긴다.
- [ ] harness 변경도 eval로 검증한다.

## 추가 조사: Claude의 Skills, Hooks, Subagents, Plugins로 Harness 확장

Claude Code는 loop를 직접 코딩하지 않아도 `Skills`, `Hooks`, `Subagents`, `MCP`, `Plugins`로 harness를 확장할 수 있다. 핵심은 "모델에게 잘 부탁하기"가 아니라 반복되는 판단과 검증을 파일/설정/도구로 고정하는 것이다.

### 구성요소 매핑

| 목적 | Claude 기능 | Harness 역할 | 예시 |
|---|---|---|---|
| 반복 절차 템플릿 | `Skill` | task-specific loop instruction | `/repair-test`, `/review-pr` |
| 실행 전후 정책 | `Hook` | guardrail, logging, verification | test 없이 완료 방지, 위험 명령 차단 |
| 역할 분리 | `Subagent` | specialist reviewer/diagnoser | security reviewer, test failure analyst |
| 외부 도구 연결 | `MCP` | tool registry/context provider | GitHub, DB read-only query, issue tracker |
| 재사용 패키징 | `Plugin` | skills/agents/hooks/MCP 묶음 배포 | 팀 공통 loop-engineering plugin |

### 1. Skill: 반복 작업을 명령처럼 만들기

공식 Skills 문서는 `SKILL.md`에 YAML frontmatter와 지침을 넣고, Claude가 task context에 맞춰 skill을 사용할 수 있게 한다. 개인/프로젝트 실험은 `.claude/` 아래 standalone 구성으로 시작하고, 팀 공유가 필요하면 plugin으로 패키징한다.

```text
.claude/
└── skills/
    └── test-repair/
        └── SKILL.md
```

```md
---
description: Use when a test command fails and the task is to diagnose and repair it without weakening tests.
---

# Test Repair Loop

1. Capture the exact failing command and relevant log lines.
2. Classify the failure as `context`, `tool`, `test`, `requirement`, or `permission`.
3. Inspect only files directly related to the failing test first.
4. Propose the smallest patch.
5. Re-run the focused failing test.
6. Re-run the broader suite when the focused test passes.

Rules:
- Do not delete or weaken tests to make the suite pass.
- Do not add dependencies unless the user explicitly approves.
- Stop after 3 same-cause failures and report the blocker.
```

### 2. Subagent: specialist reviewer 분리

Subagent는 특정 역할의 system prompt, tool 제한, model 선택을 분리하는 용도다. loop engineering에서는 main agent가 구현하고, subagent가 검증/보안/테스트 원인 분석을 맡게 하는 식이 자연스럽다.

```md
---
name: verification-reviewer
description: Reviews whether a coding task has enough evidence to be considered complete.
tools: Read, Grep, Bash
---

You are a verification reviewer.

Check:
- requirements checklist is satisfied
- changed files match the task scope
- tests or equivalent evidence exist
- no forbidden actions were used
- completion report includes commands and results

Return:
- pass/fail
- missing evidence
- recommended next verification command
```

### 3. Hook: 검증과 logging을 자동화하기

Hooks는 lifecycle event에 command를 붙여 정책을 삽입하는 기능이다. 예를 들어 `PostToolUse`에서 command 실행을 log로 남기거나, `Stop`에서 verification report가 없는 종료를 잡는 식으로 쓴다. 조직에서는 managed settings로 hook/permission 정책을 강제할 수 있다.

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "mkdir -p .claude-traces && date >> .claude-traces/commands.log"
          }
        ]
      }
    ]
  }
}
```

주의:

- hook은 shell command를 실행하므로 repo 신뢰와 secret 노출을 먼저 검토한다.
- blocking hook은 생산성을 크게 바꿀 수 있으므로 local scope에서 실험한 뒤 project/managed scope로 올린다.
- hook으로 모든 판단을 자동화하려 하지 말고, 위험 작업은 `ask` permission과 human-in-the-loop로 둔다.

### 4. Plugin: 팀 공통 harness 배포 단위

공식 plugin 문서는 plugin이 `skills`, `agents`, `hooks`, MCP server, LSP server, background monitor, default settings를 묶을 수 있다고 설명한다. 한 repo 실험은 `.claude/` standalone으로 충분하지만, 여러 repo/팀에 같은 loop를 배포하려면 plugin이 맞다.

```text
loop-harness-plugin/
├── .claude-plugin/
│   └── plugin.json
├── skills/
│   └── test-repair/
│       └── SKILL.md
├── agents/
│   └── verification-reviewer.md
├── hooks/
│   └── hooks.json
├── .mcp.json
└── settings.json
```

```json
{
  "name": "loop-harness",
  "description": "Team loop engineering harness for Claude Code",
  "version": "0.1.0",
  "author": {
    "name": "Engineering"
  }
}
```

### 5. MCP: tool registry는 read-only부터

Claude에 내부 시스템을 붙일 때는 MCP를 "무엇이든 할 수 있는 tool"로 열지 말고 harness의 tool registry로 다룬다.

| 단계 | MCP tool 정책 | 예시 |
|---|---|---|
| 1 | read-only | issue 읽기, CI 로그 조회, DB select |
| 2 | draft/write with approval | PR comment 초안, ticket update |
| 3 | destructive with explicit human gate | rollback, migration, infra 변경 |

### 추천 적용 순서

1. `CLAUDE.md`에 working loop와 completion report를 쓴다.
2. `.claude/settings.json`에 permission boundary를 둔다.
3. 자주 반복되는 업무 하나를 Skill로 만든다. 예: `test-repair`.
4. 검증 담당 Subagent를 추가한다.
5. command logging이나 completion check Hook을 local로 실험한다.
6. 여러 repo에 필요해지면 Plugin으로 묶는다.
7. 외부 도구는 MCP read-only부터 연결한다.

참고:

- Skills: https://code.claude.com/docs/en/skills
- Subagents: https://code.claude.com/docs/en/sub-agents
- Hooks: https://code.claude.com/docs/en/hooks
- Plugins: https://code.claude.com/docs/en/plugins
- MCP: https://code.claude.com/docs/en/mcp

## 관련 노트

- [[study/tech/ai/model-context-protocol-mcp]]
- [[study/tech/ai/lazy-codex]]
- [[study/tech/ai/agent-orchestration/cli-agents]]
