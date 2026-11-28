---
date: 2026-11-23
tags: [tech]
type: tech-tool-study
status: draft
---

# References와 근거 범위

## 주 자료

- [SQLite FTS5 Extension](https://www.sqlite.org/fts5.html): 정의, 사용 예제, query 문법, 구성 및 확장 항목의 공식 진입점.
- 이 노트 묶음은 사용자가 제공한 dossier를 요약·재구성한다. 공식 문서 전체를 검증했다는 뜻은 아니다.

## 읽기 지도

| 공식 문서 영역 | 이 노트에서 다루는 범위 |
|---|---|
| Overview·빌드 | virtual table, 검색·정렬, 빌드 활성화 경로 |
| Full-text Query Syntax | string, phrase, prefix, initial token, NEAR, filter, Boolean |
| Table Creation and Initialization | column 정의 제약과 configuration 도입 |
| Configuration Options 이후 | 목차에서 확인된 기능의 존재·분류만 |

## 후속 확인 목록

- [ ] `bm25()` 계산식과 기본 `rank` 연결 관계를 원문에서 확인한다.
- [ ] prefix index의 정확한 설정 문법과 저장 비용을 확인한다.
- [ ] 외부 content 구성의 동기화·삭제·복구 절차를 확인한다.
- [ ] Unicode61, Ascii, Porter, Trigram의 세부 동작을 확인한다.
- [ ] FTS3/4 비교 및 porting guide에서 이전 제약을 확인한다.
- [ ] `%_idx`, `%_data`, `%_docsize`, `%_content`, `%_config`, Segment B-Tree의 상세 설명을 읽는다.

목차에 저장 구조 이름이 있다는 사실만으로 segment 병합 방식, 압축 효율, 읽기·쓰기 비용을 추정하지 않는다. 외부 제품 비교나 성능 수치를 추가할 때는 별도 출처와 재현 조건을 함께 남긴다.

## Navigation

[[tech/data/sqlite-fts5-search-90b57f7d/README|학습 가이드]]

## Sources

- https://www.sqlite.org/fts5.html
