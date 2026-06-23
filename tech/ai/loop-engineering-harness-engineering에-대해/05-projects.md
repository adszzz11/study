---
date: 2026-06-23
tags: [tech, ai, projects, agent-harness, loop-engineering]
status: learning
type: tech-tool-study
---

# 05. Projects — 실전 적용 아이디어

## Project 1. Repo용 AGENTS.md Harness

| 항목 | 내용 |
|------|------|
| 목표 | coding agent가 repo 관습을 읽고 일하게 만들기 |
| 난이도 | 하 |
| 핵심 개념 | `AGENTS.md`, task interface, verification protocol |

```text
구현:
1. setup/test/build 명령 정리
2. code style과 architecture rule 작성
3. forbidden action 작성
4. completion report template 작성
5. 작은 버그 수정 task로 검증
```

완료 기준:

- [ ] agent가 지침을 읽고 관련 테스트를 실행한다.
- [ ] 변경 보고에 파일·이유·검증 결과가 포함된다.
- [ ] 금지 작업을 시도하지 않는다.

## Project 2. Test-Failure Repair Loop

| 항목 | 내용 |
|------|------|
| 목표 | 실패한 테스트 로그를 읽고 자동으로 수정 재시도하는 loop 만들기 |
| 난이도 | 중 |
| 핵심 개념 | failure attribution, observe-act-verify loop |

```text
loop:
  run tests
  if pass: stop
  collect failure log
  classify failure
  patch minimal code
  rerun focused test
  rerun full test
```

주의:

- 같은 실패가 3회 반복되면 사람에게 넘긴다.
- test를 삭제하거나 약화하는 patch는 금지한다.
- dependency 추가는 승인 대상으로 둔다.

## Project 3. PR Eval Gate

| 항목 | 내용 |
|------|------|
| 목표 | agent가 만든 PR을 merge 전에 자동 평가 |
| 난이도 | 중 |
| 핵심 개념 | eval gate, trace-based evaluation, entropy auditor |

```yaml
checks:
  - tests_pass
  - lint_pass
  - no_secret
  - no_unrelated_large_diff
  - verification_report_exists
  - requirements_checklist_satisfied
```

완료 기준:

- [ ] PR마다 verification report가 붙는다.
- [ ] 요구사항별 pass/fail이 보인다.
- [ ] 불필요한 대규모 변경이 gate에서 잡힌다.

## Project 4. Trace Dashboard

| 항목 | 내용 |
|------|------|
| 목표 | agent 실행을 episode 단위로 추적 |
| 난이도 | 중상 |
| 핵심 개념 | observability layer, episode package |

수집할 데이터:

| 필드 | 예시 |
|------|------|
| task id | `BUG-123` |
| model/tool | Codex, shell, MCP server |
| commands | `npm test`, `pytest` |
| changed files | `src/api/users.ts` |
| failure attribution | `test failure` |
| verification | pass/fail, logs |
| human intervention | 승인, 힌트, 수동 수정 |

## Project 5. Scheduled Operations Loop

| 항목 | 내용 |
|------|------|
| 목표 | 배포 상태나 batch job을 주기적으로 확인하고 실패 시 분석 |
| 난이도 | 중상 |
| 핵심 개념 | Routines, scheduled loop, observability |

```text
예시:
5분마다 배포 상태 확인
 -> 실패 발견
 -> 로그 수집
 -> 최근 변경 diff 확인
 -> 원인 후보 작성
 -> 알림 또는 rollback 제안
```

권한 설계:

- 로그 읽기: 허용
- 원인 분석 report: 허용
- rollback 실행: 사람 승인 필요
- production secret 접근: 금지

## Project 6. MCP Tool Harness

| 항목 | 내용 |
|------|------|
| 목표 | 내부 API/DB/SaaS를 MCP server로 감싸 agent에게 안전하게 노출 |
| 난이도 | 상 |
| 핵심 개념 | MCP, tool registry, permission boundary |

```text
설계:
1. read-only tool부터 시작
2. destructive action은 approval gate 추가
3. tool input/output schema 명확화
4. tool trace 저장
5. eval로 잘못된 tool call 탐지
```

## 프로젝트 선택 가이드

| 지금 상황 | 먼저 할 프로젝트 |
|-----------|------------------|
| agent가 repo 규칙을 자주 어긴다 | Project 1 |
| agent가 테스트 실패 후 헤맨다 | Project 2 |
| agent PR을 팀에 도입하고 싶다 | Project 3 |
| 실패 원인을 나중에 분석하고 싶다 | Project 4 |
| 운영 감시를 자동화하고 싶다 | Project 5 |
| 내부 tool을 agent에 연결하고 싶다 | Project 6 |

## 관련 노트

- [[study/tech/ai/model-context-protocol-mcp]]
- [[study/tech/ai/codex]]
- [[study/tech/ai/lazy-codex]]
