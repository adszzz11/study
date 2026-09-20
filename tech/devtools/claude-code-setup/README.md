---
date: 2026-09-20
tags: [tech]
type: tech-tool-study
status: draft
---

# Claude Code Setup

> **한 줄 정의**: Claude Code는 repository를 읽고, 파일을 수정하고, shell command와 test를 실행하며, Git·IDE·CI/CD·MCP와 연결되는 Anthropic의 agentic coding environment다.

## Overview

Claude Code setup은 CLI 설치만을 뜻하지 않는다. 안전하고 재현 가능한 개발 workflow를 만들려면 다음 네 층을 함께 설계해야 한다.

| 층 | 핵심 질문 | 대표 구성 |
|---|---|---|
| Runtime | 어디서 실행할까? | CLI, VS Code, JetBrains, Desktop, Web, CI/CD |
| Context | 무엇을 알려줄까? | `CLAUDE.md`, `AGENTS.md`, rules, skills |
| Authority | 무엇을 허용할까? | permissions, sandbox, hooks |
| Integration | 무엇과 연결할까? | MCP, plugins, GitHub Actions, cloud provider |

```text
Goal → Explore → Plan → Read/Edit/Bash/MCP → Build/Test → Observe → Iterate → Review
```

일반 chat assistant와 달리 Claude Code는 tool 실행 결과를 다음 reasoning step에 다시 넣어 여러 파일에 걸친 작업을 반복한다. 좋은 setup의 목표는 권한을 무작정 넓히는 것이 아니라, 필요한 context와 검증 명령을 제공하면서 위험한 동작은 좁게 통제하는 것이다.

> [!note] 조사 기준
> 이 노트는 2026-09-20의 공식 문서를 기준으로 한다. 설치 방식, permission mode, 지원 interface는 빠르게 바뀔 수 있으므로 실제 적용 전 공식 문서를 다시 확인한다.

## Learning Path

- [ ] [[01-overview|1. Overview]] — What/Why, agentic loop, setup의 네 층
- [ ] [[02-ecosystem|2. Ecosystem]] — Codex CLI, Gemini CLI, Cursor, GitHub Copilot과 비교
- [ ] [[03-references|3. References]] — 공식 문서 지도와 확인 순서
- [ ] [[04-learning/01-getting-started|4. Getting Started]] — 설치, 인증, 첫 session, 최소 project context
- [ ] [[04-learning/02-deep-dive|5. Deep Dive]] — memory, settings, permissions, sandbox, hooks, MCP
- [ ] [[05-projects|6. Projects]] — 개인·팀·CI setup 실습
- [ ] [[cheatsheet|7. Cheatsheet]] — 명령, 경로, 안전 점검 빠른 참조

## When To Use

- repository 전체를 탐색하고 여러 파일을 수정한 뒤 test까지 실행해야 할 때
- bug fix, refactoring, migration처럼 탐색과 반복 검증이 필요한 작업
- 팀의 build/test/architecture 규칙을 `CLAUDE.md`와 shared settings로 재현하고 싶을 때
- GitHub Actions, GitLab CI/CD 또는 MCP를 통해 issue·PR·외부 tool workflow를 자동화할 때
- CLI뿐 아니라 IDE, Desktop, Web을 오가며 같은 project context를 활용할 때

## When Not To Use

- 한 줄 completion처럼 IDE inline suggestion이 더 빠른 작업
- source code나 prompt가 외부 model provider로 전송되면 안 되는 환경
- sandbox와 permission policy 없이 credential이 많은 workstation에서 unattended task를 실행할 때
- 요구사항이나 acceptance criteria가 없고 결과 검증 방법도 정의할 수 없을 때
- deterministic script나 formatter로 충분한 반복 작업을 굳이 LLM에 맡길 때

## Related Notes

- [[MOCs/Index]]
- [[MOCs/Devtools]]
- [[../ripgrep/README|ripgrep]] — Claude Code의 repository search와 함께 이해할 도구
- [[01-overview|Claude Code Overview]]
- [[cheatsheet|Claude Code Setup Cheatsheet]]

## Sources

- [Claude Code Quickstart](https://code.claude.com/docs/en/quickstart)
- [Claude Code Advanced setup](https://code.claude.com/docs/en/setup)
- [Claude Code GitHub repository](https://github.com/anthropics/claude-code)
- [How Claude remembers your project](https://code.claude.com/docs/en/memory)
- [Settings files and precedence](https://code.claude.com/docs/en/settings)
- [Configure permissions](https://code.claude.com/docs/en/permissions)
- [Configure the sandboxed Bash tool](https://code.claude.com/docs/en/sandboxing)

