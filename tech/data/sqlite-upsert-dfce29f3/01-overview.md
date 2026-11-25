---
date: 2026-11-26
tags: [tech]
type: tech-tool-study
status: draft
---

# SQLite UPSERT 개요

## What

UPSERT는 `INSERT`에 붙는 비표준 SQL 확장이다. SQLite는 PostgreSQL 구문을 따르면서 확장했다. 기존 행을 임의로 검색하는 기능이 아니라 uniqueness constraint 위반에 반응한다.

```sql
INSERT INTO phonebook(name, phonenumber)
VALUES ('Alice', '704-555-1212')
ON CONFLICT(name) DO UPDATE SET
  phonenumber = excluded.phonenumber;
```

## Why

적재 데이터의 동일 식별자가 이미 존재할 수 있다. 단어 빈도는 누적하고 연락처는 교체하며 날짜가 있는 데이터는 최신 값만 반영해야 한다. UPSERT는 이 정책을 삽입과 함께 명시한다. 먼저 schema에서 무엇을 동일 데이터로 볼지 결정해야 한다.

## 특징과 실행 구조

1. 삽입을 시도한다.
2. `PRIMARY KEY`, `UNIQUE`, unique index 위반이면 충돌 절을 순서대로 검사한다.
3. 각 행에서 처음 일치한 절 하나만 실행하고 나머지는 건너뛴다.
4. `DO NOTHING`은 no-op, `DO UPDATE`는 기존 행 갱신이다.

마지막 절만 conflict target을 생략할 수 있다. 이 절은 앞선 절이 처리하지 않은 uniqueness constraint 위반을 받는다. 여러 절은 갱신 pipeline이 아니다.

| 값 참조 | 의미 | 예시 |
|---|---|---|
| `count` 또는 `vocabulary.count` | 삽입 시도 전 기존 값 | `count = count + 1` |
| `excluded.phonenumber` | 삽입하려던 후보 값 | 번호 교체 |
| `excluded.validDate > phonebook2.validDate` | 신규·기존 값 비교 | 최신 데이터만 반영 |

## 적용 경계

- multi-row insert도 분기는 행마다 결정한다.
- `NOT NULL`, `CHECK`, foreign key, trigger로 구현한 제약은 UPSERT의 발동 대상이 아니다.
- `DO UPDATE` 중 제약 위반은 항상 `ABORT`: 전체 `INSERT` 문장이 rollback된다. transaction 전체의 무조건적인 rollback을 뜻하지 않는다.
- 제공 문서 기준 virtual table에서는 지원하지 않는다.

## 버전

| 버전 | 날짜 | 변화 |
|---|---|---|
| 3.24.0 | 2018-06-04 | 도입. 단일 충돌 절, `DO UPDATE` target 필수 |
| 3.35.0 | 2021-03-12 | 여러 충돌 절과 target 없는 `DO UPDATE` 허용 |

## Sources

- https://www.sqlite.org/lang_upsert.html
- 내용 기준: 제공 dossier가 인용한 문서 갱신일 **2024-04-11**. 이후 변경은 이 노트의 검토 범위 밖이다.
