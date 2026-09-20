---
date: 2026-09-20
tags: [tech]
type: tech-tool-study
status: draft
---

# Claude Observer Overview

## What

Claude Observer는 Claude Code의 여러 local session을 감시하는 macOS native app이다. Claude Code hook event를 Python handler로 수집하고 filesystem에 session state를 기록한 뒤, Swift UI가 이를 polling하여 상태와 permission request를 보여준다.

```text
Claude Code instances
        │ hook event JSON
        ▼
Python hook handler
        │ atomic/session JSON
        ▼
~/.claude-observer/sessions/
        │ 2초 polling
        ▼
Native Swift macOS app
   ├─ Dynamic Island-style panel
   ├─ Menu Bar mode
   ├─ sound/animation
   ├─ terminal focus
   └─ local Web Dashboard server
```

## Why

여러 terminal에서 Claude Code를 병렬 실행하면 작업 자체보다 **어느 session이 내 응답을 기다리는지 찾는 일**이 병목이 되기 쉽다.

- 실행 중인 session과 완료된 session을 구분하기 어렵다.
- tool permission prompt를 놓치면 작업이 멈춘다.
- API error가 난 terminal을 늦게 발견할 수 있다.
- repository, window, tab, tmux pane 사이를 반복 탐색해야 한다.

Claude Observer는 각 repository/session을 이름 붙은 crab으로 표현하고, session을 클릭하면 관련 terminal 또는 tmux pane으로 focus를 전환해 이 비용을 줄인다.

## 핵심 특징

| 영역 | 동작 | 의미 |
|---|---|---|
| Hook integration | Claude Code lifecycle event를 수집 | 별도 agent wrapper 없이 상태를 관찰 |
| Local state | session별 JSON file 사용 | database·외부 SaaS가 필요 없음 |
| Native UI | floating panel 또는 Menu Bar | macOS 작업 흐름과 자연스럽게 결합 |
| Terminal focus | 지원 terminal/tmux로 전환 | 상태 확인에서 행동까지 연결 |
| Permission broker | Yes, No, category 단위 Allow all | terminal 밖에서도 승인 가능 |
| Web Dashboard | HTTP/WebSocket, PWA, mobile UI | 동일 LAN에서 원격 확인·응답 |
| Cleanup | 종료 session 제거, stale session 정리 | 오래된 상태 누적 완화 |

## 상태 모델

| 상태 | 대표 trigger | UI 의미 |
|---|---|---|
| `working` | `UserPromptSubmit`, `PreToolUse`, `PostToolUse` | Claude가 작업 중 |
| `idle` | `Stop` | 응답 완료 |
| `needs_input` | `Notification` | 사용자 입력 필요 |
| `needs_permission` | `PermissionRequest` | tool 실행 결정 필요 |
| `error` | `StopFailure` | API error 등 비정상 종료 |

`SubagentStart`와 `SubagentStop`도 활동 상태 갱신에 사용되며, `SessionStart`는 JSON을 생성하고 `SessionEnd`는 제거한다.

## 범위 밖의 기능

Claude Observer를 다음과 혼동하지 않는다.

- OpenTelemetry collector 또는 LLM APM
- prompt/token/cost analytics
- agent orchestrator나 task scheduler
- Claude model 내부를 관찰하는 observer agent
- Anthropic 공식 Claude Code 기능

## 성숙도와 제약

2026-09-20 조사 시점에 repository는 약 35 commits, 4 stars, 0 forks 수준이고 GitHub Releases가 게시되지 않았으며 root listing에서 `LICENSE`가 확인되지 않았다. 이는 법적 결론이 아니라 **도입 전에 license를 별도로 확인해야 한다는 신호**다.

또한 filesystem을 2초마다 polling하므로 짧은 상태 전환이 늦게 보일 수 있다. Claude Code hook 사양에는 Observer가 표현하지 않는 event도 있으므로, UI를 전체 lifecycle의 완전한 audit log로 간주하면 안 된다.

## Sources

- https://github.com/svenliebig/claude-observer
- https://github.com/svenliebig/claude-observer#features
- https://code.claude.com/docs/en/hooks

