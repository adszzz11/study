---
date: 2026-11-13
tags: [tech]
type: tech-tool-study
status: draft
---

# Astryx — Overview

> [[tech/devtools/astryx-design-system/README|목차로 돌아가기]] · [[tech/devtools/astryx-design-system/02-ecosystem|다음: Ecosystem]]

## What

Astryx는 React 19+ application에 component, theme, CLI를 함께 제공하는 Meta의 open-source Design System이다. component는 interaction behavior와 accessibility를 맡고, theme은 CSS custom property token으로 브랜드 표현을 맡는다. 따라서 “강한 library visual language”와 “각 팀의 copy/paste maintenance” 사이의 선택 폭을 줄이려 한다.

## Why

일반 UI library는 빠른 도입 대신 vendor의 디자인 문법을 강하게 따르게 할 수 있다. 반대로 source를 복사해 쓰면 자유롭지만 accessibility, consistency, update path를 팀이 계속 관리해야 한다. Astryx는 update 가능한 package theme을 기본으로 두고, 필요할 때 source를 `swizzle`하여 소유권을 가져가는 escape hatch를 제공한다.

AI agent에도 같은 contract를 제공하는 점이 핵심이다. `init`은 project의 `AGENTS.md` 또는 `CLAUDE.md`에 component index를 기록하고, agent는 prompt에 붙여 넣은 오래된 API 대신 로컬 CLI의 현재 docs를 조회한다.

## 핵심 특징

| 계층 | 구성 | 역할 |
|---|---|---|
| Application | React 19+ app, `<Theme>` | theme과 light/dark mode 적용 |
| Core | `@astryxdesign/core` | typed, accessible component·utility |
| Theme | `@astryxdesign/theme-*`, `defineTheme()` | token, override, custom variant |
| Delivery | pre-built CSS + typed React | consumer의 StyleX build plugin 강제 없음 |
| Tooling | `@astryxdesign/cli` | docs, search, template, build, swizzle, codemod, doctor |
| Agent interface | text/JSON CLI + instruction index | 사람과 agent의 동일한 source of truth |

- **Composability**: high-level API만 숨기지 않고 building block을 export한다.
- **StyleX without lock-in**: 작성에는 StyleX를 사용하지만 consumer는 `className`으로 Tailwind, CSS Modules, plain CSS를 병행할 수 있다.
- **Theme extension first**: package theme을 `extends`하여 upstream update를 받는다. 독립 fork가 필요한 경우에만 `eject`를 고려한다.
- **RichText**: Lexical 기반 RichText는 2026년 10월 stable이 되었고 Markdown을 lossless read/write한다고 설명한다.

## Beta 운영 관점

2026-11-13 기준 core `0.7.13`, CLI `0.7.14`는 v1 이전 Beta 상태를 뜻한다. production 도입 시 lockfile, `doctor`, upgrade test, custom theme rebuild를 release process에 넣는다. 자세한 migration/운영 흐름은 [[tech/devtools/astryx-design-system/04-learning/02-deep-dive|Deep Dive]]를 참고한다.

## Sources

- https://astryx.atmeta.com/blog/introducing-astryx
- https://github.com/meta/astryx
- https://astryx.atmeta.com/docs/theme
