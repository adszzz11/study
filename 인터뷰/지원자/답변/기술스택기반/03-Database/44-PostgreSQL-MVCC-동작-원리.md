# PostgreSQL의 MVCC 동작 원리는?

## 답변

[여기에 답변 작성]

## 핵심 키워드

- MVCC (Multi-Version Concurrency Control)
- Tuple Version
- Transaction ID (XID)
- Snapshot Isolation
- xmin, xmax
- Dead Tuple
- Visibility Rules

## MVCC 기본 원리

- 각 Row의 여러 버전 유지
- 읽기와 쓰기 작업이 서로 블로킹하지 않음
- Transaction Snapshot 기반 가시성 판단
- Undo 로그 대신 Old Version 유지

## Tuple Version 관리

- xmin: Tuple을 생성한 트랜잭션 ID
- xmax: Tuple을 삭제/수정한 트랜잭션 ID
- ctid: Tuple의 물리적 위치
- UPDATE는 INSERT + DELETE로 처리

## Snapshot Isolation

- Transaction 시작 시점의 Snapshot
- 각 트랜잭션은 일관된 데이터 뷰
- Visibility Map을 통한 최적화
- Frozen Transaction ID

## Dead Tuple과 Vacuum

- UPDATE/DELETE로 인한 Dead Tuple 생성
- Vacuum으로 Dead Tuple 정리
- Bloat 방지
- HOT (Heap Only Tuple) 최적화

## 코드/쿼리 예시

```sql
-- Tuple Version 확인
SELECT ctid, xmin, xmax, * FROM users;

-- Transaction ID 확인
SELECT txid_current();

-- 현재 Snapshot 정보
SELECT * FROM pg_current_snapshot();

-- Vacuum 상태 확인
SELECT relname, n_live_tup, n_dead_tup,
       last_vacuum, last_autovacuum
FROM pg_stat_user_tables
WHERE schemaname = 'public';

-- MVCC 동작 예시
-- Session 1
BEGIN;
SELECT * FROM accounts WHERE id = 1; -- balance = 1000
-- xmin = 100, xmax = 0

-- Session 2
BEGIN;
UPDATE accounts SET balance = 1500 WHERE id = 1;
-- 새 Tuple: xmin = 101, xmax = 0
-- 기존 Tuple: xmin = 100, xmax = 101
COMMIT;

-- Session 1 (계속)
SELECT * FROM accounts WHERE id = 1; -- balance = 1000 (여전히)
-- Session 1의 Snapshot에서는 xmin=100인 버전만 보임
COMMIT;

-- Visibility 확인 쿼리
SELECT
  lp as tuple,
  t_xmin,
  t_xmax,
  t_ctid
FROM heap_page_items(get_raw_page('accounts', 0));
```

## 참고 자료

- PostgreSQL Internals - MVCC
- Understanding PostgreSQL MVCC
