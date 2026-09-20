---
date: 2026-09-20
tags: [tech]
type: tech-tool-study
status: draft
---

# Web Design Guidelines

> **한 줄 정의**: Web design guidelines는 웹 UI를 사용자 중심·접근 가능·반응형·고성능·일관된 방식으로 설계, 구현, 검증하기 위한 표준과 실무 원칙의 체계다.

## Overview

웹은 화면 크기, 입력 방식, 네트워크, 언어, 보조기술이 모두 다르다. 따라서 시각적 완성도만으로는 충분하지 않다. 이 학습 노트는 `user task → semantic HTML → responsive layout → performance → 측정과 개선`의 흐름으로 웹 UI 품질을 다룬다.

- [[01-overview|What / Why / 핵심 특징]]
- [[02-ecosystem|표준·Design System·도구 비교]]
- [[03-references|공식 참고 자료]]
- [[cheatsheet|구현·검증 Cheatsheet]]

## Learning Path

- [ ] [[04-learning/01-getting-started|시작하기]]: semantic HTML과 mobile-first 화면 만들기
- [ ] token을 CSS custom properties로 정의하고 Button·Input을 component화한다.
- [ ] [[04-learning/02-deep-dive|심화]]: keyboard, Screen Reader, Core Web Vitals를 함께 점검한다.
- [ ] [[05-projects|프로젝트]] 중 하나를 구현하고 manual test와 field data로 개선한다.

## When To Use

- public website, product UI, form, commerce처럼 다양한 사용자와 기기를 지원할 때
- component library 또는 Design System의 품질 기준을 만들 때
- 접근성, responsive behavior, performance를 release criteria로 관리할 때

## When Not To Use

- guideline을 브랜드·사용자 연구·실제 task를 대체하는 정답 목록으로 취급할 때
- 자동 검사 통과만으로 Screen Reader와 keyboard 사용성이 검증됐다고 판단할 때
- 특정 platform 관례를 웹 표준과 semantic HTML보다 우선할 때

## Related Notes

- [[MOCs/Index]]
- [[MOCs/Devtools]]
- [[tech/devtools/anime-js/README|Anime.js]]

## Sources

- https://www.w3.org/TR/WCAG22/
- https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/CSS_layout/Responsive_Design
- https://web.dev/articles/optimize-lcp
- https://web.dev/articles/optimize-cls
