---
date: 2026-07-16
tags: [tech]
type: tech-tool-study
status: draft
---

# Archify — References

> [[02-ecosystem|이전: Ecosystem]] · [[README|목차로 돌아가기]] · [[04-learning/01-getting-started|다음: Getting Started]]

## 공식 자료

- [Archify 공식 사이트](https://archify.salahxd.dev/) — 제품 정의, 기능, confidence 철학
- [Salah-XD/archify](https://github.com/Salah-XD/archify) — source, architecture, 개발 절차
- [Chrome Web Store listing](https://chromewebstore.google.com/detail/archify/nhangkbdjnopgkgklfdkpfgmendlckpe) — 배포 version과 사용자 정보
- [Privacy](https://archify.salahxd.dev/privacy) — local processing, 수집 metadata, same-origin request
- [Apache-2.0 License](https://github.com/Salah-XD/archify/blob/master/LICENSE) — 재사용 조건

## Chrome Extension 기반 지식

- [Content scripts](https://developer.chrome.com/docs/extensions/develop/concepts/content-scripts) — isolated world와 page context 차이
- [Manifest V3 소개](https://developer.chrome.com/docs/extensions/develop/migrate/what-is-mv3) — service worker와 remotely hosted code 제한
- [Chrome DevTools](https://developer.chrome.com/docs/devtools/) — 정밀 교차 검증 도구

## Source 탐색 포인트

| 관심사 | 확인 위치/자료 | 질문 |
|---|---|---|
| detection rule | [`src/` tree](https://github.com/Salah-XD/archify/tree/master/src) | evidence와 threshold는 무엇인가? |
| architecture | [README — How it works](https://github.com/Salah-XD/archify#how-it-works) | MAIN/ISOLATED world를 어떻게 bridge하는가? |
| permission/privacy | [Privacy](https://archify.salahxd.dev/privacy) | 어떤 metadata를 읽고 어디에 보관하는가? |
| release maturity | [Web Store](https://chromewebstore.google.com/detail/archify/nhangkbdjnopgkgklfdkpfgmendlckpe) | 현재 version과 update date는 무엇인가? |
| build/test | [Repository](https://github.com/Salah-XD/archify) | Vitest/Playwright coverage와 MV3 output은 무엇인가? |

## 읽는 순서

1. 공식 사이트에서 element 중심 mental model을 익힌다.
2. GitHub README에서 MAIN world와 ISOLATED world 구조를 확인한다.
3. Privacy 문서에서 local-first의 정확한 범위를 확인한다.
4. Chrome content script와 MV3 문서로 platform constraint를 연결한다.
5. `src/engine/`과 test fixture를 읽어 detection claim을 구현과 대조한다.
6. Web Store와 repository activity를 확인해 성숙도를 다시 평가한다.

## 검증할 때의 주의

- 공식 기능 문구와 source에 명시된 instrumentation 범위를 구분한다.
- `fetch`/XHR 지원을 모든 outbound channel 지원으로 확대 해석하지 않는다.
- version, users, stars, forks는 변하는 수치이므로 조사 날짜를 함께 기록한다.
- 동명의 Flutter scaffolder, 논문, 건축 플랫폼과 혼동하지 않는다.

## Sources

- [Archify 공식 사이트](https://archify.salahxd.dev/)
- [Archify GitHub README](https://github.com/Salah-XD/archify)
- [Chrome content scripts](https://developer.chrome.com/docs/extensions/develop/concepts/content-scripts)
- [Chrome Manifest V3](https://developer.chrome.com/docs/extensions/develop/migrate/what-is-mv3)

