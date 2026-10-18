---
date: 2026-10-18
tags: [tech]
type: tech-tool-study
status: draft
---

# Responsively — Deep dive

[[tech/devtools/responsively/README|학습 진입점]] · 이전: [[tech/devtools/responsively/04-learning/01-getting-started|Getting started]]

## 1. Device suite를 제품 계약으로 다루기

Suite는 예쁜 기기 목록이 아니라 지원할 layout 폭의 계약이다. design token, analytics, browser support policy를 근거로 폭·방향·상태를 정하고 이름에 의도를 넣는다.

```text
core-responsive
  mobile-320
  mobile-375
  tablet-768
  desktop-1024
  desktop-1440
```

변경이 발견되면 "어느 폭에서 어떤 상태가 깨졌는가"를 기록한다. 수정 후에는 같은 suite에서 재확인하고, 안정적으로 재현되면 Playwright project 또는 visual test에 승격한다.

## 2. Inspector와 visual utility의 역할

- **Unified Inspector:** 동일 element를 여러 viewport에서 inspect하여 width, display, spacing 차이의 단서를 찾는다.
- **Ruler·guide:** 예상 container 폭, alignment, safe margin을 눈으로 비교한다.
- **Rotation:** orientation 변경 때 navigation, fixed element, modal의 높이를 확인한다.
- **Color-blindness simulation:** 색만으로 상태를 전달하는 UI인지 1차 점검한다. WCAG 판정은 별도 accessibility test로 보완한다.
- **Mockup overlay:** 구현과 design mockup의 spacing·alignment 차이를 비교한다. asset의 scale과 viewport 기준을 먼저 맞춘다.

## 3. MCP로 visual verification 시키기

Responsively가 실행된 상태라면 localhost MCP endpoint를 agent에 연결할 수 있다. endpoint는 local machine에서만 노출되도록 설계됐지만, agent 설정에 연결하기 전 접근 권한과 최신 tool schema를 공식 repository에서 검토한다.

검증 task는 모호한 "responsive를 확인해"보다 URL·폭·상태·판정 기준을 포함해야 한다.

```text
http://localhost:3000/checkout 를 연다.
375, 768, 1440 viewport를 활성화한다.
쿠폰 오류 상태를 재현하고 각 viewport screenshot을 찍는다.
horizontal overflow, hidden CTA, clipped modal 여부를 보고한다.
```

가능한 흐름은 `navigate` → `list_devices` → `set_active_devices` → `click`/`type_text` → `read_page` → `screenshot`이다. DOM text가 정상이어도 visual defect는 남을 수 있으므로 screenshot을 함께 판단한다.

## 4. 신뢰 경계

Chromium preview가 통과해도 iOS Safari의 viewport, font rendering, touch/keyboard, browser chrome, Android browser 차이는 남는다. 결제·가입·인증처럼 영향이 큰 flow는 실기기 또는 BrowserStack에서 최종 실행한다.

## Sources

- [Responsively App GitHub repository and MCP guide](https://github.com/responsively-org/responsively-app)
- [Responsively App guide](https://responsively.app/blog/responsively-app-guide)
- [Chrome Device Mode limitations](https://developer.chrome.google.cn/docs/devtools/device-mode?hl=en)
- [Playwright emulation](https://playwright.dev/docs/next/emulation)
