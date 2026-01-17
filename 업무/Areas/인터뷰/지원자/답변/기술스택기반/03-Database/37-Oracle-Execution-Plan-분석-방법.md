# Oracle의 Execution Plan 분석 방법은?

## 답변

[여기에 답변 작성]

## 핵심 키워드

- Execution Plan
- EXPLAIN PLAN
- AUTOTRACE
- Cost-Based Optimizer (CBO)
- Full Table Scan vs Index Scan
- Join 방식 (Nested Loop, Hash Join, Sort Merge Join)

## 분석 방법

- EXPLAIN PLAN 사용법
- SQL Developer에서 실행 계획 확인
- V$SQL_PLAN 조회
- DBMS_XPLAN 패키지 활용

## 주요 확인 사항

- Cost, Cardinality 분석
- Access Path 확인
- Join Order 및 Join Method
- 예상 Row 수와 실제 Row 수 비교

## 코드/쿼리 예시

```sql
-- EXPLAIN PLAN 사용
EXPLAIN PLAN FOR
SELECT * FROM employees WHERE department_id = 10;

-- 실행 계획 확인
SELECT * FROM TABLE(DBMS_XPLAN.DISPLAY);

-- AUTOTRACE 사용
SET AUTOTRACE ON EXPLAIN
SELECT * FROM employees WHERE department_id = 10;
```

## 참고 자료

- Oracle Database SQL Tuning Guide
- DBMS_XPLAN 공식 문서
