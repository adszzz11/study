---
date: 2026-08-11
tags: [tech]
type: tech-tool-study
status: draft
---

# Anime.js - References

> [[02-ecosystem|이전: Ecosystem]] · [[README|목차로 돌아가기]] · [[04-learning/01-getting-started|다음: Getting Started]]

## 공식 시작점

| 자료 | 읽을 이유 |
|---|---|
| [Documentation](https://animejs.com/documentation/) | v4 API의 현재 source of truth |
| [GitHub README](https://github.com/juliangarnier/anime) | 설치, package 정체성, 기본 예시 |
| [npm](https://www.npmjs.com/package/animejs) | 배포 버전과 package metadata 확인 |
| [package.json](https://raw.githubusercontent.com/juliangarnier/anime/master/package.json) | exports, types, dependency, license 직접 확인 |
| [Releases](https://github.com/juliangarnier/anime/releases) | breaking change와 feature 단위 upgrade 검토 |

## API별 문서

- [Animation](https://animejs.com/documentation/animation/)
- [Timeline](https://animejs.com/documentation/timeline/)
- [Engine](https://animejs.com/documentation/engine/)
- [Scope](https://animejs.com/documentation/scope/)
- [Web Animation API](https://animejs.com/documentation/web-animation-api/)
- [Draggable](https://animejs.com/documentation/draggable/)
- [ScrollObserver settings](https://animejs.com/documentation/events/onscroll/scrollobserver-settings/)
- [Layout](https://animejs.com/documentation/layout/)
- [SVG](https://animejs.com/documentation/svg/)
- [Adapters](https://animejs.com/documentation/adapters/)

## Migration과 release watch

| 주제 | 체크 포인트 |
|---|---|
| v3 → v4 | global `anime()` 예시인지 먼저 확인하고 v4 named import로 변환 |
| v4.3 | `createLayout()` 도입과 layout state capture 방식 확인 |
| v4.4 | transform render order 변경에 따른 visual regression 확인 |
| v4.5.0 | `registerAdapter()`, Three.js adapter, 3D stagger grid, seeded random/jitter 확인 |

- [v3 to v4 Migration Guide](https://github.com/juliangarnier/anime/wiki/Migrating-from-v3-to-v4)
- [v4.5.0 release](https://github.com/juliangarnier/anime/releases/tag/v4.5.0)

## Platform과 비교 자료

- [MDN: Web Animations API](https://developer.mozilla.org/en-US/docs/Web/API/Web_Animations_API)
- [MDN: prefers-reduced-motion](https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-reduced-motion)
- [Motion docs](https://motion.dev/docs)
- [GSAP docs](https://gsap.com/docs/v3/)

## 권장 읽기 순서

1. [[01-overview]]에서 target·engine·backend 구분을 익힌다.
2. 공식 Animation과 Timeline 문서의 runnable examples를 실행한다.
3. Scope에서 cleanup과 media query를 확인한다.
4. WAAPI 선택 기준을 읽고 같은 effect를 두 backend로 측정한다.
5. 필요한 interaction에 따라 Scroll, Draggable, Layout, SVG로 확장한다.
6. upgrade 전 Releases와 migration guide를 확인한다.

## 조사 메모

- 조사 기준일: 2026-08-11
- 확인 버전: `4.5.0`
- 라이선스: MIT
- runtime dependency: 0
- version 숫자는 노트의 영구 사실이 아니므로 실제 도입 시 npm과 Releases를 다시 확인한다.

## Sources

- [Anime.js documentation](https://animejs.com/documentation/)
- [Anime.js GitHub repository](https://github.com/juliangarnier/anime)
- [Anime.js releases](https://github.com/juliangarnier/anime/releases)
- [animejs on npm](https://www.npmjs.com/package/animejs)
- [Anime.js package exports](https://raw.githubusercontent.com/juliangarnier/anime/master/package.json)

