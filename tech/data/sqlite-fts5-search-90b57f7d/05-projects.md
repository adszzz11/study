---
date: 2026-11-23
tags: [tech]
type: tech-tool-study
status: draft
---

# Projects: 검색 의미를 검증하는 작은 실험

## 1. 이메일 검색 실험실

목표는 검색 UI의 표현과 실제 결과를 맞추는 것이다. 시작하기의 `email(sender, title, body)`를 사용한다.

| 단계 | 작업 | 완료 기준 |
|---|---|---|
| corpus | 연속·분리·역순 token 문서 작성 | phrase와 AND의 차이가 드러남 |
| query | prefix, title filter, 제외 조건 추가 | query별 기대 rowid 집합 기록 |
| 결과 | rank 정렬과 body 강조 | 일치 집합·정렬·표시를 각각 설명 |
| 변경 | 문서 수정·삭제 | 변경 후 기대 결과 재확인 |

정렬이 목적이 아닌 검증에서는 `ORDER BY rowid`로 결과를 비교한다. 관련도 점수의 공식은 추정하지 않는다.

## 2. Query builder 회귀 사례집

입력 조건을 FTS5 expression으로 조립하는 정책을 문서화한다.

- [ ] 공백 연결과 phrase 연결을 구분한다.
- [ ] 괄호 expression 사이에 명시적 operator를 생성한다.
- [ ] `NOT`에 왼쪽과 오른쪽 query가 존재하는지 확인한다.
- [ ] 구두점·double quote 입력의 quoting 사례를 수집한다.
- [ ] NEAR의 순서 비강제와 거리 경계 N/N+1을 검증한다.
- [ ] 중첩 column filter가 제외된 column을 복원하지 않음을 확인한다.

산출물은 `입력 의도 → 생성 query → 기대 문서 집합 → 실제 결과` 표다. 오류 사례와 빈 결과 사례를 구분해 기록한다.

## 3. 인덱스 설계 조사

같은 corpus와 query 집합으로 기본 구성, prefix index, 외부 content 구성의 검토 계획을 작성한다. 실행 전 공식 문서에서 설정과 동기화 절차를 추가 확인한다.

| 기록 항목 | 목적 |
|---|---|
| SQLite 버전·FTS5 활성화·tokenizer 설정 | 재현 조건 고정 |
| 문서 수·문서 길이·언어·query 분포 | workload 명시 |
| DB 크기·검색 지연·갱신 시간 | 저장 비용과 검색 비용 비교 |
| 변경·삭제 후 index 일관성 | 외부 content 검증 |

측정값 없이 특정 구성이 우수하다고 결론 내리지 않는다. 이 프로젝트는 조사·실험 제안이며 제공 자료가 성능을 보장한다는 뜻은 아니다.

## Navigation

[[tech/data/sqlite-fts5-search-90b57f7d/README|학습 가이드]]

## Sources

- https://www.sqlite.org/fts5.html
