---
date: 2026-06-17
tags:
  - tech
  - ai
  - ouroboros
  - references
  - coding-agent
status: learning
type: tech-tool-study
---

# 03. References

## Ouroboros 공식 / 소스

| 자료 | URL | 볼 것 |
|---|---|---|
| Ouroboros GitHub | https://github.com/Q00/ouroboros | project positioning, install, README |
| Ouroboros README raw | https://raw.githubusercontent.com/Q00/ouroboros/main/README.md | "Stop prompting. Start specifying.", Seed, ambiguity, execution contract |
| Ouroboros Architecture | https://raw.githubusercontent.com/Q00/ouroboros/main/docs/architecture.md | Agent OS stack, event sourcing, runtime abstraction |
| Ouroboros CLI Reference | https://raw.githubusercontent.com/Q00/ouroboros/main/docs/cli-reference.md | `setup`, `init`, `run` 같은 CLI command |
| Ouroboros Hermes runtime guide | https://raw.githubusercontent.com/Q00/ouroboros/main/docs/runtime-guides/hermes.md | Hermes backend runtime 연결 방식 |
| Ourocode shell | https://github.com/Q00/ourocode | terminal shell 역할 |
| Ouroboros plugins | https://github.com/Q00/ouroboros-plugins | UserLevel workflows와 plugin 생태계 |

## 비교 대상

| 도구 | URL | 비교 포인트 |
|---|---|---|
| Hermes Agent | https://github.com/NousResearch/hermes-agent | self-improving personal/infra agent, memory, skills, gateway |
| Claude Code docs | https://code.claude.com/docs/en/overview | agentic coding runtime, MCP, skills/hooks |
| Codex CLI docs | https://developers.openai.com/codex/cli | terminal coding agent, repo edit/run/test, approvals |
| Gemini CLI | https://github.com/google-gemini/gemini-cli | open-source terminal AI agent, large context, Google Search grounding |
| OpenCode docs | https://opencode.ai/docs/ | provider-agnostic open coding agent |
| MCP intro | https://modelcontextprotocol.io/docs/getting-started/intro | external tool/context protocol |

## 읽는 순서

1. **Ouroboros README**: 도구의 문제의식과 Seed mental model을 먼저 잡는다.
2. **Architecture**: Agent OS stack, event sourcing, runtime abstraction을 확인한다.
3. **CLI Reference**: 실제 작업 흐름이 `setup -> init -> run`인지 확인한다.
4. **Hermes runtime guide**: "Hermes랑 비슷한가?"보다 "Hermes 위에 어떻게 올라가는가?"를 본다.
5. **MCP intro**: external context/tool integration layer를 분리해서 이해한다.
6. **Claude/Codex/Gemini/OpenCode docs**: Ouroboros가 제어할 executor 후보로 비교한다.

## 검증할 질문

- Ouroboros의 `Seed` schema는 실제로 어느 정도 strict한가?
- `Ambiguity <= 0.2`는 CLI에서 어떻게 계산/노출되는가?
- event store는 어떤 event type을 append-only로 기록하는가?
- Hermes runtime adapter는 command execution만 감싸는가, memory/skill까지 활용하는가?
- multi-model consensus는 기본 기능인가 optional 기능인가?
- MCP integration은 server hosting과 client call 중 어디까지 포함하는가?

## 관련 노트

- [[study/tech/ai/model-context-protocol-mcp]] - MCP spec부터 먼저 이해할 때
- [[study/tech/ai/litellm]] - multi-provider routing과 Ouroboros optional LiteLLM 연결
- [[study/tech/ai/agent-orchestration/cli-agents]] - terminal agent 생태계 비교
- [[study/tech/ai/lazy-codex]] - independent verification과 false completion 방지 관점

→ 다음: [[04-learning/01-getting-started]]

## 추가 조사: agent 서비스 레퍼런스

조사일: 2026-06-18

### Async coding agent / SDLC automation

