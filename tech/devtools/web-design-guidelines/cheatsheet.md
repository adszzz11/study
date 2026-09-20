---
date: 2026-09-20
tags: [tech]
type: tech-tool-study
status: draft
---

# Web Design Guidelines Cheatsheet

## Semantic HTML

| 의도 | 기본 선택 | 피할 것 |
|---|---|---|
| action | `<button>` | clickable `<div>` |
| navigation | `<a href>` | button으로 페이지 이동 |
| field name | `<label for>` | placeholder만 사용 |
| page structure | `header`, `nav`, `main`, `footer` | 의미 없는 wrapper만 사용 |
| document outline | 순서 있는 `h1`–`h6` | 시각 크기만으로 heading 표현 |

## Accessibility checklist

- `:focus-visible`로 충분히 대비되는 focus indicator를 제공한다.
- keyboard의 Tab 순서는 DOM 순서와 user flow에 맞춘다.
- state와 오류는 색상 외 text/icon으로도 전달한다.
- target은 충분히 크고 spacing이 있다.
- motion은 `prefers-reduced-motion`을 존중한다.
- ARIA보다 native element를 먼저 사용한다.

## Responsive / Performance

```css
img, video { max-width: 100%; height: auto; }
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after { animation-duration: .01ms !important; transition-duration: .01ms !important; }
}
```

- mobile-first single column에서 시작한다.
- breakpoint는 콘텐츠가 충돌하는 지점에 둔다.
- image/video/embed에 dimensions 또는 `aspect-ratio`를 지정한다.
- LCP asset을 빠르게 발견하게 하고 responsive image를 제공한다.
- fonts, JavaScript, third-party script에 budget을 둔다.

## Release gate

- [ ] keyboard-only 핵심 task 성공
- [ ] Screen Reader smoke test 완료
- [ ] axe/Lighthouse 경고를 triage
- [ ] LCP, INP, CLS의 lab·field data를 구분해 확인
- [ ] 작은 화면·확대·저속 network에서 재확인

## Sources

- https://www.w3.org/TR/WCAG22/
- https://web.dev/articles/performance-budgets-101
