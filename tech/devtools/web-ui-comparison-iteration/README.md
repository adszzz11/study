---
date: 2026-11-27
tags: [tech]
type: tech-tool-study
status: draft
---

# 화면 비교를 통한 웹 UI 반복 수정

> **한 줄 정의**: 웹 UI의 기준 화면과 구현 결과를 비교해 차이를 찾고, 수정과 재관찰을 반복하는 시각적 피드백 기반 개발 과정.

## Overview

결과 생성 후 실제 화면을 다시 관찰하는 feedback loop를 학습한다. 제공 자료는 Claude에서 모션그래픽 재현을 여러 차례 수정하는 과정을 만화 형식으로 보여준다. 수정 요청, 화면 녹화 첨부, 병렬 화면 비교가 관찰되지만 내부 구현은 확인되지 않는다.

- 핵심 흐름: **수정 요청 → 결과 변경 → 화면 관찰·녹화 → 차이 판단 → 다음 요청**.
- Layout·시각 표현은 정지 화면으로, Motion·상태 전환은 공통 시작점의 녹화로 확인한다.
- `/reanimate`의 정체, 자동 수정 범위, frontend framework는 미확인이다.
- `CMS Drafts`, `417 / 417`, 진행 막대는 관찰된 표시이며 UI 일치율이나 테스트 통과율을 뜻한다고 단정할 수 없다.

## Learning Path

- [ ] [[tech/devtools/web-ui-comparison-iteration/01-overview|Overview]] — 정의, 관찰 근거, 개념적 루프 익히기
- [ ] [[tech/devtools/web-ui-comparison-iteration/02-ecosystem|작업 방식 비교]] — 텍스트·병렬 화면·녹화·정량 검증 비교
- [ ] [[tech/devtools/web-ui-comparison-iteration/03-references|References]] — 근거의 범위와 보충 문서 확인
- [ ] [[tech/devtools/web-ui-comparison-iteration/04-learning/01-getting-started|시작하기]] — 같은 조건에서 한 차이 수정하기
- [ ] [[tech/devtools/web-ui-comparison-iteration/04-learning/02-deep-dive|심화 학습]] — temporal alignment와 검증 상태 설계
- [ ] [[tech/devtools/web-ui-comparison-iteration/05-projects|Projects]] — 비교 기록과 자동 수정 실험
- [ ] [[tech/devtools/web-ui-comparison-iteration/cheatsheet|Cheatsheet]] — 반복 작업 체크리스트 활용

## When To Use

- 기준 디자인이나 Motion 장면을 구현하면서 차이를 구체적인 수정 요청으로 바꿀 때.
- AI가 변경을 완료했다고 답한 뒤 실제 렌더링 결과를 검증할 때.
- 변경과 결과의 관계를 반복별 증거로 남겨야 할 때.

## When Not To Use

- 화면만 보고 접근성, 보안, 데이터 정확성까지 검증하려는 경우. 각각 별도의 검증이 필요하다.
- 기준·viewport·초기 state가 달라 비교 조건을 맞출 수 없는 경우.
- 정지 화면만으로 Motion의 순서·속도까지 판정하려는 경우.

## Related Notes

- [[MOCs/Index]]
- [[MOCs/Devtools]]
- [[tech/devtools/web-ui-comparison-iteration/04-learning/02-deep-dive|Temporal alignment와 visual regression]] — 정적·시간적 검증을 분리하는 관련 tech 노트

## Sources

- 제공 dossier: 원본 영상·게시물 URL 미제공. 영상의 직접 재검증은 수행하지 않았으며, 관찰 서술은 dossier에 근거한다.
- 보충 학습: [Playwright — Visual comparisons](https://playwright.dev/docs/test-snapshots). 실습 설계를 위한 공식 문서이며 영상에서 사용한 도구라는 뜻은 아니다.
