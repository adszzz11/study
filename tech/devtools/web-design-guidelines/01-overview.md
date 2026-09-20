---
date: 2026-09-20
tags: [tech]
type: tech-tool-study
status: draft
---

# Web Design Guidelines: Overview

## What

Web design guidelines는 UI를 예쁘게 만드는 규칙 모음이 아니라, 사용자가 목표를 완료하도록 돕는 설계·구현·검증의 기준이다. 정보 구조, component, semantic HTML, layout, asset, interaction, 측정을 하나의 품질 체계로 본다.

## Why

desktop 중심의 화면은 작은 화면, keyboard, Screen Reader, 저속 네트워크에서 쉽게 실패한다. 결과는 모바일 사용성 저하, 접근성 배제, 느린 loading, UI 불일치다. 설계 초기에 제약조건을 반영하면 출시 후 재작업 비용을 줄일 수 있다.

## 네 가지 축

| 축 | 질문 | 실무 기준 |
|---|---|---|
| User task | 사용자가 가장 먼저 끝낼 일은? | IA와 CTA를 장식보다 먼저 결정 |
| Accessibility | 다른 감각·입력 방식도 가능한가? | WCAG 2.2 POUR, keyboard, focus, labels |
| Responsive | 콘텐츠가 어디에서 깨지는가? | mobile-first, content-driven breakpoint |
| Performance | 기다림과 layout jump가 task를 방해하는가? | LCP·INP·CLS와 performance budget |

## 품질 흐름

```text
User research / content model
          ↓
Information Architecture + user flows
          ↓
Design tokens → components → patterns → pages
          ↓
Semantic HTML + accessible interaction
          ↓
Responsive layout + optimized assets
          ↓
Automated checks + manual tests + RUM
          ↓
Iteration
```

## 핵심 특징

- **Information Architecture**: navigation, heading hierarchy, grouping은 사용자 목표와 일치해야 한다. visual hierarchy도 HTML heading과 landmark 구조에 반영한다.
- **Design system**: color, typography, spacing, motion, state를 token으로 정의해 component와 page까지 일관되게 전달한다.
- **Semantic-first**: `<button>`, `<a>`, `<label>`, `<input>`, landmark를 우선한다. ARIA는 native semantic으로 표현할 수 없는 상태·관계에만 추가한다.
- **Accessible interaction**: visible focus, 논리적 tab order, 색상 외 상태 표시, 오류 원인과 해결책을 포함한 validation을 제공한다. WCAG 2.2에는 Focus Not Obscured, Dragging Movements, Target Size, Accessible Authentication이 추가됐다.
- **Performance-aware visual design**: LCP hero asset은 빠르게 발견되게 하고, responsive image와 명시적 dimensions로 CLS를 억제한다.

## 지표를 설계 제약으로 보기

Core Web Vitals의 일반적인 good threshold는 방문의 75%에서 LCP 2.5초 이하, CLS 0.1 이하이다. lab data(Lighthouse/DevTools)는 재현과 진단에, field data(RUM)는 실제 경험 판단에 사용한다.

## Sources

- https://www.w3.org/TR/WCAG22/
- https://www.w3.org/press-releases/2025/wcag22-iso-pas/
- https://web.dev/articles/optimize-lcp
- https://web.dev/articles/optimize-cls
