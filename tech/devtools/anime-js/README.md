---
date: 2026-08-11
tags: [tech]
type: tech-tool-study
status: draft
---

# Anime.js

> **한 줄 정의**: Anime.js는 CSS·DOM attributes·SVG·JavaScript objects·Canvas/WebGL 값을 하나의 API로 tweening하고 Timeline·Scroll·Drag·Layout·WAAPI 실행을 조율하는 lightweight modular JavaScript animation engine이다.

## Overview

- 현재 기준 버전은 `4.5.0`, 라이선스는 MIT, runtime dependency는 0개다.
- v4의 중심 API는 `animate()`, `createTimeline()`, `createScope()`다.
- JavaScript/RAF engine과 `waapi.animate()` backend를 목적에 맞게 선택할 수 있다.
- DOM animation뿐 아니라 SVG, plain object, Canvas/WebGL state까지 같은 시간 모델로 다룬다.
- v4.3의 `createLayout()`, v4.5의 adapter와 Three.js 지원으로 layout·3D 영역까지 넓어졌다.

```js
import { animate, stagger } from 'animejs';

animate('.card', {
  y: [24, 0],
  opacity: [0, 1],
  delay: stagger(80),
  duration: 700,
  ease: 'outExpo',
});
```

## Learning Path

- [ ] [[01-overview|1. What/Why와 v4 핵심 특징 이해]]
- [ ] [[02-ecosystem|2. CSS·WAAPI·Motion·GSAP과 비교]]
- [ ] [[03-references|3. 공식 문서와 release 자료 훑기]]
- [ ] [[04-learning/01-getting-started|4. 설치부터 첫 animation·timeline 만들기]]
- [ ] [[04-learning/02-deep-dive|5. Engine·Scope·Scroll·Layout·adapter 심화]]
- [ ] [[05-projects|6. 실전 mini project 수행]]
- [ ] [[cheatsheet|7. API와 선택 기준 복습]]

## When To Use

- framework에 종속되지 않은 landing page, portfolio, data visualization을 만들 때
- SVG·DOM·plain object animation을 하나의 timeline에 조합할 때
- sequencing, stagger, spring, scroll/drag interaction이 CSS만으로 복잡해질 때
- Canvas·Three.js render loop와 animation clock을 통합할 때
- 작은 API surface, modular imports, MIT license가 중요한 팀

## When Not To Use

- 단순 hover·fade에는 CSS transition/animation이 더 작고 읽기 쉽다.
- React layout·gesture를 선언형 component API로 묶고 싶다면 Motion이 더 자연스러울 수 있다.
- 복잡한 scroll pinning과 검증된 plugin 생태계가 핵심이면 GSAP을 먼저 비교한다.
- main thread가 매우 바쁘다면 JS `animate()`를 바로 선택하지 말고 CSS/native WAAPI 또는 Anime.js WAAPI backend를 검토한다.
- animation이 정보 전달을 방해하거나 reduced motion 요구를 충족할 수 없다면 효과 자체를 줄인다.

## Related Notes

- [[MOCs/Index]]
- [[MOCs/Devtools]]
- [[../../scraping/playwright/README|Playwright]] - animation visual regression과 reduced-motion 검증
- [[01-overview|Anime.js 개요]]
- [[cheatsheet|Anime.js 치트시트]]

## Sources

- [Anime.js 공식 README](https://github.com/juliangarnier/anime)
- [Anime.js documentation](https://animejs.com/documentation/)
- [animejs on npm](https://www.npmjs.com/package/animejs)
- [Anime.js package.json](https://raw.githubusercontent.com/juliangarnier/anime/master/package.json)
- [Anime.js releases](https://github.com/juliangarnier/anime/releases)

