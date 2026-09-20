---
date: 2026-09-20
tags: [tech]
type: tech-tool-study
status: draft
---

# Claude Observer Ecosystem

## 비교 관점

이 도구군은 모두 “여러 Claude Code session을 놓치지 않는다”는 문제와 닿아 있지만, 중심 UI와 운영 범위가 다르다. native attention indicator가 필요한지, browser workspace가 필요한지, cross-platform remote monitoring이 필요한지를 먼저 정한다.

| 도구 | 중심 목적 | UI/플랫폼 | 상태 수집 | Remote approval | Claude Observer 대비 |
|---|---|---|---|---|---|
| [Claude Observer](https://github.com/svenliebig/claude-observer) | 여러 Claude session의 주의 전환 | Native Swift, macOS + Web/PWA | Hooks → JSON files → 2초 polling | 지원 | 가장 가볍고 시각적이나 macOS 중심이며 초기 성숙도 |
| [Claude Dashboard](https://github.com/sonpham-org/claude-dashboard) | multi-session browser workspace | React/Web, cross-platform 지향 | Hooks → HTTP → WebSocket | 상태·notification 중심 | tab/split-pane 운영 UI가 강한 대신 server stack이 더 큼 |
| [Claude Code Monitor](https://github.com/bruceyxli/claude-code-monitor) | cross-platform monitoring과 원격 승인 | Browser, Windows/macOS/Linux 지향 | Hooks → Node/Express → Web UI | 지원 | native macOS 집중도는 낮지만 범용 접근성이 높음 |
| Claude Code terminal UI | 단일 session 상호작용 | Terminal | process 내부 상태 | 현재 terminal에서 직접 처리 | 추가 설치가 없지만 여러 session을 한눈에 보기 어려움 |

> [!note]
> 비교는 2026-09-20 dossier 기준의 개략적 positioning이다. 실제 도입 전 각 repository의 최신 README, license, release activity, security model을 다시 확인한다.

## 선택 기준

### Claude Observer가 잘 맞는 경우

- 주 작업 환경이 macOS다.
- 여러 terminal의 “지금 주의가 필요한 session”만 빠르게 보고 싶다.
- native floating panel과 terminal focus가 중요하다.
- database나 큰 server stack 없이 local-first 구성을 선호한다.

### Browser dashboard 계열이 잘 맞는 경우

- Windows/Linux를 포함해야 한다.
- split-pane이나 browser workspace가 작업의 중심이다.
- 별도 server process의 운영 비용을 감수할 수 있다.
- 원격 접근 정책, authentication, TLS를 직접 검토하고 구성할 수 있다.

### 추가 도구를 쓰지 않는 편이 나은 경우

- Claude Code session이 한두 개뿐이다.
- permission은 항상 해당 terminal에서만 처리해야 한다.
- third-party hook이 command/path/code preview를 처리하는 것을 허용할 수 없다.
- audit, license, update policy가 확인되지 않은 software를 설치할 수 없다.

## 서로 대체하지 않는 영역

| 필요 | 적합한 범주 |
|---|---|
| token/cost/latency 분석 | LLM observability/APM |
| 여러 agent의 task 분배와 retry | Agent orchestrator |
| Claude Code 권한 정책 자체의 정의 | Claude Code permissions/settings |
| session attention과 terminal 복귀 | Claude Observer류 monitor |

## Sources

- https://github.com/svenliebig/claude-observer
- https://github.com/sonpham-org/claude-dashboard
- https://github.com/bruceyxli/claude-code-monitor
- https://code.claude.com/docs/en/hooks
- https://code.claude.com/docs/en/permissions

