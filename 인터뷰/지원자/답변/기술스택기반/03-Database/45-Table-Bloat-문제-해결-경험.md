# Table Bloat 문제를 해결한 경험은?

## 답변

[여기에 답변 작성]

## 핵심 키워드

- Table Bloat
- Dead Tuple
- Vacuum
- REINDEX
- pg_repack
- Autovacuum 튜닝
- Fillfactor

## Bloat 발생 원인

- 빈번한 UPDATE/DELETE
- Autovacuum 미실행 또는 지연
- Long-running Transaction
- Dead Tuple 누적
- 부적절한 Fillfactor 설정

## Bloat 확인 방법

- pgstattuple 확장 사용
- pg_stat_user_tables 조회
- Dead Tuple 비율 확인
- 테이블/인덱스 크기 모니터링

## 해결 방법

- Vacuum Full (Lock 주의)
- pg_repack 사용 (무중단)
- REINDEX
- CLUSTER
- Autovacuum 튜닝
- 파티셔닝 도입

## 예방 조치

- 적절한 Autovacuum 설정
- Fillfactor 조정
- Long Transaction 방지
- 주기적인 모니터링

## 코드/쿼리 예시

```sql
-- pgstattuple 확장 설치
CREATE EXTENSION pgstattuple;

-- Table Bloat 확인
SELECT
  schemaname, tablename,
  pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size,
  n_dead_tup,
  n_live_tup,
  ROUND(n_dead_tup * 100.0 / NULLIF(n_live_tup + n_dead_tup, 0), 2) AS dead_ratio
FROM pg_stat_user_tables
WHERE n_dead_tup > 0
ORDER BY n_dead_tup DESC;

-- 상세한 Bloat 정보
SELECT * FROM pgstattuple('large_table');

-- Vacuum Full 실행 (Lock 발생)
VACUUM FULL VERBOSE large_table;

-- pg_repack 사용 (무중단, 별도 설치 필요)
-- pg_repack -t large_table -d mydb

-- CLUSTER (특정 인덱스 기준 재정렬)
CLUSTER large_table USING large_table_pkey;

-- Fillfactor 조정 (UPDATE가 많은 테이블)
ALTER TABLE frequently_updated
SET (fillfactor = 70);

-- 인덱스 Bloat 확인
SELECT
  schemaname, tablename, indexname,
  pg_size_pretty(pg_relation_size(indexrelid)) AS index_size,
  idx_scan, idx_tup_read, idx_tup_fetch
FROM pg_stat_user_indexes
ORDER BY pg_relation_size(indexrelid) DESC;

-- REINDEX
REINDEX TABLE large_table;
REINDEX INDEX CONCURRENTLY large_table_idx; -- 무중단

-- Autovacuum 설정 조정
ALTER TABLE large_table SET (
  autovacuum_vacuum_scale_factor = 0.05,
  autovacuum_vacuum_threshold = 1000,
  autovacuum_analyze_scale_factor = 0.05
);
```

## 참고 자료

- PostgreSQL Bloat Detection and Management
- pg_repack Documentation
