---
date: 2026-09-20
tags: [tech]
type: tech-tool-study
status: draft
---

# Claude Code Setup — Ecosystem

> [[01-overview|이전: Overview]] · [[README|목차로 돌아가기]] · [[03-references|다음: References]]

## 비교 관점

Agentic coding tool은 model benchmark만으로 선택하기 어렵다. 실제 setup에서는 실행 위치, repository context, authority model, extension 방식, team governance를 함께 비교해야 한다.

> [!warning] 시점 의존성
> 아래 비교는 2026-09-20의 공식 문서 기준 요약이다. plan, model, preview feature와 기본 permission mode는 자주 바뀐다.

## 주요 도구 비교

| 도구 | 중심 경험 | Project context | 실행·격리 | 확장 | 잘 맞는 상황 |
|---|---|---|---|---|---|
| Claude Code | terminal 중심 + IDE/Desktop/Web/CI | `CLAUDE.md`, 조건부 `AGENTS.md`, rules, skills | permissions + OS-level Bash sandbox | MCP, hooks, skills, plugins, subagents | terminal에서 긴 agentic loop와 세밀한 project setup |
| OpenAI Codex | CLI, IDE, app, cloud | `AGENTS.md`, skills | approval policy + workspace sandbox/cloud environment | MCP, skills, automation | local과 cloud task를 오가며 병렬 coding workflow |
| Gemini CLI | open-source terminal agent | `GEMINI.md`, extensions | policy engine + Seatbelt/container/Windows sandbox | MCP, extensions, hooks | Google ecosystem, open-source CLI, 여러 sandbox backend |
| Cursor | AI-first editor/agent | project rules, `AGENTS.md`, skills | editor/agent permission과 sandbox 설정 | MCP, rules, plugins | GUI editor 안에서 code navigation과 agent를 결합 |
| GitHub Copilot cloud agent | GitHub issue → background PR | repository instructions, custom agents | GitHub Actions 기반 ephemeral environment | MCP, hooks, skills | issue delegation과 PR review가 중심인 GitHub workflow |

## Claude Code가 두드러지는 지점

### Runtime surface

하나의 제품군에서 terminal, IDE, Desktop, Web, Slack, CI/CD까지 연결한다. local CLI는 개발 환경과 즉시 맞물리고, GitHub Actions나 Web은 background delegation에 적합하다. 반면 surface마다 읽는 설정과 사용할 수 있는 credential이 같다고 가정하면 안 된다.

### Context hierarchy

organization, user, project, project-local, path-specific, on-demand skill을 구분한다. `CLAUDE.md`는 항상 필요한 짧은 지식에, Skill은 긴 runbook과 반복 절차에 배치할 수 있다.

### Authority 분리

permission rule은 tool invocation을, sandbox는 process가 실제로 닿을 수 있는 OS boundary를 통제한다. 둘은 대체 관계가 아니다. 예를 들어 `Bash(pnpm test *)`를 allow해도 sandbox가 filesystem과 network 범위를 제한할 수 있다.

### Hooks와 MCP

- hooks는 lifecycle event에 deterministic command를 연결한다.
- MCP는 외부 data source와 tool을 model이 호출할 수 있게 한다.
- plugin은 skills, agents, hooks, MCP 구성을 함께 배포할 수 있다.

## 선택 가이드

### Claude Code를 우선할 때

- terminal workflow와 shell/test loop가 개발 방식의 중심이다.
- `CLAUDE.md`, scoped rules, skills로 context를 세분화하고 싶다.
- permission과 Bash sandbox를 별도 layer로 운영하고 싶다.
- 같은 setup을 IDE와 CI/CD까지 확장하려 한다.

### Codex를 고려할 때

- `AGENTS.md` 중심의 cross-tool instruction을 이미 사용한다.
- local CLI/IDE와 hosted cloud task를 함께 운영한다.
- workspace-write sandbox와 approval policy가 workflow에 잘 맞는다.

### Gemini CLI를 고려할 때

- open-source implementation과 Google ecosystem 통합이 중요하다.
- Docker, Podman, Seatbelt, gVisor, LXC 등 여러 sandbox backend가 필요하다.
- TOML policy engine으로 tool rule을 구성하려 한다.

### Cursor를 고려할 때

- terminal보다 editor GUI, inline edit, visual diff review가 중심이다.
- code navigation과 agent interaction을 한 editor 안에서 끝내고 싶다.

### GitHub Copilot cloud agent를 고려할 때

- GitHub issue를 agent에게 배정하고 background에서 PR을 만드는 workflow가 핵심이다.
- repository policy, Actions environment, branch protection이 이미 운영 표준이다.

## 함께 쓰는 전략

도구를 하나만 선택할 필요는 없다. 다만 context file이 서로 복제되어 drift하지 않게 source of truth를 정한다.

```text
AGENTS.md                 # cross-agent 공통 규칙
CLAUDE.md                 # Claude-specific 보충 또는 @AGENTS.md import
.claude/rules/            # path-specific Claude rules
.claude/skills/           # Claude reusable workflows
```

Claude Code의 현재 기본 동작은 working directory 위에 `CLAUDE.md` 또는 `CLAUDE.local.md`가 없을 때 `AGENTS.md`를 fallback으로 읽는다. 둘을 항상 함께 읽게 하려면 지원 버전과 `agents-md` built-in plugin 설정을 확인한다. 일부 third-party provider나 telemetry-disabled session에서는 직접 지원이 없을 수 있으므로 `CLAUDE.md`에서 `@AGENTS.md`를 import하는 방식이 호환성 면에서 안전하다.

## Sources

- [Claude Code Quickstart](https://code.claude.com/docs/en/quickstart)
- [How Claude remembers your project](https://code.claude.com/docs/en/memory)
- [OpenAI Codex CLI](https://developers.openai.com/codex/cli)
- [OpenAI Codex security](https://developers.openai.com/codex/security)
- [Gemini CLI repository](https://github.com/google-gemini/gemini-cli)
- [Gemini CLI sandboxing](https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/sandbox.md)
- [Cursor documentation](https://cursor.com/docs)
- [GitHub Copilot cloud agent](https://docs.github.com/en/copilot/concepts/agents/cloud-agent/about-cloud-agent)

