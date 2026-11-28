---
date: 2026-11-27
tags: [tech]
type: tech-tool-study
status: draft
---

# References와 근거 범위

## 원자료 상태

제공 dossier에 원본 URL이 없어 영상·게시물 링크를 기재할 수 없다. 자료 제목, 게시자, 게시일도 확인되지 않는다. 관찰을 원본에서 독립적으로 재검증한 것으로 표현하지 않는다.

| 구분 | 이 노트에서 다루는 내용 |
|---|---|
| dossier에 기록된 관찰 | Claude 수정 요청, 녹화 첨부, 재녹화 자막, 병렬 화면, 자동 수정 언급 |
| 분석 모델 | 관찰 → 차이 판단 → 제한된 수정 → 재관찰 |
| 학습 제안 | baseline, temporal alignment, visual regression, acceptance criteria |
| 미확인 | framework, rendering engine, browser automation, diff algorithm, `/reanimate` 정체 |

00:14·00:34는 요약에 제시된 주요 시점이다. 개별 장면과 일대일로 연결하지 않는다. `417 / 417`도 지표 정의 없이는 테스트 통과 건수나 UI 일치도로 인용하지 않는다.

## 보충 문서 읽는 순서

1. Playwright Visual comparisons: screenshot baseline과 비교 환경의 일관성 이해.
2. Playwright Animations 옵션: 정적 캡처를 위한 애니메이션 제어와 Motion 검증의 차이 이해.
3. MDN `prefers-reduced-motion`: 사용자 환경 설정이 화면 동작을 바꿀 수 있음을 이해.

이 문서들은 실습을 보완한다. 원자료의 도구 선택이나 실행 성공을 입증하지 않는다.

## 연결

[[tech/devtools/web-ui-comparison-iteration/04-learning/02-deep-dive|심화 실습]] · [[tech/devtools/web-ui-comparison-iteration/README|학습 경로]]

## Sources

- 제공 dossier: 원본 영상·게시물 URL 미제공. 영상의 직접 재검증은 수행하지 않았으며, 관찰 서술은 dossier에 근거한다.
- 보충 학습: [Playwright — Visual comparisons](https://playwright.dev/docs/test-snapshots). 실습 설계를 위한 공식 문서이며 영상에서 사용한 도구라는 뜻은 아니다.

- [Playwright — toHaveScreenshot options](https://playwright.dev/docs/api/class-pageassertions#page-assertions-to-have-screenshot-1)
- [MDN — prefers-reduced-motion](https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-reduced-motion)
