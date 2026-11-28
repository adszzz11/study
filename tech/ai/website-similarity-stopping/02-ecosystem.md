---
date: 2026-11-27
tags: [tech]
type: tech-tool-study
status: draft
---

# Ecosystem: 종료 정책 비교

수집 자료에 경쟁 제품 정보가 없어 제품 순위 대신 정책 구조를 비교한다. 장단점은 구조에서 도출한 분석이다.

| 방식 | 종료 기준 | 장점 | 한계 |
|---|---|---|---|
| Single-pass | 최초 생성 후 종료 | 단순한 흐름 | 검사 후 개선 기회 없음 |
| Fixed-round | 지정 횟수 도달 | 횟수 예측 용이 | 충분한 결과도 계속 실행 가능 |
| Threshold-only | 목표 점수 달성 | 품질 목표 명확 | 미달 시 별도 종료 장치 필요 |
| Threshold + iteration cap | 목표 달성 또는 횟수 한도 | 목표와 실행 한도 병행 | 한도 종료는 목표 미달 가능 |
| Human review | 사용자 승인 | 점수 밖의 요구 판단 가능 | 검토 시간과 판단 필요 |

영상의 조건은 개념적으로 Threshold + iteration cap에 해당한다. Iteration cap은 횟수만 제한한다. 라운드별 소요 시간과 자원 사용량을 모르므로 총시간과 총비용이 고정된다고 볼 수 없다.

## 선택 기준

- 빠른 초안: Single-pass 이후 필요에 따라 검토한다.
- 반복 제작 실험: threshold와 cap을 함께 두고 종료 이유를 기록한다.
- 점수로 포착하기 어려운 요구: Human review를 별도 승인 단계로 결합한다.

이 선택 기준은 실습 설계 제안이며 제품 기능 목록이 아니다. 90%와 6회가 다른 작업에도 적합한 기본값이라는 근거는 없다.

## 다음 학습

[[tech/ai/website-similarity-stopping/04-learning/01-getting-started|평가 조건과 기록부터 시작하기]] · [[tech/ai/website-similarity-stopping/README|학습 경로]]

## Sources

- 제공된 dossier: Craft Anything 소개 영상의 수집 요약. 원본 영상 URL과 공식 문서 URL은 제공되지 않았다. 따라서 기재할 수 있는 출처 URL이 없으며, 임의로 추정하지 않는다.
- 아래 정책 해석과 실습 제안은 제품 구현이나 성능을 검증한 자료가 아니다.
