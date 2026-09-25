---
date: 2026-09-25
tags: [tech]
type: tech-tool-study
status: draft
---

# Clodex loop — Deep dive

## 1. artifact가 handoff의 API가 된다

Clodex의 핵심 산출물은 최종 code만이 아니다. plan, implementation report, 두 audit, agreement, patch, trace가 다음 단계의 입력이 된다.

| Artifact | 질문 |
|---|---|
| `01-claude-plan.json` | acceptance criteria와 non-goal이 구현 가능하게 표현됐는가? |
| `02-codex-implementation.md` | 무엇을 바꿨고, 어떤 test를 실행했으며, 무엇이 남았는가? |
| `03/04-*-audit.json` | 어느 diff hash를 어떤 persona가 audit했고, blocking finding은 무엇인가? |
| `05-agreement.json` | 두 쪽이 **같은 final hash**를 승인했는가? |
| `changes.diff` / `apply.patch` | source checkout에 적용할 실제 변경은 무엇인가? |
| `trace.jsonl` | 재개·CI 보관·incident review에 필요한 event 순서는 있는가? |

## 2. MCP와 CLI fallback

native MCP handoff는 `clodex_handoff_create`, `update`, `get`, `decide`를 제공한다. MCP가 없는 scripted/CI 상황에는 `clodex task start/get`, `clodex audit --diff`, `clodex status` 같은 CLI fallback이 있다.

MCP는 transport와 tool interface를 제공할 뿐, handoff가 좋은지 보장하지 않는다. plan의 acceptance criteria, implementation report의 test evidence, audit finding의 재현 절차가 부족하면 durable state도 잘못된 결론을 오래 보존한다.

## 3. audit policy를 설계하는 법

`CLODEX.md`는 repo-owned policy다. 기본 contract에는 required reviewer와 선택 reviewer(persona)가 있다.

```text
required: Claude plan-adherence, Codex architecture
optional: security, performance, portability, test-gap
```

변경 위험에 맞춰 persona를 선택한다. 예를 들어 migration에는 compatibility/security, cross-platform CLI에는 portability, 대형 refactor에는 plan-adherence/test-gap을 강화한다. reviewer 수를 늘릴수록 signal만 아니라 timeout·비용·불일치 triage도 증가한다.

## 4. 실패 경계와 escalation

| 조건 | 기대 행동 |
|---|---|
| audit finding이 남음 | `max_fix_loops` 안에서 targeted fix 후 동일 절차를 재실행 |
| loop cap 도달 | 자동 apply 대신 사람에게 finding·diff·test evidence를 escalate |
| agent/CLI timeout | partial artifact를 보존하고 readiness·timeout·MCP 상태를 점검 |
| diff가 audit 뒤 변함 | 새 hash에 대해 audit과 agreement를 다시 만든다 |
| test가 flaky | dual audit의 문제가 아니라 test determinism 문제로 분리해 해결 |

## 5. 안전성의 실제 의미

Git worktree와 `workspace-write`는 blast radius를 줄이지만, 실행 명령 자체의 안전성이나 code의 correctness를 보장하지 않는다. `manual apply`는 마지막 검토 지점이다. CI test/lint/SAST, dependency review, human change approval을 별도 baseline으로 유지한다.

## Sources

- https://github.com/9thLevelSoftware/Clodex/blob/main/README.md
- https://github.com/9thLevelSoftware/Clodex/blob/main/CLODEX.md
- https://docs.anthropic.com/en/docs/mcp
- https://developers.openai.com/docs/config-file/config-reference
