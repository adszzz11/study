---
date: 2026-11-01
tags: [tech]
type: tech-tool-study
status: draft
---

# OpenAI Codex Ecosystem

[[tech/devtools/openai-codex-agent/README|OpenAI Codex 학습 노트]]의 도구 비교다. 어느 도구가 “최고”인지보다 team의 repository, hosting, model policy, review 흐름에 맞는지를 본다.

| 도구 | 강점·적합한 상황 | Codex와의 차이 |
|---|---|---|
| OpenAI Codex | terminal-first, OpenAI model·ChatGPT·SDK·MCP 통합, local/cloud 연속 작업 | core CLI가 공개되어 있고 app·CLI·SDK를 함께 제공 |
| GitHub Copilot | GitHub Issue·PR·Actions 및 enterprise GitHub workflow | GitHub-native cloud delegation과 PR lifecycle에 특히 강함 |
| Cursor Agent | editor-centric UX, 다중 model 선택, UI/browser 반복 작업 | Cursor IDE 중심의 통합 개발환경에 더 무게 |
| Claude Code | terminal 중심 codebase 작업과 Claude ecosystem | model·권한 정책·SDK 생태계가 Anthropic 중심 |
| Aider | 가볍고 Git-friendly한 terminal pair programming | 상대적으로 단순하며 model provider 선택 폭이 넓음 |

## 선택 기준

- **terminal과 codebase policy 우선**: CLI, `AGENTS.md`, sandbox를 중심으로 표준화하려면 Codex가 자연스럽다.
- **GitHub lifecycle 우선**: issue에서 PR merge까지 GitHub-native automation이 핵심이면 Copilot의 연결성을 평가한다.
- **editor UX 우선**: visual editing과 editor 안의 빠른 loop가 팀의 중심이라면 Cursor를 함께 비교한다.
- **provider portability 우선**: 특정 model vendor 종속을 줄여야 하면 Aider 같은 provider-agnostic 도구도 후보다.

## Codex 내부 확장 지형

| 표면 | 역할 | 검토할 경계 |
|---|---|---|
| CLI / TUI | local interactive agent | shell·filesystem approval |
| `codex exec` | headless CI/automation | non-interactive 권한과 log 노출 |
| IDE / cloud | editor·remote 작업 연속성 | repository와 account access |
| MCP / plugins / Skills | 외부 context·도구 연결 | tool별 OAuth, write scope, prompt injection |
| TypeScript / Python SDK | application integration | thread lifecycle, service account, JSON-RPC boundary |

다음 단계는 [[tech/devtools/openai-codex-agent/04-learning/02-deep-dive|Deep Dive]]에서 integration permission을 구체화하는 것이다.

## Sources

- https://docs.github.com/en/copilot/concepts/agent-capabilities/about-agents/about-github-copilot-agents
- https://cursor.com/docs/agent/overview
- https://github.com/openai/codex
- https://learn.chatgpt.com/docs/codex-sdk
