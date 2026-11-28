---
date: 2026-11-27
tags: [tech]
type: tech-tool-study
status: draft
---

# Projects: 명세와 검사 기록 만들기

## 1. Snake 규칙 명세

확인된 세 가지 요구를 출발점으로 Control specification과 Difficulty specification을 작성한다.

- 산출물: 방향 전환·입력 반영 규칙, 성장량, 속도 Trigger·증가 폭·상한, Acceptance criteria.
- 미정 값은 `설계 결정 필요`로 표시한다.
- 경계·자기 몸 충돌, 종료·재시작, 점수는 추가 요구사항으로 분리한다.
- 완료 기준: 각 선택한 규칙에 초기 상태·입력·기대 결과가 있으며 미정 사항이 드러나 있다.

## 2. 난이도 비교 Prototype

동일한 조작과 성장 조건에서 단계별 증가와 연속 증가를 비교한다. 고정 속도는 대조 조건으로만 사용한다.

| 기록 항목 | 내용 |
|---|---|
| 공통 조건 | 격자, 조작, 성장량, 추가 규칙 |
| 정책 | Trigger, 초기 간격, 최소 간격, 증가 공식 |
| 측정 | 이동 간격, 플레이 시간, 변화 인지 시점 |
| 해석 | 예측 가능성, 체감 변화, 정책별 차이 |

두 정책은 제안된 실험 조건이다. 초기·최종 속도와 실험 시간을 가능하면 맞추고 차이가 남으면 기록한다. 완료 기준은 비교 로그와 선택 근거를 남기는 것이다.

## 3. Build·Check 기록

| 반복 | 요구사항 | 관찰 결과 | 수정 사항 | 재검사 결과 |
|---|---|---|---|---|
| 1 | 섭취 후 성장 | 직접 관찰 후 기입 | 필요 시 기입 | 통과/실패/미검사 |
| 2 | 선택한 속도 Trigger | 경계 전·후 측정 | 필요 시 기입 | 통과/실패/미검사 |

위 표는 기록 양식이며 실행 결과가 아니다. 화면이 완성됐어도 속도 조건이 실패하면 해당 동작은 미통과로 남긴다.

[[tech/devtools/snake-controls-difficulty/04-learning/01-getting-started|검사 절차]] · [[tech/devtools/snake-controls-difficulty/cheatsheet|빠른 점검]] · [[tech/devtools/snake-controls-difficulty/README|학습 경로]]

## Sources

- 사용자 제공 dossier: Craft Anything의 Snake Game 제작 요청 예시에 관한 수집 요약. 원문·영상 URL은 제공되지 않아 기재할 수 없다.
- 아래 설계안과 실습 수치는 학습용 제안이며, 원자료의 구현 사실이 아니다.
