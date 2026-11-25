---
date: 2026-11-26
tags: [tech]
type: tech-tool-study
status: draft
---

# SQLite UPSERT의 충돌 처리와 조건부 갱신

> **한 줄 정의**: SQLite UPSERT는 `INSERT`가 uniqueness constraint를 위반할 때 해당 행을 `UPDATE`하거나 no-op으로 처리하도록 지정하는 `ON CONFLICT` 절이다.

## Overview

중복 입력을 기존 값 보존·누적·교체·조건부 교체 중 어떤 정책으로 처리할지 하나의 `INSERT`에 표현한다. 중복의 기준은 검색 조건이 아니라 schema의 `PRIMARY KEY`, `UNIQUE`, unique index다.

- `excluded.column`은 삽입하려던 값, 일반 column 참조는 기존 값이다.
- 여러 충돌 절은 행마다 첫 일치 하나만 실행하는 우선순위 분기다.
- `DO UPDATE` 중 제약 위반은 전체 `INSERT` 문장을 rollback한다.

## Learning Path

- [ ] [[tech/data/sqlite-upsert-dfce29f3/01-overview|Overview]] — 적용 범위와 핵심 구조
- [ ] [[tech/data/sqlite-upsert-dfce29f3/02-ecosystem|비교]] — 보존·누적·교체 정책 선택
- [ ] [[tech/data/sqlite-upsert-dfce29f3/04-learning/01-getting-started|시작하기]] — counter와 연락처 실습
- [ ] [[tech/data/sqlite-upsert-dfce29f3/04-learning/02-deep-dive|심화 학습]] — 조건부 갱신과 실패 경계
- [ ] [[tech/data/sqlite-upsert-dfce29f3/05-projects|Projects]] — 정책을 검증 가능한 작은 프로젝트로 구현
- [ ] [[tech/data/sqlite-upsert-dfce29f3/cheatsheet|Cheatsheet]] — 구문과 주의점 복습
- [ ] [[tech/data/sqlite-upsert-dfce29f3/03-references|References]] — 원문과 버전 범위 확인

## When To Use

- 같은 식별자의 counter를 누적하거나 연락처 값을 교체할 때
- 입력 날짜가 더 최신인 경우에만 기존 레코드를 갱신할 때
- unique constraint별로 서로 다른 중복 정책을 적용할 때

## When Not To Use

- 임의의 검색 조건으로 갱신 대상을 찾아야 할 때
- `NOT NULL`, `CHECK`, foreign key, trigger 제약 위반까지 복구하려 할 때
- virtual table을 대상으로 할 때: 제공 문서 기준 지원하지 않는다.

## Related Notes

- [[MOCs/Index]]
- [[MOCs/Data]]
- [[tech/data/sqlite-upsert-dfce29f3/01-overview|SQLite UPSERT 개념과 제약 범위]]
- [[tech/data/sqlite-upsert-dfce29f3/04-learning/02-deep-dive|조건부 갱신과 ABORT 실습]]

## Sources

- https://www.sqlite.org/lang_upsert.html
- 내용 기준: 제공 dossier가 인용한 문서 갱신일 **2024-04-11**. 이후 변경은 이 노트의 검토 범위 밖이다.
