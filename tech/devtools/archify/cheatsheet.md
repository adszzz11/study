---
date: 2026-07-16
tags: [tech]
type: tech-tool-study
status: draft
---

# Archify — Cheatsheet

> [[05-projects|이전: Projects]] · [[README|목차로 돌아가기]]

## 기본 조작

| 동작 | 목적 |
|---|---|
| element hover | component/type, UI library, evidence 확인 |
| click-to-lock | 대상 element를 고정하고 interaction 관찰 |
| `Esc` | inspector dismiss |
| toolbar → Page Profile | 전체 stack, hosting, tracker, third-party script 요약 |

## 5분 조사 순서

```text
1. Page Profile로 stack 후보 확인
2. 핵심 element hover
3. confidence + evidence 기록
4. click-to-lock 후 interaction
5. fetch/XHR, route, storage key 연결 확인
6. Chrome DevTools에서 교차 검증
```

## 결과 해석

| 표시 | 해석 | 검증 도구 |
|---|---|---|
| component name | runtime에서 관찰 가능한 symbol 후보 | React/Vue DevTools, source map |
| component type only | production minification 가능 | framework DevTools, repository |
| technology fingerprint | 복수 runtime/DOM/script signal의 추론 | Sources, globals, headers |
| low confidence | 약한 hint, 확정 아님 | 독립 evidence 추가 |
| API correlation | interaction 근처 `fetch`/XHR | Network initiator/body/header |
| sensitive-field listener | 접근 가능성 signal | breakpoint, actual data flow |

## 탐지 범주

- Framework/runtime: React, Next.js, Vue, Nuxt, Angular, Svelte/SvelteKit
- UI/styling: MUI, Radix UI, Tailwind CSS 등
- Analytics/tracking: tag manager, tracking pixel
- Platform: commerce/payment, CMS/site builder, hosting/CDN
- Infrastructure: authentication, observability, bot defense

## 믿어도 되는 범위

```text
Archify 결과 = 조사 가설 + evidence + confidence
Archify 결과 ≠ source-level architecture의 완전한 복원
Archify 결과 ≠ 보안 침해의 단독 증거
```

## Network 한계

구현 설명에서 명시된 핵심 관찰 대상:

- `fetch`
- `XMLHttpRequest`

완전 수집을 가정하지 말아야 할 대상:

- WebSocket
- `navigator.sendBeacon`
- resource tag request
- Service Worker 내부 통신

## 보안 triage 판정표

| 관찰 | 다음 행동 |
|---|---|
| unknown third-party script | origin, owner, integrity/CSP 확인 |
| password/card field listener | handler breakpoint, value read 확인 |
| outbound domain | request initiator와 payload 확인 |
| suspicious sequence | proxy/client-side monitoring으로 재현 |

## 조직 도입 체크

- [ ] source와 license 검토
- [ ] manifest permission 검토
- [ ] 배포 artifact/source version 일치 검토
- [ ] 내부 page 사용 정책 확인
- [ ] telemetry 없음과 same-origin header request 조건 확인
- [ ] extension/version update 재평가 절차 마련

## 개발 메모

| 항목 | 값 |
|---|---|
| Extension stack | WXT + React + Tailwind CSS + TypeScript |
| Unit test | Vitest |
| Browser E2E | Playwright |
| Target | Chrome Manifest V3 |
| Build output | `.output/chrome-mv3/` |

## Sources

- [Archify 공식 사이트](https://archify.salahxd.dev/)
- [Archify GitHub](https://github.com/Salah-XD/archify)
- [Archify Privacy](https://archify.salahxd.dev/privacy)
- [Chrome content scripts](https://developer.chrome.com/docs/extensions/develop/concepts/content-scripts)

