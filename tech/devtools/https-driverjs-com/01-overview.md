---
date: 2026-09-07
tags: [tech]
type: tech-tool-study
status: draft
---

# Driver.js Overview

> [[README|목차]] · [[02-ecosystem|다음: Ecosystem]]

## What

Driver.js는 DOM element를 강조하는 overlay와 설명용 popover를 제공한다. 여러 `DriveStep`을 순회하면 product tour가 되고, 하나의 step만 강조하면 contextual help가 된다. 별도 `driver.js/hints` entry point는 pulsing beacon 기반 feature discovery를 제공한다.

| 모드 | 시작 API | 사용자의 흐름 | 대표 용도 |
|---|---|---|---|
| Product tour | `driver({ steps }).drive()` | 정해진 순서 | 첫 사용 onboarding, workflow 안내 |
| Single highlight | `driver().highlight(step)` | 한 번의 설명 | form help, 특정 기능 강조, 중앙 popover |
| Feature Hints | `hints({ hints }).show()` | 임의 순서 | 새 기능 discovery, dismissible 도움말 |

## Why

별도 help center는 사용자의 현재 작업 맥락을 끊는다. 일반 modal은 설명할 수 있지만 어느 UI를 조작해야 하는지 정확히 가리키기 어렵다. Driver.js는 다음 요소를 한 화면에 결합한다.

- 나머지 화면을 어둡게 하는 overlay
- target 주변의 spotlight cutout
- target과 가까운 title/description popover
- Next, Previous, Done과 progress
- keyboard, scroll, close, interaction 정책
- application state와 연결할 lifecycle/navigation hook

## 핵심 실행 모델

각 `driver()` 호출은 독립적인 config, steps, state를 가진다. 한 instance의 `setConfig()`나 `setSteps()`가 다른 instance에 전파되지 않는다.

```text
DriveStep.element
  ├─ ".save-button"           CSS selector
  ├─ document.querySelector()  Element
  └─ () => currentTarget       resolver function
             ↓
      element geometry 측정
             ↓
 overlay cutout + popover 위치 결정
             ↓
 hook 실행 + state 갱신 + 다음 navigation
```

`element`가 없는 step은 오류가 아니다. viewport 중앙 popover를 표시하여 welcome, 전환 설명, 완료 메시지처럼 사용할 수 있다.

## 핵심 특징

### UI와 interaction

- `side`와 `align`으로 popover의 선호 위치를 지정한다.
- 공간이 부족하면 viewport 안에 들어오는 위치로 자동 조정한다.
- `stagePadding`, `stageRadius`, `overlayColor`, `overlayOpacity`로 spotlight를 조절한다.
- 기본값 `disableActiveInteraction: false`이므로 강조된 element를 실제로 조작할 수 있다.
- `allowKeyboardControl`, `allowScroll`, `allowClose`, `overlayClickBehavior`로 제어 정책을 정한다.

### Dynamic UI

- `advanceOnClick`: target 자체 클릭을 다음 단계 trigger로 사용한다.
- `waitForElement`: modal, lazy rendering 등으로 늦게 생기는 target을 기다린다.
- `skipMissingElement`: 권한이나 feature flag로 없는 step을 건너뛴다.
- `onNextClick`: route 이동, API 호출, panel open 뒤 직접 이동을 이어간다.
- `data`: hook에서 사용할 application metadata를 step에 싣는다.

### Extension

- `popoverClass`와 공개 CSS class/CSS variable로 theme을 적용한다.
- `onPopoverRender`로 `PopoverDOM` reference를 받아 추가 DOM 제어를 한다.
- React, Vue, Svelte에서도 mount/unmount lifecycle에 instance를 만들고 `destroy()`하는 방식으로 통합한다.

## 장점과 비용

| 장점 | 함께 부담하는 비용 |
|---|---|
| 약 5 KB gzip, runtime dependency 0개 | product analytics와 CMS는 직접 구현 |
| MIT license | tour 상태 persistence는 application 책임 |
| framework-independent DOM API | component lifecycle과 cleanup을 직접 연결 |
| 세밀한 hook과 styling | selector와 async 상태의 복잡도가 application으로 이동 |
| 별도 Hints bundle | tour와 hint의 content governance가 필요 |

## 보안·접근성 관점

- `title`과 `description`은 HTML을 포함할 수 있으므로 remote/user content를 그대로 넣지 않는다. 신뢰된 정적 content를 쓰거나 sanitize한다.
- `allowClose: false`와 interaction 차단을 함께 쓰면 keyboard/screen reader 사용자에게 탈출하기 어려운 UI가 될 수 있다.
- popover를 visual affordance로만 보지 말고 keyboard flow, focus, reduced motion, contrast를 실제 환경에서 검사한다.
- 핵심 기능을 tour에서만 설명하지 말고 영구적으로 접근 가능한 help 경로도 둔다.

## Sources

- https://driverjs.com/docs/basic-usage
- https://driverjs.com/docs/configuration
- https://driverjs.com/docs/popover-position
- https://driverjs.com/docs/hints
- https://driverjs.com/docs/theming
- https://github.com/nilbuild/driver.js

