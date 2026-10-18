---
date: 2026-10-18
tags: [tech]
type: tech-tool-study
status: draft
---

# Responsively — Overview

[[tech/devtools/responsively/README|학습 진입점]] · 다음: [[tech/devtools/responsively/02-ecosystem|Ecosystem]]

## What

Responsively App은 하나의 web URL을 여러 device viewport에 나란히 표시하는 cross-platform desktop app이다. Electron 위에서 Chromium rendering을 사용하며, source는 AGPL-3.0으로 공개되어 있다.

## Why

Responsive UI의 오류는 특정 폭에서만 드러난다. DevTools의 폭을 하나씩 바꾸며 header, navigation, form, modal을 반복 조작하면 확인 비용이 커진다. Responsively는 한 번의 interaction을 활성 preview에 mirror하여 이 반복을 줄인다.

## 핵심 기능

| 기능 | 활용 |
|---|---|
| Multi-viewport preview | 기본 device profile 30개 이상과 custom device를 병렬 비교 |
| Mirrored interaction | click, scroll, navigation, text input을 여러 preview에 동기화 |
| Preview Suite | 자주 쓰는 device 조합을 저장하고 전환 |
| Unified Inspector | 동일 element의 viewport별 layout 차이를 조사 |
| Visual utilities | viewport/full-page screenshot, ruler·guide, rotation, color-blindness simulation, mockup overlay |
| Browser capability | cookie, local/session storage, bookmarks, DevTools 사용 |

## 경계와 검증 원칙

Device profile은 browser viewport의 **preview**이지 물리 기기의 완전한 복제본이 아니다. Chrome도 desktop의 device emulation을 first-order approximation으로 설명한다. 따라서 다음 순서를 권장한다.

1. Responsively로 빠르게 breakpoint 결함을 발견한다.
2. 재현 가능한 viewport를 Playwright screenshot/assertion에 기록해 CI 회귀를 막는다.
3. 핵심 user flow는 iOS Safari·Android browser를 포함한 실기기 또는 BrowserStack에서 최종 확인한다.

## MCP 연동

App이 실행 중일 때 localhost 전용 MCP endpoint `http://127.0.0.1:12720/mcp`를 제공한다. agent는 `navigate`, `list_devices`, `set_active_devices`, `screenshot`, `read_page`, `click`, `type_text` 같은 도구로 local UI를 점검할 수 있다. endpoint와 app의 실행 상태, 접근 범위는 실제 도입 시 공식 repository의 최신 안내로 확인한다.

## Sources

- [Responsively App GitHub repository and MCP guide](https://github.com/responsively-org/responsively-app)
- [Responsively App guide](https://responsively.app/blog/responsively-app-guide)
- [Chrome DevTools Device Mode — limitations](https://developer.chrome.google.cn/docs/devtools/device-mode?hl=en)
