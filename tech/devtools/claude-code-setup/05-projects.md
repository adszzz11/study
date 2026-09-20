---
date: 2026-09-20
tags: [tech]
type: tech-tool-study
status: draft
---

# Claude Code Setup — Projects

> [[04-learning/02-deep-dive|이전: Deep Dive]] · [[README|목차로 돌아가기]] · [[cheatsheet|다음: Cheatsheet]]

## 프로젝트 1. 안전한 개인 Setup

### 목표

기존 repository에서 read-only 탐색부터 작은 verified edit까지 수행한다.

### 절차

```bash
claude --version
claude doctor
cd /path/to/project
claude
```

```text
/status
/context
/permissions
/sandbox
```

- [ ] working directory와 Git branch 확인
- [ ] load된 instruction file 확인
- [ ] `.env`와 credential path가 deny되어 있는지 확인
- [ ] sandbox가 실제 available 상태인지 확인
- [ ] read-only repository summary 요청
- [ ] 작은 documentation 또는 test change 수행
- [ ] `git diff --check`, test, `git status --short`로 검증

### 완료 기준

변경 이유, diff, 실행한 test와 결과를 한 번에 설명할 수 있다.

## 프로젝트 2. Team Context Baseline

### 목표

새 팀원이 clone한 repository에서도 동일한 command와 architecture constraint를 제공한다.

### 산출물

```text
CLAUDE.md
.claude/
├── settings.json
├── rules/
│   ├── backend.md
│   └── frontend.md
└── skills/
    └── verify-change/
        └── SKILL.md
```

### 설계 순서

1. 기존 README, package script, CI config에서 실제 command를 측정한다.
2. `CLAUDE.md`에는 build/test와 중요한 architecture boundary만 넣는다.
3. path-specific convention은 rules로 옮긴다.
4. 긴 release/test runbook은 Skill로 옮긴다.
5. shared settings에는 반복적으로 안전한 command만 allow한다.
6. 새 clone 또는 clean worktree에서 `/context`와 `/permissions`를 확인한다.

### Review 질문

- 문서의 command가 CI에서 쓰는 command와 같은가?
- 시간이 지나면 쉽게 낡을 정보가 항상-loaded context에 들어갔는가?
- personal preference가 team settings에 섞였는가?
- permission wildcard가 예상보다 넓게 match하는가?

## 프로젝트 3. Fail-Closed Sandbox Lab

### 목표

Sandbox dependency가 없거나 command가 boundary를 넘을 때 조용히 unsandboxed 실행되지 않게 한다.

### 설정 예시

```json
{
  "$schema": "https://json.schemastore.org/claude-code-settings.json",
  "sandbox": {
    "enabled": true,
    "failIfUnavailable": true,
    "allowUnsandboxedCommands": false
  },
  "permissions": {
    "deny": [
      "Read(./.env)",
      "Read(./.env.*)"
    ]
  }
}
```

### 실습

- [ ] macOS 또는 Linux/WSL2에서 `/sandbox` 상태 확인
- [ ] workspace 안의 harmless command 실행
- [ ] workspace 밖 write와 차단된 network access가 거부되는지 확인
- [ ] dependency가 없을 때 session이 fail-closed하는지 disposable environment에서 확인
- [ ] `allowUnsandboxedCommands: false`가 유지되는지 확인

> [!warning]
> Sandbox test에 destructive command를 쓰지 않는다. 임시 directory와 harmless marker file을 사용하고, production credential이 없는 disposable environment에서 검증한다.

## 프로젝트 4. Cross-Agent Instruction 정리

### 목표

Claude Code, Codex, 기타 tool이 서로 다른 지침 사본을 읽어 drift하는 문제를 줄인다.

### 패턴 A — `AGENTS.md`를 source of truth로 사용

```markdown
<!-- CLAUDE.md -->
@AGENTS.md

## Claude Code

- Run `/context` after changing instruction files.
```

### 패턴 B — Claude 전용 setup

`CLAUDE.md`를 source of truth로 유지하고, cross-tool 공통 규칙만 `AGENTS.md`에 둔다. 현재 session의 Project instructions 설정이 두 파일을 함께 읽는지 `/config`와 `/context`로 확인한다.

### 완료 기준

- [ ] 공통 rule의 authoritative file이 하나다.
- [ ] tool-specific exception이 분리되어 있다.
- [ ] 지원하지 않는 session에서도 fallback 방식이 있다.
- [ ] 같은 내용이 두 번 context에 들어가지 않는다.

## 프로젝트 5. GitHub Actions Pilot

### 목표

낮은 위험의 issue triage나 documentation PR에서 Claude Code automation을 시험한다.

### 단계

1. 공식 GitHub Actions setup flow를 사용한다.
2. test repository 또는 제한된 path에서 pilot을 시작한다.
3. token permission을 최소화한다.
4. protected branch에 direct push를 허용하지 않는다.
5. untrusted issue/comment content를 prompt injection input으로 취급한다.
6. required review와 CI check를 통과해야 merge되게 한다.

### Pilot 후보

| 작업 | 위험 | 적합성 |
|---|---|---|
| Issue 요약/label 제안 | 낮음 | 첫 pilot에 적합 |
| 문서 typo PR | 낮음 | diff review가 쉬움 |
| Dependency update | 중간 | lockfile/test 검증 필요 |
| Production deploy | 높음 | 초기 pilot에 부적합 |
| Secret rotation | 매우 높음 | agent 단독 실행 금지 |

## 프로젝트 6. MCP Integration Review

### 목표

하나의 MCP server를 최소 scope로 연결하고 authority와 data flow를 문서화한다.

### Checklist

- [ ] publisher/source와 update channel 확인
- [ ] tool 목록 및 read/write capability 기록
- [ ] credential scope와 storage 위치 확인
- [ ] project/user/local 중 올바른 scope 선택
- [ ] destructive tool은 ask/deny 유지
- [ ] untrusted output의 prompt injection 가능성 점검
- [ ] 연결 제거와 credential revoke 절차 기록

## Sources

- [Claude Code common workflows](https://code.claude.com/docs/en/common-workflows)
- [Claude Code best practices](https://code.claude.com/docs/en/best-practices)
- [Configure permissions](https://code.claude.com/docs/en/permissions)
- [Configure the sandboxed Bash tool](https://code.claude.com/docs/en/sandboxing)
- [Claude Code GitHub Actions](https://code.claude.com/docs/en/github-actions)
- [Connect Claude Code to tools via MCP](https://code.claude.com/docs/en/mcp)

