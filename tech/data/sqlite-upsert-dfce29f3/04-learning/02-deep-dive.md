---
date: 2026-11-26
tags: [tech]
type: tech-tool-study
status: draft
---

# 심화: 조건부 갱신과 실패 경계

## 1. 최신 데이터만 반영

```sql
CREATE TABLE phonebook2(name TEXT PRIMARY KEY, phonenumber TEXT, validDate DATE);
INSERT INTO phonebook2 VALUES('Alice', '111', '2018-05-08');
INSERT INTO phonebook2 VALUES('Alice', '222', '2018-05-09')
ON CONFLICT(name) DO UPDATE SET
  phonenumber = excluded.phonenumber,
  validDate = excluded.validDate
WHERE excluded.validDate > phonebook2.validDate;
```

예상 결과는 `Alice | 222 | 2018-05-09`다. 같은 패턴으로 이전 날짜·동일 날짜를 넣으면 no-op이다. 날짜 실습은 비교 순서가 유지되는 `YYYY-MM-DD` 문자열을 사용한다. 임의 날짜 형식의 자동 정규화를 가정하지 않는다.

| WHERE 위치 | 역할 |
|---|---|
| conflict target 쪽 | 충돌 대상을 기술하는 구문의 일부. 상세 규칙은 제공 자료 범위 밖 |
| `DO UPDATE` 끝 | 이미 충돌한 행의 갱신 허용 여부 결정 |

끝의 `WHERE`에 대상 행을 다시 찾는 조건은 필요하지 않다. 새 날짜가 더 클 때만 갱신하므로 동일 날짜도 no-op이다.

## 2. 첫 일치 절만 실행

SQLite 3.35.0 이상에서 실행한다.

```sql
CREATE TABLE accounts(id INTEGER PRIMARY KEY, email TEXT UNIQUE, hits INT);
INSERT INTO accounts VALUES(1, 'a@example.test', 1);
INSERT INTO accounts VALUES(1, 'a@example.test', 100)
ON CONFLICT(id) DO UPDATE SET hits = hits + 1
ON CONFLICT(email) DO UPDATE SET hits = hits + 100
ON CONFLICT DO NOTHING;
SELECT * FROM accounts;
-- 예상: 1 | a@example.test | 2
```

id와 email이 모두 충돌해도 첫 절만 실행된다. 마지막 target 없는 절은 앞의 절이 처리하지 않은 uniqueness constraint 위반을 받는다.

## 3. 행별 분기와 문장 rollback

아래 마지막 `INSERT`는 의도적으로 실패한다. 오류 이후의 조회는 별도 실행한다.

```sql
CREATE TABLE items(id INTEGER PRIMARY KEY, qty INT CHECK(qty >= 0));
INSERT INTO items VALUES(1, 10);
INSERT INTO items VALUES(2, 20), (1, -1)
ON CONFLICT(id) DO UPDATE SET qty = excluded.qty;
-- CHECK constraint failed
SELECT * FROM items;
-- 예상: 1 | 10 만 존재. 먼저 삽입한 id=2도 rollback됨.
```

id 충돌로 시작한 `DO UPDATE`가 `CHECK`를 위반한다. 이때 항상 `ABORT`이므로 전체 `INSERT`가 rollback된다. 바깥 `INSERT`나 trigger가 지정한 다른 conflict algorithm도 이를 바꾸지 못한다. 더 큰 transaction의 모든 작업까지 무조건 rollback된다고 해석하지 않는다.

실패 입력의 qty를 30으로 바꾸면 id=2는 삽입, id=1은 갱신된다. 즉 정상 경로에서는 같은 문장 안에서도 행별 처리가 다르다.

## 4. INSERT ... SELECT의 parsing ambiguity

```sql
CREATE TABLE t1(x INT PRIMARY KEY, y TEXT);
CREATE TABLE t2(x INT, y TEXT);
INSERT INTO t2 VALUES(1, 'new');
INSERT INTO t1
SELECT * FROM t2 WHERE true
ON CONFLICT(x) DO UPDATE SET y = excluded.y;
```

`SELECT`의 `WHERE`가 없으면 `ON`을 join 구문으로 볼지 UPSERT로 볼지 모호할 수 있다. 필터가 필요 없어도 문서의 권고대로 `WHERE true`를 포함한다.

## 로컬 검증 기록

2026-11-26, Python `sqlite3` / SQLite 3.54.1의 in-memory database에서 예제를 실행했다. counter 누적, 번호 교체·보존, 날짜 이전·동일·이후 분기, 첫 충돌 절만 실행, 정상 multi-row 처리, CHECK 실패 시 문장 rollback, SELECT 입력 구문을 확인했다.

## Sources

- https://www.sqlite.org/lang_upsert.html
- 내용 기준: 제공 dossier가 인용한 문서 갱신일 **2024-04-11**. 이후 변경은 이 노트의 검토 범위 밖이다.
