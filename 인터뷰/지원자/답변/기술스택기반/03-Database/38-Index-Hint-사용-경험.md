# Index Hint를 사용해야 했던 상황은?

## 답변

[여기에 답변 작성]

## 핵심 키워드

- Index Hint
- Optimizer Hint
- Cost-Based Optimizer
- Query 성능 최적화
- 통계 정보

## 사용 시나리오

- Optimizer가 잘못된 인덱스 선택
- 통계 정보가 부정확한 경우
- 특정 비즈니스 로직에 최적화된 인덱스 강제
- 테스트 및 성능 비교 목적

## Hint 종류

- INDEX Hint
- INDEX_FULL_SCAN Hint
- NO_INDEX Hint
- USE_NL (Nested Loop Join)
- USE_HASH (Hash Join)

## 코드/쿼리 예시

```sql
-- INDEX Hint 사용
SELECT /*+ INDEX(emp emp_dept_idx) */
  emp_name, department_id
FROM employees emp
WHERE department_id = 10;

-- INDEX_FULL_SCAN Hint
SELECT /*+ INDEX_FFS(emp emp_idx) */
  COUNT(*)
FROM employees emp;

-- 여러 Hint 조합
SELECT /*+ LEADING(d e) USE_NL(e) INDEX(e emp_dept_idx) */
  d.dept_name, e.emp_name
FROM departments d, employees e
WHERE d.dept_id = e.dept_id;
```

## 참고 자료

- Oracle Optimizer Hints 공식 문서
- SQL Tuning Best Practices
