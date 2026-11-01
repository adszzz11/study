---
date: 2026-11-01
tags: [tech]
type: tech-tool-study
status: draft
---

# Agent Skills Ecosystem

## 방식 비교

| 방식 | 적합한 용도 | 장점 | 한계 |
|---|---|---|---|
| Agent Skills | 조건부·반복 전문 workflow | on-demand loading, scripts/resources 포함, 재사용성 | routing description과 보안 검토가 중요 |
| `AGENTS.md` / custom instructions | 모든 작업에 적용할 repo 규칙 | 단순하고 일관된 baseline | 커지면 context bloat, task별 분리 어려움 |
| Prompt template | 일회성 또는 사람이 직접 고르는 작업 | 가장 빠르게 시작 가능 | 자동 선택·versioned assets·실행 검증 약함 |
| MCP | 외부 시스템의 tools/data 연결 | Slack, DB, GitHub 등 live capability 제공 | 업무 절차 자체를 잘 정의하지는 않음 |
| GitHub Copilot Agent Skills | GitHub/VS Code 중심 개발팀 | Copilot cloud agent·CLI·code review와 연결 | Copilot 환경과 경로 규약에 의존 |
| OpenAI Codex Skills | Codex/Responses·Agents API workflow | hosted 또는 local execution, open format 호환 | sandbox capability directory 및 배포 모델 이해 필요 |

## 플랫폼 관점

Claude, OpenAI Codex/Agents API, GitHub Copilot은 모두 `SKILL.md` 기반의 on-demand capability 구조로 수렴하고 있다. 그러나 다음은 제품별로 다를 수 있다.

- discovery directory와 repository-local/global precedence
- sandbox에서 허용되는 filesystem·network·shell 권한
- hosted bundle과 local package의 배포·versioning 방식
- Skill이 호출할 수 있는 tools와 secret handling

따라서 포맷이 유사해도, 각 runtime에서 **발견·권한·실행·배포**를 별도로 검증해야 한다.

## 선택 가이드

| 질문 | 권장 출발점 |
|---|---|
| 항상 지켜야 하는 규칙인가? | `AGENTS.md` |
| 반복되는 전문 절차인가? | Agent Skill |
| 외부 시스템을 읽거나 조작해야 하는가? | MCP + 필요한 경우 Skill |
| 사람이 즉시 한 번 실행할 문안인가? | Prompt template |

## Related Notes

- [[tech/ai/agent-skills-ecosystem/README|Agent Skills README]]
- [[tech/ai/agent-skills-ecosystem/01-overview|Overview]]
- [[tech/ai/agent-skills-ecosystem/04-learning/02-deep-dive|Deep Dive]]

## Sources

- https://docs.github.com/en/copilot/concepts/customizations/agent-skills
- https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/add-skills
- https://developers.openai.com/api/docs/guides/tools-skills
