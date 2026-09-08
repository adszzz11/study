---
date: 2026-09-09
tags: [tech]
type: tech-tool-study
status: draft
---

# Remotion

> **한 줄 정의**: Remotion은 React·TypeScript로 영상의 각 프레임을 정의하고, 데이터에 따라 개인화된 영상과 영상 제작 애플리케이션을 만드는 programmatic video framework다.

## Overview

영상의 레이아웃과 motion을 React component로 작성하고 이름·수치·이미지 같은 가변 데이터를 `props`로 전달한다. 템플릿 하나로 고객별 연말 결산, 상품 광고, 데이터 리포트 영상을 반복 생성하는 데 유용하다.

- **핵심 모델:** `화면 = f(frame, props, assets)`. 재생 시간 대신 현재 frame에서 화면을 계산한다.
- **출력 단위:** `Composition`에 component·해상도·fps·총 frame 수를 등록한다.
- **Preview:** Studio는 개발용 작업 공간, Player는 React 앱에 넣는 미리보기 component다.
- **Export:** 서버의 Browser + FFmpeg 경로 또는 브라우저의 `@remotion/web-renderer` 경로를 선택한다. Player만 추가해도 파일이 생성되는 것은 아니다.
- **조사 기준:** 2026-09-09. 확인한 GitHub Latest는 2026-09-07의 `v4.0.522`. 버전과 지원 범위는 도입 시 다시 확인한다.

공식 개념은 [Fundamentals](https://www.remotion.dev/docs/the-fundamentals), 데이터 활용은 [Parameterized videos](https://www.remotion.dev/docs/parameterized-rendering)를 기준으로 정리했다.

## Learning Path

- [ ] [[tech/devtools/remotion/01-overview|1. Overview]] — What/Why와 frame 기반 사고방식 설명하기
- [ ] [[tech/devtools/remotion/02-ecosystem|2. Ecosystem]] — 대안과 렌더링 경로 선택하기
- [ ] [[tech/devtools/remotion/03-references|3. References]] — 공식 문서와 버전 확인 지점 익히기
- [ ] [[tech/devtools/remotion/04-learning/01-getting-started|4. Getting started]] — 5초짜리 타이틀 영상을 MP4로 출력하기
- [ ] [[tech/devtools/remotion/04-learning/02-deep-dive|5. Deep dive]] — 동적 metadata, 재현성, 운영 구조 익히기
- [ ] [[tech/devtools/remotion/05-projects|6. Projects]] — 개인화 영상과 편집 앱으로 확장하기
- [ ] [[tech/devtools/remotion/cheatsheet|7. Cheatsheet]] — 자주 쓰는 API와 문제 해결 복습하기

## When To Use

- 동일한 브랜드 디자인에 고객·상품·언어별 데이터를 넣어 많은 영상을 생성한다.
- React 기반 서비스에서 사용자가 문구와 색상을 바꾸며 결과를 확인해야 한다.
- 영상 템플릿을 코드 리뷰, 버전 관리, 자동화 파이프라인에 포함하고 싶다.
- 데이터 리포트나 반복되는 motion graphics를 component로 재사용한다.

## When Not To Use

- 일회성 실사 영상의 정교한 컷 편집·색보정이 주업무이고 코드 기반 자동화의 이점이 작다.
- 자르기·합치기·포맷 변환만 필요하다면 FFmpeg 같은 미디어 도구부터 검토한다.
- 모든 CSS 효과가 브라우저 export에서도 동일하게 표현되어야 하지만 검증할 여력이 없다.
- React 개발 및 렌더링 운영 부담을 감당하기 어렵다면 관리형 API나 기존 편집기를 비교한다.

위 선택 기준은 기능을 바탕으로 한 학습용 판단이다. 실제 비용과 지연 시간은 대표 영상으로 측정한다.

## Related Notes

- [[MOCs/Index]]
- [[MOCs/Devtools]]
- [[tech/scraping/playwright/README|Playwright]] — Player를 넣은 웹 UI의 입력·미리보기 흐름을 검증할 때 연결되는 학습 주제

## Sources

- [Fundamentals](https://www.remotion.dev/docs/the-fundamentals)
- [Parameterized videos](https://www.remotion.dev/docs/parameterized-rendering)
- [Player](https://www.remotion.dev/docs/player)
- [Client-side rendering](https://www.remotion.dev/docs/client-side-rendering)
- [Client-side limitations](https://www.remotion.dev/docs/client-side-rendering/limitations)
- [Server-side rendering 비교](https://www.remotion.dev/docs/compare-ssr)
- [v4.0.522 Release](https://github.com/remotion-dev/remotion/releases/tag/v4.0.522)
