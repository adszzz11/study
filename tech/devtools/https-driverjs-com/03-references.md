---
date: 2026-09-07
tags: [tech]
type: tech-tool-study
status: draft
---

# Driver.js References

> [[02-ecosystem|이전: Ecosystem]] · [[README|목차]] · [[04-learning/01-getting-started|다음: Getting Started]]

## 조사 기준

- 조사일: **2026-09-07**
- npm `latest`: **1.8.0**
- release: **2026-07-17**
- license: **MIT**
- runtime dependencies: **0**
- TypeScript declarations: **built-in**

다운로드 수와 repository 지표는 계속 변하므로 채택성의 보조 지표로만 취급한다.

## 공식 문서 지도

| 주제 | 링크 | 읽을 포인트 |
|---|---|---|
| Homepage | https://driverjs.com/ | library의 범위, demo, positioning |
| Installation | https://driverjs.com/docs/installation | npm/pnpm/yarn, ESM, CDN/IIFE, Hints CSS |
| Basic Usage | https://driverjs.com/docs/basic-usage | tour, single highlight, hints의 최소 예제 |
| Configuration | https://driverjs.com/docs/configuration | `Config`, `DriveStep`, `Popover`, hooks |
| API Reference | https://driverjs.com/docs/api | instance method와 state query |
| Async Tour | https://driverjs.com/docs/async-tour | async action 뒤 수동 navigation |
| Multi-Page Tour | https://driverjs.com/docs/multi-page-tour | route 사이 index 저장과 재개 |
| Popover Buttons | https://driverjs.com/docs/buttons | button hook override 규칙 |
| Popover Position | https://driverjs.com/docs/popover-position | `side`, `align`, viewport fallback |
| Theming | https://driverjs.com/docs/theming | CSS class, variable, `popoverClass` |
| Feature Hints | https://driverjs.com/docs/hints | beacon, dismiss/restore, persistence |
| Changelog | https://driverjs.com/docs/changelog | version별 breaking/change 확인 |

## Package와 Source

- npm package: https://www.npmjs.com/package/driver.js
- npm versions: https://www.npmjs.com/package/driver.js?activeTab=versions
- GitHub repository: https://github.com/nilbuild/driver.js
- 1.8.0 release: https://github.com/nilbuild/driver.js/releases/tag/1.8.0
- License: https://github.com/nilbuild/driver.js/blob/master/LICENSE
- package metadata: https://github.com/nilbuild/driver.js/blob/master/package.json

## 1.8.0 핵심 변화

- `driver.js/hints`와 독립 stylesheet로 Hints subsystem 추가
- highlighted element click으로 진행하는 `advanceOnClick`
- DOM 등장까지 대기하는 `waitForElement`
- `sideEffects` metadata로 tree-shaking 개선
- skip을 고려해 마지막 도달 가능 step의 Done 처리 수정
- build system을 Vite에서 `tsdown`으로 이전

## 검증 체크리스트

- [ ] 설치 전에 npm `latest`와 changelog를 다시 확인한다.
- [ ] copied example이 현재 major version API인지 확인한다.
- [ ] TypeScript의 실제 `Config`/`DriveStep` type을 source와 IDE에서 확인한다.
- [ ] commercial 배포 전 dependency license scan에 MIT license를 기록한다.
- [ ] bundle analyzer로 자신의 build에서 실제 포함 크기를 측정한다.
- [ ] accessibility는 공식 주장만 인용하지 않고 실제 browser/AT로 검증한다.

## Sources

- https://driverjs.com/docs/changelog
- https://www.npmjs.com/package/driver.js?activeTab=code
- https://www.npmjs.com/package/driver.js?activeTab=versions
- https://github.com/nilbuild/driver.js/releases

