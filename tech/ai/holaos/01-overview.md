---
date: 2026-08-17
tags: [tech]
type: tech-tool-study
status: draft
---

# holaOS Overview

> [[README|목차로 돌아가기]] | [[02-ecosystem|다음: Ecosystem]]

## What

holaOS는 AI agent가 장기 작업을 이어갈 수 있게 Desktop, workspace contract, Runtime, memory, Apps/MCP, Skills, Automations와 Agent Harness를 하나의 local-first workspace로 묶는다.

```text
holaOS Desktop
  ↓ operator UI / workspace·model·state 관리
Workspace Contract
  ├─ workspace.yaml
  ├─ AGENTS.md
  ├─ Skills
  ├─ Apps
  └─ Commands
  ↓ per-run compilation
Runtime Services
  ├─ API Server
  ├─ SQLite State Store
  ├─ Memory / Continuity
  ├─ App Orchestration
  └─ Capability Projection
  ↓ reduced execution package
Harness Host → Agent Harness(pi)
  ↓
Model + Browser + Runtime Tools + MCP Servers
```

Desktop은 operator UI이고, Runtime은 상태와 capability를 관리하며, Harness는 compile된 package로 agent loop를 실행한다. 이 분리는 특정 model이나 agent CLI의 session format에 workspace 전체가 종속되는 문제를 줄이려는 설계다.

## Why

일반적인 assistant나 coding agent는 한 번의 대화 또는 session에는 강하지만, 작업이 며칠 이상 이어지거나 agent를 바꾸면 context가 쉽게 분산된다.

| 문제 | holaOS의 접근 |
|---|---|
| 결정과 진행 상태가 chat history에 묻힘 | continuity snapshot과 runtime state로 분리 |
| agent마다 memory와 tool을 다시 설정 | workspace contract로 authored environment 선언 |
| 실제 업무 tool과 agent 결과물이 분리 | Apps와 MCP capability를 workspace에 결합 |
| policy, 실행 상태, 장기 기억이 혼재 | `AGENTS.md`, SQLite, runtime memory, knowledge로 수명 분리 |
| tool이 늘수록 권한과 lifecycle이 복잡 | manifest, grant, health check, capability projection으로 관리 |

즉 “더 좋은 model”만 고르는 대신 model 바깥에 지속 가능한 **Environment Engineering** layer를 둔다.

## Workspace Contract

각 workspace는 하나의 use case에 대응하는 독립 실행 환경이다.

| 경로 | 역할 | 누가 관리하는가 |
|---|---|---|
| `workspace.yaml` | agent/model, Apps, Skills, Commands, MCP registry | author |
| `AGENTS.md` | standing instructions와 policy | author |
| `ONBOARD.md` | 최초 onboarding 지시 | author/template |
| `skills/<id>/SKILL.md` | 필요할 때 읽는 재사용 instruction pack | author |
| `apps/<id>/app.runtime.yaml` | App lifecycle, port, integration, MCP contract | app author |
| `.holaboss/` | harness session, attachment 등 runtime state | Runtime |
| `.git/` | local agent checkpoint | Git/agent |

중요한 구분은 **authored contract**와 **runtime-managed state**다. 전자는 사람이 검토하고 version control하기 쉬워야 하며, 후자는 실행 중 자주 변하므로 별도 lifecycle이 필요하다.

## Core Features

### Per-run compilation

Runtime은 workspace 전체를 model에 그대로 넣지 않는다. run마다 model, composed prompt, selected tools, MCP payload, recalled memory와 checksum을 포함하는 **reduced execution package**를 만든다.

이 방식은 다음 질문에 답할 수 있게 한다.

- 이번 run에 어떤 instruction이 들어갔는가?
- 어떤 tool과 MCP server가 노출됐는가?
- 어떤 memory가 recall됐는가?
- 실행 package가 workspace 상태와 일치하는가?

### Memory와 continuity 분리

