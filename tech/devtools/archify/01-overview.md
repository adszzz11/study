---
date: 2026-07-16
tags: [tech]
type: tech-tool-study
status: draft
---

# Archify — What, Why, 특징

> [[README|목차로 돌아가기]] · [[02-ecosystem|다음: Ecosystem]]

## What

Archify는 현재 열린 웹 페이지를 runtime에서 관찰하는 open-source Chrome extension이다. DOM만 정적으로 읽는 대신 framework internals, scripts, headers, network activity를 조합해 element와 애플리케이션 구조 사이의 관계를 추론한다.

주요 결과는 두 가지 UI로 제공된다.

- **Hover inspector**: element별 component type/name, UI library, 관련 API와 evidence
- **Page Profile**: 페이지 전체의 framework, hosting/CDN, tracker, commerce/payment 등 stack 요약

Archify는 source code를 보고 설계를 완전히 복원하거나 component name을 생성하는 AI가 아니다. 관찰 가능한 runtime evidence에 fingerprint rule과 confidence score를 적용한다.

## Why

현대 SPA를 역으로 이해하려면 보통 여러 도구를 오간다.

| 질문 | 주로 확인하는 곳 |
|---|---|
| 이 DOM은 어떤 component인가? | Elements + React/Vue DevTools |
| click 뒤 어떤 API가 호출되는가? | Network panel |
| 어떤 stack과 tracker를 쓰는가? | Sources/Application + fingerprinting tool |
| 어떤 third-party script가 form field를 보는가? | Sources/Network + 별도 security inspection |

AI-generated code와 복잡한 SPA에서는 코드를 만드는 비용 못지않게 component, API, script 사이의 연결을 이해하는 비용이 크다. Archify의 핵심 가치는 이 signal들을 **element 중심 system view**로 압축해 첫 조사 시간을 줄이는 데 있다.

## 핵심 특징

### Architecture intelligence

- DOM element hover, click-to-lock, `Esc` dismiss
- React, Next.js, Vue, Nuxt, Angular, Svelte/SvelteKit 탐지
- development build에서 실제 component name 탐색
- MUI, Radix UI, Tailwind CSS 등 UI/styling fingerprint
- element interaction과 `fetch`/XHR request의 runtime correlation
- evidence와 confidence를 동반한 판단 지향

> [!warning] Production build
> minify/mangle된 symbol은 복구할 수 없다. 이 경우 component type과 confidence만 표시될 수 있으며, 확인되지 않은 이름을 사실처럼 받아들이면 안 된다.

### Technology fingerprint

공식 설명은 100개 이상의 fingerprint를 사용한다고 밝힌다.

- framework/runtime, UI library, CSS framework
- analytics, tag manager, tracking pixel
- commerce/payment, CMS/site builder
- hosting/CDN, authentication, observability, bot defense

HTML 문자열 하나가 아니라 DOM, globals/runtime 흔적, script, header, network activity를 조합한다. `shadcn/ui`처럼 runtime에서 기반 primitive와 분리하기 어려운 항목은 낮은 confidence hint가 적절하다.

### Client-side security view

- third-party scripts와 outbound domain/call 목록
- password/card input 같은 sensitive field에 listener를 등록한 script
- form/payment field access에 대한 exposure signal

이는 supply-chain script나 skimmer-like behavior를 찾는 **triage**에 유용하지만 악성 여부를 확정하지 않는다. listener가 존재한다는 사실은 data read나 exfiltration의 증거와 다르다.

### Local-first와 privacy

- backend server, account, telemetry, analytics 없음
- body/value 대신 method, URL, status, storage key 같은 metadata 중심
- 분석 상태는 tab/navigation lifecycle에 종속
- hosting header 확인을 위해 현재 URL로 same-origin request를 한 번 보낼 수 있음
- Apache-2.0 license

Local-first는 cloud 전송 위험을 낮추지만 extension이 page runtime을 관찰하는 높은 권한을 가진다는 사실은 바꾸지 않는다. 조직 배포 전 source, manifest permission, 배포 artifact의 일치 여부를 검토해야 한다.

## 현재 성숙도

조사 기준일은 2026-07-16이다. Chrome Web Store에는 `v0.2.0`(2026-07-03 업데이트), 약 230 users로, GitHub에는 22 stars와 2 forks로 표시됐다. 따라서 enterprise-standard scanner보다 빠르게 성장 중인 실험적 developer tool로 평가하는 편이 안전하다.

## Sources

- [Archify 공식 사이트](https://archify.salahxd.dev/)
- [GitHub README](https://github.com/Salah-XD/archify)
- [Chrome Web Store](https://chromewebstore.google.com/detail/archify/nhangkbdjnopgkgklfdkpfgmendlckpe)
- [Privacy 설명](https://archify.salahxd.dev/privacy)
- [Apache-2.0 License](https://github.com/Salah-XD/archify/blob/master/LICENSE)

