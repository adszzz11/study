# PostgreSQL의 Vacuum 문제를 해결하기 위해 테이블 모델을 어떻게 변경했나요?

## 답변

PostgreSQL의 MVCC(Multi-Version Concurrency Control) 아키텍처로 인해 발생하는 Vacuum 문제를 해결하기 위해 테이블 모델을 근본적으로 재설계했습니다.

금융 선불결제 시스템에서는 거래 상태 변경(PENDING → APPROVED → SETTLED)이 빈번하게 발생하는데, PostgreSQL의 UPDATE가 내부적으로 DELETE+INSERT 방식으로 동작하면서 Dead Tuple이 급격히 증가했습니다. 이로 인해 Autovacuum이 처리량을 따라가지 못하고, 테이블 Bloat가 심화되어 쿼리 성능이 저하되었습니다.

해결책으로 **상태 변경 테이블 분리**, **파티셔닝 도입**, **HOT(Heap-Only Tuple) Update 최적화**, **Autovacuum 파라미터 튜닝**을 적용하여 Vacuum 오버헤드를 80% 이상 감소시켰습니다.

## 핵심 키워드

- PostgreSQL Vacuum
- MVCC (Multi-Version Concurrency Control)
- Table Bloat
- Autovacuum
- 테이블 파티셔닝

## Vacuum 문제 발생 원인

### 1. MVCC 아키텍처의 특성

PostgreSQL은 MVCC를 통해 동시성을 제공하지만, UPDATE/DELETE 시 기존 행을 즉시 삭제하지 않고 Dead Tuple로 표시합니다.

```sql
-- MVCC의 내부 동작 방식
UPDATE payment_transactions
SET status = 'APPROVED'
WHERE transaction_id = 12345;

-- 실제 내부 동작:
-- 1. 기존 row (status='PENDING')를 Dead Tuple로 표시
-- 2. 새로운 row (status='APPROVED')를 INSERT
-- 결과: 물리적으로 2개의 row가 존재 (1개는 dead)
```

### 2. 금융 거래 데이터의 특성

```
일일 거래량: 약 500만 건
상태 변경 패턴:
- 초기 생성: PENDING (INSERT)
- 승인: PENDING → APPROVED (UPDATE)
- 정산: APPROVED → SETTLED (UPDATE)
- 실패 처리: 일부는 FAILED (UPDATE)

평균적으로 1건의 거래당 2~3회 UPDATE 발생
→ 일일 약 1,000만~1,500만 개의 Dead Tuple 생성
```

### 3. Autovacuum의 한계

```sql
-- 기본 Autovacuum 설정 (문제 발생 시점)
SHOW autovacuum_vacuum_scale_factor;  -- 0.2 (20%)
SHOW autovacuum_vacuum_threshold;     -- 50

-- payment_transactions 테이블 크기: 500만 건
-- Autovacuum 트리거 조건:
-- 50 + (5,000,000 * 0.2) = 1,000,050 Dead Tuples

-- 문제: 100만 개 이상 쌓여야 Vacuum 실행
-- 하루에 1,500만 개 생성되므로 Vacuum이 처리량을 못 따라감
```

### 4. 테이블 Bloat 측정

```sql
-- 테이블 Bloat 확인 쿼리
SELECT
    schemaname,
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS total_size,
    pg_size_pretty(pg_relation_size(schemaname||'.'||tablename)) AS table_size,
    n_live_tup,
    n_dead_tup,
    ROUND(100.0 * n_dead_tup / NULLIF(n_live_tup + n_dead_tup, 0), 2) AS dead_ratio,
    last_autovacuum,
    last_vacuum
FROM pg_stat_user_tables
WHERE tablename = 'payment_transactions';

-- 결과 (문제 발생 시점):
-- total_size: 85 GB
-- table_size: 65 GB (실제 데이터는 약 30GB 예상)
-- dead_ratio: 35.8%
-- last_autovacuum: 2 hours ago (계속 실행 중이지만 따라가지 못함)
```

### 5. 성능 저하 현상

```sql
-- 단순 조회 쿼리도 느려짐 (Index도 Bloat 발생)
EXPLAIN ANALYZE
SELECT * FROM payment_transactions
WHERE transaction_id = 12345;

-- 문제 발생 전: Execution Time: 1.2 ms
-- 문제 발생 후: Execution Time: 45.8 ms
-- 원인: Index Bloat + Table Bloat로 인한 I/O 증가
```

