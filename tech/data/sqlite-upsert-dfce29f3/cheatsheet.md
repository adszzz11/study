---
date: 2026-11-26
tags: [tech]
type: tech-tool-study
status: draft
---

# SQLite UPSERT Cheatsheet

## 기본 패턴

```sql
-- 보존
INSERT INTO phonebook VALUES('Alice', '111')
ON CONFLICT(name) DO NOTHING;

-- 교체
INSERT INTO phonebook VALUES('Alice', '222')
ON CONFLICT(name) DO UPDATE SET phonenumber = excluded.phonenumber;

-- 누적
INSERT INTO vocabulary(word) VALUES('jovial')
ON CONFLICT(word) DO UPDATE SET count = count + 1;

-- 조건부 교체
INSERT INTO phonebook2 VALUES('Alice', '333', '2018-05-09')
ON CONFLICT(name) DO UPDATE SET
  phonenumber = excluded.phonenumber, validDate = excluded.validDate
WHERE excluded.validDate > phonebook2.validDate;
```

## 빠른 점검

| 항목 | 기억할 점 |
|---|---|
| 발동 대상 | `PRIMARY KEY`, `UNIQUE`, unique index 위반 |
| 기존 값 | `column` 또는 `table.column` |
| 입력 후보 | `excluded.column` |
| 여러 절 | 작성 순서, 행마다 첫 일치 하나 |
| target 생략 | 마지막 절에서만 가능 |
| 조건부 WHERE | 대상 검색이 아니라 갱신 허용 여부 |
| multi-row | 정상 분기는 행별, 갱신 제약 위반은 문장 전체 rollback |
| 실패 algorithm | `DO UPDATE`는 항상 `ABORT` |
| 범위 밖 | `NOT NULL`, `CHECK`, foreign key, trigger 제약을 UPSERT로 복구하지 못함 |
| virtual table | 제공 문서 기준 미지원 |
| 버전 | 기본 3.24.0+, 복수 절/target 없는 UPDATE는 3.35.0+ |

## SELECT 입력

```sql
INSERT INTO t1 SELECT * FROM t2 WHERE true
ON CONFLICT(x) DO UPDATE SET y = excluded.y;
```

필터가 없어도 `WHERE true`로 `ON`의 parsing ambiguity를 피한다.

## Sources

- https://www.sqlite.org/lang_upsert.html
- 내용 기준: 제공 dossier가 인용한 문서 갱신일 **2024-04-11**. 이후 변경은 이 노트의 검토 범위 밖이다.
