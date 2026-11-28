---
date: 2026-11-27
tags: [tech]
type: tech-tool-study
status: draft
---

# Cheatsheet

## 확인된 요구

- 방향키로 조작한다.
- 먹이 섭취 후 성장한다.
- 속도 증가 조건이 존재한다.

## 설계 전에 결정

| 영역 | 결정할 것 |
|---|---|
| Input | 반대 방향, 연속 입력, 반영 시점 |
| Growth | 성장량, 적용 시점 |
| Difficulty | 초기 속도, Trigger, 증가 폭, 최대 속도 |
| 추가 기능 | 충돌, 점수, 종료, 재시작, 먹이 생성 |

## 빠른 검사

- [ ] 각 방향키와 이동 방향이 연결된다.
- [ ] 연속 입력과 반대 방향 동작이 선택한 명세와 같다.
- [ ] 섭취 전후 길이 차이가 선택한 성장량과 같다.
- [ ] 속도 Trigger 직전·도달·직후가 기대값과 같다.
- [ ] 동일 조건의 반복 평가가 의도치 않은 중복 증가를 일으키지 않는다.
- [ ] 속도 상한 이후 값이 유지된다(상한을 채택한 경우).
- [ ] 수정 뒤 같은 조건으로 재검사했다.

## 공식과 주의점

```text
한 tick에 한 칸 이동하는 모델:
speed_cells_per_sec = 1000 / interval_ms
interval_ms 감소 → 이동 속도 증가
```

먹이 섭취 → 성장은 확인되었다. 먹이 섭취 → 속도 증가는 선택 가능한 설계다. 웹사이트 유사도 90%·최대 6라운드는 Snake 규칙으로 가져오지 않는다. 구현 언어·Engine·Framework는 미확인이다.

[[tech/devtools/snake-controls-difficulty/04-learning/02-deep-dive|공식과 경계 예시]] · [[tech/devtools/snake-controls-difficulty/README|학습 경로]]

## Sources

- 사용자 제공 dossier: Craft Anything의 Snake Game 제작 요청 예시에 관한 수집 요약. 원문·영상 URL은 제공되지 않아 기재할 수 없다.
- 아래 설계안과 실습 수치는 학습용 제안이며, 원자료의 구현 사실이 아니다.
