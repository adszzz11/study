---
date: 2026-08-17
tags: [tech]
type: tech-tool-study
status: draft
---

# holaOS Cheatsheet

> [[05-projects|이전: Projects]] | [[README|목차로 돌아가기]]

## One-line Model

```text
Desktop → Workspace Contract → Runtime → Reduced Package → Harness → Model + Tools
```

**holaOS = agent 자체라기보다 장기 agent 작업을 위한 local-first environment/workspace layer**

## Key Files

| 경로 | 기억할 역할 |
|---|---|
| `workspace.yaml` | model/agent, Apps, Skills, Commands, MCP registry |
| `AGENTS.md` | 항상 적용할 authored policy |
| `ONBOARD.md` | 최초 onboarding |
| `skills/<id>/SKILL.md` | on-demand Markdown instruction pack |
| `apps/<id>/app.runtime.yaml` | lifecycle, port, health, MCP, integration scope |
| `.holaboss/` | harness session/attachment 등 runtime-managed state |
| `.git/` | local checkpoint와 authored contract history |

## State Layers

| 기억할 질문 | 계층 | 저장소 예 |
|---|---|---|
| “항상 지킬 규칙인가?” | Workspace policy | `AGENTS.md` |
| “실제로 실행된 turn은?” | Execution truth | `state/runtime.db` |
| “다음 run에 무엇을 이어가나?” | Runtime continuity | `memory/workspace/.../runtime/` |
| “재사용할 검증된 사실인가?” | Durable knowledge | `memory/workspace/.../knowledge/` |
| “사용자 고유 선호인가?” | User memory | `memory/preference/`, `memory/identity/` |

```text
observation ≠ durable memory
observation → proposal → review → accept/edit/reject
```

## Runtime Compilation

Run package에 포함되는 핵심:

- selected model
- composed prompt
- selected tools
- MCP payload
- recalled memory
- checksum

검증 공식:

```text
compiled tools ⊆ explicitly intended capabilities
recalled memory ⊆ allowed scope ∩ relevant context
```

## Capability Sources

- browser tools
- Runtime tools: todo, scratchpad, web search, cronjob, image generation, report 등
- Skills와 Commands
- local/remote MCP servers
- App-provided MCP tools

> [!danger] Allowlist
> empty MCP allowlist가 “deny all”이라고 추정하지 않는다. enabled server의 모든 discovered tool을 expose할 수 있으므로 명시적인 `server.tool` allowlist를 사용하고 compiled package를 확인한다.

## App vs Skill vs Template vs Automation

| 항목 | 한 문장 |
|---|---|
| App | UI, MCP, state, background job, integration을 소유하는 runtime capability |
| Skill | agent가 필요할 때 읽는 instruction pack |
| Template | Apps, Skills, files, onboarding을 묶은 workspace scaffold |
| Automation | cron/event로 workspace task를 시작하는 trigger |

## Provider Locality

| 선택 | 의미 |
|---|---|
| Cloud provider | 관련 context가 provider로 전송될 수 있음 |
| Ollama | fully local inference 가능, model/hardware 운영 필요 |
| local-first | workspace/state 중심 표현이며 local inference 보장은 아님 |

문서상 provider path: holaOS Proxy, OpenAI, Anthropic, OpenRouter, Gemini, Ollama, MiniMax.

## Safety Checklist

- [ ] MCP tool을 task별 최소 allowlist로 제한
- [ ] secret을 workspace/Git/prompt/log에 저장하지 않음
- [ ] App manifest와 실제 process 권한 비교
- [ ] signed grant의 scope, audience, expiry 확인
- [ ] write/send/pay/publish 전에 exact preview와 approval
- [ ] retry에 idempotency key와 hard limit 적용
- [ ] memory proposal의 source, scope, expiry 검토
- [ ] stop/resume, timeout, approval cancel failure drill 수행

## Adoption Red Flags

- target platform 설치 경로를 검증하지 않음
- `pi` 외 harness가 완성됐다고 가정
- local-first를 fully local inference로 해석
- approval UI만으로 custom App/MCP가 안전하다고 판단
- 객관적 benchmark 없이 장기 안정성을 전제
- Modified Apache 2.0을 표준 Apache-2.0으로 간주

## License Reminder

```text
Internal single-organization use → dossier 기준 commercial license 없이 허용
Third-party SaaS/managed service/embedded product → 별도 commercial license 검토
```

법률 자문이 아니며 배포 전 최신 `LICENSE` 원문을 확인한다.

## Sources

- Product overview: https://www.holaos.ai/docs/getting-started
- Quick Start: https://www.holaos.ai/docs/getting-started/quick-start
- Workspace Model: https://www.holaos.ai/docs/concepts/workspace-model
- Memory: https://www.holaos.ai/docs/concepts/memory-and-continuity
- Runtime Tools: https://www.holaos.ai/docs/concepts/agent-harness/runtime-tools
- Run Compilation: https://www.holaos.ai/docs/contribute/runtime/run-compilation
- App Anatomy: https://www.holaos.ai/docs/build/apps/app-anatomy
- Repository: https://github.com/holaboss-ai/holaOS
- Installer: https://github.com/holaboss-ai/holaOS/blob/main/INSTALL.md
- License: https://github.com/holaboss-ai/holaOS/blob/main/LICENSE
