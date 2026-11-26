---
date: 2026-11-26
tags: [tech]
type: tech-tool-study
status: draft
---

# Build·Check 반복 개발 흐름과 완료 조건 설계

> **한 줄 정의**: Build·Check 반복 개발 흐름은 결과물을 제작하고 검사한 뒤, 목표 충족 여부와 반복 한도에 따라 수정 또는 완료를 결정하는 개발 방식이다.

## Overview

Craft Anything 소개 자료는 **Browse → Build → Check → Complete**와 Build·Check 사이의 반복을 보여준다. 이 노트는 특정 제품의 설치 안내보다, 요구사항을 검사 가능한 조건으로 바꾸고 반복의 종료 사유를 설계하는 방법을 학습한다.

- **제작됨 ≠ 검증됨:** Snake 화면이 나와도 방향키 조작·성장·속도 증가를 각각 확인해야 한다.
- **목표 충족 ≠ 한도 도달:** 웹사이트 예시의 유사도 90% 또는 최대 6라운드는 서로 다른 종료 사유를 만든다.
- **확인 범위:** 유사도 계산법, 라운드 집계, 언어·framework·AI 모델·검사 도구는 미공개다. 90%와 6라운드가 공통 기본값인지도 알 수 없다.

## Learning Path

- [ ] [[tech/devtools/build-check-iteration/README|학습 지도 다시 보기]]
- [ ] [[tech/devtools/build-check-iteration/01-overview|Overview]]
- [ ] [[tech/devtools/build-check-iteration/02-ecosystem|Ecosystem]]
- [ ] [[tech/devtools/build-check-iteration/03-references|References]]
- [ ] [[tech/devtools/build-check-iteration/04-learning/01-getting-started|시작하기]]
- [ ] [[tech/devtools/build-check-iteration/04-learning/02-deep-dive|Deep Dive]]
- [ ] [[tech/devtools/build-check-iteration/05-projects|Projects]]
- [ ] [[tech/devtools/build-check-iteration/cheatsheet|Cheatsheet]]

## When To Use

- 생성된 게임·웹사이트의 실제 동작을 요구사항과 대조할 때
- 검사 결과를 수정 항목과 연결하고 회귀를 추적할 때
- 목표와 시간·비용에 대응하는 반복 한도를 함께 관리할 때

## When Not To Use

- 검사 기준이 없는 상태에서 반복 횟수만으로 완성도를 보증하려 할 때
- 시각적 유사도 하나를 기능 정확성이나 전체 품질로 대체하려 할 때
- 보안·안전 등 별도의 전문 검증이 필요한 작업을 이 흐름만으로 승인하려 할 때

## Related Notes

- [[MOCs/Index]]
- [[MOCs/Devtools]]
- [[tech/devtools/qa/README|QA]] — 검사 기준과 검증 활동을 함께 살펴볼 관련 노트.

## Sources

- 사용자 제공 dossier: Craft Anything 소개 영상의 수집 요약. 원본 URL은 제공되지 않아 기재할 수 없다. 제품 구현·성능·라이선스는 별도 확인이 필요하다.
- 보조 학습: [Playwright Assertions](https://playwright.dev/docs/test-assertions) — 검사 작성 참고이며 Craft Anything의 사용 도구라는 근거는 아니다.
