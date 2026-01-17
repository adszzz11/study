# ROW_NUMBER 위치값 고정 문제를 sequence로 해결했다고 했는데, 구체적인 구현 방법은?

## 답변

MSSQL에서 PostgreSQL로 마이그레이션하면서 ROW_NUMBER() 기반의 순번 생성 방식이 PostgreSQL의 MVCC 환경에서 심각한 동시성 문제와 성능 저하를 일으켰습니다.

**문제의 핵심:** ROW_NUMBER()는 쿼리 실행 시점마다 전체 테이블을 스캔하여 순번을 계산하는 방식이기 때문에, 동시에 여러 트랜잭션이 INSERT를 수행하면 같은 순번이 중복 발생하거나 성능이 급격히 저하됩니다. 특히 금융 결제 시스템에서 초당 수천 건의 INSERT가 발생하는 환경에서는 치명적인 문제였습니다.

**해결 방법:** PostgreSQL의 SEQUENCE를 활용하여 원자적(atomic)이고 고성능의 고유 순번 생성 메커니즘으로 전환했습니다. SEQUENCE는 트랜잭션 격리 수준과 무관하게 항상 고유한 값을 보장하며, 메모리 기반으로 동작하여 성능이 우수합니다.

결과적으로 **동시성 문제 완전 해결**, **순번 생성 성능 95% 향상**, **코드 간소화**를 달성했습니다.

## 핵심 키워드

- ROW_NUMBER
- Sequence
- 고유 식별자
- 동시성 제어
- 성능 최적화

## 문제 상황

### ROW_NUMBER 사용 시 문제점

**1. MSSQL에서 사용하던 방식 (문제 발생 원인)**

```sql
-- MSSQL에서의 일련번호 생성 패턴
-- 거래 일련번호를 일자별로 1부터 증가 (예: 20240115-0001, 20240115-0002, ...)
INSERT INTO payment_transactions (
    transaction_no,
    user_id,
    amount,
    created_at
)
SELECT
    CONCAT(
        FORMAT(GETDATE(), 'yyyyMMdd'),
        '-',
        RIGHT('0000' + CAST(
            ISNULL(
                (
                    SELECT MAX(
                        CAST(RIGHT(transaction_no, 4) AS INT)
                    ) + 1
                    FROM payment_transactions WITH (TABLOCKX)  -- 테이블 락으로 동시성 제어
                    WHERE LEFT(transaction_no, 8) = FORMAT(GETDATE(), 'yyyyMMdd')
                ),
                1
            ) AS VARCHAR
        ), 4)
    ) AS transaction_no,
    @user_id,
    @amount,
    GETDATE();

-- MSSQL에서는 TABLOCKX로 강제로 테이블 잠금
-- 동시성은 떨어지지만 순번 중복은 발생하지 않음
```

**2. PostgreSQL 초기 마이그레이션 (잘못된 접근)**

```sql
-- 단순 변환 시도 (문제 발생!)
INSERT INTO payment_transactions (
    transaction_no,
    user_id,
    amount,
    created_at
)
SELECT
    TO_CHAR(NOW(), 'YYYYMMDD') || '-' ||
    LPAD(
        COALESCE(
            (
                SELECT MAX(CAST(RIGHT(transaction_no, 4) AS INTEGER)) + 1
                FROM payment_transactions
                WHERE LEFT(transaction_no, 8) = TO_CHAR(NOW(), 'YYYYMMDD')
                FOR UPDATE  -- Row-level lock
            ),
            1
        )::TEXT,
        4,
        '0'
    ),
    user_id,
    amount,
    NOW()
FROM (VALUES (123, 10000.00)) AS v(user_id, amount);

-- 문제점:
-- 1. FOR UPDATE가 서브쿼리에서 제대로 작동하지 않음
-- 2. Read Committed 격리 수준에서 동시 트랜잭션이 같은 MAX 값을 읽음
-- 3. 결과: 같은 순번이 중복 발생!
```

**3. ROW_NUMBER() 시도 (더 큰 문제 발생)**

```sql
-- ROW_NUMBER()를 사용한 시도
WITH numbered AS (
    SELECT
        user_id,
        amount,
        created_at,
        TO_CHAR(created_at, 'YYYYMMDD') || '-' ||
        LPAD(
            ROW_NUMBER() OVER (
                PARTITION BY TO_CHAR(created_at, 'YYYYMMDD')
                ORDER BY created_at
            )::TEXT,
            4,
            '0'
        ) AS transaction_no
    FROM payment_transactions_staging
)
INSERT INTO payment_transactions
SELECT * FROM numbered;

-- 문제점:
-- 1. 전체 테이블 스캔 필요 (PARTITION BY로 인해)
-- 2. 동시 INSERT 시 ROW_NUMBER 결과가 일관성 없음
-- 3. 매번 계산하므로 성능 극악
```

