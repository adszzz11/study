---
date: 2026-08-17
tags: [tech]
type: tech-tool-study
status: draft
---

# holaOS Projects

> [[04-learning/02-deep-dive|이전: Deep Dive]] | [[README|목차로 돌아가기]] | [[cheatsheet|다음: Cheatsheet]]

## Project Ladder

| 프로젝트 | 난이도 | 핵심 학습 | 외부 side effect |
|---|---:|---|---|
| Long-running research workspace | 1 | contract, continuity, knowledge | 없음 |
| Read-only inbox triage | 2 | App/MCP, scope, classification | 없음 |
| Multi-harness portability audit | 2 | run package, adapter gap | 없음 |
| Approval-gated content pipeline | 3 | automation, preview, approval | 공개 게시 가능 |
| Reusable workspace Template | 3 | App, Skill, onboarding, distribution | 설치/setup |

## 1. Long-running Research Workspace

### Goal

7일 이상 이어지는 research에서 source, 결정, blocker와 next action을 session 사이에 유지한다.

### Contract

```text
research-workspace/
├── workspace.yaml
├── AGENTS.md
├── ONBOARD.md
├── skills/
│   └── evidence-review/SKILL.md
└── reports/
```

### Acceptance criteria

- [ ] policy는 `AGENTS.md`, 사실은 durable knowledge, 다음 행동은 continuity에 저장된다.
- [ ] 모든 사실 주장에 source URL과 verified/inferred 상태가 있다.
- [ ] 3회 이상 stop/resume 후 같은 blocker와 next action을 이어간다.
- [ ] 오래된 사실을 새 source로 supersede할 수 있다.
- [ ] report 생성 외 external write tool은 노출되지 않는다.

## 2. Read-only Inbox Triage

### Goal

메일을 읽어 action category와 draft response를 만들되 실제 전송은 하지 않는다.

```text
Inbox App/MCP
  → read + search only
  → classify
  → draft locally
  → human reviews outside automation
```

| 영역 | 제한 |
|---|---|
| Scope | 최소 mailbox/folder, read-only |
| Tools | list/read/search만 allowlist |
| Memory | sender content를 user preference로 자동 저장하지 않음 |
| Output | local draft와 source message ID |
| Prohibited | send, delete, archive, forward |

### Failure tests

- prompt injection이 포함된 mail이 tool 추가 호출을 유도하는가?
- attachment 내용이 durable memory로 무분별하게 승격되는가?
- expired grant 뒤 App가 access를 계속하는가?
- empty allowlist가 send tool까지 expose하는가?

## 3. Multi-harness Portability Audit

### Goal

동일한 authored workspace가 harness 변경 시 어느 정도 재사용되는지 측정한다. 현재 실제 구현 범위를 먼저 확인하고, 지원되지 않는 harness는 문서 수준 비교로 남긴다.

| 평가 항목 | 측정 |
|---|---|
| Policy fidelity | standing instruction 준수율 |
| Tool exposure | compiled tool 집합 차이 |
| Resume | session/continuity 복원 여부 |
| Attachments | type, size, reference 보존 |
| Reasoning | provider-native option mapping |
| Errors | timeout/cancel/tool error normalization |

```markdown
## Harness audit

- holaOS version:
- Harness adapter/version:
- Model/provider:
- Workspace commit:
- Compiled capability set:
- Passed scenarios:
- Gaps:
```

## 4. Approval-gated Content Pipeline

### Goal

source 수집부터 draft까지 automation하고, 외부 게시 직전에 사람이 destination과 최종 내용을 승인한다.

```text
Cron/Event
  → collect sources
  → draft
  → fact/source validation
  → immutable preview
  → approval
  → publish once
  → audit + result
```

### Guardrails

- publish tool은 draft 단계에 노출하지 않는다.
- approval 화면에 destination, account, full content를 표시한다.
- 승인 대상 content의 hash를 실행 시 다시 검증한다.
- idempotency key로 retry 중복 게시를 막는다.
- run별 게시 수와 비용에 hard limit를 둔다.
- approval에는 expiry를 설정한다.

## 5. Reusable Workspace Template

### Goal

App, Skill, onboarding, initial files를 묶어 다른 사용자가 같은 환경을 재현하게 한다.

| 구성요소 | 포함할 것 |
|---|---|
| `ONBOARD.md` | goal, required integration, first safe task |
| `AGENTS.md` | stable policy만 포함 |
| Skills | 좁은 목적, input/output, failure condition |
| Apps | lifecycle, health, MCP endpoint, minimal scopes |
| Initial files | examples와 empty working area |
| Docs | supported platform/version, uninstall, data location |

### Distribution review

- [ ] secret, local path, personal identifier가 bundle에 없다.
- [ ] setup script가 하는 일을 사용자가 미리 볼 수 있다.
- [ ] App failure가 전체 workspace를 손상시키지 않는다.
- [ ] version compatibility와 migration path가 있다.
- [ ] Modified Apache 2.0이 배포 방식에 맞는지 확인했다.

## Project Review Template

```markdown
# Project Review

## Environment
- holaOS version:
- Platform:
- Harness:
- Provider/model:

## Contract
- Workspace commit:
- Enabled Apps/Skills:
- MCP allowlist:

## State
- Continuity restored:
- Memory proposals accepted/rejected:

## Safety
- External side effects:
- Approval path:
- Credential scope:
- Failure drills:

## Result
- Success criteria:
- Gaps:
- Rollback:
```

## Sources

- https://www.holaos.ai/docs/concepts/workspace-model
- https://www.holaos.ai/docs/concepts/memory-and-continuity
- https://www.holaos.ai/docs/concepts/agent-harness/runtime-tools
- https://www.holaos.ai/docs/build/apps/app-anatomy
- https://www.holaos.ai/docs/contribute/runtime/run-compilation

