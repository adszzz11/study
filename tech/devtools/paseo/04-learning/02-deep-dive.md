---
date: 2026-08-08
tags: [tech]
type: tech-tool-study
status: draft
---

# Paseo — Deep Dive

> [[01-getting-started|이전: Getting Started]] | [[../README|목차로 돌아가기]] | [[../05-projects|다음: Projects]]

## 1. Control Plane과 Data Plane

Paseo daemon은 session과 workspace를 조정하는 control plane이다. 실제 model interaction과 code modification은 사용자가 설치한 provider CLI process에서 일어난다.

| Plane | 주요 구성요소 | 책임 |
|---|---|---|
| Client | desktop, mobile, web, CLI | 관찰, 승인, prompt/follow-up 전송 |
| Control | Paseo daemon, WebSocket/local socket, MCP/API | session lifecycle, routing, state, orchestration |
| Execution | provider CLI, terminal, script, service | model 호출, shell 실행, file edit |
| Workspace | Git worktree, branch, ports | task별 working tree와 runtime 자원 구분 |
| Transport | direct connection 또는 E2EE relay | remote client와 daemon 연결 |

## 2. Adapter Boundary

Native adapter와 ACP adapter는 provider-specific behavior를 공통 session/control API로 번역한다.

```text
Common control request
        │
        ├── Native adapter ──> Claude Code / Codex / OpenCode / Pi
        │
        └── ACP adapter ─────> JSON-RPC over stdio ──> ACP agent
```

Custom ACP provider는 startup 시 JSON-RPC `initialize`를 수행하고 runtime에 model, mode, capability를 보고한다. 설계·검증 시 다음 질문이 중요하다.

- provider의 permission request가 공통 UX에 어떻게 매핑되는가?
- streaming message와 tool call의 ordering이 보존되는가?
- cancel, reconnect, resume semantics는 무엇인가?
- provider-native feature가 공통 capability model 밖에 있을 때 어떻게 노출되는가?

## 3. Orchestration Lifecycle

```text
discover providers/models
          ↓
create worker ── choose same workspace or new worktree
          ↓
send task ── run terminal/script/service
          ↓
wait / observe / heartbeat
          ↓
follow-up or collect structured output
          ↓
human review and branch integration
```

Cross-provider delegation의 실질적 차이는 parent와 worker가 같은 vendor일 필요가 없다는 점이다. 예를 들어 Claude Code가 planning을 맡고 Codex가 isolated worktree에서 implementation을 수행하도록 구성할 수 있다.

### Workspace 선택

| 선택 | 적합한 작업 | 위험 |
|---|---|---|
| 동일 workspace | read-only 조사, 순차 follow-up, 같은 변경의 연속 작업 | 동시 edit collision |
| 별도 worktree | 병렬 구현, 독립 experiment, provider 비교 | setup 비용, merge conflict |

## 4. `paseo.json`과 Runtime Isolation

Repository-level configuration으로 다음 lifecycle을 선언할 수 있다.

- worktree `setup` / `teardown`
- test, lint, codegen 같은 named script
- 장기 실행 dev server
- service별 dynamic port
- daemon reverse proxy
- 자동 terminal tab

Dynamic port는 여러 workspace가 동일 application을 동시에 띄울 때 bind collision을 줄인다. 그러나 database schema, queue, object storage, third-party API quota 같은 외부 상태는 config에서 별도 namespace를 부여해야 한다.

## 5. Remote Security Model

### E2EE relay handshake

```text
Daemon                         Client
  │ persistent ECDH keypair       │
  │── public key via QR/link ─────>│
  │<── Curve25519 ECDH ───────────>│
  │<══ XSalsa20-Poly1305 box ═════>│
                  │
                Relay
         ciphertext + metadata
```

- QR/pairing URL이 trust anchor이므로 secret처럼 관리한다.
- Relay는 message와 code 내용은 해독하지 못하도록 설계됐다.
- Relay가 볼 수 있는 metadata에는 IP, timing, message size, session ID가 포함된다.
- direct connection password는 access control이지 encryption이 아니다.
- `0.0.0.0` bind에는 password와 HTTPS/VPN을 함께 사용한다.
- Docker mount에 노출한 code와 credential은 agent가 접근할 수 있다.

## 6. Threat Boundary

| 오해 | 실제 경계 | 대응 |
|---|---|---|
| worktree가 agent를 sandbox한다 | file tree만 분리하며 OS 권한은 동일 | container/VM, least privilege, secret scope 축소 |
| relay E2EE가 metadata도 숨긴다 | payload 보호, metadata는 관찰 가능 | network/privacy 요구사항 별도 평가 |
| password가 direct traffic을 암호화한다 | access control만 제공 | HTTPS 또는 VPN 사용 |
| local-first면 credential risk가 없다 | agent subprocess가 local credential에 접근 가능 | 전용 계정, short-lived token, permission review |

## 7. 운영 관찰 지표

- agent별 duration, completion/error/cancel 비율
- workspace setup/teardown 실패율
- provider adapter reconnect/resume 실패
- 동시 service port와 external resource collision
- human approval 대기 시간
- worktree당 merge conflict와 abandoned branch 비율

## Sources

- [Custom providers](https://paseo.sh/docs/custom-providers)
- [Orchestration](https://paseo.sh/docs/orchestration)
- [Orchestration workflows](https://paseo.sh/docs/orchestration-workflows)
- [Git worktrees](https://paseo.sh/docs/worktrees)
- [Security architecture](https://paseo.sh/docs/security)
- [Relay repository](https://github.com/getpaseo/paseo-relay)
