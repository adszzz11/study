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

## 관련 노트

- [[study/tech/ai/model-context-protocol-mcp]]
- [[study/tech/ai/lazy-codex]]
- [[study/tech/ai/agent-orchestration/cli-agents]]
