---
date: 2026-06-23
tags: [tech, ai, cheatsheet, agent-loop, agent-harness]
status: learning
type: tech-tool-study
---

# Cheatsheet — Loop Engineering & Harness Engineering

## 한 줄

- `loop engineering`: agent가 `observe -> act -> verify -> continue/stop`을 반복하는 방식을 설계.
- `harness engineering`: 그 loop가 안전하고 재현 가능하게 돌도록 context, tools, memory, permissions, evals, traces를 설계.

## 기본 Loop

```text
Goal -> Plan -> Retrieve context -> Use tools -> Observe -> Diagnose -> Patch -> Verify -> Stop/Continue
```

## Harness 11요소

| 요소 | 역할 |
|------|------|
| `Task interface` | 목표, 요구사항, 성공기준 |
| `Context manager` | 필요한 파일/문서 선별 |
| `Tool registry` | 사용 가능한 tool/command 선언 |
| `Project memory` | 아키텍처, 테스트 규칙, 과거 실패 |
| `Task state` | 현재 가설, 본 파일, 다음 단계 |
| `Observability layer` | logs, traces, runtime output |
| `Failure attribution` | 실패 원인 분류 |
| `Verification protocol` | 완료 증거 생성 |
| `Permission boundary` | 허용/금지 작업 경계 |
| `Entropy auditor` | 유지보수 부담 감지 |
| `Intervention logger` | 인간 개입 기록 |

## 전문용어

| 용어 | 뜻 |
|------|-----|
| `agent harness` | model 주변의 runtime support layer |
| `agent loop` | model/tool/feedback 반복 실행 흐름 |
| `trace-based evaluation` | 실행 로그 전체를 episode로 기록해 평가 |
| `episode package` | patch, tool trace, verification report, failure attribution 묶음 |
| `eval gate` | 배포/merge 전에 agent 결과를 자동 평가하는 gate |
| `human-in-the-loop` | 사람 승인 또는 판단을 loop 중간에 넣는 방식 |
| `subagent` | 특정 업무만 맡는 specialist agent |
| `worktree isolation` | 병렬 agent가 서로 다른 git worktree에서 작업 |
| `MCP` | AI app이 외부 data/tools/workflows에 연결되는 표준 protocol |
| `AGENTS.md` | coding agent용 repo-level instruction file |
| `observability` | agent가 무엇을 보고, 어떤 tool을 썼고, 왜 실패했는지 추적 |
| `permission boundary` | agent가 해도 되는 일과 금지된 일을 나누는 안전 경계 |

## 최소 AGENTS.md

```md
# AGENTS.md

## Setup
- Run `npm install`.

## Test
- Run `npm test` before completion.

## Style
- Keep changes scoped.
- Follow existing patterns.

## Forbidden
- Do not deploy.
- Do not access secrets.
- Do not delete data.

## Report
- Changed files
- Reason for change
- Verification command and result
```

## 실패 분류

| Failure | 의미 | 대응 |
|---------|------|------|
| `context failure` | 잘못된 파일/문서 봄 | search 범위 수정 |
| `tool failure` | 명령/API/tool 문제 | setup 또는 tool schema 확인 |
| `test failure` | 검증 실패 | 실패 test 중심 patch |
| `requirement failure` | 요구사항 오해 | checklist 재작성 |
| `permission failure` | 승인 필요 작업 | 사람에게 넘김 |

## 설계 체크리스트

- [ ] 목표와 성공 기준이 명확한가?
- [ ] agent가 볼 context의 우선순위가 있는가?
- [ ] 허용 tool과 금지 tool이 분리되어 있는가?
- [ ] 실패 로그를 agent가 관찰할 수 있는가?
- [ ] 실패 원인 분류가 남는가?
- [ ] 완료 증거가 test/eval/report로 남는가?
- [ ] 위험 변경에는 human-in-the-loop가 있는가?
- [ ] trace와 intervention log가 저장되는가?

## 기억할 비유

```text
prompt = "버그 고쳐줘"라는 말
loop = junior 개발자가 실패 로그 보고 다시 고치는 업무 절차
harness = 이슈 설명서, 코드베이스 안내, 실행 권한, 테스트 기준, 보고 양식
```

## 관련 노트

- [[study/tech/ai/lazy-codex]]
- [[study/tech/ai/model-context-protocol-mcp]]
- [[study/tech/ai/agent-orchestration/cli-agents]]
