---
date: 2026-11-26
tags: [tech]
type: tech-tool-study
status: draft
---

# Cheatsheet: Build·Check 반복

## 핵심 용어

| 용어 | 뜻 | 기록할 것 |
|---|---|---|
| acceptance criteria | 완료 판단 기준 | 입력·기대 결과·관찰 방법 |
| feedback loop | 검사 결과의 수정 반영 | 실패 관찰 → 수정 항목 |
| regression check | 기존 동작 재확인 | 이전 pass → 현재 fail 여부 |
| termination condition | 반복 종료 규칙 | 목표·최대 횟수·집계법 |

## 실행 전

- [ ] 각 요구사항에 ID와 관찰 가능한 기준 부여
- [ ] 검사 환경과 시작 상태 고정
- [ ] 기능 검사와 시각 점수 분리
- [ ] 목표·반복 한도·라운드 정의 작성

## 매 라운드

- [ ] Build 후 같은 기준으로 Check
- [ ] 기대 결과와 실제 결과, 증거 기록
- [ ] 실패 항목과 다음 수정 연결
- [ ] 이전 통과 조건도 재검사

## 종료 시

- [ ] 모두 충족하면 goal_met
- [ ] 미충족 상태로 한도 소진이면 limit_reached
- [ ] fail·not_run과 남은 위험 명시
- [ ] 최종 산출물과 검사 기록 함께 전달

```text
round | criterion_id | expected | observed | result
previous_result | evidence | next_change | termination_reason
```

## 해석 주의

- 90%·6라운드: 자료의 웹사이트 예시 조건이며 보편적 기본값은 미확인.
- 유사도: 계산법 미공개. 기능 정확성·전체 품질로 확대 해석하지 않기.
- 반복: 매번 품질이 상승한다는 보장은 없음.
- 상세 피드백·회귀 기록·종료 상태 구분: 이 노트의 설계 제안.
- 무료·LICENSE·별 그래픽: 가격 범위·라이선스 종류·사용 규모의 검증 자료가 아님.

## 연결

[[tech/devtools/build-check-iteration/README|학습 지도]] · [[tech/devtools/build-check-iteration/03-references|근거 범위와 참고 문서]]

## Sources

- 사용자 제공 dossier: Craft Anything 소개 영상의 수집 요약. 원본 URL은 제공되지 않아 기재할 수 없다. 제품 구현·성능·라이선스는 별도 확인이 필요하다.
- 보조 학습: [Playwright Assertions](https://playwright.dev/docs/test-assertions) — 검사 작성 참고이며 Craft Anything의 사용 도구라는 근거는 아니다.
