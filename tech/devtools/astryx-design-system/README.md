---
date: 2026-11-13
tags: [tech]
type: tech-tool-study
status: draft
---

# Astryx — Meta의 agent-ready React Design System

> **한 줄 정의**: Astryx는 Meta가 내부에서 8년간 발전시킨 뒤 2026년 Beta로 공개한 React 19+용 접근성 중심, AI agent 친화적 Design System이다.

## Overview

Astryx는 완성된 React component의 behavior·accessibility와 브랜드 token/theme을 분리한다. 즉, 팀은 검증된 UI 기반을 package로 업데이트하면서도 color, typography, radius, motion 및 component override로 자기 브랜드를 유지할 수 있다.

- `@astryxdesign/core`: 150개 이상의 typed, accessible React component와 utility
- `@astryxdesign/theme-*`: seven first-party theme 및 `defineTheme()` 기반 확장
- `@astryxdesign/cli`: docs/search/template/theme build/swizzle/codemod/doctor를 제공하는 사람·agent 공용 interface
- 공개 시점의 Meta 설명: 내부 13,000개 이상 앱에서 사용
- 2026-11-13 확인 기준 npm: core `0.7.13`, CLI `0.7.14`; v1 전 Beta이므로 upgrade 검증이 필요

## Learning Path

- [ ] [[tech/devtools/astryx-design-system/01-overview|Overview]] — 문제, 설계 원칙, 계층 구조
- [ ] [[tech/devtools/astryx-design-system/02-ecosystem|Ecosystem]] — shadcn/ui, MUI, Radix와의 선택 기준
- [ ] [[tech/devtools/astryx-design-system/04-learning/01-getting-started|시작하기]] — 설치, CLI 탐색, 첫 Theme
- [ ] [[tech/devtools/astryx-design-system/04-learning/02-deep-dive|Deep Dive]] — theme compiler, SSR, agent workflow
- [ ] [[tech/devtools/astryx-design-system/05-projects|Projects]] — 적용 패턴과 설계 판단
- [ ] [[tech/devtools/astryx-design-system/03-references|References]] — 공식 문서와 검증 지점
- [ ] [[tech/devtools/astryx-design-system/cheatsheet|Cheatsheet]] — command와 운영 규칙 빠른 참조

## When To Use

- branded internal tool 또는 product를 빠르게 만들되 accessibility와 component quality를 기본값으로 원할 때
- coding agent가 설치된 버전의 component docs·template·token을 CLI로 직접 검색해야 할 때
- 하나의 component layer를 유지하면서 multi-brand 또는 region별 theme을 운영할 때
- Next.js/Remix SSR에서 compile된 theme artifact로 first-paint flash를 줄이고 싶을 때

## When Not To Use

- visual layer까지 전부 자체 설계해야 하며 headless primitive만 필요한 경우
- Material Design 채택과 enterprise ecosystem의 성숙도가 가장 중요한 경우
- Tailwind file ownership 및 외부 registry의 component별 copy-in 모델이 우선인 경우
- Beta version 변동을 추적하거나 upgrade·theme rebuild를 검증할 여력이 없는 경우

## Related Notes

- [[MOCs/Index]]
- [[MOCs/Devtools]]
- [[tech/devtools/web-design-guidelines/README|Web Design Guidelines]]

## Sources

- https://github.com/meta/astryx
- https://astryx.atmeta.com/blog/introducing-astryx
- https://www.npmjs.com/package/@astryxdesign/core
- https://www.npmjs.com/package/@astryxdesign/cli
