---
date: 2026-09-07
tags: [tech]
type: tech-tool-study
status: draft
---

# Driver.js Projects

> [[04-learning/02-deep-dive|이전: Deep Dive]] · [[README|목차]] · [[cheatsheet|다음: Cheatsheet]]

## Project 1 — Stable 3-Step Onboarding

**목표**: 실제 UI에 중앙 welcome, target 2개, Done으로 끝나는 최소 tour를 구현한다.

### 요구사항

- `[data-tour]` selector만 사용
- progress 표시와 keyboard navigation 유지
- close와 complete를 구분해 local state에 기록
- component unmount 시 `destroy()`
- mobile viewport E2E test 추가

### 완료 기준

- [ ] DOM class refactor 뒤에도 tour가 동작한다.
- [ ] 모든 step에 Next/Previous/Done이 올바르게 표시된다.
- [ ] `Escape`로 종료할 수 있다.
- [ ] 종료 뒤 overlay/listener가 남지 않는다.

## Project 2 — Async Interactive Tour

**시나리오**: 사용자가 “Create project”를 클릭하면 modal이 lazy render되고, 생성 완료 후 새 project 화면의 다음 step으로 이동한다.

```text
step 0: 설명
  ↓ advanceOnClick
step 1: Create 클릭
  ↓ modal lazy render + waitForElement
step 2: form 입력
  ↓ onNextClick + API request
step 3: route 이동
  ↓ saved resume index
step 4: 결과 확인
```

### 구현 포인트

- `waitForElement` timeout과 error message
- `onNextClick`의 in-flight 중복 방지
- API 실패 시 현재 step 유지와 retry
- route 전 `{ tourVersion, nextStepId }` 저장
- 권한 때문에 보이지 않는 optional step에만 `skipMissingElement`

### 완료 기준

- [ ] slow network와 API error를 재현한다.
- [ ] custom hook마다 `moveNext()`/`destroy()` 경로가 명확하다.
- [ ] refresh 후 잘못된 과거 tour를 재개하지 않는다.
- [ ] telemetry에서 abandon과 failure를 구분한다.

## Project 3 — Persistent Feature Hints

**목표**: 새 기능 3개에 beacon을 표시하고 dismiss 상태를 사용자별로 저장한다.

### 요구사항

- stable, versioned hint ID 사용: `export-v2`
- 로그인 전 localStorage, 로그인 후 server profile 정책 결정
- dismiss/restore 설정 화면 제공
- tour 실행 중 beacon이 숨고 종료 후 복귀하는지 확인
- `prefers-reduced-motion`과 keyboard 사용성 검증

### 완료 기준

- [ ] close와 dismiss가 서로 다르게 동작한다.
- [ ] 다른 device에서의 동기화 정책이 문서화되어 있다.
- [ ] 새 major feature를 다시 노출하는 versioning 전략이 있다.

## Project 4 — Production Readiness Audit

| 영역 | 질문 |
|---|---|
| Selector | style class가 아니라 stable contract인가? |
| Content | HTML source가 trusted/sanitized인가? |
| Accessibility | keyboard, focus, zoom, contrast, reduced motion을 확인했는가? |
| Resilience | missing target, delayed target, route/API failure를 처리하는가? |
| State | started, dismissed, completed, resumed의 저장 범위가 명확한가? |
| Analytics | tour/step version과 최소 event contract가 있는가? |
| Lifecycle | SPA unmount와 navigation에서 `destroy()`하는가? |
| Release | exact version, changelog, license를 기록했는가? |

## 권장 산출물

- `tour-registry.ts`: tour ID/version과 step definition
- `tour-analytics.ts`: vendor-neutral telemetry adapter
- `tour-storage.ts`: completion/resume/dismiss persistence
- `data-tour` selector contract 문서
- Playwright happy-path/error-path test
- keyboard와 screen reader 수동 test 기록

## Sources

- https://driverjs.com/docs/async-tour
- https://driverjs.com/docs/multi-page-tour
- https://driverjs.com/docs/hints
- https://driverjs.com/docs/configuration
- https://driverjs.com/docs/changelog

