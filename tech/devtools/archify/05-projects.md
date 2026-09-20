---
date: 2026-07-16
tags: [tech]
type: tech-tool-study
status: draft
---

# Archify — Projects

> [[04-learning/02-deep-dive|이전: Deep Dive]] · [[README|목차로 돌아가기]] · [[cheatsheet|다음: Cheatsheet]]

## 프로젝트 1: 낯선 SPA Architecture Map

### 목표

로그인부터 dashboard 진입까지 element, component, API, route의 관계를 짧은 architecture map으로 만든다.

### 절차

1. Page Profile에서 framework, UI library, hosting 후보를 기록한다.
2. login input/button을 hover하고 click-to-lock한다.
3. submit 뒤의 `fetch`/XHR와 route/storage key 변화를 기록한다.
4. DevTools Network와 framework DevTools로 각 claim을 확인한다.
5. 확정, 유력, 미확인을 confidence와 함께 구분한다.

| Element | Component evidence | Interaction | API | Route/storage | 검증 상태 |
|---|---|---|---|---|---|
| Login button | Button type, name unavailable | click | `POST /api/login` | `/dashboard` | Network 확인 필요 |
| Search input | React component hint | input/submit | `GET /api/search` | `q` route param | initiator 확인 |

### 완료 조건

- [ ] 핵심 user flow의 element 5개 이상 기록
- [ ] API correlation을 DevTools로 교차 검증
- [ ] component name 미확인을 추측으로 채우지 않음
- [ ] diagram에 confidence/evidence 표기

## 프로젝트 2: Third-party Script Exposure Triage

### 목표

password/payment form 주변 third-party script와 sensitive-field listener를 inventory하고 조사 우선순위를 정한다.

### 절차

1. 테스트 계정과 비실제 결제 데이터만 사용한다.
2. Page Profile의 third-party script와 outbound domain을 기록한다.
3. sensitive field별 listener와 script origin을 연결한다.
4. Sources breakpoint로 value read 여부를 확인한다.
5. Network/proxy로 외부 전송 여부를 별도 확인한다.

| Evidence | 의미 | 결론으로 쓰면 안 되는 것 |
|---|---|---|
| listener 등록 | field event 관찰 가능 | 악성 script 확정 |
| value read | runtime에서 값을 읽음 | 외부 전송 확정 |
| outbound request | domain으로 통신 | sensitive value 포함 확정 |
| payload에서 값 확인 | 실제 data flow evidence | 의도/정당성 자동 판정 |

### 산출물

- script/domain inventory
- listener → handler → request evidence chain
- false positive와 확인 불가 항목
- CSP/SRI/vendor review 권고

## 프로젝트 3: Fingerprint Rule Contribution

### 목표

새 technology detection rule을 evidence 중심으로 추가하고 false positive를 통제한다.

### 절차

1. `src/engine/`에서 유사 rule과 confidence model을 읽는다.
2. technology의 stable runtime signal을 2개 이상 찾는다.
3. positive fixture와 혼동 가능한 negative fixture를 만든다.
4. Vitest unit test와 Playwright E2E를 실행한다.
5. Page Profile evidence 문구가 과장되지 않았는지 검토한다.

```text
좋은 rule 후보
- stable global/runtime marker
- 공식 script origin 또는 고유 bundle marker
- 서로 독립적인 signal 조합

피해야 할 rule
- 흔한 class name 하나
- 쉽게 복사되는 DOM 문자열
- version/build마다 사라지는 단일 marker
```

## 프로젝트 4: Coverage Boundary 실험

### 목표

Archify가 관찰하는 network channel과 관찰하지 않는 channel을 재현 가능한 test page에서 구분한다.

### 실험 matrix

| Channel | Archify 관찰 | DevTools 관찰 | 메모 |
|---|---:|---:|---|
| `fetch` | 확인 | 확인 | runtime correlation 검사 |
| `XMLHttpRequest` | 확인 | 확인 | status/method/URL 대조 |
| WebSocket | 검증 | 확인 | 완전 지원을 가정하지 않음 |
| `sendBeacon` | 검증 | 확인 | navigation 시점 주의 |
| resource tag | 검증 | 확인 | script/image/link 분리 |
| Service Worker | 검증 | 확인 | initiator와 scope 기록 |

### 완료 조건

- [ ] 각 channel을 독립적으로 발생시키는 test page 사용
- [ ] 결과에 extension version과 Chrome version 기록
- [ ] 미관찰을 bug와 unsupported scope로 성급히 단정하지 않음
- [ ] 재현 절차와 DevTools evidence 보존

## Best Practices

- public 또는 허가받은 page만 조사한다.
- Archify 결과는 hypothesis와 triage에 사용한다.
- confidence score와 raw evidence를 함께 기록한다.
- security 결론에는 DevTools, proxy, CSP reporting 등 독립 evidence를 요구한다.
- version이 빠르게 변하는 초기 프로젝트이므로 실험마다 version/date를 남긴다.

## Sources

- [Archify GitHub](https://github.com/Salah-XD/archify)
- [Archify 기능 설명](https://archify.salahxd.dev/#how-it-works)
- [Archify Privacy](https://archify.salahxd.dev/privacy)
- [Chrome DevTools Network](https://developer.chrome.com/docs/devtools/network/)

