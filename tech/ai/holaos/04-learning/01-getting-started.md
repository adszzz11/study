---
date: 2026-08-17
tags: [tech]
type: tech-tool-study
status: draft
---

# holaOS Getting Started

> [[../README|목차로 돌아가기]] | [[02-deep-dive|다음: Deep Dive]]

## Goal

첫 실습의 목표는 많은 App을 연결하는 것이 아니라, **한 workspace의 authored contract와 runtime state가 분리되는지** 확인하는 것이다.

- use case 하나를 정의한다.
- 최소 권한의 workspace contract를 만든다.
- run이 끝난 뒤 continuity가 남는지 확인한다.
- model/provider와 MCP exposure를 기록한다.
- side effect 없이 stop/resume을 검증한다.

## 0. Preflight

### Platform

| 확인 | 기준 |
|---|---|
| Signed Desktop | Quick Start 기준 macOS Apple Silicon 우선 |
| Source install | macOS, Linux, WSL 절차는 최신 `INSTALL.md` 확인 |
| Windows | build path 존재와 polished installer 제공을 구분 |
| Version | manifest/release에서 현재 version 재확인 |

```bash
# repository와 설치 문서를 로컬에서 검토할 때의 출발점
git clone https://github.com/holaboss-ai/holaOS.git
cd holaOS

# 실행 전에 현재 branch의 안내와 license를 먼저 읽는다.
sed -n '1,240p' INSTALL.md
sed -n '1,240p' LICENSE
```

설치 command와 dependency는 빠르게 변할 수 있으므로 이 노트에 고정하지 않는다. **현재 checkout의 `INSTALL.md`를 그대로 따른다.**

### Data and Provider

- [ ] cloud provider로 보낼 수 있는 data 범위를 정했다.
- [ ] fully local inference가 필요하면 Ollama와 hardware 요구사항을 확인했다.
- [ ] API key를 workspace file이나 Git에 직접 넣지 않는다.
- [ ] test workspace에는 production credential을 연결하지 않는다.
- [ ] backup/export할 대상과 runtime-managed state를 구분했다.

## 1. Pick One Workspace

좋은 첫 use case는 **read-heavy, reversible, observable**하다.

예: “일주일 동안 특정 주제를 조사하고, 매 session의 결정과 다음 질문을 이어가는 research workspace”

| 항목 | 첫 실습 값 예시 |
|---|---|
| Goal | 공식 자료를 읽고 근거가 있는 research brief 작성 |
| Input | 공개 URL과 local notes |
| Output | Markdown report |
| Side effect | 없음 |
| Memory | source facts와 다음 session의 blocker |
| Tool | browser/search 또는 read-only MCP만 |

## 2. Draft the Authored Contract

아래는 개념적 skeleton이다. 실제 schema와 field name은 현재 Workspace Model 문서와 생성된 sample을 기준으로 맞춘다.

```text
research-workspace/
├── workspace.yaml
├── AGENTS.md
├── ONBOARD.md
├── skills/
│   └── source-review/
│       └── SKILL.md
├── apps/
└── .git/
```

### `AGENTS.md` 예시

```markdown
# Research Policy

- Prefer primary sources.
- Record source URLs next to factual claims.
- Separate verified facts, inference, and open questions.
- Ask for approval before any external write or message.
- Never store secrets or transient observations as durable knowledge.
```

### `workspace.yaml` 설계 메모

```yaml
# Conceptual example only; verify the current schema first.
agent: pi
model: <chosen-provider-and-model>

mcp_registry:
  # Start with no server, then add one read-only server.
  # Use an explicit server.tool allowlist when supported.
```

> [!important] Schema 확인
> 이 예시는 책임 경계를 설명하기 위한 pseudo-config다. 그대로 실행 가능한 최신 schema라고 가정하지 않는다.

## 3. First Run

첫 run에서는 다음 순서로 관찰한다.

1. Desktop에서 새 workspace를 열거나 공식 onboarding flow로 생성한다.
2. 선택된 provider/model과 harness를 기록한다.
3. agent에게 goal, output format, source policy를 확인하게 한다.
4. 공개 source 하나를 읽고 짧은 summary를 만들게 한다.
5. “다음 session에 이어갈 blocker와 next action”을 명시하게 한다.
6. workspace를 중지하고 다시 열어 continuity가 복원되는지 확인한다.

### Observation Log

```markdown
## Run 1

- Model/provider:
- Harness:
- Exposed tools:
- Recalled memory:
- Output:
- Blocker:
- Next action:
- Unexpected side effect:
```

## 4. Add One Capability

첫 continuity 확인 후 read-only MCP server 또는 App 하나만 추가한다.

| 단계 | 확인할 것 |
|---|---|
| Enable | server/App가 어느 workspace에만 활성화되는가? |
| Discovery | 발견된 tool 목록은 무엇인가? |
| Allowlist | `server.tool` 단위로 명시했는가? |
| Compile | 실제 run package에 어떤 tool이 포함됐는가? |
| Execute | read-only call의 input/output이 예상 범위인가? |
| Disable | 제거 후 다음 run에서 capability가 사라지는가? |

empty allowlist가 all-tools exposure로 해석될 수 있으므로 명시적인 least-privilege 목록을 우선한다.

## 5. Test Continuity, Not Just Memory

다음 세 가지를 일부러 다르게 적어본다.

- **Policy**: “항상 primary source를 우선한다.” → `AGENTS.md`
- **Knowledge**: “공식 문서상 signed Desktop은 macOS Apple Silicon 중심이다.” → durable knowledge 후보
- **Continuity**: “다음 run에서 Linux installer를 검증한다.” → resume snapshot

재시작 후 policy는 항상 적용되고, fact는 필요할 때 recall되며, next action은 최근 진행 상태로 복원되는지 본다. transient 관찰이 user preference로 자동 승격되지 않는지도 확인한다.

## Troubleshooting

| 증상 | 가능한 원인 | 확인 |
|---|---|---|
| 이전 진행이 복원되지 않음 | session binding 또는 continuity write 실패 | Runtime state와 workspace binding 확인 |
| 예상 밖 tool이 보임 | empty allowlist/default discovery | `mcp_registry`, enabled server, compiled package 확인 |
| App가 start되지 않음 | setup/start command, port, health check 실패 | `app.runtime.yaml`과 Runtime log 확인 |
| 다른 model이 실행됨 | routing/default/credential 문제 | selected model과 compiled package 비교 |
| local-first인데 network 전송 발생 | cloud provider 또는 remote MCP 사용 | provider, proxy, MCP endpoint 목록 확인 |
| 승인 없이 side effect 우려 | custom tool manifest/implementation 문제 | production credential 제거 후 sandbox test |

## Completion Checklist

- [ ] 한 workspace와 한 use case만 사용했다.
- [ ] authored policy와 runtime state를 구분했다.
- [ ] provider, harness, exposed tools를 기록했다.
- [ ] stop/resume 후 blocker와 next action을 복원했다.
- [ ] read-only capability 하나를 explicit allowlist로 제한했다.
- [ ] credential이 file, prompt, log, Git에 남지 않았다.
- [ ] 삭제/rollback/backup 방법을 확인했다.

## Sources

- https://www.holaos.ai/docs/getting-started/quick-start
- https://github.com/holaboss-ai/holaOS/blob/main/INSTALL.md
- https://www.holaos.ai/docs/concepts/workspace-model
- https://www.holaos.ai/docs/concepts/memory-and-continuity
- https://www.holaos.ai/docs/concepts/agent-harness/runtime-tools

