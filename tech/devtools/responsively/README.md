---
date: 2026-10-18
tags: [tech]
type: tech-tool-study
status: draft
---

# Responsively

> **한 줄 정의**: Responsively App은 여러 device viewport를 한 창에 동시에 띄우고 interaction을 동기화해 responsive web UI를 빠르게 점검하는 무료·오픈소스 Electron browser DevTool이다.

## Overview

Breakpoint마다 DevTools 창을 바꾸고 같은 click·scroll·form 입력을 반복하는 일을 줄인다. 하나의 URL을 mobile, tablet, desktop viewport에 병렬로 렌더링하고, 활성 preview 사이의 interaction을 mirror한다.

- **개발 중 발견:** `Preview Suite`로 자주 보는 device 조합을 저장하고 즉시 전환한다.
- **시각 확인:** screenshot, ruler·guide, rotation, color-blindness simulation, mockup overlay를 쓴다.
- **검사:** Unified Inspector로 같은 element의 viewport별 차이를 비교한다.
- **자동화 연결:** 실행 중인 app은 localhost MCP endpoint를 제공해 AI coding agent의 visual verification에 쓸 수 있다.

Responsively는 Chromium 기반 emulation/preview 도구다. 실제 iOS Safari, Android browser, hardware·keyboard 동작은 실기기 또는 real-device cloud로 최종 확인한다.

## Learning Path

- [ ] [[tech/devtools/responsively/01-overview|1. Overview]] — What/Why와 기능 경계 이해하기
- [ ] [[tech/devtools/responsively/02-ecosystem|2. Ecosystem]] — DevTools·Polypane·Playwright·BrowserStack과 역할 나누기
- [ ] [[tech/devtools/responsively/03-references|3. References]] — 공식 문서와 검증 근거 확인하기
- [ ] [[tech/devtools/responsively/04-learning/01-getting-started|4. Getting started]] — local URL을 세 viewport에서 점검하기
- [ ] [[tech/devtools/responsively/04-learning/02-deep-dive|5. Deep dive]] — breakpoint suite, screenshot, MCP 검증 흐름 만들기
- [ ] [[tech/devtools/responsively/05-projects|6. Projects]] — Design-system QA와 PR review에 적용하기
- [ ] [[tech/devtools/responsively/cheatsheet|7. Cheatsheet]] — 반복 점검 항목을 빠르게 복습하기

## When To Use

- 로컬 개발 중 여러 breakpoint의 layout·overflow·CTA 노출을 빠르게 비교할 때
- 동일한 navigation, scroll, form 입력을 mobile/tablet/desktop에서 함께 확인할 때
- Storybook, component route, PR 변경 화면의 screenshot set을 만들 때
- AI agent가 local UI를 screenshot과 DOM text로 검증하도록 할 때

## When Not To Use

- 실제 iOS Safari·Android browser·hardware keyboard 동작을 확정해야 할 때
- CI에서 cross-browser regression을 코드로 차단하려는 경우: Playwright 같은 test framework를 병행한다.
- network, sensor, performance 조건을 세밀하게 emulation해야 할 경우: Chrome DevTools 또는 전용 도구를 먼저 검토한다.
- 인증된 원격 device matrix의 출시 전 검증이 필요한 경우: BrowserStack 또는 보유 실기기를 사용한다.

## Related Notes

- [[MOCs/Index]]
- [[MOCs/Devtools]]
- [[tech/scraping/playwright/README|Playwright]] — 재현한 viewport를 CI visual regression test로 옮길 때 연결된다.

## Sources

- [Responsively App](https://responsively.app/)
- [Download and releases](https://responsively.app/download)
- [Responsively App GitHub repository](https://github.com/responsively-org/responsively-app)
- [Chrome DevTools Device Mode](https://developer.chrome.google.cn/docs/devtools/device-mode?hl=en)
- [Playwright emulation](https://playwright.dev/docs/next/emulation)
