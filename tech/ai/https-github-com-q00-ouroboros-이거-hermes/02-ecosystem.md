---
date: 2026-06-17
tags:
  - tech
  - ai
  - ouroboros
  - hermes
  - comparison
  - coding-agent
status: learning
type: tech-tool-study
---

# 02. Ecosystem — 비교

## 포지션 맵

Ouroboros는 "또 하나의 coding agent"라기보다 agent들을 통제하는 **orchestration/spec layer**에 가깝다.

```text
User vague intent
  -> Ouroboros interview/spec/evaluation
  -> Claude Code / Codex CLI / Hermes / Gemini CLI / OpenCode
  -> repo changes + tests + audit trail
```

## 도구 비교

| 도구 | 포지션 | 강점 | Ouroboros와의 관계 |
|---|---|---|---|
| **Ouroboros** | Spec-first Agent OS/workflow layer | interview, Seed, replayable ledger, evaluation gate, multi-runtime adapter | coding agent 자체라기보다 agent들을 통제하는 orchestration/spec layer |
| **Hermes Agent** | Self-improving personal/infra agent | memory, skills creation, messaging gateway, cron, subagents, terminal backends, "agent that grows with you" | Ouroboros가 Hermes runtime 위에 올라갈 수 있음. Hermes는 broader personal agent, Ouroboros는 spec-first coding workflow에 더 집중 |
| **Claude Code** | Anthropic agentic coding tool | codebase read/edit/run, git/PR, MCP, skills/hooks, multiple agents | Ouroboros의 주요 backend 후보. Claude Code는 실행자, Ouroboros는 요구사항과 evaluation control layer |
| **Codex CLI** | OpenAI terminal coding agent | local repo inspect/edit/run, Rust CLI, subagents, web search, MCP, approval modes | Ouroboros의 backend 후보. Codex CLI는 terminal execution surface |
| **Gemini CLI** | Google open-source terminal AI agent | free tier, 1M context, Google Search grounding, file/shell/web tools, MCP | Ouroboros의 backend 후보. large-context exploration에 유리 |
| **OpenCode** | Open-source AI coding agent | terminal, desktop, IDE extension, provider-agnostic, AGENTS.md | Ouroboros가 runtime으로 지원. 오픈 생태계와 provider flexibility가 장점 |
| **GitHub Copilot Agent/HQ** | GitHub-native agent ecosystem | issue/PR workflow, GitHub platform integration, Claude/Codex/Gemini agent routing | repo workflow에는 강하지만 local spec-first loop는 Ouroboros가 더 직접적 |

## Hermes와 비교

| 축 | Ouroboros | Hermes Agent |
|---|---|---|
| 핵심 정체성 | spec-first workflow engine | self-improving personal/infra agent |
| 주요 질문 | "이 작업의 executable spec은 무엇인가?" | "나를 위해 계속 학습하고 실행하는 agent를 어떻게 운영할까?" |
| 실행 방식 | Seed -> runtime execution -> evaluation gate | memory, skills, gateways, cron, subagents, terminal backend |
| 강점 | ambiguity reduction, acceptance criteria, replayability | 지속 운영, 개인화, infra integration |
| 결합 방식 | Hermes를 backend runtime으로 선택 | Ouroboros의 spec/evaluation discipline을 runtime으로 실행 |

### 같이 쓰는 mental model

- Hermes는 "항상 켜진 개인/운영 agent"에 가깝다.
- Ouroboros는 "작업 하나를 모호하지 않은 spec과 평가 가능한 contract로 만드는 engine"에 가깝다.
- 둘을 결합하면 Hermes의 운영/메모리/자동화 능력 위에 Ouroboros의 spec-first gate를 얹는 구조가 된다.

## Claude Code / Codex CLI와 비교

| 축 | Claude Code / Codex CLI | Ouroboros |
|---|---|---|
| 기본 단위 | prompt, command, task | Seed, workflow, evaluation contract |
| 강점 | repo 탐색, edit, command, test, PR | ambiguity 제거, spec crystallization, replayable execution |
| 실패 패턴 | 모호한 지시를 추측해서 구현 | clarity 부족 시 execution 이전에 멈춤 |
| 확장 지점 | MCP, skills, hooks, subagents | plugins, runtime adapters, event store |

[[study/tech/ai/codex]]나 [[study/tech/ai/claude]]를 이미 쓰고 있다면 Ouroboros는 "더 좋은 agent"보다 "agent에게 넘길 작업을 더 좋은 contract로 만드는 layer"로 이해하는 편이 정확하다.

## MCP와의 관계

MCP(Model Context Protocol)는 AI app이 local files, databases, search, workflows 같은 external tools와 context에 표준 방식으로 연결되게 하는 open protocol이다.

| 계층 | 예 |
|---|---|
| Context/tool protocol | [[study/tech/ai/model-context-protocol-mcp]] |
| Agent runtime | Claude Code, Codex CLI, Gemini CLI, OpenCode, Hermes |
| Spec/evaluation workflow | Ouroboros |

Ouroboros가 MCP를 쓰면 spec-first workflow 안에서 external data, internal API, search, issue tracker, deployment checks 같은 tool을 runtime-agnostic하게 연결할 수 있다.

## 선택 기준

| 원하는 것 | 우선 볼 도구 |
|---|---|
| local repo에서 바로 코딩 agent 실행 | Codex CLI, Claude Code, Gemini CLI, OpenCode |
| 개인 agent 인프라와 장기 memory | Hermes Agent |
| GitHub issue/PR 중심 workflow | GitHub Copilot Agent/HQ |
| external tool/context 표준 연결 | MCP |
| 요구사항 명확화, Seed, acceptance/evaluation gate | Ouroboros |

## 결론

Ouroboros는 Hermes와 "비슷한 급의 agent"라기보다, Hermes 같은 agent runtime을 **더 안전하게 일하게 만드는 specification-first operating layer**로 보는 편이 좋다.

→ 다음: [[03-references]] · 실습: [[04-learning/01-getting-started]]
