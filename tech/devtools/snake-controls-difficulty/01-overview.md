---
date: 2026-11-27
tags: [tech]
type: tech-tool-study
status: draft
---

# Overview: What / Why / 특징

## What

Snake 제작 요청에서 확인된 기능은 방향키 Input, 먹이 섭취 후 Growth, 속도 증가 조건이다. 이 노트는 제품 사용 설명서가 아니라 게임 요구사항을 구체화하는 tool-study다.

## Why

화면이 완성되어도 방향 입력이 반영되지 않거나 먹이를 먹은 뒤 길이가 바뀌지 않으면 요구사항을 충족하지 못한다. 사용자 입력 → 상태 변화 → 관찰 가능한 결과를 연결하는 검사가 필요하다.

## 특징과 개념적 구조

다음은 요구사항 분석을 위한 분해이며 Craft Anything의 실제 내부 구현을 나타내지 않는다.

| 요소 | 확인된 내용 | 검사할 내용 |
|---|---|---|
| Input | 방향키 조작 | 키별 방향, 입력 반영 시점, 연속 입력 순서 |
| Growth | 섭취 후 성장 | 섭취 판정과 길이 증가의 연결 |
| Difficulty | 속도 증가 조건 | Trigger, 증가량, 중복 증가, 상한 |
| Workflow | Browse → Build → Check → Complete | 규칙별 합격 기준 |
| Iteration | Build·Check 반복 | 수정 뒤 동일 조건 재검사 |

## 규칙의 경계

- 반대 방향으로 즉시 전환할 수 있는지는 미정이다.
- 입력 즉시 이동할지 다음 tick에 방향만 반영할지도 미정이다.
- 성장량과 속도 수치는 제공되지 않았다.
- 성장에 따른 충돌 위험은 충돌 규칙을 추가로 정해야 평가할 수 있다.
- 속도가 높아지면 동일 이동 거리에서 방향을 결정할 시간이 줄어든다. 이는 요구사항에 대한 해석이다.

## 다음 학습

[[tech/devtools/snake-controls-difficulty/02-ecosystem|설계 대안 비교]] · [[tech/devtools/snake-controls-difficulty/README|학습 경로]]

## Sources

- 사용자 제공 dossier: Craft Anything의 Snake Game 제작 요청 예시에 관한 수집 요약. 원문·영상 URL은 제공되지 않아 기재할 수 없다.
- 아래 설계안과 실습 수치는 학습용 제안이며, 원자료의 구현 사실이 아니다.