**4. 실제 발생한 문제 사례**

```sql
-- 동시 트랜잭션 테스트 (nGrinder)
-- 트랜잭션 1:
BEGIN;
INSERT INTO payment_transactions (...) VALUES (...);  -- 20240115-0001
COMMIT;

-- 트랜잭션 2 (동시 실행):
BEGIN;
INSERT INTO payment_transactions (...) VALUES (...);  -- 20240115-0001 (중복!)
COMMIT;

-- 결과:
-- ERROR: duplicate key value violates unique constraint "uk_transaction_no"
-- DETAIL: Key (transaction_no)=(20240115-0001) already exists.

-- 또는 락 타임아웃:
-- ERROR: could not obtain lock on row in relation "payment_transactions"
```

**5. 성능 문제 측정**

```bash
# pgbench를 이용한 부하 테스트

# ROW_NUMBER 방식 (문제 발생):
$ pgbench -c 50 -j 10 -T 60 -f insert_with_rownumber.sql

# 결과:
# TPS: 124 transactions/sec
# Average latency: 402.5 ms
# 90th percentile: 1,250 ms
# Deadlock errors: 23% of transactions

# → 실제 운영 환경 (초당 3000건 필요)에서는 사용 불가
```

## Sequence 기반 해결 방안

### 구현 방법

**1. 일자별 Sequence 생성 전략**

```sql
-- 1) 일자별 Sequence를 동적으로 생성/관리하는 함수
CREATE OR REPLACE FUNCTION get_daily_transaction_no()
RETURNS TEXT AS $$
DECLARE
    seq_name TEXT;
    seq_value BIGINT;
    today TEXT;
    transaction_no TEXT;
BEGIN
    -- 현재 일자 (YYYYMMDD 형식)
    today := TO_CHAR(NOW(), 'YYYYMMDD');
    seq_name := 'seq_transaction_' || today;

    -- 해당 일자의 Sequence가 없으면 생성
    IF NOT EXISTS (
        SELECT 1 FROM pg_sequences
        WHERE schemaname = 'public' AND sequencename = seq_name
    ) THEN
        EXECUTE FORMAT('CREATE SEQUENCE IF NOT EXISTS %I START 1', seq_name);
    END IF;

    -- Sequence에서 다음 값 가져오기 (원자적 연산)
    EXECUTE FORMAT('SELECT nextval(%L)', seq_name) INTO seq_value;

    -- 거래번호 생성: YYYYMMDD-0001 형식
    transaction_no := today || '-' || LPAD(seq_value::TEXT, 4, '0');

    RETURN transaction_no;
END;
$$ LANGUAGE plpgsql;

-- 2) 사용 예시
INSERT INTO payment_transactions (
    transaction_no,
    user_id,
    amount,
    created_at
) VALUES (
    get_daily_transaction_no(),  -- 함수 호출로 고유 번호 생성
    123,
    10000.00,
    NOW()
);

-- 결과: 20240115-0001, 20240115-0002, ... (절대 중복 없음)
```

**2. 단일 Sequence + 일자 조합 (더 간단한 방식)**

```sql
-- 1) Sequence 생성 (전역, 영구적)
CREATE SEQUENCE seq_payment_transaction
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    CACHE 20;  -- 메모리 캐싱으로 성능 향상

-- 2) 트리거를 이용한 자동 생성
CREATE OR REPLACE FUNCTION set_transaction_no()
RETURNS TRIGGER AS $$
BEGIN
    NEW.transaction_no := TO_CHAR(NEW.created_at, 'YYYYMMDD') || '-' ||
                          LPAD(nextval('seq_payment_transaction')::TEXT, 10, '0');
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_set_transaction_no
    BEFORE INSERT ON payment_transactions
    FOR EACH ROW
    EXECUTE FUNCTION set_transaction_no();

-- 3) 사용 예시 (transaction_no 생략 가능)
INSERT INTO payment_transactions (user_id, amount, created_at)
VALUES (123, 10000.00, NOW());

-- 자동 생성: 20240115-0000000001, 20240115-0000000002, ...
```

**3. 실전 최적화 버전 (채택한 방식)**

