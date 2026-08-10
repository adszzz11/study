---
date: 2026-08-11
tags: [tech]
type: tech-tool-study
status: draft
---

# Anime.js - Ecosystem 비교

> [[01-overview|이전: Overview]] · [[README|목차로 돌아가기]] · [[03-references|다음: References]]

## 포지션

Anime.js의 장점은 CSS·DOM·SVG·JavaScript object·Canvas/WebGL 값을 비교적 작은 modular API와 공유 playhead로 연결하는 데 있다. 모든 animation 문제의 기본 선택이라기보다 CSS와 대규모 animation platform 사이의 실용적인 중간 지점이다.

## 대안 비교

| 선택지 | 강점 | 주의점 | 잘 맞는 상황 |
|---|---|---|---|
| CSS transition / keyframes | dependency 없음, browser-native, 단순 상태 변화에 명확함 | 동적 sequencing·runtime control·object tweening이 제한적 | hover, fade, 작은 loading effect |
| Native Web Animations API | browser-native play control, CSS properties animation | cross-target orchestration과 편의 API를 직접 구성 | 작은 imperative CSS animation |
| Anime.js `waapi.animate()` | WAAPI 위에 easing·stagger·composition 편의 제공, 경량 import | DOM/CSS 중심이며 browser/property 특성에 영향 | compositor-friendly UI animation |
| Anime.js `animate()` | DOM/SVG/object, timeline, callbacks, shared engine | JS main thread 비용과 lifecycle 관리 필요 | creative coding, 복합 timeline, 많은 targets |
| Motion | React 친화적 선언형 API, layout·gesture 흐름 | framework 결합도가 높음 | React component animation과 gesture |
| GSAP | 성숙한 sequencing과 plugin ecosystem, 고난도 scroll 제작 | 더 넓은 API surface와 별도 라이선스 조건 검토 필요 | 복잡한 branded experience, ScrollTrigger 중심 작업 |

## Anime.js 내부 선택: JS vs WAAPI

```text
CSS/DOM property 중심인가?
├─ 예 → main-thread 부담이나 bundle이 중요한가?
│  ├─ 예 → waapi.animate()부터 검토
│  └─ 아니오 → timeline/callback 복잡도에 따라 양쪽 비교
└─ 아니오 → object, Canvas, WebGL, SVG attribute인가?
   └─ 예 → animate() 우선
```

| 질문 | `animate()` | `waapi.animate()` |
|---|---:|---:|
| plain object tweening | 적합 | 부적합 |
| Canvas/WebGL state | 적합 | 부적합 |
| 500개 이상 targets | 공식 문서상 우선 검토 | 개별 native animation 비용 측정 필요 |
| 복잡한 timeline/callback | 적합 | 상대적으로 제한적 |
| CSS 중심·작은 bundle | 약 10KB gzip 경로 | 약 3KB gzip 경로 |
| compositor acceleration | property/browser에 좌우 | property/browser에 좌우 |

## 선택 시나리오

### Anime.js를 고른다

- SVG path와 DOM label, Canvas state를 하나의 timeline으로 맞춘다.
- framework-independent landing page에 stagger와 spring이 필요하다.
- Three.js render loop에 animation clock을 연결한다.
- MIT license와 zero runtime dependency를 선호한다.

### CSS 또는 native WAAPI를 고른다

- button hover, accordion fade처럼 상태가 단순하다.
- dependency 추가 없이 platform primitive로 충분하다.
- animation ownership과 cleanup을 직접 관리할 수 있다.

### Motion을 고른다

- React component tree와 animation state를 선언적으로 연결한다.
- mount/unmount, shared layout, gesture가 component 설계의 중심이다.

### GSAP을 고른다

- scroll pinning과 복잡한 scene orchestration이 제품 핵심이다.
- plugin과 production 사례의 폭이 package size/API 단순성보다 중요하다.

## 평가 체크리스트

- [ ] animation target이 DOM만인가, plain object/Canvas/WebGL도 포함하는가?
- [ ] sequencing, labels, seek/reverse가 필요한가?
- [ ] framework lifecycle과 cleanup 전략이 명확한가?
- [ ] `prefers-reduced-motion` fallback이 있는가?
- [ ] transform/opacity 외 property의 layout·paint 비용을 측정했는가?
- [ ] dependency license와 bundle budget을 확인했는가?
- [ ] representative device에서 visual/performance regression을 검사했는가?

## Sources

- [Anime.js WAAPI overview](https://animejs.com/documentation/web-animation-api/)
- [Anime.js: When to use WAAPI](https://animejs.com/documentation/web-animation-api/when-to-use-waapi/)
- [MDN: Web Animations API](https://developer.mozilla.org/en-US/docs/Web/API/Web_Animations_API)
- [Motion documentation](https://motion.dev/docs)
- [GSAP documentation](https://gsap.com/docs/v3/)
- [Anime.js npm package](https://www.npmjs.com/package/animejs)

