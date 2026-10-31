---
date: 2026-09-07
tags: [tech]
type: tech-tool-study
status: draft
---

# Driver.js

> **한 줄 정의**: Driver.js는 Web UI의 특정 DOM element를 spotlight로 강조하고 popover를 배치하여 product tour, contextual help, feature hint를 구현하는 경량·dependency-free Vanilla TypeScript library다.

## Overview

- **핵심 문제**: 사용자가 복잡한 UI에서 기능의 위치와 작업 순서를 발견하기 어렵다.
- **해결 방식**: overlay, spotlight cutout, popover, navigation을 현재 화면 위에 조합한다.
- **세 가지 모드**: 순차적 product tour, 단일 `highlight()`, 독립적인 `driver.js/hints`.
- **개발 모델**: framework 전용 component가 아닌 imperative DOM API다.
- **2026-09-07 기준**: npm stable `1.8.0`, MIT, runtime dependency 0개, built-in TypeScript declarations, tour core 약 5 KB gzip이다.
- **제품 포지션**: 완성형 product-adoption SaaS가 아니라 application 안에 직접 조립하는 UI primitive에 가깝다.

```text
Config + DriveStep[]
        ↓
driver() instance
        ↓
target resolver (selector | Element | function)
        ↓
overlay + spotlight + popover + lifecycle hooks
        ↓
moveNext() / movePrevious() / moveTo() / destroy()
```

## Learning Path

- [ ] [[01-overview|1. What/Why와 핵심 특징]]
- [ ] [[02-ecosystem|2. 대안 및 product-adoption SaaS와 비교]]
- [ ] [[03-references|3. 공식 문서 지도와 참고자료]]
- [ ] [[04-learning/01-getting-started|4. 설치와 첫 tour 만들기]]
- [ ] [[04-learning/02-deep-dive|5. async UI, lifecycle, hints, 운영 설계]]
- [ ] [[05-projects|6. 실전 프로젝트로 검증하기]]
- [ ] [[cheatsheet|7. API와 설정 빠르게 찾기]]

## When To Use

- SaaS dashboard나 복잡한 업무 UI에 짧은 in-app onboarding이 필요할 때
- 특정 기능을 spotlight와 contextual popover로 설명할 때
- 사용자가 highlighted element를 실제로 조작하는 interactive tutorial을 만들 때
- framework와 무관한 작은 bundle, MIT license, 세밀한 lifecycle 제어가 중요할 때
- tour content, 완료 상태, analytics를 application이 직접 소유하려 할 때
- 새 기능을 순서 없이 발견하게 하는 dismissible feature hint가 필요할 때

## When Not To Use

- non-developer가 tour를 편집할 CMS와 remote publishing이 필요할 때
- segmentation, A/B test, funnel analytics, localization workflow가 제품 요구사항의 핵심일 때
- 여러 페이지와 여러 서비스에 걸친 onboarding 운영을 별도 orchestration 없이 해결하려 할 때
- 단순한 form validation이나 영구 도움말이면 충분할 때
- selector 안정성, accessibility, content sanitization을 관리할 여력이 없을 때
- 사용자를 빠져나갈 수 없는 강제 tour에 묶으려 할 때

## Related Notes

- [[MOCs/Index]]
- [[MOCs/Devtools]]
- [[tech/scraping/playwright/README|Playwright]] - tour의 selector와 navigation을 end-to-end test하는 도구
- [[tech/devtools/qa/danal-auto-testing-tool|QA 자동화]] - onboarding regression을 검증하는 맥락

## Sources

- https://driverjs.com/
- https://driverjs.com/docs/basic-usage
- https://driverjs.com/docs/configuration
- https://driverjs.com/docs/hints
- https://driverjs.com/docs/changelog
- https://www.npmjs.com/package/driver.js?activeTab=versions
- https://github.com/nilbuild/driver.js/releases/tag/1.8.0

