---
date: 2026-09-20
tags: [tech]
type: tech-tool-study
status: draft
---

# Claude Observer Deep Dive

## Event Pipeline

Claude Code는 lifecycle event마다 JSON input을 hook process에 전달한다. Observer의 Python handler는 event를 UI용 상태로 축약해 session별 JSON에 기록하고, Swift app은 directory를 약 2초마다 polling한다.

| Claude Code event | Observer 처리 |
|---|---|
| `SessionStart` | session JSON 생성 |
| `UserPromptSubmit` | `working` |
| `PreToolUse`, `PostToolUse` | `working` 유지 |
| `SubagentStart`, `SubagentStop` | 활동 상태 갱신 |
| `Stop` | `idle` |
| `StopFailure` | `error`와 sound alert |
| `Notification` | `needs_input` |
| `PermissionRequest` | permission UI 표시 후 응답 대기 |
| `SessionEnd` | session JSON 제거 |

이 모델은 운영 UI에 필요한 상태를 단순화한 **projection**이지 모든 hook event의 원본 audit trail은 아니다.

## Filesystem as IPC

### 장점

- database와 message broker가 없다.
- 각 session 상태를 일반 JSON으로 검사할 수 있다.
- producer인 hook과 consumer인 app이 느슨하게 결합된다.
- app이 재시작돼도 남아 있는 session state를 다시 읽을 수 있다.

### trade-off

- polling interval만큼 UI 반영이 늦어진다.
- 짧은 중간 상태가 다음 write로 덮이면 UI가 보지 못할 수 있다.
- partial write를 피하려면 temp file 작성 후 rename 같은 atomic write가 중요하다.
- stale process 판정은 PID reuse, sleep/wake, crash 같은 경계조건을 다뤄야 한다.
- session JSON에 민감한 command/path/code가 남는다면 local file permission과 cleanup이 중요하다.

## Permission Broker

`PermissionRequest`는 실제 permission decision이 필요할 때 발생한다. Observer는 tool name, command/path/URL 요약, file-write code preview를 UI에 표시하고 다음 선택을 반환한다.

- **Yes**: 현재 요청 허용
- **No**: 현재 요청 거절
- **Allow all `<category>`**: 해당 session에서 category 범위 허용

공식 protocol의 `updatedPermissions`는 session 또는 settings destination에 permission rule을 추가할 수 있다. 단, matching `deny` rule은 hook이 `allow`를 반환해도 우선한다.

```text
PermissionRequest
      │
      ▼
Observer panel / Web Dashboard
      │ Yes / No / Allow all category
      ▼
Hook decision + optional updatedPermissions
      │
      ▼
Claude Code permission engine
      │ matching deny rule wins
      ▼
Tool executes or is blocked
```

### Threat model 질문

- preview가 긴 command나 encoded payload를 충분히 보여주는가?
- symlink, relative path, shell expansion 뒤의 실제 대상이 드러나는가?
- category allow가 현재 session에만 적용되는가, persistent settings에도 쓰이는가?
- UI와 hook 사이의 response를 다른 local process가 위조할 수 있는가?
- 120초 timeout은 fail-closed인가?

## Web Dashboard Security Boundary

Dashboard는 기본 port `9321`의 HTTP/WebSocket interface, polling fallback, mobile approval, PWA, sound/vibration을 제공한다. 이는 편리함과 함께 permission 결정 경계를 LAN까지 확장한다.

README가 같은 LAN의 `http://<your-ip>:9321` 접근을 안내한다는 사실만으로 authentication의 존재 여부를 단정할 수 없다. 다음은 server source와 runtime 설정에서 확인해야 한다.

| 검토 항목 | 실패 시 위험 |
|---|---|
| bind address | 의도하지 않은 network interface에 노출 |
| authentication | LAN의 다른 사용자가 상태 열람 또는 승인 |
| TLS | command/path/preview와 결정의 평문 노출 |
| CSRF protection | 사용자가 연 page가 승인 action 유도 |
| WebSocket Origin validation | 악성 origin이 상태 stream에 연결 |
| rate limiting/timeouts | resource exhaustion 또는 stale approval |

## Identity and Cleanup

- repository별 deterministic crab name을 `personalities.json`에 유지한다.
- process가 죽고 5분 이상 비활성인 session을 자동 제거한다.
- permission request는 120초 후 timeout된다.
- terminal badge와 process/session 정보를 조합해 focus 대상을 찾는다.

복수 worktree, 동일 repository의 여러 terminal, tmux nesting에서는 “repository identity”와 “실행 위치 identity”가 충돌할 수 있으므로 실제 focus 동작을 시험해야 한다.

## Compatibility Drift

2026년 공식 hook 사양에는 `PermissionDenied`, `PostToolBatch`, `TaskCreated`, `TaskCompleted`, `TeammateIdle`, `PostCompact`, model-switch event 등이 포함된다. Observer가 추적하는 subset만으로는 다음을 놓칠 수 있다.

- task lifecycle의 세부 진행
- compact 이후 context 변화
- batch tool 처리 경계
- permission denial의 별도 의미
- teammate/model 전환 상태

Claude Code update 후에는 hook 이름뿐 아니라 input/output schema와 permission decision contract를 regression test한다.

## Sources

- https://github.com/svenliebig/claude-observer
- https://code.claude.com/docs/en/hooks
- https://code.claude.com/docs/en/hooks#hook-events
- https://code.claude.com/docs/en/hooks#permissionrequest-decision-control
- https://code.claude.com/docs/en/permissions

