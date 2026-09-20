---
date: 2026-09-20
tags: [tech]
type: tech-tool-study
status: draft
---

# Getting Started

## 목표

작은 signup 또는 checkout form을 semantic HTML로 만들고, mobile-first layout과 keyboard 사용성을 확보한다.

## 1. HTML을 먼저 쓴다

`header`, `main`, `nav`, `form` landmark와 한 개의 `h1`을 먼저 만든다. 행동에는 `<button>`, 페이지 이동에는 `<a>`를 사용하고, 모든 input에는 연결된 `<label>`을 둔다.

```html
<form>
  <label for="email">Email</label>
  <input id="email" name="email" type="email" autocomplete="email" required>
  <button type="submit">Continue</button>
</form>
```

## 2. mobile-first와 tokens

단일 column에서 시작하고, 콘텐츠가 충돌하는 지점에만 breakpoint를 추가한다. 기기명이 breakpoint의 근거가 되면 안 된다.

```css
:root { --space-4: 1rem; --content-max: 72rem; --focus: #005fcc; }
.page { max-width: var(--content-max); margin: auto; padding: var(--space-4); }
:focus-visible { outline: 3px solid var(--focus); outline-offset: 3px; }
@media (min-width: 48rem) { .form-grid { display: grid; grid-template-columns: 1fr 1fr; gap: var(--space-4); } }
```

## 3. 첫 검증

- [ ] Tab / Shift+Tab만으로 모든 control에 도달하고 순서가 자연스럽다.
- [ ] Enter는 submit, Escape는 열린 Dialog 닫기처럼 예측 가능하게 동작한다.
- [ ] focus가 보이고 sticky header나 overlay에 가려지지 않는다.
- [ ] 오류는 색상만이 아니라 text로 설명되며, 해결 방법을 제시한다.
- [ ] 320 CSS px 폭에서도 overflow와 가로 scroll이 없다.

## 다음 단계

[[02-deep-dive|심화 학습]]에서 responsive asset, performance budget, automated/manual 검증을 추가한다.

## Sources

- https://www.w3.org/TR/WCAG22/
- https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/CSS_layout/Responsive_Design