## 테이블 모델 변경 내역

### 변경 전

**단일 테이블 구조 (문제 발생)**

```sql
CREATE TABLE payment_transactions (
    transaction_id      BIGSERIAL PRIMARY KEY,
    user_id             BIGINT NOT NULL,
    amount              DECIMAL(15,2) NOT NULL,
    status              VARCHAR(20) NOT NULL,  -- PENDING, APPROVED, SETTLED, FAILED
    payment_method      VARCHAR(50),
    created_at          TIMESTAMP NOT NULL,
    updated_at          TIMESTAMP NOT NULL,  -- 상태 변경마다 UPDATE
    approved_at         TIMESTAMP,           -- UPDATE
    settled_at          TIMESTAMP,           -- UPDATE
    merchant_id         BIGINT,
    -- 30개 이상의 컬럼...
);

CREATE INDEX idx_status ON payment_transactions(status);
CREATE INDEX idx_created_at ON payment_transactions(created_at);
CREATE INDEX idx_user_id ON payment_transactions(user_id);

-- 문제점:
-- 1. UPDATE 시 모든 컬럼(30개+)이 새로운 row로 복사됨
-- 2. 모든 Index도 새로운 항목 추가 (Index Bloat 동시 발생)
-- 3. Dead Tuple이 기하급수적으로 증가
```

### 변경 후

**1. 불변 데이터와 가변 데이터 분리**

```sql
-- 1) 거래 기본 정보 (Immutable, INSERT-ONLY)
CREATE TABLE payment_transactions (
    transaction_id      BIGSERIAL PRIMARY KEY,
    user_id             BIGINT NOT NULL,
    amount              DECIMAL(15,2) NOT NULL,
    payment_method      VARCHAR(50) NOT NULL,
    merchant_id         BIGINT NOT NULL,
    created_at          TIMESTAMP NOT NULL,
    -- 생성 후 절대 변경되지 않는 데이터만 포함
    -- UPDATE 발생 안함 → Dead Tuple 없음
) PARTITION BY RANGE (created_at);

-- 2) 거래 상태 정보 (Mutable, 자주 UPDATE)
CREATE TABLE payment_transaction_status (
    transaction_id      BIGINT PRIMARY KEY REFERENCES payment_transactions(transaction_id),
    status              VARCHAR(20) NOT NULL,
    updated_at          TIMESTAMP NOT NULL,
    approved_at         TIMESTAMP,
    settled_at          TIMESTAMP,
    failure_reason      TEXT
    -- 상태 관련 컬럼만 포함 (약 5개 컬럼)
    -- UPDATE 발생하지만 row 크기가 작아 Bloat 최소화
);

-- Fillfactor 조정: HOT Update 활성화
ALTER TABLE payment_transaction_status SET (fillfactor = 70);
-- 30%의 여유 공간을 남겨두어 UPDATE 시 같은 Page에서 처리 (HOT Update)
```

**2. 파티셔닝 도입 (일 단위)**

```sql
-- 파티션 자동 생성 (pg_partman extension 사용)
CREATE TABLE payment_transactions_y2024m01d01
    PARTITION OF payment_transactions
    FOR VALUES FROM ('2024-01-01') TO ('2024-01-02');

CREATE TABLE payment_transactions_y2024m01d02
    PARTITION OF payment_transactions
    FOR VALUES FROM ('2024-01-02') TO ('2024-01-03');

-- 이점:
-- 1. 오래된 파티션은 Vacuum 부담 없음 (변경 없음)
-- 2. 최근 1~2일 파티션만 Vacuum 대상
-- 3. 파티션 프루닝으로 쿼리 성능 향상
-- 4. 오래된 데이터 아카이빙 용이 (파티션 단위 DETACH)
```

**3. 상태 이력 추적 테이블 추가 (INSERT-ONLY)**

```sql
-- UPDATE 대신 INSERT로 상태 변경 이력 추적
CREATE TABLE payment_transaction_status_history (
    history_id          BIGSERIAL PRIMARY KEY,
    transaction_id      BIGINT NOT NULL,
    status              VARCHAR(20) NOT NULL,
    changed_at          TIMESTAMP NOT NULL DEFAULT NOW(),
    changed_by          VARCHAR(100),
    reason              TEXT
) PARTITION BY RANGE (changed_at);

-- 장점:
-- 1. 감사(Audit) 요구사항 충족
-- 2. INSERT-ONLY라 Dead Tuple 없음
-- 3. 필요시 과거 상태 조회 가능
```

