---
date: 2026-09-20
tags: [tech]
type: tech-tool-study
status: draft
---

# Deep Dive

## Accessible interaction

Dialog, menu, validation처럼 상태가 바뀌는 UI는 component contract를 문서화한다. trigger, focus 이동·복귀, Escape, disabled/loading, error announcement를 각각 test한다. ARIA role과 attribute는 native HTML로 해결되지 않는 상태만 보완한다.

## Responsive assets와 CLS

LCP image는 CSS background보다 HTML에서 발견 가능한 `<img>`를 우선 고려한다. `srcset`/`sizes` 또는 `<picture>`로 화면과 density에 맞는 asset을 제공하고, image/video/embed/ad에는 width·height 또는 `aspect-ratio`로 공간을 예약한다.

```html
<img
  src="hero-1280.webp"
  srcset="hero-640.webp 640w, hero-1280.webp 1280w"
  sizes="(max-width: 48rem) 100vw, 70vw"
  width="1280" height="720"
  alt="제품의 핵심 기능을 사용하는 화면">
```

## Performance budget

page weight, image size, font family/weight 수, third-party script, animation을 release 전에 제한한다. Lighthouse로 trace를 재현하고, RUM 또는 PageSpeed Insights의 field data로 실제 방문자 경험을 확인한다.

| Metric | 점검 관점 |
|---|---|
| LCP | hero resource 발견·전송·render가 늦지 않은가 |
| INP | 긴 JavaScript task와 interaction handler가 막지 않는가 |
| CLS | 늦게 삽입되는 content가 layout을 밀지 않는가 |

## 검증 순서

1. lint, unit/component test, axe로 반복 가능한 결함을 먼저 탐지한다.
2. keyboard-only와 Screen Reader로 핵심 task를 수행한다.
3. 작은 화면, 확대, reduced motion, 저속 network에서 실패 경로를 확인한다.
4. 실제 사용자 task test와 field data를 바탕으로 우선순위를 조정한다.

자동화는 결함 탐지 보조 수단이며, 사용자 경험을 보증하지 않는다.

## Sources

- https://web.dev/articles/serve-responsive-images
- https://web.dev/articles/performance-budgets-101
- https://web.dev/articles/optimize-lcp
- https://web.dev/articles/optimize-cls
