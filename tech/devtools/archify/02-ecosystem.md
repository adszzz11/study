---
date: 2026-07-16
tags: [tech]
type: tech-tool-study
status: draft
---

# Archify — Ecosystem과 비교

> [[01-overview|이전: Overview]] · [[README|목차로 돌아가기]] · [[03-references|다음: References]]

## 포지션

Archify의 차별점은 각 영역에서 가장 상세한 정보를 제공하는 것이 아니라, **element → component → API → stack/security signal**을 하나의 탐색 흐름으로 묶는 데 있다. 정밀 debugger나 전문 scanner를 대체하기보다 초기에 가설과 조사 범위를 좁히는 도구다.

## 비교

| 도구 | 주된 관점 | Component 분석 | Network/API | Tech fingerprint | Client-side security | 처리 위치/특징 |
|---|---|---:|---:|---:|---:|---|
| **Archify** | element에서 system relation으로 이동 | 다중 framework, build 상태에 따라 정확도 변동 | `fetch`/XHR runtime correlation | 100+ fingerprints 주장 | third-party script, sensitive-field listener | local-first extension, 초기 단계 |
| **Chrome DevTools** | browser 구현과 debugging 전반 | framework 의미론은 제한적 | body, header, timing, initiator 등 가장 상세 | 자동 stack 요약은 핵심 기능 아님 | Security/Application/Network에서 수동 조사 | Chrome 내장, 강력하지만 panel별 분산 |
| **React Developer Tools** | React component semantics | React tree, props, state, profiler에 강함 | 일반 API correlation은 핵심 기능 아님 | React 외 stack 탐지 아님 | 보안 분석 도구 아님 | React 앱의 정밀 component debugging |
| **Vue Devtools** | Vue component semantics | Vue tree, state, event와 performance에 강함 | 일반 API correlation은 제한적 | Vue 외 stack 탐지 아님 | 보안 분석 도구 아님 | Vue/Nuxt 앱의 정밀 debugging |
| **Wappalyzer 계열** | site-level technology fingerprint | element-component 연결 없음 | interaction별 API 연결 없음 | 넓은 technology catalog | 제한적 | 빠른 stack inventory에 적합 |
| **Burp Suite / OWASP ZAP** | HTTP traffic과 web security testing | framework component 의미론 없음 | proxy 기반 정밀 관찰·조작 | 부차적 | 취약점 조사와 active testing | 전문 보안 도구, 설정과 범위 통제 필요 |

## 선택 가이드

### Archify가 먼저인 경우

- 낯선 화면에서 특정 element가 어떤 runtime 구조와 연결되는지 빠르게 알고 싶다.
- component와 click 이후 request의 상관관계를 짧은 시간 안에 가설화한다.
- stack inventory와 client-side exposure signal을 한 화면에서 함께 훑는다.

### Chrome DevTools가 먼저인 경우

- request/response payload, header, cookie, timing, initiator chain이 필요하다.
- DOM mutation, breakpoint, performance trace, storage 값을 정확히 조사한다.
- WebSocket이나 Service Worker처럼 Archify가 명시적으로 포괄하지 않는 통신을 본다.

### Framework DevTools가 먼저인 경우

- React/Vue의 정확한 component tree, props/state, render performance를 디버깅한다.
- 개발 중인 앱이라 framework-specific semantic 정보가 가장 중요하다.

### 전문 security tool이 먼저인 경우

- 악성 동작이나 data exfiltration을 증명해야 한다.
- passive triage를 넘어 request interception, replay, active scan이 필요하다.
- audit evidence와 재현 가능한 coverage가 필요하다.

## 권장 조합

```text
Archify로 가설 형성
  → Chrome DevTools로 request/initiator와 runtime evidence 확인
  → React/Vue DevTools로 component semantics 확인
  → 필요 시 proxy/CSP reporting/client-side monitoring으로 보안 검증
```

Archify의 confidence는 조사 우선순위이지 진실값이 아니다. 특히 low-confidence UI library hint와 sensitive-field listener는 독립 evidence로 교차 검증한다.

## Sources

- [Archify — How it works](https://archify.salahxd.dev/#how-it-works)
- [Archify GitHub](https://github.com/Salah-XD/archify)
- [Chrome DevTools](https://developer.chrome.com/docs/devtools/)
- [React Developer Tools](https://react.dev/learn/react-developer-tools)
- [Vue DevTools](https://devtools.vuejs.org/)
- [Wappalyzer](https://www.wappalyzer.com/)
- [OWASP ZAP](https://www.zaproxy.org/)