```sql
-- 성능과 관리 편의성을 고려한 하이브리드 방식

-- 1) 일자별 Sequence 자동 생성 및 정리
CREATE OR REPLACE FUNCTION get_transaction_no(p_date TIMESTAMP DEFAULT NOW())
RETURNS TEXT AS $$
DECLARE
    v_seq_name TEXT;
    v_seq_value BIGINT;
    v_date_str TEXT;
BEGIN
    v_date_str := TO_CHAR(p_date, 'YYYYMMDD');
    v_seq_name := 'seq_txn_' || v_date_str;

    -- Sequence 생성 (이미 있으면 무시)
    BEGIN
        EXECUTE FORMAT('CREATE SEQUENCE %I START 1 CACHE 50', v_seq_name);
    EXCEPTION WHEN duplicate_table THEN
        -- 이미 존재하면 무시
    END;

    -- Sequence 값 획득
    EXECUTE FORMAT('SELECT nextval(%L)', v_seq_name) INTO v_seq_value;

    RETURN v_date_str || '-' || LPAD(v_seq_value::TEXT, 6, '0');
END;
$$ LANGUAGE plpgsql;

-- 2) 기본값으로 설정
ALTER TABLE payment_transactions
    ALTER COLUMN transaction_no SET DEFAULT get_transaction_no();

-- 3) 오래된 Sequence 정리 (배치 작업)
CREATE OR REPLACE FUNCTION cleanup_old_sequences()
RETURNS void AS $$
DECLARE
    seq_record RECORD;
    cutoff_date TEXT;
BEGIN
    -- 90일 이전 Sequence 삭제
    cutoff_date := TO_CHAR(NOW() - INTERVAL '90 days', 'YYYYMMDD');

    FOR seq_record IN
        SELECT sequencename
        FROM pg_sequences
        WHERE schemaname = 'public'
          AND sequencename LIKE 'seq_txn_%'
          AND SUBSTRING(sequencename FROM 9) < cutoff_date
    LOOP
        EXECUTE FORMAT('DROP SEQUENCE IF EXISTS %I', seq_record.sequencename);
    END LOOP;
END;
$$ LANGUAGE plpgsql;

-- 크론잡으로 매일 실행
-- 0 2 * * * psql -U postgres -d payment_db -c "SELECT cleanup_old_sequences();"
```

### 동시성 처리

**1. Sequence의 원자성 보장**

```sql
-- Sequence는 트랜잭션 격리 수준과 무관하게 동작

-- 트랜잭션 1:
BEGIN ISOLATION LEVEL READ COMMITTED;
SELECT nextval('seq_payment_transaction');  -- 결과: 1
ROLLBACK;  -- 트랜잭션 롤백해도 Sequence 값은 롤백 안됨!

-- 트랜잭션 2:
BEGIN ISOLATION LEVEL READ COMMITTED;
SELECT nextval('seq_payment_transaction');  -- 결과: 2 (1이 아님!)
COMMIT;

-- 이점:
-- - 절대 중복되지 않음
-- - 동시성 제어 불필요 (내부적으로 락 관리)
-- - 롤백 시에도 안전 (gap 발생하지만 중복은 없음)
```

**2. 동시성 테스트**

```sql
-- pgbench를 이용한 동시성 테스트

-- test_insert.sql:
INSERT INTO payment_transactions (user_id, amount, created_at)
VALUES (:user_id, :amount, NOW());

-- 동시 실행 테스트 (50개 클라이언트, 60초간)
$ pgbench -c 50 -j 10 -T 60 -f test_insert.sql \
    -D user_id=123 -D amount=10000

# 결과:
# - 총 INSERT: 약 180,000건
# - 중복 오류: 0건
# - Deadlock: 0건
# - transaction_no가 모두 고유함 확인
```

**3. CACHE 옵션 활용**

```sql
-- CACHE를 사용하여 성능 향상
CREATE SEQUENCE seq_payment_transaction
    START WITH 1
    INCREMENT BY 1
    CACHE 100;  -- 100개씩 메모리에 캐싱

-- 이점:
-- 1. 디스크 I/O 감소 (100번마다 1번만 기록)
-- 2. 락 경합 감소
-- 3. 성능 대폭 향상

-- 단점:
-- 1. 서버 재시작 시 캐시된 값은 손실 (gap 발생)
-- 2. 금융 시스템에서는 일반적으로 문제 없음 (순번 연속성이 필수가 아니므로)
```

**4. 멀티 마스터 환경 대응 (옵션)**

```sql
-- 여러 DB 서버에서 동시에 INSERT할 경우 (Active-Active 구성)

-- 서버 1 (홀수만):
CREATE SEQUENCE seq_payment_transaction_server1
    START WITH 1
    INCREMENT BY 2;  -- 1, 3, 5, 7, ...

-- 서버 2 (짝수만):
CREATE SEQUENCE seq_payment_transaction_server2
    START WITH 2
    INCREMENT BY 2;  -- 2, 4, 6, 8, ...

-- 또는 서버 ID를 prefix로 사용:
-- 서버 1: 1-0001, 1-0002, ...
-- 서버 2: 2-0001, 2-0002, ...
```

