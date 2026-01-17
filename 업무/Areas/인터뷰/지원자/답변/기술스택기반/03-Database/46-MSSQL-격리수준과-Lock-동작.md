# MSSQL의 격리 수준과 Lock 동작 방식은?

## 답변

[여기에 답변 작성]

## 핵심 키워드

- Transaction Isolation Level
- Lock
- Shared Lock (S)
- Exclusive Lock (X)
- Row Versioning
- SNAPSHOT Isolation
- NOLOCK Hint
- Deadlock

## 격리 수준 (Isolation Level)

1. READ UNCOMMITTED: Dirty Read 허용
2. READ COMMITTED: 기본 수준, Shared Lock
3. REPEATABLE READ: 읽은 데이터 재읽기 보장
4. SERIALIZABLE: 가장 높은 격리 수준
5. SNAPSHOT: Row Versioning 기반

## Lock 유형

- Shared Lock (S): 읽기 시 획득
- Exclusive Lock (X): 쓰기 시 획득
- Update Lock (U): UPDATE 시 Deadlock 방지
- Intent Lock (IS, IX, IU)
- Schema Lock (Sch-S, Sch-M)

## Lock 단위 (Granularity)

- Row Lock (RID)
- Page Lock (PAG)
- Table Lock (TAB)
- Database Lock (DB)
- Lock Escalation

## Row Versioning

- SNAPSHOT Isolation
- READ_COMMITTED_SNAPSHOT
- tempdb의 Version Store 사용
- 읽기 작업 비차단

## 코드/쿼리 예시

```sql
-- 격리 수준 설정
SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED;
SET TRANSACTION ISOLATION LEVEL READ COMMITTED;
SET TRANSACTION ISOLATION LEVEL REPEATABLE READ;
SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;
SET TRANSACTION ISOLATION LEVEL SNAPSHOT;

-- 현재 격리 수준 확인
DBCC USEROPTIONS;

-- NOLOCK Hint (READ UNCOMMITTED와 동일)
SELECT * FROM orders WITH (NOLOCK);

-- Lock Hint 사용
SELECT * FROM orders WITH (ROWLOCK, UPDLOCK);
SELECT * FROM orders WITH (TABLOCKX);

-- 활성 Lock 확인
SELECT
  resource_type,
  resource_database_id,
  resource_associated_entity_id,
  request_mode,
  request_type,
  request_status,
  request_session_id
FROM sys.dm_tran_locks
WHERE request_session_id = @@SPID;

-- Deadlock 모니터링
SELECT
  blocking_session_id,
  wait_type,
  wait_time,
  wait_resource
FROM sys.dm_exec_requests
WHERE blocking_session_id <> 0;

-- SNAPSHOT Isolation 활성화
ALTER DATABASE MyDB
SET ALLOW_SNAPSHOT_ISOLATION ON;

ALTER DATABASE MyDB
SET READ_COMMITTED_SNAPSHOT ON;

-- Lock Timeout 설정
SET LOCK_TIMEOUT 5000; -- 5초

-- Transaction 예시
BEGIN TRANSACTION;
  UPDATE accounts SET balance = balance - 100 WHERE id = 1;
  UPDATE accounts SET balance = balance + 100 WHERE id = 2;
COMMIT TRANSACTION;
```

## 참고 자료

- MSSQL Transaction Locking and Row Versioning Guide
- Understanding Isolation Levels
