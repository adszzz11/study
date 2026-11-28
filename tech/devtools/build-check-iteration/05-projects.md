---
date: 2026-11-26
tags: [tech]
type: tech-tool-study
status: draft
---

# Projects: 반복 개발 적용

## 1. Snake 요구사항 검증 기록

- **목적:** 제작 결과와 검증된 결과의 차이 확인.
- **진행:** 방향키·성장·속도 증가를 독립 검사하고 실패 관찰을 다음 수정에 연결한다.
- **산출물:** 게임, acceptance criteria, 라운드별 pass/fail/not_run, 수정 내역, 종료 보고.
- **완료:** 사전 정의한 세 기능 조건 모두 통과. 한도 도달 시 실패·미실행 항목을 보고한다.

구체적인 수치 조건은 [[tech/devtools/build-check-iteration/04-learning/01-getting-started|시작하기 실습]]의 별도 설정을 참고한다.

## 2. 웹사이트 유사도 개선 실험

- **목적:** 평가 범위를 고정한 상태에서 변경의 영향을 관찰.
- **진행:** 기준 화면·환경·채점법을 정하고 90% 목표, 최대 6라운드를 실험 설정으로 적용한다.
- **산출물:** 기준/결과 화면, rubric, 라운드별 점수·기능 검사·수정 내역.
- **완료:** 실험에서 정한 시각 목표와 필수 기능 조건을 충족. 미충족 상태로 횟수 소진 시 한도 도달로 보고한다.

이는 영상의 반복 구조 응용이며 내부 유사도 알고리즘 재현이 아니다. [[tech/devtools/build-check-iteration/04-learning/02-deep-dive|평가 설계]]를 먼저 작성한다.

## 3. 반복 개발 상태판

- **목적:** 횟수보다 개선 내용과 남은 문제를 추적.
- **진행:** 요구사항 ID, 라운드, 검사 결과, 이전 결과, 수정 항목, 증거, 종료 사유를 표시한다.
- **산출물:** 표 또는 상태판 prototype과 기록 예제. 언어·framework는 별도 결정한다.
- **완료:** pass→fail 회귀가 표시되고 목표 충족과 한도 도달이 구분되며, 미실행 항목을 완료로 오인하지 않는다.

| 라운드 | 요구사항 | 이전 → 현재 | 수정·증거 | 종료 사유 |
|---|---|---|---|---|
| 1 | S2 성장 | not_run → fail | 섭취 전후 길이 동일 | 계속 |
| 2 | S2 성장 | fail → pass | 꼬리 처리 수정·전후 로그 | 다른 항목도 검사 후 판단 |

표는 가상 기록이며 실제 제품 평가 결과가 아니다.

## 연결

[[tech/devtools/build-check-iteration/cheatsheet|검사 체크리스트]] · [[tech/devtools/build-check-iteration/README|학습 지도]]

## Sources

- 사용자 제공 dossier: Craft Anything 소개 영상의 수집 요약. 원본 URL은 제공되지 않아 기재할 수 없다. 제품 구현·성능·라이선스는 별도 확인이 필요하다.
- 보조 학습: [Playwright Assertions](https://playwright.dev/docs/test-assertions) — 검사 작성 참고이며 Craft Anything의 사용 도구라는 근거는 아니다.
