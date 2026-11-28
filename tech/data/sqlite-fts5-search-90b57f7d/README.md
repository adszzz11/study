---
date: 2026-11-23
tags: [tech]
type: tech-tool-study
status: draft
---

# SQLite FTS5의 검색 모델과 인덱스 설계

> **한 줄 정의**: SQLite FTS5는 문서를 token 단위로 인덱싱하고 phrase·prefix·proximity·Boolean 검색을 SQL에서 수행하게 하는 SQLite virtual table module이다.

## Overview

문서 검색은 많은 문서에서 검색 조건에 맞는 부분집합을 찾는 문제다. FTS5는 이를 SQLite의 SQL 인터페이스에 통합한다. 핵심은 **원문 문자열이 아니라 tokenizer가 추출한 token을 검색한다**는 점이다.

- SQL로 검색용 virtual table을 만들고 `INSERT`, `UPDATE`, `DELETE`로 변경한다.
- phrase, prefix, `NEAR`, column filter, Boolean expression으로 검색 의도를 표현한다.
- 일치 문서 선택과 `ORDER BY rank`를 통한 관련도 정렬을 구분한다.
- tokenizer, prefix index, 외부 content 구성은 검색 모델과 저장 설계를 함께 검토할 지점이다.

이 노트는 제공 dossier를 근거로 한다. 확인된 본문 범위는 공식 문서 4장 configuration option 도입부까지이며, 이후 기능은 존재와 분류만 기록한다. BM25 계산식, 저장 구조의 성능, 외부 content 동기화 절차는 확정하지 않는다.

## Learning Path

- [ ] [[tech/data/sqlite-fts5-search-90b57f7d/README|학습 가이드]] — 전체 목표와 사용 적합성 확인
- [ ] [[tech/data/sqlite-fts5-search-90b57f7d/01-overview|Overview]] — What/Why와 virtual table 구조
- [ ] [[tech/data/sqlite-fts5-search-90b57f7d/02-ecosystem|Ecosystem]] — SQLite 내부 선택지 비교
- [ ] [[tech/data/sqlite-fts5-search-90b57f7d/03-references|References]] — 확인 범위와 추가 조사 항목
- [ ] [[tech/data/sqlite-fts5-search-90b57f7d/04-learning/01-getting-started|시작하기]] — 생성·문서 변경·검색·정렬 실습
- [ ] [[tech/data/sqlite-fts5-search-90b57f7d/04-learning/02-deep-dive|Deep Dive]] — phrase·NEAR·Boolean 의미와 query builder
- [ ] [[tech/data/sqlite-fts5-search-90b57f7d/05-projects|Projects]] — 검색 회귀 실험과 설계 과제
- [ ] [[tech/data/sqlite-fts5-search-90b57f7d/cheatsheet|Cheatsheet]] — 문법과 주의점 빠른 참조

## When To Use

- SQLite 기반 애플리케이션에서 문서 검색을 SQL로 다루고 싶을 때.
- 단어 포함 여부를 넘어 연속 phrase, prefix, proximity, column별 조건이 필요할 때.
- 관련도 정렬과 일치 부분 강조를 검색 결과에 결합할 때.

## When Not To Use

- 원문 문자열의 임의 부분 일치만을 기대하고 tokenization 차이를 허용할 수 없을 때.
- 일반 관계형 table의 type·constraint·PRIMARY KEY 선언을 검색 table에 그대로 적용하려 할 때.
- 언어별 검색 품질이나 대규모 처리 성능을 검증 없이 보장해야 할 때. 제공 자료에는 이를 판단할 측정값이 없다.

## Related Notes

- [[MOCs/Index]]
- [[MOCs/Data]]
- [[tech/data/dolt/README|Dolt 학습 가이드]] — SQL 데이터 관리라는 공통 주제. 버전 관리와 full-text 검색은 별도의 설계 축이다.

## Sources

- https://www.sqlite.org/fts5.html
