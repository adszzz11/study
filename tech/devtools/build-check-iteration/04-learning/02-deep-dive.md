---
date: 2026-11-26
tags: [tech]
type: tech-tool-study
status: draft
---

# Deep Dive: 평가·회귀·종료 조건

## 기능과 유사도 분리

유사도 90%는 비교 대상과 계산법 없이는 해석할 수 없다. 이미지가 비슷해도 버튼이나 게임 규칙은 실패할 수 있다. 기능 검사는 별도 통과 조건으로 관리한다.

웹사이트 실습에서는 기준 화면, viewport, browser, 폰트, 데이터, 캡처 시점을 고정한다. 예를 들어 아래 점수는 **직접 설계한 실험용 rubric**이며 Craft Anything의 알고리즘이 아니다.

| 평가 범위 | 배점 | 사전에 정할 내용 |
|---|---|---|
| 레이아웃 | 40 | 위치·간격의 허용 오차 |
| 타이포그래피 | 20 | 글꼴·크기·줄바꿈 기준 |
| 색상 | 20 | 비교 영역과 허용 오차 |
| 이미지·아이콘 | 20 | 대상 자산과 크기 기준 |

각 항목의 채점 규칙을 Build 전에 적고 합계/100을 실험 점수로 사용한다. 이 수치는 pixel similarity가 아니며 객관적인 제품 성능 지표로 보고하지 않는다. 상호작용은 이 점수 밖에서 기능별로 검사한다.

## Feedback loop와 regression check

기록 단위는 `라운드 → 요구사항 ID → 기대/실제 결과 → 수정 → 재검사`로 연결한다. 이전 pass가 fail로 바뀌면 regression으로 표시한다. 최종 라운드의 현재 결과로 판단하고 이전 점수만으로 완료 처리하지 않는다.

## 종료 판정 설계

아래는 실습용 의사코드다. 첫 Build·Check를 1라운드로 세며 목표 검사에 미실행 항목이 있으면 충족으로 보지 않는다.

```python
for round_no in range(1, max_rounds + 1):
    artifact = build(requirements, feedback)
    report = check(artifact, criteria)  # 기존 통과 항목도 포함
    save(round_no, report)
    if goal_met(report):
        return outcome("goal_met", report)
    if round_no == max_rounds:
        return outcome("limit_reached", report)
    feedback = actionable_failures(report)
```

- 같은 라운드에 목표와 최대 횟수 조건이 동시에 성립하면 목표 충족으로 기록한다. 이는 이 실습의 명시적 우선순위다.
- 검사 실행 자체가 실패하면 결과 불명을 기록하고 원인을 보고한다. 이를 기능 통과로 간주하지 않는다.
- 최대 횟수에서 끝났다는 사실은 품질 목표 달성을 뜻하지 않는다.

## 종료 보고 예시

```text
status: limit_reached
rounds_used: 6/6
visual_score: 88/100 (실험용 rubric)
functional_checks: 4 pass, 1 fail
remaining: 메뉴 키보드 조작 실패
```

예시 수치는 관찰된 제품 결과가 아니다. 라운드별 점수와 회귀 기록을 함께 보아 개선·정체·악화를 구분한다.

## 연결

[[tech/devtools/build-check-iteration/05-projects|실전 프로젝트]] · [[tech/devtools/build-check-iteration/README|학습 지도]]

## Sources

- 사용자 제공 dossier: Craft Anything 소개 영상의 수집 요약. 원본 URL은 제공되지 않아 기재할 수 없다. 제품 구현·성능·라이선스는 별도 확인이 필요하다.
- 보조 학습: [Playwright Assertions](https://playwright.dev/docs/test-assertions) — 검사 작성 참고이며 Craft Anything의 사용 도구라는 근거는 아니다.
