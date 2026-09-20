---
date: 2026-09-07
tags: [tech]
type: tech-tool-study
status: draft
---

# Driver.js Getting Started

> [[../03-references|이전: References]] · [[../README|목차]] · [[02-deep-dive|다음: Deep Dive]]

## 목표

15~30분 안에 stable selector를 가진 3-step tour를 만들고, 종료 시 cleanup되는지 확인한다.

## 1. 설치

```bash
npm install driver.js
# 또는: pnpm add driver.js
# 또는: yarn add driver.js
```

JavaScript와 기본 stylesheet를 함께 import한다.

```ts
import { driver } from "driver.js";
import "driver.js/dist/driver.css";
```

> production에서는 CDN의 `@latest` 대신 검증한 exact version을 고정한다.

## 2. Stable selector 준비

style class나 DOM 깊이에 tour를 묶지 말고 명시적 selector를 둔다.

```html
<button data-tour="create-project">Create project</button>
<nav data-tour="project-nav">Projects</nav>
<button data-tour="invite-member">Invite</button>
```

## 3. 첫 Product Tour

```ts
const onboarding = driver({
  showProgress: true,
  progressText: "{{current}} / {{total}}",
  allowClose: true,
  allowKeyboardControl: true,
  smoothScroll: true,
  steps: [
    {
      popover: {
        title: "Welcome",
        description: "핵심 workflow를 1분 안에 둘러봅니다.",
      },
    },
    {
      element: '[data-tour="create-project"]',
      popover: {
        title: "Create a project",
        description: "새 workspace를 시작합니다.",
        side: "bottom",
        align: "start",
      },
    },
    {
      element: '[data-tour="invite-member"]',
      popover: {
        title: "Invite your team",
        description: "협업자를 초대할 수 있습니다.",
      },
    },
  ],
  onDestroyed: () => {
    console.log("tour closed");
  },
});

document.querySelector("#start-tour")?.addEventListener("click", () => {
  onboarding.drive();
});
```

## 4. Single Highlight

```ts
const help = driver({ stagePadding: 6, stageRadius: 8 });

help.highlight({
  element: '[data-tour="invite-member"]',
  popover: {
    title: "Invite",
    description: "이 버튼에서 member를 추가합니다.",
    side: "left",
  },
});
```

`element`를 생략하면 target 없이 중앙 popover가 열린다.

## 5. Feature Hints

Hints는 별도 entry와 stylesheet를 사용한다.

```ts
import { hints } from "driver.js/hints";
import "driver.js/dist/hints.css";

const featureHints = hints({
  hints: [
    {
      id: "invite-v1",
      element: '[data-tour="invite-member"]',
      beacon: { side: "top", align: "end" },
      popover: {
        title: "New: Team invite",
        description: "링크로 member를 초대할 수 있습니다.",
      },
    },
  ],
});

featureHints.show();
```

Dismissal은 session memory에만 남는다. 사용자별 persistence가 필요하면 `id`와 `onDismiss`를 storage/API에 연결한다.

## 6. Framework Lifecycle

imperative instance는 component cleanup에서 제거한다. React 예시:

```tsx
useEffect(() => {
  const tour = driver({ steps });

  if (shouldStart) tour.drive();

  return () => tour.destroy();
}, [shouldStart]);
```

실제 application에서는 `steps` reference가 render마다 바뀌어 tour가 재생성되지 않도록 상수화나 memoization도 검토한다.

## 확인할 동작

- [ ] Next/Previous/Done과 `Escape`가 예상대로 동작한다.
- [ ] 작은 viewport에서 popover가 잘리지 않는다.
- [ ] scroll container와 sticky/fixed element에서 위치가 맞는다.
- [ ] keyboard만으로 닫고 이동할 수 있다.
- [ ] component unmount 후 overlay와 event listener가 남지 않는다.
- [ ] highlighted element의 click 허용 여부가 요구사항과 일치한다.

## 자주 하는 실수

- CSS를 import하지 않아 overlay/popover가 깨짐
- selector가 여러 element와 match하거나 아직 DOM에 없음
- custom `onNextClick` 안에서 `moveNext()`를 호출하지 않아 멈춤
- 매 render마다 새 instance를 만들고 기존 instance를 `destroy()`하지 않음
- untrusted HTML을 `title`/`description`에 삽입함

## Sources

- https://driverjs.com/docs/installation
- https://driverjs.com/docs/basic-usage
- https://driverjs.com/docs/simple-highlight
- https://driverjs.com/docs/hints
- https://driverjs.com/docs/configuration
