---
date: 2026-09-20
tags: [tech]
type: tech-tool-study
status: draft
---

# Claude Observer Projects

## Project 1: Local Session State Lab

### 목표

격리된 test repository에서 주요 lifecycle event와 UI state mapping을 검증한다.

### 과제

- session 시작부터 종료까지 state timeline 기록
- `working`, `idle`, `needs_input`, `needs_permission`, `error` 관찰
- hook event 시각, JSON 수정 시각, UI 표시 시각 비교
- 2초 polling이 체감 지연과 누락에 미치는 영향 기록

### 완료 기준

- [ ] 각 상태를 재현하는 최소 절차가 있다.
- [ ] 예상 상태와 실제 상태 차이를 표로 남겼다.
- [ ] real project의 민감한 내용 없이 재현 가능하다.

## Project 2: Permission Boundary Audit

### 목표

Observer를 통한 승인·거절이 Claude Code permission engine과 어떻게 결합되는지 확인한다.

### Test Matrix

| Scenario | 기대 결과 |
|---|---|
| 단일 read 요청에 Yes | 해당 요청만 실행 |
| 요청에 No | 실행 차단 |
| matching deny rule + UI Yes | deny 우선 |
| 응답 없이 120초 경과 | 안전한 timeout |
| category Allow all | 문서화된 scope에서만 적용 |

### 완료 기준

- [ ] 각 결정의 실제 scope와 persistence를 확인했다.
- [ ] `updatedPermissions`가 쓰이는 destination을 확인했다.
- [ ] timeout과 app crash가 fail-safe인지 확인했다.
- [ ] `Allow all Bash` 없이 test를 완료했다.

## Project 3: LAN Dashboard Threat Review

### 목표

Web Dashboard를 network에 노출하기 전에 source와 runtime behavior를 점검한다.

### 과제

- listen address와 port 확인
- authentication/session mechanism 추적
- HTTP action의 CSRF 방어 확인
- WebSocket handshake의 Origin 검사 확인
- mobile permission response가 전송되는 경로 확인
- firewall rule과 trusted network 범위 설계

### 안전 조건

- 공용 Wi-Fi에서 실행하지 않는다.
- router port forwarding을 사용하지 않는다.
- 검토가 끝나기 전 민감한 repository session을 연결하지 않는다.
- 문제가 발견되면 dashboard를 끄고 local UI만 사용한다.

## Project 4: Compatibility Regression Checklist

### 목표

Claude Code 또는 Observer update 때 반복할 smoke test를 만든다.

```text
SessionStart → UserPromptSubmit → PreToolUse/PostToolUse
             → PermissionRequest → Stop/StopFailure → SessionEnd
```

### 완료 기준

- [ ] hook schema 변경을 탐지한다.
- [ ] 기존 `settings.json` hook과 충돌하지 않는다.
- [ ] terminal focus와 tmux pane focus를 각각 확인한다.
- [ ] stale session이 정책대로 정리된다.
- [ ] rollback 후 Claude Code가 정상 동작한다.

## Sources

- https://github.com/svenliebig/claude-observer
- https://code.claude.com/docs/en/hooks
- https://code.claude.com/docs/en/permissions

