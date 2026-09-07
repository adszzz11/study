---
date: 2026-09-07
tags: [tech]
type: tech-tool-study
status: draft
---

# Driver.js Deep Dive

> [[01-getting-started|이전: Getting Started]] · [[../README|목차]] · [[../05-projects|다음: Projects]]

## 1. Instance, State, Navigation

각 `driver()` instance는 config, steps, state를 독립 소유한다. runtime에는 다음 API로 제어한다.

```ts
tour.setConfig(nextConfig);
tour.setSteps(nextSteps);
tour.drive();       // 처음부터
tour.drive(2);      // index 2부터
tour.moveNext();
tour.movePrevious();
tour.moveTo(4);
tour.destroy();
```

상태 query는 UI button이나 application state와 tour를 동기화할 때 유용하다.

```ts
tour.isActive();
tour.hasNextStep();
tour.hasPreviousStep();
tour.getActiveIndex();
tour.getActiveStep();
tour.getState();
```

## 2. Lifecycle Hook 설계

hook을 세 부류로 나누면 복잡도를 줄일 수 있다.

| 부류 | 예 | 책임 |
|---|---|---|
| 관찰 | `onHighlighted`, `onDeselected` | analytics, logging |
| UI extension | `onPopoverRender` | DOM customization, test hook 추가 |
| 제어 | `onNextClick`, `onCloseClick`, `onDoneClick` | async action, confirm, custom navigation |

### 가장 중요한 override 규칙

`onNextClick`, `onPrevClick`, `onCloseClick`, `onDoneClick`을 정의하면 해당 built-in action을 대체한다. callback에서 다음 상태를 명시적으로 결정해야 한다.

```ts
onNextClick: async (_element, _step, { driver }) => {
  await saveDraft();
  await openNextPanel();
  driver.moveNext(); // 생략하면 현재 step에 머문다.
}
```

중복 click을 막아야 하는 async 작업이라면 application state로 in-flight guard를 두고 error 시 retry/close 경로를 제공한다.

## 3. Dynamic Target 전략

```ts
const tour = driver({
  waitForElement: 3_000,
  skipMissingElement: true,
  steps: [
    {
      element: '[data-tour="open-settings"]',
      advanceOnClick: true,
      popover: { title: "Open settings" },
    },
    {
      element: () => document.querySelector('[data-tour="profile-panel"]')!,
      popover: { title: "Edit profile" },
    },
  ],
});
```

의사결정 순서:

1. target이 곧 나타날 예정이면 `waitForElement`.
2. 권한/feature flag 때문에 없을 수 있으면 `skipMissingElement`.
3. route나 panel open을 직접 통제해야 하면 `onNextClick` 후 `moveNext()`.
4. target identity가 runtime에 바뀌면 element resolver function.

`skipMissingElement`는 selector 오류도 조용히 숨길 수 있다. production resilience에는 좋지만 test에서는 필수 target의 존재를 별도 assertion한다.

## 4. Cross-Page Tour

Driver.js가 route를 orchestration하지는 않는다. application이 다음 index와 tour version을 저장하고 다음 화면에서 재개한다.

```ts
const STORAGE_KEY = "onboarding:project-create:v2";

const goToBilling = (_el, _step, { driver }) => {
  sessionStorage.setItem(STORAGE_KEY, JSON.stringify({ nextIndex: 3 }));
  driver.destroy();
  window.location.assign("/settings/billing");
};

const saved = JSON.parse(sessionStorage.getItem(STORAGE_KEY) ?? "null");
if (saved) {
  sessionStorage.removeItem(STORAGE_KEY);
  driver({ steps }).drive(saved.nextIndex);
}
```

- tour 정의가 바뀔 수 있으므로 raw index만 저장하지 말고 tour version을 함께 둔다.
- resume target이 준비된 뒤 시작하고 timeout/fallback을 제공한다.
- multi-tab 충돌을 피하려면 session scope 또는 server-side state 정책을 명확히 한다.

## 5. Analytics Contract

library hook을 직접 vendor SDK 호출로 흩뿌리지 말고 작은 adapter를 둔다.

```ts
type TourEvent = {
  tourId: string;
  tourVersion: number;
  stepId?: string;
  index?: number;
  action: "view" | "next" | "back" | "close" | "done";
};

function trackTour(event: TourEvent) {
  analytics.track("product_tour", event);
}
```

PII나 popover의 raw HTML을 event에 넣지 않는다. 최소한 start, step view, close, complete를 구분하고 tour version을 포함한다.

## 6. Hint Persistence

Driver.js는 dismiss를 현재 session memory에서 관리하지만 영구 저장은 하지 않는다.

```ts
const key = "dismissed-feature-hints:v1";
const dismissed = new Set<string>(JSON.parse(localStorage.getItem(key) ?? "[]"));

const productHints = hints({
  hints: allHints.filter((hint) => !dismissed.has(String(hint.id))),
  onDismiss: (_element, hint) => {
    dismissed.add(String(hint.id));
    localStorage.setItem(key, JSON.stringify([...dismissed]));
  },
});
```

로그인 사용자의 여러 device에서 동기화하려면 localStorage 대신 server profile에 저장한다. 새 버전을 다시 보여주려면 hint ID나 persistence schema에 version을 넣는다.

## 7. Styling과 Layout

```css
.driver-popover.product-tour {
  --driver-popover-font-family: system-ui, sans-serif;
  max-width: 22rem;
}

.driver-popover.product-tour .driver-popover-title {
  font-size: 1rem;
}
```

- `popoverClass`로 theme scope를 좁힌다.
- portal, transformed ancestor, nested scroll container, sticky header를 test한다.
- image가 들어간 popover는 layout shift를 줄이도록 width/height를 예약한다.
- Hints의 pulse는 `prefers-reduced-motion` 환경에서도 확인한다.

## 8. Security와 Accessibility

### HTML content

`title`/`description`은 HTML을 render할 수 있다. 다음 원칙을 적용한다.

- source code에 포함된 trusted static content를 우선한다.
- CMS/API content는 allowlist 기반 sanitizer를 거친다.
- 사용자 입력을 HTML string으로 연결하지 않는다.
- URL, image, button 등 active content 정책을 별도로 제한한다.

### Escape path

- 기본적으로 close control과 `Escape`를 유지한다.
- `allowClose: false`가 정말 필요한지 검토한다.
- focus order, accessible name, zoom 200%, high contrast, reduced motion을 test한다.
- tour를 건너뛰어도 핵심 기능과 help에 접근할 수 있어야 한다.

## 9. Test 전략

```ts
// Playwright 개념 예시
await page.getByRole("button", { name: "Start tour" }).click();
await expect(page.locator(".driver-popover-title")).toHaveText("Welcome");
await page.getByRole("button", { name: /next/i }).click();
await expect(page.locator('[data-tour="create-project"]')).toBeVisible();
await page.keyboard.press("Escape");
await expect(page.locator(".driver-overlay")).toHaveCount(0);
```

- 모든 required selector를 정적 또는 component test에서 검증한다.
- missing/late target, route failure, resize, scroll을 포함한다.
- analytics는 event name과 metadata contract를 검증한다.
- accessibility scanner와 keyboard 수동 test를 함께 사용한다.

## Sources

- https://driverjs.com/docs/api
- https://driverjs.com/docs/configuration
- https://driverjs.com/docs/async-tour
- https://driverjs.com/docs/multi-page-tour
- https://driverjs.com/docs/buttons
- https://driverjs.com/docs/hints
- https://driverjs.com/docs/theming
