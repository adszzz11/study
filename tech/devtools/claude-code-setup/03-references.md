---
date: 2026-09-20
tags: [tech]
type: tech-tool-study
status: draft
---

# Claude Code Setup — References

> [[02-ecosystem|이전: Ecosystem]] · [[README|목차로 돌아가기]] · [[04-learning/01-getting-started|다음: Getting Started]]

## 공식 문서 지도

| 주제 | 먼저 볼 자료 | 확인할 내용 |
|---|---|---|
| 첫 실행 | [Quickstart](https://code.claude.com/docs/en/quickstart) | 설치, login, 기본 명령, 지원 interface |
| 설치/업데이트 | [Advanced setup](https://code.claude.com/docs/en/setup) | OS 요구사항, installer, release channel, uninstall |
| 인증 | [Authentication](https://code.claude.com/docs/en/authentication) | subscription, Console, cloud provider, credential storage |
| Project context | [Memory](https://code.claude.com/docs/en/memory) | `CLAUDE.md`, `AGENTS.md`, imports, rules, `/init`, `/context` |
| Settings | [Settings](https://code.claude.com/docs/en/settings) | scope, precedence, shared/local/managed configuration |
| 권한 | [Permissions](https://code.claude.com/docs/en/permissions) | allow/ask/deny rule과 permission mode |
| 격리 | [Sandboxing](https://code.claude.com/docs/en/sandboxing) | filesystem/network boundary와 fail-closed 설정 |
| 반복 절차 | [Skills](https://code.claude.com/docs/en/skills) | personal/project/nested/plugin skill |
| 자동화 | [Hooks guide](https://code.claude.com/docs/en/hooks-guide) | lifecycle event와 deterministic command |
| 외부 연결 | [MCP](https://code.claude.com/docs/en/mcp) | local/remote server, scope, OAuth, tool search |
| CI/CD | [GitHub Actions](https://code.claude.com/docs/en/github-actions) | `@claude`, workflow, token과 security |
| 명령 참조 | [CLI reference](https://code.claude.com/docs/en/cli-reference) | flags, print mode, resume, settings override |
| 변경 추적 | [Changelog](https://code.claude.com/docs/en/changelog) | breaking change, new permission mode, platform support |

## Source 우선순위

1. 실제 환경의 `claude --version`, `/status`, `/context`, `/permissions`
2. Anthropic 공식 문서와 official GitHub repository
3. schema와 CLI built-in help
4. issue tracker와 community discussion
5. blog, video, third-party tutorial

빠르게 변하는 제품에서는 오래된 tutorial보다 실행 중인 version과 공식 문서를 우선한다. 특히 npm 설치, model 이름, plan별 기능, auto mode, sandbox platform 지원은 날짜를 함께 기록한다.

## 검증용 명령

```bash
claude --version
claude doctor
claude --help
claude mcp list
```

Session 안에서는 다음을 확인한다.

```text
/status       # version, model, account, settings source
/context      # 실제 context 사용량과 memory file
/permissions  # effective permission rules
/sandbox      # sandbox 상태와 설정
/doctor       # runtime health 확인
```

## 읽기 순서

### 처음 시작할 때

1. Quickstart
2. Advanced setup
3. Authentication
4. Memory
5. Permissions

### 팀 baseline을 만들 때

1. Settings and precedence
2. Memory와 rules
3. Permissions
4. Sandboxing
5. Hooks
6. Managed settings

### 외부 system을 연결할 때

1. MCP
2. MCP server의 자체 security 문서
3. Authentication/credential storage
4. Permissions와 managed MCP configuration
5. GitHub Actions 또는 GitLab CI/CD 문서

## 사실 확인 체크포인트

- [ ] 설치 명령이 current official recommendation인가?
- [ ] 사용 중인 release channel과 auto-update 동작을 확인했는가?
- [ ] `AGENTS.md`가 이 version/provider/session에서 실제로 load되는가?
- [ ] project settings와 local settings의 precedence를 `/status`로 확인했는가?
- [ ] sandbox dependency가 없을 때 fail-open인지 fail-closed인지 확인했는가?
- [ ] MCP server가 어떤 credential과 data에 접근하는지 검토했는가?
- [ ] CI token의 repository permission과 branch protection을 최소화했는가?

## Sources

- [Claude Code documentation index](https://code.claude.com/docs/llms.txt)
- [Claude Code GitHub repository](https://github.com/anthropics/claude-code)
- [Claude Code settings JSON schema](https://json.schemastore.org/claude-code-settings.json)
- [Claude Code troubleshooting](https://code.claude.com/docs/en/troubleshooting)
- [Claude Code security](https://code.claude.com/docs/en/security)

