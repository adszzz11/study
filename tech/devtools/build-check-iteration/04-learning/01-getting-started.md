---
date: 2026-11-26
tags: [tech]
type: tech-tool-study
status: draft
---

# 시작하기: Snake 기능 검증

## 실습 목표

Build 성공과 요구사항 통과를 구분하고, 실패 관찰을 다음 수정에 연결한다. 구현 언어·framework는 자유 선택이며 자료에서 지정하지 않았다.

## 1. Acceptance criteria 작성

아래 수치와 세부 규칙은 **실습용으로 직접 정한 요구사항**이다. 영상에는 속도 임계값이나 실제 검사표가 공개되지 않았다.

| ID | 입력·사전 조건 | 기대 결과 | 관찰 방법 |
|---|---|---|---|
| S1 | 안전한 빈 공간에서 방향키 입력 | 허용된 방향으로 다음 이동이 바뀜 | 화면 이동 또는 좌표 로그 |
| S2 | 먹이 앞에 위치해 한 칸 이동 | 먹이 섭취 후 길이 +1 | 전후 몸통 칸 수 비교 |
| S3 | 새 게임에서 먹이 총 3개 섭취 | 이동 간격 200ms → 160ms | timer 설정 또는 이동 timestamp |

실습에서는 반대 방향 즉시 전환을 허용하지 않는 규칙을 별도로 정한다. 검사 중 충돌 등 다른 조건이 개입하지 않게 시작 상태를 고정한다.

## 2. 반복 규칙 정하기

- 첫 Build와 그 Check를 합쳐 1라운드로 센다.
- 최대 6라운드를 실습 한도로 사용한다. 이 집계 방식은 제품의 공개 사양이 아니다.
- 완료 기준은 S1~S3 모두 통과다. 유사도 점수는 이 게임의 완료 조건에 넣지 않는다.

## 3. Build → Check → 수정

1. 세 조건을 구현한 첫 결과물을 실행한다.
2. 각 조건을 동일한 시작 상태에서 검사하고 실제 결과를 적는다.
3. 실패 조건의 원인 후보와 수정 항목을 연결한다.
4. 다음 Build 후 세 조건을 모두 재검사한다.
5. 모두 통과하면 목표 충족, 6라운드까지 실패가 남으면 한도 도달로 종료한다.

```text
round: 1
criterion: S2
expected: 먹이 섭취 후 길이 +1
observed: 길이 3 유지
result: fail
next_change: 성장 처리와 꼬리 제거 순서 확인
```

위 기록은 예시이며 실제 실행 결과가 아니다. 실행하지 않은 조건은 pass 대신 not_run으로 남기며 완료로 판정하지 않는다.

## 산출물

- 실행 가능한 게임, 요구사항표, 라운드별 검사·수정 기록
- 종료 사유와 미통과·미실행 항목 목록

## 다음 단계

[[tech/devtools/build-check-iteration/04-learning/02-deep-dive|Deep Dive]] · [[tech/devtools/build-check-iteration/README|학습 지도]]

## Sources

- 사용자 제공 dossier: Craft Anything 소개 영상의 수집 요약. 원본 URL은 제공되지 않아 기재할 수 없다. 제품 구현·성능·라이선스는 별도 확인이 필요하다.
- 보조 학습: [Playwright Assertions](https://playwright.dev/docs/test-assertions) — 검사 작성 참고이며 Craft Anything의 사용 도구라는 근거는 아니다.