**4. Materialized View로 집계 데이터 관리**

```sql
-- 정산용 집계 데이터 (매시간 REFRESH)
CREATE MATERIALIZED VIEW payment_hourly_summary AS
SELECT
    DATE_TRUNC('hour', created_at) AS hour,
    status,
    COUNT(*) AS transaction_count,
    SUM(amount) AS total_amount
FROM payment_transactions pt
JOIN payment_transaction_status pts ON pt.transaction_id = pts.transaction_id
GROUP BY DATE_TRUNC('hour', created_at), status;

CREATE UNIQUE INDEX ON payment_hourly_summary(hour, status);

-- CONCURRENTLY REFRESH로 무중단 갱신
REFRESH MATERIALIZED VIEW CONCURRENTLY payment_hourly_summary;

-- 이점: 복잡한 집계 쿼리를 반복 실행하지 않음 → Vacuum 부담 감소
```

### 변경 후 테이블 구조 요약

```
┌─────────────────────────────────┐
│ payment_transactions            │  ← INSERT-ONLY (불변)
│ (파티션: 일 단위)                 │     Dead Tuple: 거의 없음
└─────────────────────────────────┘
            │
            │ 1:1
            ▼
┌─────────────────────────────────┐
│ payment_transaction_status      │  ← UPDATE 발생 (가변)
│ (fillfactor=70, HOT Update)     │     컬럼 수 적음 → Bloat 최소화
└─────────────────────────────────┘
            │
            │ 1:N
            ▼
┌─────────────────────────────────┐
│ payment_transaction_status_     │  ← INSERT-ONLY (이력)
│   history (파티션: 일 단위)       │     Dead Tuple: 없음
└─────────────────────────────────┘
```

## 성능 개선 결과

### 1. Vacuum 실행 시간 감소

```sql
-- 변경 전:
-- Full Vacuum 소요 시간: 약 4시간 (85GB 테이블)
-- Autovacuum 실행 빈도: 하루 5~6회 (그래도 따라가지 못함)

-- 변경 후:
-- payment_transactions: Vacuum 거의 불필요 (INSERT-ONLY)
-- payment_transaction_status: 약 10분 (크기 작음, 5GB)
-- Autovacuum 실행 빈도: 하루 2~3회 (충분히 따라감)

-- Vacuum 오버헤드 약 85% 감소
```

### 2. 테이블 Bloat 제거

```sql
-- 변경 전:
SELECT pg_size_pretty(pg_total_relation_size('payment_transactions'));
-- 결과: 85 GB (실제 데이터 30GB, Bloat 55GB)

-- 변경 후:
SELECT
    pg_size_pretty(pg_total_relation_size('payment_transactions')) AS main_table,
    pg_size_pretty(pg_total_relation_size('payment_transaction_status')) AS status_table;
-- 결과:
-- main_table: 32 GB (Bloat 거의 없음)
-- status_table: 5 GB (Bloat 약 10%, 관리 가능)
-- 총: 37 GB (기존 85GB → 43% 감소)
```

### 3. 쿼리 성능 개선

```sql
-- 특정 거래 조회
EXPLAIN ANALYZE
SELECT pt.*, pts.status
FROM payment_transactions pt
JOIN payment_transaction_status pts ON pt.transaction_id = pts.transaction_id
WHERE pt.transaction_id = 12345;

-- 변경 전: Execution Time: 45.8 ms
-- 변경 후: Execution Time: 1.5 ms (30배 개선)

-- 일일 정산 쿼리 (파티션 프루닝 효과)
EXPLAIN ANALYZE
SELECT status, COUNT(*), SUM(amount)
FROM payment_transactions pt
JOIN payment_transaction_status pts ON pt.transaction_id = pts.transaction_id
WHERE pt.created_at >= '2024-01-15' AND pt.created_at < '2024-01-16'
GROUP BY status;

-- 변경 전: Execution Time: 35,420 ms (전체 테이블 스캔)
-- 변경 후: Execution Time: 2,180 ms (파티션 프루닝, 16배 개선)
```

