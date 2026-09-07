---
date: 2026-09-07
tags: [tech]
type: tech-tool-study
status: draft
---

# Driver.js Cheatsheet

> [[05-projects|이전: Projects]] · [[README|목차]]

## Install과 Import

```bash
npm install driver.js
```

```ts
// Tour / highlight
import { driver } from "driver.js";
import "driver.js/dist/driver.css";

// Hints: 별도 entry와 CSS
import { hints } from "driver.js/hints";
import "driver.js/dist/hints.css";
```

## 최소 Recipe

```ts
const tour = driver({
  showProgress: true,
  steps: [
    { popover: { title: "Welcome", description: "Start here" } },
    {
      element: '[data-tour="save"]',
      popover: { title: "Save", side: "bottom", align: "center" },
    },
  ],
});

tour.drive();
```

```ts
driver().highlight({
  element: "#target",
  popover: { title: "Title", description: "Description" },
});
```

```ts
const featureHints = hints({
  hints: [
    { id: "export-v1", element: "#export", popover: { title: "Export" } },
  ],
});
featureHints.show();
```

## Target와 Popover

```ts
const step = {
  element: ".selector",                  // string
  // element: document.querySelector("#x"), // Element
  // element: () => getCurrentTarget(),     // resolver
  popover: {
    title: "Title",
    description: "Description",
    side: "top",       // top | right | bottom | left
    align: "center",   // start | center | end
    popoverClass: "product-tour",
  },
  data: { stepId: "save" },
};
```

`element`가 없으면 viewport 중앙 popover다. 위치는 viewport 공간에 따라 자동 보정될 수 있다.

## 자주 쓰는 Config

| 목적 | 옵션 |
|---|---|
| progress | `showProgress`, `progressText` |
| button | `showButtons`, `disableButtons`, label options |
| overlay | `overlayColor`, `overlayOpacity` |
| spotlight | `stagePadding`, `stageRadius` |
| scroll | `smoothScroll`, `allowScroll` |
| close | `allowClose`, `overlayClickBehavior` |
| keyboard | `allowKeyboardControl` |
| target interaction 차단 | `disableActiveInteraction: true` |
| target click으로 진행 | `advanceOnClick: true` |
| 늦은 DOM 대기 | `waitForElement: 3000` |
| 없는 optional step skip | `skipMissingElement: true` |
| theme | `popoverClass` |

## Instance API

```ts
tour.drive();
tour.drive(index);
tour.highlight(step);
tour.moveNext();
tour.movePrevious();
tour.moveTo(index);
tour.destroy();

tour.setConfig(config);
tour.setSteps(steps);
tour.getConfig();
tour.getState();
tour.getActiveIndex();
tour.getActiveStep();
tour.isActive();
tour.hasNextStep();
tour.hasPreviousStep();
```

## Hook Pattern

```ts
const tour = driver({
  onHighlighted: (_el, step, { index }) => {
    track("tour_step_view", { index, stepId: step.data?.stepId });
  },
  onNextClick: async (_el, _step, { driver }) => {
    await prepareNextUI();
    driver.moveNext();
  },
  onCloseClick: (_el, _step, { driver }) => {
    if (window.confirm("안내를 종료할까요?")) driver.destroy();
  },
});
```

> **함정**: navigation button hook은 built-in action을 override한다. `moveNext()`, `movePrevious()`, `destroy()` 등을 callback에서 직접 호출한다.

## Hints API

```ts
featureHints.show();
featureHints.hide();
featureHints.open("export-v1");
featureHints.close();
featureHints.dismiss("export-v1");
featureHints.restore("export-v1");
featureHints.restoreAll();
featureHints.setHints(nextHints);
featureHints.getHints();
featureHints.getActive();
featureHints.isVisible();
featureHints.refresh();
```

```ts
const featureHints = hints({
  overlay: false,
  hints: [{
    id: "export-v1",
    element: "#export",
    beacon: { side: "top", align: "end", offsetX: 0, offsetY: 0 },
    popover: { title: "Export", buttonText: "Got it" },
  }],
  onDismiss: (_el, hint) => persistDismissal(String(hint.id)),
});
```

## Production Checklist

- [ ] exact package version 고정 및 changelog 확인
- [ ] `data-tour` 같은 stable selector 사용
- [ ] unmount/route change에서 `destroy()`
- [ ] custom hook의 다음 상태 명시
- [ ] completion/resume/hint dismiss persistence 설계
- [ ] HTML content 신뢰 경계와 sanitization 확인
- [ ] keyboard, close path, focus, contrast, reduced motion test
- [ ] missing/async target과 small viewport E2E test
- [ ] analytics에 tour ID/version/step ID 포함

## Sources

- https://driverjs.com/docs/installation
- https://driverjs.com/docs/configuration
- https://driverjs.com/docs/api
- https://driverjs.com/docs/buttons
- https://driverjs.com/docs/hints

