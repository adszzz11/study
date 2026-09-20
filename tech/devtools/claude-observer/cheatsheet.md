---
date: 2026-09-20
tags: [tech]
type: tech-tool-study
status: draft
---

# Claude Observer Cheatsheet

## 한눈에 보기

| 항목 | 값 |
|---|---|
| 목적 | 여러 Claude Code session의 attention state monitoring |
| 대상 | macOS native UI + LAN Web/PWA |
| 수집 | Claude Code hooks |
| 저장 | `~/.claude-observer/sessions/`의 session JSON |
| 갱신 | native app이 약 2초 polling |
| Dashboard | 기본 port `9321` |
| Permission timeout | 120초 |
| Stale cleanup | process 종료 + 5분 이상 비활성 |
| UI mode | floating panel, `--menubar`, `--statusbar` |

## Event → State

| Event | Result |
|---|---|
| `SessionStart` | session 생성 |
| `UserPromptSubmit` | `working` |
| `PreToolUse`, `PostToolUse` | `working` |
| `SubagentStart`, `SubagentStop` | 활동 갱신 |
| `Stop` | `idle` |
| `StopFailure` | `error` + alert |
| `Notification` | `needs_input` |
| `PermissionRequest` | `needs_permission` + decision UI |
| `SessionEnd` | session 제거 |

## UI State

| State | 표시 |
|---|---|
| `working` | 주황색 animated crab, green glow |
| `idle` | 회색 sleeping crab |
| `needs_input` | 붉은 crab + `!`, pulsing orange |
| `needs_permission` | action이 포함된 warning |
| `error` | pink/pulsing error state |

## Permission Rules

- Yes: 현재 요청 허용
- No: 현재 요청 거절
- Allow all `<category>`: session 범위의 category 승인 가능
- matching `deny` rule이 hook `allow`보다 우선
- `Allow all Bash`보다 command/path/domain 단위 rule 선호
- preview가 실제 실행 효과 전체를 보여준다고 가정하지 않기

## Local Paths

```text
~/.claude/settings.json
~/.claude-observer/hooks/
~/.claude-observer/sessions/
~/.claude-observer/personalities.json
```

## Supported Terminal Targets

- Ghostty
- iTerm2
- Terminal.app
- WezTerm
- Alacritty
- kitty
- tmux

## Troubleshooting Order

1. Claude Code version과 hook event 지원 확인
2. `settings.json`의 Observer hook 등록 확인
3. hook handler 실행 error 확인
4. session JSON 존재·갱신 시각 확인
5. 2초 polling 지연 고려
6. terminal badge/process/session identity 확인
7. stale cleanup 조건 확인

## Web Dashboard Safety

- source에서 bind address 확인
- authentication과 TLS 확인
- CSRF 및 WebSocket Origin 검증 확인
- 공용 Wi-Fi, 회사 LAN, port forwarding 노출 금지
- 확인 전에는 local UI만 사용

## 도입 전 Gate

- [ ] license 확인
- [ ] release/update strategy 확인
- [ ] install/rollback 검증
- [ ] hook compatibility test
- [ ] permission boundary review
- [ ] dashboard network security review

## Sources

- https://github.com/svenliebig/claude-observer
- https://code.claude.com/docs/en/hooks
- https://code.claude.com/docs/en/permissions