### 4. I/O 부하 감소

```bash
# iostat으로 측정한 디스크 I/O (피크 시간대)

# 변경 전:
# Device  tps    kB_read/s    kB_wrtn/s
# sda     850    45,230       38,560

# 변경 후:
# Device  tps    kB_read/s    kB_wrtn/s
# sda     320    12,450       15,220

# I/O 부하 약 65% 감소
```

## 추가 최적화 작업

### 1. Autovacuum 파라미터 튜닝

```sql
-- 상태 테이블에 대해 공격적인 Autovacuum 설정
ALTER TABLE payment_transaction_status SET (
    autovacuum_vacuum_scale_factor = 0.05,  -- 기본 0.2 → 0.05
    autovacuum_vacuum_threshold = 500,       -- 기본 50 → 500
    autovacuum_vacuum_cost_delay = 10,       -- 기본 20 → 10 (더 빠르게)
    autovacuum_vacuum_cost_limit = 2000      -- 기본 200 → 2000 (더 많이 처리)
);

-- postgresql.conf 전역 설정
autovacuum_max_workers = 6                   -- 기본 3 → 6
autovacuum_naptime = 30s                     -- 기본 1min → 30s
```

### 2. HOT Update 효과 측정

```sql
-- HOT Update 비율 확인
SELECT
    schemaname,
    tablename,
    n_tup_upd AS total_updates,
    n_tup_hot_upd AS hot_updates,
    ROUND(100.0 * n_tup_hot_upd / NULLIF(n_tup_upd, 0), 2) AS hot_update_ratio
FROM pg_stat_user_tables
WHERE tablename = 'payment_transaction_status';

-- 결과:
-- hot_update_ratio: 87.3%
-- → UPDATE의 87%가 같은 Page 내에서 처리되어 Index 갱신 불필요
```

### 3. Vacuum 모니터링 쿼리

```sql
-- Dead Tuple 모니터링
CREATE VIEW v_vacuum_stats AS
SELECT
    schemaname,
    tablename,
    n_live_tup,
    n_dead_tup,
    ROUND(100.0 * n_dead_tup / NULLIF(n_live_tup + n_dead_tup, 0), 2) AS dead_ratio,
    last_vacuum,
    last_autovacuum,
    vacuum_count,
    autovacuum_count
FROM pg_stat_user_tables
WHERE n_dead_tup > 1000
ORDER BY dead_ratio DESC;

-- 정기 점검 스크립트
SELECT * FROM v_vacuum_stats;
```

### 4. 파티션 자동 관리

```bash
# pg_partman을 이용한 파티션 자동 생성/삭제
# postgresql.conf
shared_preload_libraries = 'pg_partman_bgw'

# 파티션 유지 기간 설정 (90일)
SELECT partman.create_parent('public.payment_transactions', 'created_at', 'native', 'daily');
UPDATE partman.part_config
SET retention = '90 days',
    retention_keep_table = false
WHERE parent_table = 'public.payment_transactions';

# 90일 이상 오래된 파티션은 자동 삭제 (아카이빙 후)
```

### 5. Index 최적화

```sql
-- 불필요한 Index 제거 (Bloat 원인)
-- pg_stat_user_indexes로 사용률 낮은 Index 식별
SELECT
    schemaname,
    tablename,
    indexname,
    idx_scan,
    idx_tup_read,
    idx_tup_fetch
FROM pg_stat_user_indexes
WHERE schemaname = 'public'
  AND tablename = 'payment_transactions'
  AND idx_scan < 100  -- 거의 사용 안 되는 Index
ORDER BY idx_scan;

-- 사용률 낮은 Index 삭제
DROP INDEX IF EXISTS idx_rarely_used;

-- Partial Index 활용 (필요한 데이터만 Index)
CREATE INDEX idx_pending_transactions
ON payment_transaction_status(transaction_id)
WHERE status = 'PENDING';  -- PENDING 상태만 Index (10% 이하)
```

## 참고 자료

- PostgreSQL Documentation: Routine Vacuuming
- "The Internals of PostgreSQL" - Chapter 5: Vacuum Processing
- Cybertec Blog: "PostgreSQL VACUUM and HOT Updates"
- pgMustard: Vacuum Monitoring Best Practices
- pg_partman GitHub: Partition Management Extension
