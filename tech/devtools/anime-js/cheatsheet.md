---
date: 2026-08-11
tags: [tech]
type: tech-tool-study
status: draft
---

# Anime.js - Cheatsheet

> [[05-projects|이전: Projects]] · [[README|목차로 돌아가기]]

## 설치와 import

```bash
npm install animejs
```

```js
import {
  animate,
  createTimeline,
  createScope,
  stagger,
  waapi,
} from 'animejs';
```

```js
// 필요한 module만 명시
import { animate } from 'animejs/animation';
import { createTimeline } from 'animejs/timeline';
import { waapi } from 'animejs/waapi';
```

## 기본 animation

```js
const animation = animate('.item', {
  x: [0, 160],
  opacity: [0, 1],
  rotate: '1turn',
  duration: 800,
  delay: 100,
  ease: 'outExpo',
  loop: false,
  alternate: false,
  autoplay: true,
});
```

| 목적 | API/parameter |
|---|---|
| target tweening | `animate(targets, parameters)` |
| browser WAAPI 경로 | `waapi.animate(targets, parameters)` |
| sequence composition | `createTimeline()` |
| per-target 분배 | `stagger()` |
| lifecycle boundary | `createScope()` / `scope.revert()` |
| scroll 연결 | `onScroll()` |
| pointer interaction | `createDraggable()` |
| layout state 전환 | `createLayout()` |
| 외부 object 연결 | `registerAdapter()` |

## Timeline

```js
const tl = createTimeline({
  defaults: { duration: 500, ease: 'outQuad' },
});

tl.label('enter')
  .add('.title', { y: [-20, 0], opacity: [0, 1] })
  .add('.card', { scale: [0.9, 1] }, '<-=150')
  .call(() => console.log('ready'));

tl.pause();
tl.resume();
tl.reverse();
tl.seek(300);
```

## Stagger

```js
animate('.item', {
  y: [20, 0],
  opacity: [0, 1],
  delay: stagger(60),
});

animate('.cell', {
  scale: [0, 1],
  delay: stagger(40, { grid: [8, 5], from: 'center' }),
});
```

## Backend 선택

| 조건 | 먼저 검토 |
|---|---|
| simple hover/fade | CSS transition/keyframes |
| CSS/DOM, small bundle, main-thread 부담 | `waapi.animate()` |
| object/Canvas/WebGL/SVG attributes | `animate()` |
| complex timeline·callbacks·많은 targets | `animate()` |
| React 선언형 layout/gesture | Motion 비교 |
| advanced scroll pinning/plugin 중심 | GSAP 비교 |

## Scope cleanup pattern

```js
const scope = createScope({
  root: document.querySelector('.component'),
  mediaQueries: {
    reduceMotion: '(prefers-reduced-motion: reduce)',
  },
}).add((self) => {
  animate('.item', {
    opacity: [0, 1],
    y: self.matches.reduceMotion ? 0 : [16, 0],
  });
});

// unmount
scope.revert();
```

## v3 → v4 빠른 변환

| v3 | v4 |
|---|---|
| `anime({...})` | `animate(targets, {...})` |
| `anime.timeline()` | `createTimeline()` |
| `easing` | `ease` |
| `direction: 'reverse'` | `reversed: true` |
| `direction: 'alternate'` | `alternate: true` |
| global/default import 중심 | named ESM imports 중심 |

## 성능·접근성 체크

- `transform`·`opacity` 우선, layout/paint 비용은 측정한다.
- WAAPI도 property/browser에 따라 compositor acceleration이 달라진다.
- `prefers-reduced-motion`에서는 큰 이동·회전·parallax를 줄인다.
- animation 전후에도 keyboard focus와 reading order를 보존한다.
- component/route 종료 시 `revert()`로 정리한다.
- upgrade 시 initial/mid/final frame visual regression을 비교한다.
- Three.js/game loop에서는 duplicate RAF 대신 external `engine.update()`를 검토한다.

## 버전 메모

| 기준일 | npm | License | Runtime dependencies |
|---|---:|---|---:|
| 2026-08-11 | `4.5.0` | MIT | 0 |

## Sources

- [Anime.js documentation](https://animejs.com/documentation/)
- [Animation documentation](https://animejs.com/documentation/animation/)
- [Timeline documentation](https://animejs.com/documentation/timeline/)
- [Scope documentation](https://animejs.com/documentation/scope/)
- [Web Animation API](https://animejs.com/documentation/web-animation-api/)
- [v3 to v4 Migration Guide](https://github.com/juliangarnier/anime/wiki/Migrating-from-v3-to-v4)
