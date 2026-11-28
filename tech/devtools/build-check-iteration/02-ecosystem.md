---
date: 2026-11-26
tags: [tech]
type: tech-tool-study
status: draft
---

# Ecosystem: 반복 개발 절차 비교

## 비교 범위

자료에는 경쟁 제품이 등장하지 않는다. 아래는 제품별 성능·가격 비교가 아닌 개념적인 절차 비교다.

| 방식 | 진행 구조 | 장점 | 한계·주의점 |
|---|---|---|---|
| 일회성 Build | 제작 후 전달 | 단순한 절차 | 누락 발견·반영 기회가 적음 |
| 수동 반복 개발 | 사람이 검토하고 수정 지시 | 맥락 판단이 쉬움 | 기준·기록이 불일치할 수 있음 |
| Build·Check 반복 | 제작 → 검사 → 수정 | 검사와 수정 연결 | 부실한 기준이면 잘못된 방향으로 반복 |
| 고정 횟수 반복 | 정한 횟수 수행 | 반복량 제한 | 완성 후에도 계속하거나 미완성으로 종료 |
| 목표·횟수 조건 결합 | 목표 충족 또는 한도 도달 | 품질 목표와 반복량 함께 표현 | 종료 사유를 구분해 보고해야 함 |

## 선택 기준

- 동작 검증이 중요하면 기능별 acceptance criteria를 먼저 정의한다.
- 외형 재현이 목적이면 비교 화면·viewport·평가 범위를 고정한다.
- 자원이 제한되면 최대 라운드를 정하되 남은 실패 항목을 함께 전달한다.

Craft Anything의 웹사이트 시연 조건은 마지막 방식에 가깝다. 이를 모든 작업의 기본 설정이라고 일반화할 수 없다. Snake 기능 검사와 웹사이트 유사도가 같은 평가 체계라는 근거도 없다.

## 연결

[[tech/devtools/build-check-iteration/04-learning/01-getting-started|첫 실습]] · [[tech/devtools/build-check-iteration/README|학습 지도]]

## Sources

- 사용자 제공 dossier: Craft Anything 소개 영상의 수집 요약. 원본 URL은 제공되지 않아 기재할 수 없다. 제품 구현·성능·라이선스는 별도 확인이 필요하다.
- 보조 학습: [Playwright Assertions](https://playwright.dev/docs/test-assertions) — 검사 작성 참고이며 Craft Anything의 사용 도구라는 근거는 아니다.
