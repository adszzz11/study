# Partition Table 설계 경험과 고려사항은?

## 답변

[여기에 답변 작성]

## 핵심 키워드

- Table Partitioning
- Range Partition
- List Partition
- Hash Partition
- Composite Partition
- Partition Pruning
- 데이터 관리 효율성

## 설계 고려사항

- Partition Key 선정 기준
- Partition 개수 및 크기
- 조회 패턴 분석
- 유지보수 및 데이터 정제 전략
- 인덱스 전략 (Local vs Global Index)

## Partition 유형별 특징

- Range Partition: 날짜, 숫자 범위
- List Partition: 특정 값 목록
- Hash Partition: 균등 분산
- Composite Partition: 복합 파티셔닝

## 코드/쿼리 예시

```sql
-- Range Partition 예시
CREATE TABLE orders (
  order_id NUMBER,
  order_date DATE,
  amount NUMBER
)
PARTITION BY RANGE (order_date) (
  PARTITION p_2023 VALUES LESS THAN (TO_DATE('2024-01-01', 'YYYY-MM-DD')),
  PARTITION p_2024 VALUES LESS THAN (TO_DATE('2025-01-01', 'YYYY-MM-DD')),
  PARTITION p_max VALUES LESS THAN (MAXVALUE)
);

-- List Partition 예시
CREATE TABLE sales (
  sale_id NUMBER,
  region VARCHAR2(50),
  amount NUMBER
)
PARTITION BY LIST (region) (
  PARTITION p_north VALUES ('서울', '경기', '인천'),
  PARTITION p_south VALUES ('부산', '대구', '광주'),
  PARTITION p_etc VALUES (DEFAULT)
);

-- Partition 추가
ALTER TABLE orders ADD PARTITION p_2025
VALUES LESS THAN (TO_DATE('2026-01-01', 'YYYY-MM-DD'));

-- Partition 삭제
ALTER TABLE orders DROP PARTITION p_2023;
```

## 참고 자료

- Oracle Partitioning Guide
- Partitioning Best Practices
