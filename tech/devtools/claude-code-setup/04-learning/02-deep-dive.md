---
date: 2026-09-20
tags: [tech]
type: tech-tool-study
status: draft
---

# Claude Code Setup — Deep Dive

> [[01-getting-started|이전: Getting Started]] · [[../README|목차로 돌아가기]] · [[../05-projects|다음: Projects]]

## 1. Context와 memory 계층

| 범위 | 주요 위치 | 목적 |
|---|---|---|
| Organization | OS별 managed `CLAUDE.md`, managed settings | 전사 정책·보안·표준 |
| User | `~/.claude/CLAUDE.md`, `~/.claude/settings.json` | 개인 기본 선호와 권한 |
| Project | `./CLAUDE.md`, `.claude/settings.json` | 팀 공통 build/test/architecture |
| Project-local | `CLAUDE.local.md`, `.claude/settings.local.json` | commit하지 않을 개인 override |
| Path-specific | `.claude/rules/*.md` | package·path·file type별 규칙 |
| Reusable workflow | `.claude/skills/<name>/SKILL.md` | 필요할 때 load하는 절차와 지식 |

### `AGENTS.md` 호환성

2026-09-20 기준 기본 `claude-md-or-agents-md` 동작은 working directory와 상위 경로에 project/local `CLAUDE.md`가 없을 때 `AGENTS.md`를 읽는다. `claude-md-and-agents-md` 설정은 둘을 함께 읽는다. 다만 다음 경우 native support가 없을 수 있다.

- Claude Code v2.1.277 이전
- feature flag를 가져오지 않는 third-party provider session
- telemetry를 끈 일부 session
- built-in `agents-md` plugin을 막는 hook/plugin policy

Cross-agent source of truth가 `AGENTS.md`라면 `CLAUDE.md`에 `@AGENTS.md`를 import하는 방식이 명시적이다.

```markdown
@AGENTS.md

## Claude Code

- Use plan mode for changes under `src/billing/`.
```

## 2. Settings scope와 precedence

```text
~/.claude/settings.json           # user settings
.claude/settings.json             # team-shared project settings
.claude/settings.local.json       # personal project override
.mcp.json                         # project MCP configuration
```

Settings는 strict JSON이다. comment와 trailing comma를 허용하지 않는다. `.claude/settings.json`은 team policy로 commit할 수 있지만 `.claude/settings.local.json`은 개인 예외이므로 commit하지 않는다.

```json
{
  "$schema": "https://json.schemastore.org/claude-code-settings.json",
  "permissions": {
    "allow": [
      "Bash(pnpm lint)",
      "Bash(pnpm test *)"
    ],
    "deny": [
      "Read(./.env)",
      "Read(./.env.*)"
    ]
  },
  "sandbox": {
    "enabled": true,
    "allowUnsandboxedCommands": false
  }
}
```

`/status`로 적용 source를, `/permissions`로 effective rule을 확인한다. Managed settings는 조직 baseline에 적합하지만 array가 scope 간 merge되는 항목은 local entry가 policy를 넓힐 수 있는지 별도로 확인해야 한다.

## 3. Permission model

Rule은 `Tool` 또는 `Tool(specifier)` 형식이다.

| Rule | 의미 |
|---|---|
| `Bash(pnpm lint)` | 정확한 lint command 허용 |
| `Bash(pnpm test *)` | 인자가 붙는 test command 허용 |
| `Read(./.env)` | `.env` read에 대한 rule |
| `WebFetch(domain:docs.example.com)` | 특정 domain fetch에 대한 rule |
| `Bash` | 모든 Bash command에 해당하는 매우 넓은 rule |

운영 원칙:

- 반복되는 안전한 command만 allow한다.
- secret path와 destructive command는 deny한다.
- broad `Bash` allow보다 command prefix를 좁게 쓴다.
- permission prompt와 sandbox boundary를 혼동하지 않는다.
- `bypassPermissions`는 외부 격리가 보장된 container/VM에서만 사용한다.

## 4. Bash sandbox

