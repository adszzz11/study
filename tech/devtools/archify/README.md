---
date: 2026-07-16
tags: [tech]
type: tech-tool-study
status: draft
---

# Archify

> **한 줄 정의**: Archify는 실행 중인 웹 페이지의 DOM, framework internals, network activity, third-party scripts를 결합해 component/API/tech stack/client-side exposure를 보여주는 open-source, local-first Chrome Manifest V3 extension이다.

## Overview

Archify는 여러 DevTools panel에 흩어진 runtime signal을 element 중심의 system view로 묶는다. 페이지의 버튼이나 입력 필드를 가리키면 가능한 component type, UI library, 상호작용 뒤의 API request, storage key, route transition을 연관 지어 보여준다.

```text
DOM element
  → React/Vue component 또는 component type
  → UI library
  → click 이후 발생한 fetch/XHR
  → storage key
  → route transition
```

- AI/LLM 제품이 아니라 `runtime instrumentation + fingerprint rules + confidence scoring` 기반 도구다.
- backend, account, telemetry 없이 tab 안에서 분석하는 local-first 모델을 지향한다.
- 2026-07-16 기준 Chrome Web Store `v0.2.0`의 초기 프로젝트다.
- production build의 minification 때문에 실제 component name을 항상 복원할 수는 없다.

## Learning Path

- [ ] [[01-overview|Overview]] — What/Why, 핵심 기능과 한계
- [ ] [[02-ecosystem|Ecosystem]] — Chrome DevTools, framework DevTools, Wappalyzer 계열과 비교
- [ ] [[03-references|References]] — 공식 문서와 검증 자료
- [ ] [[04-learning/01-getting-started|Getting Started]] — 설치, 기본 inspection, 교차 검증
- [ ] [[04-learning/02-deep-dive|Deep Dive]] — MV3 execution world, correlation, fingerprint와 security model
- [ ] [[05-projects|Projects]] — SPA reverse engineering과 client-side exposure triage
- [ ] [[cheatsheet|Cheatsheet]] — 빠른 사용 순서와 판단 기준

## When To Use

- 낯선 SPA에서 특정 element가 어느 framework/component와 연결되는지 빠르게 탐색할 때
- UI interaction 뒤의 `fetch`/XHR와 route/storage 변화를 초기에 추적할 때
- 페이지의 framework, hosting, analytics, payment 등 tech stack을 한눈에 가설화할 때
- third-party script와 sensitive field listener를 client-side security triage 신호로 볼 때
- DevTools의 정밀 조사 전에 조사 범위와 가설을 좁힐 때

## When Not To Use

- request/response body, headers, timing, initiator를 포함한 완전한 network debugging이 필요할 때
- WebSocket, `sendBeacon`, resource tag, Service Worker 통신까지 빠짐없이 수집해야 할 때
- minified production bundle에서 정확한 component name을 보장해야 할 때
- listener 존재만으로 악성 행위나 data exfiltration을 입증하려 할 때
- 검증된 enterprise security scanner나 compliance evidence가 필요할 때

## Related Notes

- [[MOCs/Index]]
- [[MOCs/Devtools]]
- [[tech/devtools/ripgrep/README|ripgrep]] — Archify source와 detection rule을 탐색할 때 유용한 code search tool
- [[tech/scraping/browserless/README|Browserless]] — browser runtime automation과 관찰 맥락

## Sources

- [Archify 공식 사이트](https://archify.salahxd.dev/)
- [Salah-XD/archify GitHub](https://github.com/Salah-XD/archify)
- [Chrome Web Store — Archify](https://chromewebstore.google.com/detail/archify/nhangkbdjnopgkgklfdkpfgmendlckpe)
- [Archify Privacy](https://archify.salahxd.dev/privacy)
- [Chrome Extensions — Content scripts](https://developer.chrome.com/docs/extensions/develop/concepts/content-scripts)

