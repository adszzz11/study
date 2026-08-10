---
date: 2026-08-11
tags: [tech]
type: tech-tool-study
status: draft
---

# Anime.js - Getting Started

> [[../03-references|이전: References]] · [[../README|목차로 돌아가기]] · [[02-deep-dive|다음: Deep Dive]]

## 1. 설치

```bash
npm install animejs
```

전체 entry 또는 기능별 subpath에서 import할 수 있다.

```js
import { animate, stagger, createTimeline } from 'animejs';

// bundle 구성을 더 명시하고 싶을 때
import { animate } from 'animejs/animation';
import { createTimeline } from 'animejs/timeline';
```

> 오래된 예제의 `import anime from 'animejs'`와 `anime({...})`는 v3 문법일 수 있다. v4에서는 named import와 `animate()`를 기준으로 시작한다.

## 2. 첫 animation

```html
<button id="replay">Replay</button>
<div class="dot"></div>
```

```css
.dot {
  width: 2rem;
  aspect-ratio: 1;
  border-radius: 50%;
  background: currentColor;
}
```

```js
import { animate } from 'animejs';

const play = () => animate('.dot', {
  x: [0, 240],
  rotate: '1turn',
  scale: [0.7, 1],
  duration: 900,
  ease: 'inOutExpo',
});

document.querySelector('#replay').addEventListener('click', play);
play();
```

배열 값은 `[from, to]`를 명시한다. 명시하지 않은 시작 값은 현재 computed state에 의존하므로 재실행 결과를 예측하기 어렵다면 시작 값을 고정한다.

## 3. Stagger

```js
import { animate, stagger } from 'animejs';

animate('.grid .cell', {
  scale: [0, 1],
  opacity: [0, 1],
  delay: stagger(55, { grid: [8, 5], from: 'center' }),
  duration: 500,
  ease: 'outBack',
});
```

- `stagger()`는 target마다 delay 또는 value를 분배한다.
- DOM order가 motion order가 되므로 접근성상 읽기 순서와 시각 순서를 어긋나게 만들지 않는다.

## 4. Timeline

```js
import { createTimeline } from 'animejs';

const intro = createTimeline({
  defaults: { duration: 600, ease: 'outQuad' },
});

intro
  .label('intro')
  .add('.title', { y: [-24, 0], opacity: [0, 1] })
  .add('.card', { scale: [0.9, 1], opacity: [0, 1] }, '<-=200')
  .call(() => console.log('ready'));
```

Timeline은 absolute time, relative position, label을 이용해 animation·timer·callback·다른 timeline을 하나의 playhead에 둔다. magic delay를 흩뿌리기보다 label과 relative position으로 의도를 표현한다.

## 5. WAAPI backend 맛보기

```js
import { waapi, stagger } from 'animejs';

waapi.animate('.toast', {
  opacity: [0, 1],
  y: [12, 0],
  delay: stagger(60),
  duration: 350,
  ease: 'outQuad',
});
```

CSS property 중심의 짧은 animation은 WAAPI backend와 비교한다. 이름만 WAAPI라고 무조건 GPU accelerated 되는 것은 아니다. `transform`·`opacity`를 우선하고 browser Performance panel에서 확인한다.

## 6. Reduced motion

```js
const reduceMotion = matchMedia('(prefers-reduced-motion: reduce)').matches;

animate('.panel', {
  opacity: [0, 1],
  y: reduceMotion ? 0 : [20, 0],
  duration: reduceMotion ? 1 : 500,
  ease: 'outQuad',
});
```

reduced motion은 모든 정보를 숨기는 옵션이 아니다. 큰 이동·회전·parallax를 제거하되 상태 변화는 opacity나 즉시 전환으로 전달한다. component 단위 프로젝트에서는 다음 단계의 `createScope()` media queries를 사용한다.

## 7. 완료 체크

- [ ] v4 named imports로 example을 실행했다.
- [ ] transform, opacity, stagger를 조합했다.
- [ ] label과 overlap이 있는 timeline을 만들었다.
- [ ] JS와 WAAPI backend의 차이를 설명할 수 있다.
- [ ] reduced-motion mode에서 의미가 유지되는지 확인했다.
- [ ] DevTools에서 layout/paint와 frame drop을 관찰했다.

## Sources

- [Anime.js installation](https://animejs.com/documentation/getting-started/installation/)
- [Animation documentation](https://animejs.com/documentation/animation/)
- [Timeline documentation](https://animejs.com/documentation/timeline/)
- [Stagger utility](https://animejs.com/documentation/utilities/stagger/)
- [Web Animation API](https://animejs.com/documentation/web-animation-api/)
- [MDN: prefers-reduced-motion](https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-reduced-motion)

