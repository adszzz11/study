---
date: 2026-10-18
tags: [tech]
type: tech-tool-study
status: draft
---

# Responsively — Getting started

[[tech/devtools/responsively/README|학습 진입점]] · 다음: [[tech/devtools/responsively/04-learning/02-deep-dive|Deep dive]]

## 목표와 준비

**local development server의 한 화면을 mobile, tablet, desktop 세 viewport에서 동시에 조작하고 screenshot으로 남긴다.** 이 노트는 앱의 UI가 version에 따라 달라질 수 있으므로 메뉴명보다 검증 순서에 집중한다.

- [공식 다운로드](https://responsively.app/download)에서 OS에 맞는 stable을 설치한다.
- 실행할 프로젝트의 local server를 시작한다. 예: `http://localhost:3000`.
- 테스트할 route와 login 같은 사전 조건을 준비한다.

## 1. URL과 초기 device 선택

1. Responsively를 열고 local URL을 연다.
2. mobile, tablet, desktop을 각각 하나씩 고른다.
3. 대표 시작 폭은 `375`, `768`, `1440`px로 잡되, 제품의 실제 CSS breakpoint를 우선한다.
4. viewport가 모두 같은 route를 렌더링하는지 확인한다.

## 2. 한 번 조작하고 동시에 관찰

Header와 navigation을 열고, form에 입력하고, modal을 띄운다. interaction mirroring이 활성화되어 있다면 다음을 viewport별로 관찰한다.

| 점검 대상 | 확인 질문 |
|---|---|
| Header/navigation | 메뉴가 겹치거나 hamburger가 사라지지 않는가? |
| Form | label, validation error, submit CTA가 잘리지 않는가? |
| Modal | 작은 폭에서 viewport 밖으로 밀리거나 scroll이 막히지 않는가? |
| Card/grid | column 전환 지점에서 overflow 또는 과도한 빈 공간이 없는가? |

## 3. 위험 breakpoint를 custom device로 고정

기기명만 따르지 말고 CSS가 바뀌는 경계와 그 주변을 등록한다.

```text
320px   작은 mobile
375px   일반 mobile
768px   tablet 전환점
1024px  desktop 전환점
1440px  넓은 desktop
```

이 조합을 Preview Suite로 저장해 다음 PR에서도 같은 기준을 사용한다. breakpoint의 정확한 값은 제품 stylesheet와 design token에서 가져온다.

## 4. 상태를 넓혀 확인하고 캡처

- portrait/landscape를 번갈아 본다.
- 긴 콘텐츠와 validation error를 만든다.
- localization으로 길어진 text를 넣는다.
- viewport 또는 full-page screenshot을 캡처해 PR 검토 자료에 첨부한다.

## 완료 기준

- [ ] 세 viewport가 같은 local route를 표시한다.
- [ ] header, navigation, form, modal을 모두 조작했다.
- [ ] 최소 한 개의 breakpoint 위험 구간을 custom device 또는 suite에 기록했다.
- [ ] 긴 text와 validation error를 확인했다.
- [ ] 재현 가능한 screenshot을 남겼다.

## Sources

- [Responsively Download](https://responsively.app/download)
- [Responsively App guide](https://responsively.app/blog/responsively-app-guide)
- [Responsively App GitHub repository](https://github.com/responsively-org/responsively-app)
