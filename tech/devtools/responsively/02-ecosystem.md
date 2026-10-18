---
date: 2026-10-18
tags: [tech]
type: tech-tool-study
status: draft
---

# Responsively — Ecosystem

[[tech/devtools/responsively/README|학습 진입점]] · 이전: [[tech/devtools/responsively/01-overview|Overview]]

## 비교

| 도구 | 적합한 상황 | 강점 | 한계 |
|---|---|---|---|
| **Responsively** | 로컬 개발 중 반복 responsive 확인 | 무료·오픈소스, 동시 multi-viewport, mirrored interaction, MCP | Chromium 계열 preview 중심, 실기기·실제 Safari 검증 아님 |
| **Chrome DevTools Device Mode** | 즉석 breakpoint debugging | 기본 탑재, CPU/network throttling·sensor simulation | 한 번에 보는 viewport가 제한적이고 desktop simulation |
| **Polypane** | responsive + accessibility/SEO 품질 점검 | 다중 pane, accessibility·meta·quality workflow가 넓음 | 상용 제품, 유료 도입 검토 필요 |
| **Playwright** | CI breakpoint regression 자동화 | device parameter, Chromium/Firefox/WebKit, code 기반 test | interactive visual 작업대가 아닌 test framework |
| **BrowserStack Live/Responsive** | 출시 전 실제 device/browser matrix 검증 | real-device cloud, cross-browser/iOS 검증 | 비용·원격 환경 의존, 로컬 반복 개발에는 무거움 |

## 권장 조합

```text
개발 중 빠른 발견  →  Responsively
CI 회귀 방지       →  Playwright screenshot / assertion
출시 전 최종 확인  →  BrowserStack 또는 보유 실기기
```

이는 도구의 역할을 분리한 학습용 기준이다. 팀의 browser support policy, CI 시간, 실기기 보유 현황에 따라 대상 device와 빈도를 정한다.

## 선택 질문

- 한 화면의 CSS가 몇 개 viewport에서 동시에 어떻게 달라지는지 봐야 하는가? → Responsively
- network throttling, geolocation, sensor 값까지 즉시 바꿔야 하는가? → Chrome DevTools
- 변경을 pull request마다 자동 비교해야 하는가? → Playwright
- 실제 Safari/iOS 또는 Android의 browser·hardware 차이를 확인해야 하는가? → BrowserStack 또는 실기기

## Sources

- [Responsively App](https://responsively.app/)
- [Chrome DevTools Device Mode](https://developer.chrome.google.cn/docs/devtools/device-mode?hl=en)
- [Polypane documentation](https://polypane.app/docs/)
- [Playwright emulation](https://playwright.dev/docs/next/emulation)
- [BrowserStack Responsive Testing](https://www.browserstack.com/docs/testing-toolkit/responsive-testing)