| Platform | 구현 | 비고 |
|---|---|---|
| macOS | Seatbelt | OS-level filesystem/network restriction |
| Linux/WSL2 | bubblewrap + socat | dependency와 user namespace 설정 필요 |
| Native Windows | 미지원 | sandbox가 필요하면 WSL2 사용 |

Ubuntu/Debian/WSL2의 dependency 예:

```bash
sudo apt-get install bubblewrap socat
```

Session에서 상태를 확인한다.

```text
/sandbox
```

일회성 강제 설정:

```bash
claude --settings \
  '{"sandbox":{"enabled":true,"allowUnsandboxedCommands":false}}'
```

기본 동작의 중요한 함정은 sandbox를 시작할 수 없을 때 warning 후 unsandboxed command로 진행할 수 있다는 점이다. 조직 security gate라면 managed settings로 fail-closed를 적용한다.

```json
{
  "sandbox": {
    "enabled": true,
    "failIfUnavailable": true,
    "allowUnsandboxedCommands": false
  }
}
```

## 5. Rules와 Skills

### Rules

`.claude/rules/*.md`는 path-specific instruction을 분리한다. Monorepo에서 backend, frontend, infrastructure 규칙이 서로 다른 경우 유용하다.

```text
.claude/rules/
├── backend.md
├── frontend.md
└── migrations.md
```

### Skills

Skill은 `SKILL.md`와 supporting file을 가진 on-demand workflow다.

```text
.claude/skills/release-check/
├── SKILL.md
├── checklist.md
└── scripts/
    └── verify.sh
```

- 항상 필요한 한두 줄은 `CLAUDE.md`
- 특정 path에만 필요한 rule은 `.claude/rules/`
- 긴 절차, reference, script는 Skill

Project skill은 repository에 commit해 팀과 공유할 수 있다. Personal skill은 `~/.claude/skills/`에 둔다. Cloud/Cowork session은 local personal skill을 자동으로 읽지 않으므로 account sync, committed project skill, plugin 중 맞는 배포 경로를 선택한다.

## 6. Hooks, MCP, Plugins

| 기능 | 실행 주체 | 적합한 용도 | 주요 위험 |
|---|---|---|---|
| Hook | lifecycle event에 local command | formatter, policy check, audit | hook 자체가 임의 code 실행 |
| MCP | model이 external tool 호출 | issue tracker, database, browser, docs | credential·data exposure, untrusted output |
| Plugin | 구성 bundle | skill/agent/hook/MCP 배포 | 공급망과 update trust |

Hook은 prompt로 강제하는 규칙과 다르게 deterministic하다. 예를 들어 edit 후 formatter 실행이나 dangerous command 차단에 적합하다. 하지만 repository hook은 code와 같은 수준으로 review하고 workspace trust 전에는 실행하지 않는다.

MCP server를 추가하기 전에는 다음을 확인한다.

- server publisher와 source
- local process인지 remote service인지
- 읽고 쓸 수 있는 data scope
- OAuth/token 저장 위치와 rotation
- tool output이 prompt injection을 포함할 가능성
- project `.mcp.json`을 공유해도 되는지

## 7. Defense in Depth

```text
Clear goal and review
        ↓
Minimal context and trusted instructions
        ↓
Fine-grained permissions
        ↓
OS sandbox / container boundary
        ↓
Hooks and CI policy
        ↓
Tests, diff, branch protection
```

어느 한 layer도 단독으로 충분하지 않다. Permission allowlist가 있어도 broad command가 우회 경로를 만들 수 있고, sandbox가 있어도 writable workspace 안의 source를 망가뜨릴 수 있다. 최종 방어선은 version control, test, human diff review다.

## Sources

- [How Claude remembers your project](https://code.claude.com/docs/en/memory)
- [Settings files and precedence](https://code.claude.com/docs/en/settings)
- [Configure permissions](https://code.claude.com/docs/en/permissions)
- [Configure the sandboxed Bash tool](https://code.claude.com/docs/en/sandboxing)
- [Extend Claude with skills](https://code.claude.com/docs/en/skills)
- [Automate workflows with hooks](https://code.claude.com/docs/en/hooks-guide)
- [Connect Claude Code to tools via MCP](https://code.claude.com/docs/en/mcp)

