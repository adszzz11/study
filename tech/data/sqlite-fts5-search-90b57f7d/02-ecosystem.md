---
date: 2026-11-23
tags: [tech]
type: tech-tool-study
status: draft
---

# FTS5 Ecosystem과 선택지 비교

## 비교 범위

제공 자료로 확인되는 SQLite 내부 선택지와 확장 지점을 비교한다. 외부 검색 제품의 성능·운영 특성이나 FTS3/4의 상세 차이는 근거가 없어 단정하지 않는다.

| 선택지 | 확인된 내용 | 선택·검토 관점 | 미확인 항목 |
|---|---|---|---|
| 일반 SQLite table | DML은 유사하나 생성 규칙은 다름 | 관계형 schema와 검색 schema 분리 | 일반 table 검색 대비 성능 수치 |
| FTS5 기본 사용 | token·phrase·prefix·NEAR·Boolean, 관련도 정렬 예제 | SQLite 안의 문서 검색 | 규모별 지연·처리량 |
| FTS5 + prefix index | 추가 disk index로 prefix query 가속 가능 | prefix 빈도와 저장 비용 | 설정 문법·크기 증가율 |
| FTS5 + 외부 content | 다른 곳의 content 인덱싱 가능 | 원문과 index의 저장 위치 | 동기화·삭제·복구 절차 |
| Custom tokenizer / auxiliary function | C 구현 및 등록 경로 | 기본 tokenization·결과 정보의 적합성 | 구현 API·언어별 품질 |
| FTS3/4 | 비교·porting guide가 목차에 있음 | 기존 구현 이전 검토 | 호환성·성능·기능 상세 |

## Tokenizer와 확장

Tokenizer 목차에는 Unicode61, Ascii, Porter, Trigram이 등장한다. 이름만으로 한국어 형태소 처리, substring 검색 품질, 설정값을 확정하지 않는다. 실제 입력 corpus로 기대 token과 검색 결과를 확인하는 과제가 필요하다.

`fts5.h`는 FTS5 extension 자체를 컴파일하는 데 필요하지 않지만 custom tokenizer나 auxiliary function을 구현하는 애플리케이션에서 사용한다.

## 인덱스 설계 질문

- 어떤 column을 검색하고 어떤 column은 표시·식별에 쓰는가?
- prefix 검색은 얼마나 자주 실행되는가? 추가 저장 비용을 측정할 수 있는가?
- 원문을 별도 저장한다면 index와의 일관성을 어떻게 검증할 것인가?
- 기본 tokenizer가 실제 언어와 구두점 처리 기대에 맞는가?

이는 검토 질문이다. 제공 자료만으로 특정 구성을 더 빠르거나 저렴하다고 결론 내릴 수 없다.

## Navigation

[[tech/data/sqlite-fts5-search-90b57f7d/README|학습 가이드]]

## Sources

- https://www.sqlite.org/fts5.html
