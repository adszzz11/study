---
date: 2026-06-17
tags:
  - tech
  - ai
  - ouroboros
  - cheatsheet
  - hermes
status: learning
type: tech-tool-study
---

# Cheatsheet — Ouroboros

## 한 줄

`Ouroboros = vague prompt를 executable Seed spec으로 바꾸고, agent runtime 실행과 evaluation gate를 통제하는 spec-first Agent OS/workflow engine`

## 핵심 명령

```bash
pipx install 'ouroboros-ai[all]'
ouroboros setup
ouroboros init "Build a local-first task management CLI"
ouroboros run seed.yaml
```

Hermes runtime:

```bash
hermes
hermes model
ouroboros setup --runtime hermes
ouroboros run seed.yaml --runtime hermes
```

## Mental model

| 용어 | 의미 |
|---|---|
| coding agent | executor. repo read/edit/run/test 담당 |
| Ouroboros | requirements/spec/evaluation control plane |
| MCP | external tool/context protocol |
| Seed | workflow constitution |
| Ambiguity Score | 실행 가능한 수준인지 판단하는 clarity gate |
| Double Diamond | Discover -> Define -> Design -> Deliver |
| Event sourcing | append-only event log로 resume/audit/replay |

## Seed에 꼭 들어갈 것

```yaml
goal: ""
constraints: []
acceptance_criteria: []
ontology: {}
exit_conditions: []
```

좋은 acceptance criteria:

- 관찰 가능하다.
- test 또는 command로 확인 가능하다.
- non-goal과 충돌하지 않는다.
- "깔끔하게", "좋게" 같은 주관어를 피한다.

## Ambiguity 낮추는 질문

- 사용자는 누구인가?
- 가장 중요한 workflow는 무엇인가?
- 하지 않을 것은 무엇인가?
- 기술/보안/운영 constraint는 무엇인가?
- 완료 여부를 어떻게 검증할 것인가?
- 실패하면 안 되는 edge case는 무엇인가?

## Evaluation pipeline

| 단계 | 예 |
|---|---|
| Mechanical checks | lint, format, build, test, static analysis |
| Semantic verification | acceptance criteria별 실제 동작 확인 |
| Multi-model consensus | high-risk change를 여러 model/runtime 관점으로 검토 |

## 도구 비교 한 줄

| 도구 | 한 줄 |
|---|---|
| Ouroboros | spec-first workflow/evaluation layer |
| Hermes | self-improving personal/infra agent |
| Claude Code | Anthropic coding runtime |
| Codex CLI | OpenAI terminal coding agent |
| Gemini CLI | large-context open-source terminal agent |
| OpenCode | provider-agnostic open coding agent |
| MCP | tool/context integration protocol |

## 언제 Ouroboros를 쓰나

- 요구사항이 vague할 때
- acceptance criteria가 중요한 작업
- 여러 runtime/agent를 비교하고 싶을 때
- execution history를 replay/audit해야 할 때
- Hermes 같은 personal agent에 더 엄격한 spec gate를 붙이고 싶을 때

## 관련 노트

- [[README]] - 시리즈 시작
- [[01-overview]] - What/Why/architecture
- [[02-ecosystem]] - Hermes와 agent runtime 비교
- [[study/tech/ai/model-context-protocol-mcp]] - MCP
- [[study/tech/ai/codex]] - Codex CLI
- [[study/tech/ai/lazy-codex]] - verification harness 관점
