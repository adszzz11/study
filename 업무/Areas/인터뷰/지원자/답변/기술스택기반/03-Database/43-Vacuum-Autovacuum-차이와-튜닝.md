# Vacuum과 Autovacuum의 차이와 튜닝 방법은?

## 답변

[여기에 답변 작성]

## 핵심 키워드

- Vacuum
- Autovacuum
- Dead Tuple
- MVCC (Multi-Version Concurrency Control)
- Table Bloat
- 공간 재사용

## Vacuum vs Autovacuum

- Vacuum: 수동 실행
- Autovacuum: 자동 백그라운드 프로세스
- Vacuum Full: 테이블 재작성 (Lock 발생)
- Analyze: 통계 정보 갱신

## Autovacuum 동작 방식

- Dead Tuple 임계치 도달 시 자동 실행
- 백그라운드 워커 프로세스
- 테이블별 독립적 실행
- Cost-based Delay

## 튜닝 포인트

- autovacuum_vacuum_threshold 조정
- autovacuum_vacuum_scale_factor 조정
- autovacuum_naptime 설정
- autovacuum_max_workers 증가
- maintenance_work_mem 증가
- autovacuum_vacuum_cost_delay 조정

## 코드/쿼리 예시

```sql
-- 수동 Vacuum 실행
VACUUM VERBOSE table_name;

-- Vacuum과 Analyze 함께
VACUUM ANALYZE table_name;

-- Vacuum Full (테이블 재작성)
VACUUM FULL table_name;

-- Autovacuum 설정 확인
SHOW autovacuum;
SHOW autovacuum_vacuum_threshold;
SHOW autovacuum_vacuum_scale_factor;

-- 테이블별 Autovacuum 통계 확인
SELECT schemaname, relname,
       last_vacuum, last_autovacuum,
       n_dead_tup, n_live_tup,
       n_tup_ins, n_tup_upd, n_tup_del
FROM pg_stat_user_tables
WHERE schemaname = 'public'
ORDER BY n_dead_tup DESC;

-- 특정 테이블의 Autovacuum 설정 변경
ALTER TABLE large_table SET (
  autovacuum_vacuum_threshold = 1000,
  autovacuum_vacuum_scale_factor = 0.05,
  autovacuum_vacuum_cost_delay = 10
);

-- postgresql.conf 설정 예시
-- autovacuum = on
-- autovacuum_max_workers = 3
-- autovacuum_naptime = 1min
-- autovacuum_vacuum_threshold = 50
-- autovacuum_vacuum_scale_factor = 0.1
-- maintenance_work_mem = 256MB
```

## 참고 자료

- PostgreSQL Official Documentation - Routine Vacuuming
- Autovacuum Tuning Basics
