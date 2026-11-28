---
date: 2026-11-26
tags: [tech]
type: tech-tool-study
status: draft
---

# 시작하기: 누적과 교체

## 준비

SQLite CLI 또는 SQLite 연결이 있는 환경에서 빈 database로 시작한다. `SELECT sqlite_version();`으로 버전을 확인한다. 아래 기본 UPSERT는 3.24.0 이상이 필요하다.

## 1. 기존 값으로 counter 누적

```sql
CREATE TABLE vocabulary(word TEXT PRIMARY KEY, count INT DEFAULT 1);
INSERT INTO vocabulary(word) VALUES('jovial')
ON CONFLICT(word) DO UPDATE SET count = count + 1;
INSERT INTO vocabulary(word) VALUES('jovial')
ON CONFLICT(word) DO UPDATE SET count = count + 1;
SELECT word, count FROM vocabulary;
-- 예상: jovial | 2
```

첫 입력은 기본값 1을 삽입한다. 두 번째 입력의 `count`는 기존 값을 가리켜 2가 된다. `excluded.count`로 교체하면 누적과 의미가 달라진다.

## 2. 입력 후보로 번호 교체

```sql
CREATE TABLE phonebook(name TEXT PRIMARY KEY, phonenumber TEXT);
INSERT INTO phonebook VALUES('Alice', '111');
INSERT INTO phonebook VALUES('Alice', '222')
ON CONFLICT(name) DO UPDATE SET phonenumber = excluded.phonenumber;
SELECT * FROM phonebook;
-- 예상: Alice | 222

INSERT INTO phonebook VALUES('Alice', '333')
ON CONFLICT(name) DO NOTHING;
SELECT * FROM phonebook;
-- 예상: Alice | 222
```

`excluded`는 충돌이 없었다면 삽입했을 값이다. `DO NOTHING`은 기존 번호를 유지한다.

## 확인 목록

- [ ] counter가 두 번 실행 후 2인지 확인한다.
- [ ] 번호 교체 후 `DO NOTHING`으로 기존 번호가 보존되는지 확인한다.
- [ ] primary key를 제거하면 동일 이름이 중복 삽입되는 이유를 설명한다.

## 로컬 검증 기록

2026-11-26, Python `sqlite3` / SQLite 3.54.1의 in-memory database에서 예제를 실행했다. counter 누적, 번호 교체·보존, 날짜 이전·동일·이후 분기, 첫 충돌 절만 실행, 정상 multi-row 처리, CHECK 실패 시 문장 rollback, SELECT 입력 구문을 확인했다.

## Sources

- https://www.sqlite.org/lang_upsert.html
- 내용 기준: 제공 dossier가 인용한 문서 갱신일 **2024-04-11**. 이후 변경은 이 노트의 검토 범위 밖이다.
