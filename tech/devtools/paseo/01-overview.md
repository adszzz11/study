---
date: 2026-08-08
tags: [tech]
type: tech-tool-study
status: draft
---

# Paseo — Overview

> [[README|목차로 돌아가기]] | [[02-ecosystem|다음: Ecosystem]]

## What

Paseo는 기존 coding-agent CLI를 실행하고 상태를 모아 보여 주며, 사람과 agent가 이들을 다시 제어할 수 있게 하는 local-first orchestration platform이다. 자체 model을 제공하거나 model request를 proxy하지 않고, 사용자가 설치·인증한 provider CLI와 subscription을 그대로 쓴다.

```text
Desktop / iOS / Android / Web / CLI
                  │
          WebSocket / local socket
                  │
             Paseo daemon
       ┌──────────┼───────────────┐
       │          │               │
 Agent adapter  Workspace       MCP/API
       │        manager          tools
       │          │               │
Claude/Codex   Git worktree   Agent-to-agent
OpenCode/Pi    terminal       orchestration
ACP agents     services       schedules
                  │
       optional E2EE relay
                  │
             Remote clients
```

## Why

AI coding agent가 늘면서 개발 workflow는 provider별 CLI와 terminal로 분산됐다.

| 문제 | Paseo의 접근 |
|---|---|
| agent마다 model·permission·session UX가 다름 | provider adapter와 공통 control API |
| 책상 밖에서 장시간 작업을 확인하기 어려움 | mobile/web client와 remote connection |
| 여러 agent가 같은 checkout을 수정해 충돌 | task별 Git worktree와 branch |
| native subagent가 provider 경계를 넘지 못함 | MCP/CLI 기반 cross-provider delegation |
| terminal, dev server, diff, conversation이 분산 | daemon과 workspace 중심 상태 관리 |

핵심 관점은 "새 agent를 만든다"가 아니라 "기존 agent 위에 control plane을 둔다"이다.

## 핵심 특징

### Local-first daemon

- laptop, homelab 또는 server에서 agent CLI를 subprocess로 실행한다.
- code, dependency, shell config, MCP server와 credential이 기존 개발환경에 남는다.
- Paseo는 기본 security sandbox가 아니다. agent는 현재 사용자 권한과 provider CLI의 permission model로 실행된다.

### Multi-provider adapter

- native adapter: Claude Code, Codex, OpenCode, Pi
- ACP adapter: GitHub Copilot을 포함한 다수 Agent Client Protocol agent
- custom ACP provider는 stdio JSON-RPC `initialize`에서 model, mode, capability를 보고한다.

### Cross-provider orchestration

MCP tools 또는 CLI를 통해 provider/model discovery, worker 생성, follow-up, terminal/script/service 실행, completion wait, heartbeat, cron schedule, structured JSON output을 제어할 수 있다.

```text
Claude Code ──delegate──> Codex
     │                       │
     └──follow-up────────────┘

Codex ──delegate──> ACP-compatible agent
```

### Worktree와 service isolation

Parallel agent마다 별도 Git worktree와 branch를 만들 수 있다. `paseo.json`에는 worktree setup/teardown, named script, dev server, dynamic port, reverse proxy, terminal tab을 선언한다. 이는 개발 작업의 격리이며 security sandbox는 아니다.

### Cross-device control

QR 또는 pairing link로 remote client를 연결할 수 있다. E2EE relay 경로에서는 Curve25519 ECDH로 key를 합의하고 XSalsa20-Poly1305 기반 NaCl `box`로 메시지를 authenticated encryption한다. Relay는 IP, timing, message size, session ID 같은 metadata는 볼 수 있다.

## Package Map

| Package | 역할 |
|---|---|
| `packages/server` | daemon, process orchestration, WebSocket API, MCP server |
| `packages/app` | Expo 기반 iOS·Android·web client |
| `packages/cli` | `paseo` CLI |
| `packages/desktop` | Electron desktop app |
| `packages/relay` | client–daemon relay transport와 encryption |
| `packages/website` | 문서와 website |

## 성숙도 판단

2026-08-08 기준 stable `v0.2.5`, pre-release `v0.3.0-beta.4`다. 기능 범위는 넓지만 다음을 production adoption 전에 검증한다.

- provider adapter의 target version 호환성
- daemon upgrade와 workspace recovery 절차
- repository별 setup/teardown idempotency
- credential exposure 범위
- relay/direct connection의 network policy

## Sources

- [Why Paseo](https://paseo.sh/docs/why)
- [Providers](https://paseo.sh/docs/providers)
- [Supported providers](https://paseo.sh/docs/supported-providers)
- [Custom providers](https://paseo.sh/docs/custom-providers)
- [Repository package map](https://github.com/getpaseo/paseo#development)
- [Security](https://paseo.sh/docs/security)
- [GitHub Releases](https://github.com/getpaseo/paseo/releases)
