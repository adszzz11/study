---
date: 2026-08-11
tags: [tech]
type: tech-tool-study
status: draft
---

# Anime.js - Overview

> [[README|목차로 돌아가기]] · [[02-ecosystem|다음: Ecosystem]]

## What

Anime.js는 browser animation을 구성하는 여러 대상을 하나의 시간 모델로 묶는 JavaScript engine이다. CSS properties와 transforms, DOM/SVG attributes뿐 아니라 plain object의 숫자 값도 tweening할 수 있다.

```js
import { animate } from 'animejs';

const state = { progress: 0 };

animate(state, {
  progress: 100,
  duration: 1200,
  ease: 'inOutQuad',
  onUpdate: () => renderCanvas(state.progress),
});
```

## Why

CSS transition은 두 상태 사이의 간단한 변화에 좋다. 그러나 다음 요구가 겹치면 timing과 lifecycle을 직접 관리하기 어려워진다.

- 여러 element의 순차·병렬 실행과 overlap
- stagger, keyframes, easing, spring
- SVG path drawing·morphing·motion path
- scroll progress와 playhead 동기화
- pointer drag, inertia, snapping, bounds
- responsive breakpoint와 `prefers-reduced-motion`
- Canvas·WebGL·plain object처럼 DOM이 아닌 값의 tweening
- component unmount 시 animation·listener·inline mutation 정리

Anime.js는 이 문제를 `animate()`, `createTimeline()`, `createScope()`와 interaction/layout API로 통합한다.

## 핵심 특징

### Modular package

```js
import { animate } from 'animejs/animation';
import { createTimeline } from 'animejs/timeline';
import { createScope } from 'animejs/scope';
import { waapi } from 'animejs/waapi';
import { createDraggable } from 'animejs/draggable';
import { createLayout } from 'animejs/layout';
```

`animejs`는 ESM·CommonJS·TypeScript declarations와 함께 `animation`, `timeline`, `scope`, `draggable`, `events`, `layout`, `svg`, `text`, `waapi`, `adapters` 등의 subpath export를 제공한다.

### 공유 Engine

전역 `engine`이 `Timer`, `Animation`, `Timeline` instance를 drive한다.

| 설정 | 의미 |
|---|---|
| `speed` | 전체 재생 속도 배율 |
| `fps` | engine frame rate 제한 |
| `timeUnit` | 시간 단위 |
| `precision` | 계산 정밀도 |
| `pauseOnDocumentHidden` | hidden document에서 pause 여부 |
| `useDefaultMainLoop` | built-in animation loop 사용 여부 |

외부 game/render loop에서는 built-in loop를 끄고 `engine.update()`로 clock을 직접 공급할 수 있다.

### 두 backend

| Backend | 강점 | 우선 검토할 상황 |
|---|---|---|
| `animate()` | 대상과 callback 범위가 넓고 timeline 제어가 세밀함 | objects, Canvas/WebGL, SVG attributes, 복잡한 timeline, 많은 targets |
| `waapi.animate()` | browser `Element.animate()` 활용, CSS animation에 가벼움 | transform/opacity 중심 UI, main-thread 부하, 작은 bundle |

공식 문서는 대략 JS 경로를 10KB gzip, WAAPI 경로를 3KB gzip으로 소개한다. 실제 compositor acceleration은 browser와 property에 따라 달라지므로 Performance panel로 검증해야 한다.

## v4에서 달라진 점

| 변화 | 의미 |
|---|---|
| v3 `anime()` → v4 `animate()` | named ESM import 중심으로 API 재설계 |
| `easing` → `ease` | parameter 이름 변경 |
| `direction` → `reversed` / `alternate` | 재생 방향 설정 분리 |
| `anime.timeline()` → `createTimeline()` | factory API 통일 |
| v4.3 `createLayout()` | 두 layout state 사이 자동 animation |
| v4.4 transform order 고정 | `perspective → translate → rotate → scale → skew`; visual regression 주의 |
| v4.5 adapter·Three.js | mesh, material, camera, uniform 등을 `animate()`로 연결 |

v3 tutorial을 그대로 복사하지 말고 migration guide와 현재 v4 documentation을 함께 확인해야 한다.

## 설계 원칙

- 먼저 motion의 의미와 reduced-motion fallback을 정한다.
- DOM/CSS 중심이면 WAAPI, object/복합 timeline이면 JS engine에서 시작한다.
- component 또는 route마다 `Scope`를 lifecycle boundary로 둔다.
- `transform`과 `opacity`를 우선하고 layout-triggering property는 측정한다.
- minor upgrade에도 representative animation의 screenshot/visual regression test를 수행한다.

## Sources

- [Anime.js 공식 README](https://github.com/juliangarnier/anime)
- [Engine documentation](https://animejs.com/documentation/engine/)
- [WAAPI overview](https://animejs.com/documentation/web-animation-api/)
- [When to use WAAPI](https://animejs.com/documentation/web-animation-api/when-to-use-waapi/)
- [Migrating from v3 to v4](https://github.com/juliangarnier/anime/wiki/Migrating-from-v3-to-v4)
- [Anime.js releases](https://github.com/juliangarnier/anime/releases)

