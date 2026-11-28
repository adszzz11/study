---
date: 2026-11-26
tags: [tech]
type: tech-tool-study
status: draft
---

# Ecosystem: 관련 QA 유형 비교

## 비교 관점

자료에는 경쟁 제품·framework·측정 도구가 없다. 다음 항목은 도구의 대안이 아니라 대체로 서로 보완하는 QA 유형이다.

| 유형·항목 | 자료의 역할 | 속도·호환성과의 관계 | 자료의 한계 |
|---|---|---|---|
| Performance testing | 응답 속도 측정 | 속도 검증에 직접 연결 | 측정 구간·지표·합격선 없음 |
| 기기·브라우저 호환성 | 환경 간 호환성 확인 | 환경별 동작 검증에 직접 연결 | 지원 환경 목록 없음 |
| Smoke testing | 새 빌드의 핵심 기능을 빠르게 확인 | 상세 검증 전 핵심 동작 확인에 연결 가능 | 속도·호환성 보장 설명 없음 |
| Regression testing | 변경 후 기존 기능 재점검 | 기존 환경별 결과 재확인에 연결 가능 | 재검증 범위 없음 |
| Exploratory testing | 시나리오 없이 사용하며 버그 탐색 | 사전 항목 밖의 문제 탐색 보완 | 재현·기록 방법 없음 |
| Acceptance testing | 고객·기획 기준으로 출시 준비 확인 | 관찰 결과와 출시 기준 연결 | 구체적 수용 기준 없음 |
| Alpha/Beta testing | 내부 참여자와 실제 사용자 역할 구분 | 참여자 범위 고려 | 환경·측정 방식 없음 |
| Load testing | 전체 12종에 포함 | performance testing과 함께 등장 | 부하 조건과 응답 속도 관계 설명 없음 |

## 적용할 때의 구분

핵심 기능 확인 → 속도·환경별 상세 검증 → 기준에 따른 출시 검토로 연결하는 것은 실습 구성 제안이다. 영상이 이 실행 순서를 규정한 것은 아니다.

Load testing은 이름의 포함만 확인된다. 이 자료만으로 performance testing과의 세부 차이, 실행 방법, 부하 규모를 정할 수 없다. 도구 추천도 근거가 부족하므로 유보한다.

## 다음 학습

[[tech/devtools/response-time-compatibility/04-learning/01-getting-started|검증 기록 시작하기]] · [[tech/devtools/response-time-compatibility/README|학습 경로]]

## Sources

- 제공된 dossier: 영상 「핵심 기능 점검부터 보안까지, QA 테스트 12종 소개」 요약. **원본 URL 미제공**으로 출처 URL을 기재할 수 없다.
- 관련 시점: 00:35, 00:40. 각 시점과 개별 검증 항목의 정확한 대응은 확인되지 않았다.
- 실습 절차·기록 양식·프로젝트는 dossier에 근거한 학습 제안이며 영상의 상세 실행 절차가 아니다.