## 성능 비교

| 항목 | ROW_NUMBER | Sequence |
|------|------------|----------|
| **성능** | 매우 느림 (전체 스캔)<br/>TPS: ~120<br/>평균 지연: 402ms | 매우 빠름 (메모리)<br/>TPS: ~3,000<br/>평균 지연: 16ms |
| **동시성** | 심각한 문제<br/>- 중복 발생 가능<br/>- Deadlock 빈발 (23%)<br/>- 락 타임아웃 | 완벽한 보장<br/>- 중복 절대 없음<br/>- Lock-free 설계<br/>- Deadlock 없음 |
| **안정성** | 불안정<br/>- 트랜잭션 충돌<br/>- 고부하 시 오류 증가 | 매우 안정적<br/>- 원자적 연산<br/>- 고부하에서도 일정 |
| **확장성** | 낮음<br/>- 테이블 크기에 비례하여 성능 저하 | 높음<br/>- 테이블 크기 무관<br/>- 수평 확장 가능 |
| **코드 복잡도** | 높음<br/>- 복잡한 서브쿼리<br/>- 락 관리 필요 | 낮음<br/>- 단순한 함수 호출<br/>- 트리거로 자동화 |
| **Gap 발생** | 없음<br/>- 연속된 순번 보장 | 발생 가능<br/>- 롤백 시 gap<br/>- 금융에서는 문제 없음 |
| **리소스 사용** | 높음<br/>- CPU: 테이블 스캔<br/>- I/O: 많은 읽기 | 낮음<br/>- CPU: 거의 없음<br/>- I/O: 캐싱으로 최소화 |

### 실측 데이터

```bash
# 부하 테스트 비교 (pgbench, 동일 조건)

# ROW_NUMBER 방식:
$ pgbench -c 50 -j 10 -T 60 -f insert_rownumber.sql
# TPS: 124 (excluding connections establishing)
# Latency avg: 402.5 ms
# Latency 90th percentile: 1,250 ms
# Errors: 28 deadlocks, 15 timeouts

# Sequence 방식:
$ pgbench -c 50 -j 10 -T 60 -f insert_sequence.sql
# TPS: 3,021 (excluding connections establishing)
# Latency avg: 16.5 ms
# Latency 90th percentile: 28 ms
# Errors: 0

# 성능 개선:
# - TPS: 24배 향상 (124 → 3,021)
# - 지연 시간: 95% 감소 (402ms → 16ms)
# - 오류율: 100% 감소 (43건 → 0건)
```

### 스토리지 효율성

```sql
-- Sequence 메타데이터 크기
SELECT
    schemaname,
    sequencename,
    pg_size_pretty(pg_relation_size(schemaname||'.'||sequencename)) AS size
FROM pg_sequences
WHERE sequencename LIKE 'seq_txn_%';

-- 결과:
-- 각 Sequence: 약 8KB (매우 작음)
-- 1년치 Sequence (365개): 약 2.9MB
-- → 무시할 수 있는 수준
```

### 마이그레이션 과정

```sql
-- 1) 기존 데이터 검증
SELECT
    transaction_no,
    COUNT(*) AS cnt
FROM payment_transactions
GROUP BY transaction_no
HAVING COUNT(*) > 1;
-- 중복 발견 및 수정

-- 2) Sequence 함수 생성
CREATE OR REPLACE FUNCTION get_transaction_no() ...

-- 3) 신규 INSERT부터 Sequence 적용
ALTER TABLE payment_transactions
    ALTER COLUMN transaction_no SET DEFAULT get_transaction_no();

-- 4) 모니터링
SELECT
    TO_CHAR(created_at, 'YYYY-MM-DD') AS date,
    COUNT(*) AS total_transactions,
    COUNT(DISTINCT transaction_no) AS unique_transaction_nos
FROM payment_transactions
WHERE created_at >= NOW() - INTERVAL '7 days'
GROUP BY TO_CHAR(created_at, 'YYYY-MM-DD')
ORDER BY date DESC;
-- unique_transaction_nos == total_transactions 확인
```

## 참고 자료

- PostgreSQL Documentation: Sequence Manipulation Functions
- "PostgreSQL: Up and Running" - Chapter 6: Sequences
- PostgreSQL Wiki: Don't Do This - ROW_NUMBER for Identity
- Stack Overflow: "Why Sequence is better than MAX(id) + 1"
- "High Performance PostgreSQL for Rails" - Sequences and Auto-increment
