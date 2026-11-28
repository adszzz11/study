---
date: 2026-11-23
tags: [tech]
type: tech-tool-study
status: draft
---

# 시작하기: WAL 전환과 Snapshot 관찰

## 준비

실제 운영 파일이 아닌 로컬 실습용 database를 사용한다. SQLite CLI 두 개를 같은 host에서 같은 파일로 연결한다. 다음 SQL은 실습 제안이며 실행 결과를 기록한 것은 아니다.

```sh
sqlite3 wal-lab.db
```

## 1. 버전과 WAL 활성화 확인

```sql
SELECT sqlite_version();
PRAGMA journal_mode=WAL;
PRAGMA journal_mode;
PRAGMA synchronous;
PRAGMA wal_autocheckpoint;
CREATE TABLE IF NOT EXISTS counter(id INTEGER PRIMARY KEY, value INTEGER);
INSERT OR IGNORE INTO counter VALUES(1, 0);
```

`journal_mode=WAL`의 반환값이 `wal`인지 확인한다. VFS가 필요한 shared-memory 기능을 제공하지 않으면 이전 mode가 반환될 수 있다. WAL mode는 재연결해도 유지되고 같은 database의 모든 connection에 적용된다.

## 2. Reader와 writer 동시 실행

connection A에서 읽기를 시작한다. 실제 SELECT가 snapshot을 관찰하도록 한다.

```sql
BEGIN;
SELECT value FROM counter WHERE id=1;
```

A의 transaction을 유지한 채 connection B에서 실행한다.

```sql
BEGIN;
UPDATE counter SET value=value+1 WHERE id=1;
COMMIT;
```

A에서 다시 읽은 뒤 transaction을 종료하고 새로 읽는다.

```sql
SELECT value FROM counter WHERE id=1;
COMMIT;
SELECT value FROM counter WHERE id=1;
```

예상 관찰: A의 기존 transaction은 기존 값을 유지하고, transaction 종료 후 새 읽기는 B의 변경을 본다. reader–writer 공존을 확인하는 실습이며 여러 writer의 병렬 실행을 뜻하지 않는다.

## 3. Checkpoint 호출과 종료

```sql
PRAGMA wal_checkpoint;
```

호출 자체가 완료를 보장하지 않는다. 활성 reader와 WAL frame 반영 상태를 함께 살핀다. 일반 checkpoint 뒤에도 WAL의 물리 크기는 유지될 수 있다. 두 connection을 정상 종료한 후 파일 상태를 관찰하되 `-wal`을 수동 삭제하지 않는다.

## 운영 전 확인

- `page_size` 변경은 WAL mode를 벗어난 뒤 수행한다.
- 여러 ATTACH database 전체의 atomicity를 전제로 하지 않는다.
- read-only WAL은 3.22.0 이상에서도 WAL·SHM의 가독성, directory 생성 권한, 또는 immutable 조건을 확인한다.
- read-only media 배포는 `journal_mode=DELETE` 전환을 검토한다.

## 다음 단계

[[tech/backend/sqlite-wal-architecture-d6f43ae0/04-learning/02-deep-dive|Checkpoint와 내구성]] · [[tech/backend/sqlite-wal-architecture-d6f43ae0/README|학습 경로]]

## Sources

- https://www.sqlite.org/wal.html — 제공된 dossier의 본문 범위(§6 checkpoint starvation 설명 도중까지)를 근거로 정리.