| 계층 | 저장 내용 | 대표 저장소 |
|---|---|---|
| Workspace policy | 역할, 규칙, 행동 지침 | `AGENTS.md` |
| Execution truth | session, turn, queue, binding, proposal | `state/runtime.db` |
| Runtime continuity | 최근 turn, blocker, resume snapshot | `memory/workspace/.../runtime/` |
| Durable knowledge | facts, procedures, references | `memory/workspace/.../knowledge/` |
| User memory | preference, identity | `memory/preference/`, `memory/identity/` |

Memory update를 proposal로 다루는 이유는 한 번의 관찰을 곧바로 영구 preference로 승격하는 오류를 줄이기 위해서다.

### Capability projection

Runtime은 browser tools, runtime tools, Skills, Commands, MCP servers, Apps의 MCP tools를 합쳐 이번 run에 필요한 capability만 투영한다. `mcp_registry`에 allowlist가 있으면 `server.tool` 단위로 제한한다.

> [!danger] Empty allowlist
> allowlist가 비어 있으면 enabled MCP server에서 발견된 모든 tool이 노출될 수 있다. “비어 있음”을 “아무것도 허용하지 않음”으로 가정하지 말고 현재 구현을 확인한다.

### Apps, Skills, Templates, Automations

| 구성요소 | 책임 |
|---|---|
| App | UI, MCP server, local state, background job, integration, output을 함께 소유 |
| Skill | agent가 필요할 때 읽는 Markdown instruction pack |
| Template | Apps, Skills, 초기 파일, onboarding을 묶은 workspace scaffold |
| Automation | cron 또는 event trigger로 workspace task 실행 |

App은 setup/start/stop, MCP endpoint, health check, integration scope를 `app.runtime.yaml`에 선언한다. 외부 계정 연결에는 raw credential 직접 전달 대신 Runtime의 signed grant와 broker URL을 사용하는 구조가 제시된다.

## Model, Harness, Approval

- 문서상 provider path: holaOS Proxy, OpenAI, Anthropic, OpenRouter, Gemini, Ollama, MiniMax
- provider별 reasoning option은 Runtime이 provider-native parameter로 정규화
- 공개 게시, 메시지 전송, 유료 작업 같은 side effect는 approval 요청을 기본 원칙으로 설계
- 현재 OSS runtime에서 실제 탑재된 harness path는 `pi`

Harness boundary가 교체 가능하게 설계됐다는 것과 모든 harness가 같은 수준으로 구현됐다는 것은 다르다. 또한 approval UI가 있어도 custom MCP/App의 manifest, permission, tool implementation이 안전하다는 보장은 없다.

## Strengths and Limits

### 장점

- model/harness와 별개로 장기 workspace의 정책과 상태를 유지한다.
- memory를 policy, execution truth, continuity, knowledge, preference로 나눈다.
- Apps, Skills, MCP, Automation을 하나의 배포 가능한 환경으로 묶는다.
- run별 capability와 memory를 축소해 compile하는 경계를 둔다.

### 한계와 확인 사항

- `0.1.0` 수준의 빠르게 변하는 초기 project다.
- signed Desktop Quick Start는 우선 macOS Apple Silicon 중심이다.
- source installer는 macOS, Linux, WSL을 다루고 Windows build path도 있지만 platform별 UX는 직접 검증해야 한다.
- local-first는 local inference와 동의어가 아니다. cloud provider를 선택하면 관련 context가 해당 provider로 전송된다.
- 완전한 local inference에는 Ollama 같은 local provider 구성이 필요하다.
- 객관적 agent benchmark와 장기 안정성 자료가 아직 부족하다.
- Modified Apache 2.0의 상용 제공 제한을 표준 Apache-2.0과 혼동하면 안 된다.

## Sources

- https://www.holaos.ai/docs/getting-started
- https://www.holaos.ai/docs/concepts/concepts
- https://www.holaos.ai/docs/concepts/workspace-model
- https://www.holaos.ai/docs/concepts/memory-and-continuity
- https://www.holaos.ai/docs/contribute/runtime/run-compilation
- https://www.holaos.ai/docs/concepts/agent-harness/runtime-tools
- https://www.holaos.ai/docs/build/apps/app-anatomy
- https://www.holaos.ai/docs/getting-started/quick-start
- https://github.com/holaboss-ai/holaOS/blob/main/INSTALL.md

