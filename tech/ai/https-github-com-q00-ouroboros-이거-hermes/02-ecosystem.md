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

## 추가 조사: agent 서비스 지형

조사일: 2026-06-18

사용자 의견의 "이런 느낌의 agent 서비스"는 크게 두 부류로 나뉜다.

| 카테고리 | 대표 서비스 | 기본 입력 | 산출물 | Ouroboros 관점 |
|---|---|---|---|---|
| Async coding agent | Devin, Google Jules, GitHub Copilot coding agent, OpenAI Codex cloud, Factory Droid | issue, ticket, repo task, PR comment | branch, diff, draft PR, test log | Seed/acceptance criteria를 먼저 만들면 agent에게 넘길 ticket 품질이 올라감 |
| Local/IDE agent | Claude Code, Codex CLI, Cursor Agent, Windsurf/Devin in IDE, Factory Droid CLI | local prompt, editor selection, terminal task | working tree patch, command transcript | runtime adapter 후보. approval, sandbox, tool permission 차이가 중요 |
| Prompt-to-app / app builder | Replit Agent, Lovable, Bolt, Firebase Studio | product idea, screenshot, Figma, natural language | full-stack app, preview, deploy, GitHub sync | "앱 전체"를 만들수록 spec gate와 보안/데이터 모델 검증이 더 중요 |
| SDLC automation platform | Factory Software Factory, Devin automations, Copilot agents panel | backlog, signals, CI, incident, review queue | triage, codegen, validation, release/docs automation | Ouroboros의 event/replay/evaluation layer와 가장 가까운 운영형 확장 방향 |

### 서비스별 메모

| 서비스 | 포지션 | 주목 기능 | 리스크/검증 포인트 |
|---|---|---|---|
| Devin | autonomous AI software engineer | web/CLI/Desktop/API, cloud sessions, embedded IDE/browser/shell, Linear/Jira/Slack/GitHub workflow, parallel backlog 처리 | docs 자체도 "clear prompts, explicit completion criteria, easy verification"를 강조. 즉 Ouroboros식 Seed가 직접 보완재 |
| Google Jules | async GitHub coding agent | repo/branch 선택, issue에 `jules` label로 task assign, Cloud VM에서 plan 생성, diff 확인 후 PR 생성 | plan 승인, PR diff review, concurrent task quota를 기준으로 운영해야 함 |
| OpenAI Codex cloud | cloud coding agent | cloud environment에서 background/parallel task 실행, IDE/GitHub delegation, 환경 설정과 internet access control | local CLI보다 장기/병렬 작업에 유리하지만 env setup, secrets, network policy가 중요 |
| GitHub Copilot coding agent | GitHub-native agent | issue/task assign, GitHub Actions 기반 cloud env, draft PR, review comment 응답, agents panel | GitHub issue 품질이 성패를 좌우. issue template을 Seed-like하게 만드는 것이 효과적 |
| Factory Droid | agent-native SDLC platform | Droid CLI/App/Exec, custom Droids, skills, hooks, MCP, Droid Computers, readiness, code review/QA/security review | 단순 coding agent보다 팀 SDLC 자동화 플랫폼. governance/observability/on-prem 요구에 맞음 |
| Replit Agent | browser IDE + app builder | natural language로 code, infra, tests, deploy; Plan mode; checkpoints/rollback; Lite/Economy/Power modes | 비개발자 접근성이 강함. database/auth/secret 권한과 rollback/checkpoint 정책 확인 필요 |
| Lovable | full-stack AI development platform | frontend/backend/db/auth/integration 생성, GitHub sync, workspace collaboration, enterprise governance | prompt-to-app 계열. 생성 코드 ownership은 장점이나 Supabase/RLS 같은 backend access control 검증 필수 |
| Bolt | AI app/site builder | Plan/Build, Figma/GitHub import, design system, model routing, Bolt Cloud hosting/db/auth | UI/prototype 속도가 장점. "production" claim은 test, auth, data model, deploy boundary로 검증 |
| Firebase Studio | Google cloud browser IDE/app prototyping | Gemini App Prototyping agent, Firebase Auth/Firestore setup, Code OSS 기반 VM, preview/publish | 현재 문서상 2027-03-22 sunset 예정. 신규 장기 도입보다 migration 대상/비교군으로 보는 편이 안전 |
| Cursor Agent | IDE-native agent | codebase indexing, natural language code changes, agentic PR/commit traces가 연구 데이터에 등장 | editor UX는 강하지만 team-level audit/replay는 별도 정책 필요 |

### Ouroboros와 연결되는 관찰

- **Issue readiness가 핵심 병목**: 최근 agentic PR 연구들은 agent 성공률이 task/issue 품질, scope, relevant artifact hint, validation instruction에 민감하다고 본다. 이는 Ouroboros의 `Seed`와 `Ambiguity gate`가 해결하려는 문제와 거의 같다.
- **서비스들이 plan mode를 흡수 중**: Replit/Bolt/Jules/Devin 모두 실행 전 plan, task list, approval, review loop를 제품 기능으로 넣고 있다. Ouroboros는 이 흐름을 vendor-neutral하게 추상화할 수 있다.
- **prompt-to-app은 더 높은 검증이 필요**: 앱 생성 서비스는 frontend뿐 아니라 auth, database, storage, deployment까지 만들기 때문에 `acceptance_criteria`에 security rule, data access, rollback, observability를 포함해야 한다.
- **운영형 agent는 event/audit가 경쟁 축**: Factory, Devin, Codex cloud, Copilot coding agent는 background/parallel work를 강조한다. 병렬성이 늘수록 "누가 왜 무엇을 바꿨는가"를 남기는 event sourcing/replay가 중요해진다.

### Seed-like issue template

GitHub Copilot coding agent, Devin, Jules, Codex cloud 같은 async agent에게 넘길 issue는 다음 형태가 유리하다.

```md
## Goal
- 

## Non-goals
- 

## Context
- Relevant files:
- Related issue/PR:
- External docs:

## Constraints
- Runtime/env:
- Security/data:
- Backward compatibility:

## Acceptance Criteria
- [ ] Mechanical:
- [ ] Semantic:
- [ ] UX/API:

## Validation
- Commands:
- Manual smoke test:
- CI expectations:

## Handoff Notes
- Rollback plan:
- Reviewer focus:
```
