---
date: 2026-09-20
tags: [tech]
type: tech-tool-study
status: draft
---

# Projects

## 1. Accessible Checkout

address/payment form을 설계한다. `label`, inline validation, error summary, keyboard focus 복귀, loading state를 구현하고 WCAG 2.2 AA 기준으로 점검한다.

**완료 기준**

- [ ] 오류 summary의 링크가 해당 field로 이동한다.
- [ ] 오류 원인과 수정 방법이 text로 전달된다.
- [ ] payment 진행과 실패 상태가 Screen Reader에 전달된다.

## 2. Responsive Editorial Page

읽기 쉬운 typography scale과 line length, table of contents, responsive image, dark mode, `prefers-reduced-motion`을 적용한다.

**완료 기준**: 320 px부터 wide layout까지 내용이 잘리지 않고, media가 CLS를 만들지 않으며, heading 구조만으로 문서 개요를 파악할 수 있다.

## 3. Mini Design System

Figma와 code 양쪽에 token과 Button/Input/Alert/Modal을 구축하고 Storybook에서 variant·state·a11y test를 문서화한다.

**완료 기준**: disabled, error, loading, focus, dark mode를 포함한 state가 token과 component API에 반영된다.

## 4. Core Web Vitals 개선 실험

느린 sample page의 hero image, font, third-party script, layout shift를 측정하고 하나씩 개선한다. 변경 전후의 Lighthouse 결과와 field data를 분리해 기록한다.

## Sources

- https://www.w3.org/TR/WCAG22/
- https://web.dev/articles/optimize-lcp
- https://web.dev/articles/optimize-cls
