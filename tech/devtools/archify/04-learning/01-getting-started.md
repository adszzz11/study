---
date: 2026-07-16
tags: [tech]
type: tech-tool-study
status: draft
---

# Archify — Getting Started

> [[../03-references|이전: References]] · [[../README|목차로 돌아가기]] · [[02-deep-dive|다음: Deep Dive]]

## 1. 설치 전 확인

Archify는 page runtime을 관찰하는 extension이다. 개인 환경에서는 Chrome Web Store 설치가 가장 간단하지만, 조직 환경에서는 먼저 다음을 검토한다.

- extension source와 Apache-2.0 license
- `manifest.json`의 host/extension permissions
- Web Store artifact와 검토한 source version의 일치 여부
- 민감한 내부 페이지에서 extension 사용을 허용하는 조직 정책

## 2. 설치 방법

### Chrome Web Store

1. [Archify listing](https://chromewebstore.google.com/detail/archify/nhangkbdjnopgkgklfdkpfgmendlckpe)을 연다.
2. 게시자, version, 최근 업데이트, permission을 확인한다.
3. extension을 설치하고 테스트용 public page에서 먼저 실행한다.

### Source에서 개발용 build

Repository의 현재 script와 package manager는 README/package metadata를 우선한다. 공식 설명상 extension은 WXT, React, Tailwind CSS, TypeScript를 사용하며 build output은 `.output/chrome-mv3/`이다.

```text
1. repository clone
2. dependency install
3. repository에 정의된 build command 실행
4. chrome://extensions 에서 Developer mode 활성화
5. Load unpacked로 .output/chrome-mv3/ 선택
```

명령 이름을 추측해 고정하지 말고 clone한 revision의 `README.md`와 `package.json`을 확인한다.

## 3. 첫 inspection

테스트용 SPA를 열고 다음 순서로 관찰한다.

1. Archify inspector를 활성화한다.
2. button 또는 input을 hover한다.
3. overlay에서 framework/component type, UI library, confidence/evidence를 읽는다.
4. element를 click-to-lock한 뒤 실제 interaction을 수행한다.
5. 연결된 `fetch`/XHR, storage key, route transition이 나타나는지 본다.
6. `Esc`로 inspector를 닫는다.
7. toolbar의 **Page Profile**에서 전체 stack과 third-party script를 확인한다.

```text
관찰 기록 예시
- Element: Login button
- Component: Button type / name unavailable
- UI hint: Radix UI (low confidence)
- Interaction: POST /api/login
- Route: /dashboard
- Verification: DevTools Network에서 request initiator 확인
```

## 4. 결과 읽는 법

| 결과 | 올바른 해석 | 다음 확인 |
|---|---|---|
| component name 발견 | development symbol과 runtime evidence가 보임 | framework DevTools/tree와 대조 |
| component type만 표시 | production minification 가능성 | source map 또는 repository 확인 |
| UI library low confidence | fingerprint hint | DOM attribute/style/source 확인 |
| API correlation | interaction 시간대의 `fetch`/XHR 연관 | Network initiator와 payload 확인 |
| sensitive-field listener | 접근 가능성/관찰 signal | listener source와 실제 data flow 확인 |

## 5. 교차 검증 실습

### API request

- Archify에서 method와 URL을 기록한다.
- Chrome DevTools Network에서 같은 request의 header, body, timing, initiator를 확인한다.
- redirect, preflight, Service Worker 개입 여부를 확인한다.

### Component

- Archify의 name/type/confidence를 기록한다.
- React/Vue DevTools에서 실제 component tree를 확인한다.
- production build라 name이 없으면 실패가 아니라 관찰 한계로 기록한다.

### Security signal

- listener가 붙은 sensitive field와 script origin을 기록한다.
- DevTools Sources/Event Listeners와 Network에서 동작을 재현한다.
- listener 존재와 실제 value read/exfiltration을 분리해 결론 낸다.

## 6. 첫날 체크리스트

- [ ] public test page에서 extension 동작 확인
- [ ] hover → click-to-lock → `Esc` workflow 수행
- [ ] Page Profile의 stack claim 3개를 수동 검증
- [ ] interaction 1개와 `fetch`/XHR 1개를 Network panel에서 대조
- [ ] confidence와 evidence를 함께 기록
- [ ] 미탐지와 오탐을 구분해 메모

## Sources

- [Archify 공식 사이트](https://archify.salahxd.dev/)
- [Chrome Web Store](https://chromewebstore.google.com/detail/archify/nhangkbdjnopgkgklfdkpfgmendlckpe)
- [Archify GitHub](https://github.com/Salah-XD/archify)
- [Chrome — Load an unpacked extension](https://developer.chrome.com/docs/extensions/get-started/tutorial/hello-world#load-unpacked)

