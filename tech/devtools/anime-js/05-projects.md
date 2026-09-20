---
date: 2026-08-11
tags: [tech]
type: tech-tool-study
status: draft
---

# Anime.js - Projects

> [[04-learning/02-deep-dive|이전: Deep Dive]] · [[README|목차로 돌아가기]] · [[cheatsheet|다음: Cheatsheet]]

## Project 1. Accessible landing intro

### 목표

title, subtitle, CTA card를 label과 overlap이 있는 timeline으로 등장시키고 reduced-motion variant를 제공한다.

### 요구사항

- `createTimeline()`과 `defaults` 사용
- transform·opacity 중심
- `prefers-reduced-motion: reduce`에서 큰 이동 제거
- replay button으로 timeline 재실행
- keyboard focus가 animation 때문에 가려지거나 이동하지 않음

### 완료 조건

- [ ] motion on/off 모두 정보 순서가 같다.
- [ ] 4× CPU throttling에서 눈에 띄는 frame drop이 없다.
- [ ] initial/mid/final screenshot test가 있다.

## Project 2. Scroll-synced SVG story

### 목표

SVG path drawing, marker motion path, 설명 text를 scroll progress에 동기화한다.

```text
ScrollObserver
├─ SVG path draw progress
├─ marker position/rotation
└─ chapter label opacity
```

### 실험 항목

- document scroll와 nested container scroll 비교
- scrub smoothing 유무 비교
- fast scroll, reverse scroll, resize 처리
- reduced-motion에서 static SVG와 chapter navigation 제공

### 완료 조건

- [ ] marker와 label이 동일한 playhead를 공유한다.
- [ ] resize 후 geometry가 틀어지지 않는다.
- [ ] JS가 실패해도 핵심 내용이 보인다.

## Project 3. Draggable snap carousel

### 목표

`createDraggable()`로 card carousel을 만들고 inertia, bounds, snap point를 적용한다.

### 요구사항

- pointer drag와 keyboard previous/next button 모두 제공
- viewport resize 시 bounds 재계산
- current slide를 접근 가능한 text로 알림
- component destroy 시 `Scope.revert()`로 cleanup

### 측정

| 항목 | 질문 |
|---|---|
| Input latency | drag가 손가락/포인터를 즉시 따라오는가? |
| Bounds | overscroll 후 안정적으로 복귀하는가? |
| Accessibility | keyboard와 reduced motion에서 같은 작업이 가능한가? |
| Cleanup | route 왕복 후 listener가 중복되지 않는가? |

## Project 4. Layout filter gallery

### 목표

grid item을 category별로 filter/sort하면서 `createLayout()`으로 before/after layout을 연결한다.

### 학습 포인트

- CSS grid 변경과 DOM order 변경의 차이
- removed item의 exit와 remaining item의 reflow 조율
- rapid repeated filter 입력의 interruption policy
- visual order, DOM order, focus order의 일치

### 완료 조건

- [ ] 빠르게 filter를 연속 클릭해도 잘못된 최종 상태가 남지 않는다.
- [ ] focus가 제거된 item 안에 갇히지 않는다.
- [ ] v4 upgrade 전후 visual regression fixture로 활용할 수 있다.

## Project 5. Three.js data sculpture

### 목표

v4.5 Three.js adapter와 external engine loop를 사용해 instanced mesh의 값과 camera를 timeline으로 조율한다.

### 단계

1. scene의 단일 render loop를 만든다.
2. Anime.js default main loop를 끄고 `engine.update()`를 연결한다.
3. camera와 uniform의 scalar/vector 변화를 animation한다.
4. seeded random으로 3D stagger/jitter를 재현 가능하게 만든다.
5. instance 수를 늘리며 CPU·GPU frame time을 기록한다.

### 산출물

- 실행 가능한 demo
- JS `animate()`와 수동 interpolation 비교표
- target count별 frame-time 기록
- pause/resume, hidden tab, cleanup test

## 공통 Review Checklist

- [ ] effect가 content hierarchy 또는 interaction feedback을 강화하는가?
- [ ] backend 선택 이유가 기록되어 있는가?
- [ ] motion reduction과 keyboard path가 있는가?
- [ ] route/component lifecycle cleanup이 검증됐는가?
- [ ] Chrome DevTools Performance trace를 확인했는가?
- [ ] representative viewport의 visual regression이 있는가?

## Sources

- [Timeline documentation](https://animejs.com/documentation/timeline/)
- [SVG documentation](https://animejs.com/documentation/svg/)
- [ScrollObserver settings](https://animejs.com/documentation/events/onscroll/scrollobserver-settings/)
- [Draggable documentation](https://animejs.com/documentation/draggable/)
- [Layout documentation](https://animejs.com/documentation/layout/)
- [Adapters documentation](https://animejs.com/documentation/adapters/)

