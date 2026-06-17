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
