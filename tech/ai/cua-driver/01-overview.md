---
date: 2026-11-05
tags: [tech]
type: tech-tool-study
status: draft
---

# Cua Driver: Overview

[[tech/ai/cua-driver/README|Cua Driver 목차]] · [[tech/ai/cua-driver/02-ecosystem|Ecosystem]]

## What

Cua Driver는 LLM이 제안한 행동을 실제 OS와 browser에 연결하는 tool runtime이다. agent harness는 MCP, CLI 또는 Python/TypeScript SDK로 driver를 호출한다. 따라서 Cua Driver 자체는 모델도 planner도 아니며, desktop·browser의 관찰과 입력을 담당한다.

## Why

많은 업무 GUI에는 API가 없고, 화면 좌표만으로 조작하면 해상도·layout 변화에 취약하다. Driver는 Accessibility tree의 의미 있는 element와 screenshot의 시각 정보를 결합해 이 간극을 줄인다. browser-only automation을 넘어 legacy desktop app, PDF viewer, spreadsheet까지 같은 agent workflow에 넣을 수 있다.

## 특징과 동작

- **Observe**: `get_window_state`는 Accessibility tree, action 가능한 `element_token`, screenshot을 함께 반환한다.
- **Act then verify**: token 기반 named action을 좌표 click보다 먼저 쓰고, 매 action 뒤 새 state를 읽어 결과를 확인한다.
- **Background-first**: 대상 app에 입력을 전달하면서 사용자의 focus/cursor를 가능한 유지한다. 지원하지 않는 foreground 조건은 제약 또는 refusal로 다뤄야 한다.
- **Browser route**: Chrome/Edge와 일부 Electron을 `(pid, window_id)`로 bind한 후 CDP의 typed browser action을 사용한다.
- **권한 경계**: 모든 호출은 authorization check를 거치지만, `standard` mode가 넓은 app input을 허용할 수 있어 allowlist와 최소 권한이 필요하다.

```text
list_windows → get_window_state → element_token action → fresh state verification
                                      │
                         tree가 부실한 canvas면 screenshot/perception 보완
```

## Platform 및 라이선스

macOS 14+는 Accessibility와 Screen Recording 권한이 필요하다. Windows 10/11/Server, x86_64 Linux desktop도 지원하지만 Linux Wayland는 compositor별 제약을 먼저 확인한다. Driver와 SDK는 MIT이고, Cua Spaces 및 일부 benchmark 영역은 별도 FSL 계열 라이선스다.

## Sources

- https://cua.ai/docs/cua-driver/concepts/how-cua-driver-works
- https://cua.ai/docs/cua-driver/concepts/platform-support
- https://github.com/trycua/cua