| 자료 | URL | 볼 것 |
|---|---|---|
| Devin Docs — Introducing Devin | https://docs.devin.ai/get-started/devin-intro | autonomous AI software engineer, web/CLI/Desktop/API, embedded IDE/browser/shell, task suitability |
| Cognition | https://cognition.ai/ | Devin positioning, production code, enterprise deployment, Windsurf/Devin ecosystem |
| Google Jules | https://jules.google/ | GitHub repo/branch task delegation, Cloud VM plan, diff review, PR 생성, concurrency plans |
| OpenAI Codex cloud | https://developers.openai.com/codex/cloud | cloud background tasks, parallel work, IDE/GitHub delegation, environment/internet access control |
| Factory Docs | https://docs.factory.ai/welcome | Droid CLI/App/Exec, Software Factory, readiness, QA/review/security automation, MCP/hooks/skills/custom Droids |
| Factory homepage | https://factory.ai/ | "self-improving system for your SDLC", model independence, sovereign deployment, SDLC-wide automation |
| GitHub Copilot coding agent article | https://www.theverge.com/news/669339/github-ai-coding-agent-fix-bugs | issue/task assign, GitHub Actions cloud env, draft PR, review comments |
| GitHub agents panel article | https://www.itpro.com/software/development/github-just-launched-a-new-mission-control-center-for-developers-to-delegate-tasks-to-ai-coding-agents | GitHub-wide agents panel, natural-language task delegation, task tracking |

### Prompt-to-app / app builder

| 자료 | URL | 볼 것 |
|---|---|---|
| Replit Agent docs | https://docs.replit.com/references/agent/overview | natural language app generation, infra/test/deploy, Plan mode, checkpoints/rollback, Lite/Economy/Power |
| Lovable docs | https://docs.lovable.dev/introduction/welcome | full-stack AI development platform, GitHub sync, workspace, governance, security/compliance |
| Bolt | https://bolt.new/ | chat-based apps/websites, Plan/Build, Figma/GitHub import, design system, Bolt Cloud |
| Bolt Help Center | https://support.bolt.new/ | Plan mode, agent 선택, GitHub/Figma/Supabase/Netlify/MCP integration |
| Firebase Studio docs | https://firebase.google.com/docs/studio | Gemini App Prototyping agent, Firebase Auth/Firestore, Code OSS VM, preview/publish, sunset notice |

### 연구 / 벤치마크

| 자료 | URL | 시사점 |
|---|---|---|
| AIDev: Studying AI Coding Agents on GitHub | https://arxiv.org/abs/2602.09185 | OpenAI Codex, Devin, GitHub Copilot, Cursor, Claude Code의 agentic PR 대규모 데이터셋 |
| Agentic Much? Adoption of Coding Agents on GitHub | https://arxiv.org/abs/2601.18341 | 2025년 상반기 GitHub에서 coding agent adoption이 빠르게 증가했다는 실증 연구 |
| Understanding the Rejection of Fixes Generated by Agentic Pull Requests | https://arxiv.org/abs/2606.13468 | agent fix rejection 원인. 구현 오류, CI/test failure, session loss, low priority 등 |
| What Makes a GitHub Issue Ready for Copilot? | https://arxiv.org/abs/2512.21426 | well-scoped issue, relevant artifact hint, implementation/validation guidance가 merge 가능성을 높임 |
| From Prompt to Product | https://arxiv.org/abs/2512.18080 | Replit/Bolt/Firebase Studio 같은 prompt-to-app system을 usability/trust/visual quality로 비교 |

## 추가 조사: 읽는 순서

1. **Devin / Jules / Codex cloud / Copilot coding agent**: async PR-producing agent가 공통으로 요구하는 issue quality와 review workflow를 본다.
2. **Factory Droid**: 개별 coding task가 아니라 SDLC 전체를 agent-native platform으로 운영하는 방향을 본다.
3. **Replit / Lovable / Bolt / Firebase Studio**: non-developer 또는 product team이 prompt에서 deploy까지 가는 app-builder workflow를 본다.
4. **AIDev / rejection 연구**: 실제 agent PR이 왜 merge되지 않는지 보고 Ouroboros의 `Seed`, `acceptance_criteria`, `validation` 항목으로 되돌린다.

## 추가 조사: 검증 질문

- async agent에게 넘기는 issue가 `Goal`, `Non-goal`, `Constraints`, `Acceptance Criteria`, `Validation`을 포함하는가?
- 생성된 PR이 CI를 통과했는가, 아니면 agent가 "테스트하지 못함"을 명시했는가?
- prompt-to-app 서비스가 만든 auth/database rule을 사람이 재검토할 수 있는가?
- service가 cloud VM/sandbox/secrets/network access를 어떻게 격리하는가?
- background/parallel agent 작업의 audit trail, session log, rollback, reviewer handoff가 남는가?
- 해당 서비스가 MCP, GitHub, Linear/Jira, Slack/Teams, IDE/CLI와 어떻게 연결되는가?
