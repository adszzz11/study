---
date: 2026-11-27
tags: [tech]
type: tech-tool-study
status: draft
---

# References와 근거 범위

## 자료 목록

| 자료 | 확인 가능한 범위 | 제약 |
|---|---|---|
| 제공된 Craft Anything 소개 영상 dossier | 단계 이름·반복 흐름·90%·6라운드·Snake 요청 예시 | 원본 URL·timestamp·원문 미제공 |

## 사실·해석·제안 구분

- **관찰 사실:** 수집 요약에 Browse, Build, Check, Complete와 두 종료 수치가 표시된다.
- **개념적 해석:** `score >= 0.90 OR rounds >= 6`으로 정책을 표현한다.
- **적용 제안:** 종료 이유 분리, 최고 결과 보관, 기능 검사 분리, 평가 환경 고정.
- **미확인:** metric, reference 선정, 실제 달성률, 기능 평가 범위, 반환 정책, 모델과 framework.

## 추가 자료 확보 시 확인할 항목

- 원본 영상 URL과 해당 장면의 timestamp
- Similarity 산식·점수 범위·평가 도구와 reference
- 라운드 계산 방식과 cap 도달 시 동작
- 실제 실행 로그, 시간·자원 사용량, 사람 평가와 점수의 일치 정도

URL을 확보하면 원문에서 확인한 사실과 기존 해석을 다시 대조한다. 현재는 제품의 실제 성능을 주장할 근거가 부족하다.

## 연결

[[tech/ai/website-similarity-stopping/01-overview|관찰 흐름과 해석]] · [[tech/ai/website-similarity-stopping/README|학습 경로]]

## Sources

- 제공된 dossier: Craft Anything 소개 영상의 수집 요약. 원본 영상 URL과 공식 문서 URL은 제공되지 않았다. 따라서 기재할 수 있는 출처 URL이 없으며, 임의로 추정하지 않는다.
- 아래 정책 해석과 실습 제안은 제품 구현이나 성능을 검증한 자료가 아니다.
