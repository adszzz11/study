---
date: 2026-07-16
tags: [tech]
type: tech-tool-study
status: draft
---

# Archify — Deep Dive

> [[01-getting-started|이전: Getting Started]] · [[../README|목차로 돌아가기]] · [[../05-projects|다음: Projects]]

## 1. 두 execution world를 잇는 구조

Chrome content script는 기본적으로 page script와 분리된 isolated world에서 실행된다. 이 context만으로는 framework runtime internals나 page가 사용하는 `fetch`/`XMLHttpRequest`를 같은 방식으로 관찰하기 어렵다. Archify는 MAIN world 관찰과 ISOLATED world 분석을 bridge한다.

```text
Web page: MAIN world
  ├─ framework runtime internals 관찰
  ├─ fetch/XMLHttpRequest instrumentation
  └─ runtime signal 생성
            ↓ bridge
Chrome extension: ISOLATED world
  ├─ DOM 및 signal correlation
  ├─ fingerprint engine
  ├─ confidence scoring
  └─ Shadow DOM overlay / Page Profile
```

| 영역 | 책임 | 설계 이유 |
|---|---|---|
| MAIN-world script | framework 흔적, `fetch`/XHR runtime signal | page JavaScript context 접근 |
| bridge | page signal을 extension 쪽으로 전달 | execution world 경계 연결 |
| isolated content script | DOM correlation, rule 평가, UI | page script와 분리된 extension context |
| Shadow DOM overlay | hover inspector와 profile UI | 대상 페이지 CSS와 충돌 감소 |

## 2. Runtime correlation의 의미

사용자가 element를 lock하고 interaction하면 그 전후에 발생한 signal을 묶어 관계를 추론할 수 있다.

```text
element 선택
  → interaction window 시작
  → click / input / navigation
  → fetch 또는 XHR 관찰
  → route/storage 변화 관찰
  → element context와 시간적 evidence를 조합
```

이 관계는 source-level call graph와 같지 않다. 동시에 여러 component가 request를 만들거나 background polling이 실행되면 시간적 근접성만으로 false correlation이 생길 수 있다. Chrome DevTools의 initiator chain과 breakpoint로 확인한다.

## 3. Fingerprint와 confidence

Fingerprint engine은 여러 약한 signal을 조합한다.

| Signal | 예 | 한계 |
|---|---|---|
| DOM | attribute, class, element pattern | copy/customization으로 오탐 가능 |
| Global/runtime | framework hook, runtime object | production optimization과 version 차이 |
| Script | URL, bundle marker, third-party origin | bundling/self-hosting으로 흔적 변화 |
| Header | hosting/CDN 특성 | proxy와 multi-CDN 구성 |
| Network | endpoint/domain/activity | lazy load와 조건부 실행 |

Confidence score는 이 evidence의 강도를 표현해야 한다. `shadcn/ui`처럼 runtime에서 Radix primitive 등과 분리하기 어려운 기술은 명확한 확정값보다 low-confidence hint가 정직하다.

새 rule을 기여할 때는 `src/engine/`의 기존 구조를 따르고 positive/negative fixture를 함께 둔다. 탐지율만 높이고 specificity를 잃으면 Page Profile의 신뢰도가 빠르게 낮아진다.

## 4. Network coverage 경계

README의 구체적 구현 설명은 `fetch`와 `XMLHttpRequest` interception을 명시한다. 따라서 제품의 “outbound calls” 표현을 다음까지 완전 수집한다는 의미로 확대하면 안 된다.

- WebSocket
- `navigator.sendBeacon`
- `<img>`, `<script>`, `<link>` 같은 resource tag
- Service Worker 내부 통신
- browser/extension이 자체 생성한 request

정밀 조사는 Network panel, proxy, CSP reporting, dedicated client-side monitoring과 교차 검증한다.

## 5. Client-side security threat model

Sensitive-field listener는 script가 password/card field의 event를 관찰할 수 있다는 **exposure signal**이다.

```text
listener 발견
  ≠ field value를 실제로 읽음
  ≠ 외부로 전송함
  ≠ 악성 script임
```

검증 단계는 다음과 같다.

1. listener를 등록한 script와 origin을 식별한다.
2. handler가 value를 읽는지 breakpoint로 확인한다.
3. interaction 이후 network/resource activity를 기록한다.
4. CSP, SRI, dependency inventory와 대조한다.
5. legitimate payment/analytics 동작과 unauthorized behavior를 구분한다.

## 6. Privacy와 trust boundary

Archify는 backend, account, telemetry가 없고 request body/storage value 대신 metadata를 중심으로 처리한다고 설명한다. 그러나 local-first는 무권한이나 무위험을 뜻하지 않는다.

- extension code는 민감한 page runtime을 관찰할 수 있다.
- same-origin hosting header 확인 request가 한 번 발생할 수 있다.
- tab/navigation이 바뀌면 분석 state도 달라진다.
- source가 공개돼도 배포 artifact가 동일한지는 별도 검증 대상이다.

## 7. 개발 stack과 검증

| 영역 | 기술 |
|---|---|
| Extension | WXT, React, Tailwind CSS, TypeScript |
| Marketing site | Astro, Svelte, Tailwind CSS |
| Unit test | Vitest |
| Browser E2E | Playwright |
| Platform | Chrome Manifest V3 |
| Output | `.output/chrome-mv3/` |

MV3는 remotely hosted code를 허용하지 않고 background context를 service worker 중심으로 바꾼다. Archify의 MAIN-world instrumentation과 content script bridge를 이해할 때 MV3 lifecycle과 CSP constraint도 함께 봐야 한다.

## Sources

- [Archify GitHub — How it works](https://github.com/Salah-XD/archify#how-it-works)
- [Archify 기능 설명](https://archify.salahxd.dev/#how-it-works)
- [Chrome content scripts](https://developer.chrome.com/docs/extensions/develop/concepts/content-scripts)
- [Chrome Manifest V3](https://developer.chrome.com/docs/extensions/develop/migrate/what-is-mv3)
- [Archify Privacy](https://archify.salahxd.dev/privacy)

