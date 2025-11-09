# Sequence Cache 설정의 trade-off는?

## 답변

[여기에 답변 작성]

## 핵심 키워드

- Sequence Cache
- 성능 최적화
- 번호 결번 (Gap)
- 메모리 사용량
- RAC 환경

## Cache 설정의 장점

- Dictionary Table 접근 감소
- 성능 향상 (특히 INSERT 작업)
- Lock Contention 감소
- 동시성 향상

## Cache 설정의 단점

- 인스턴스 재시작 시 번호 결번 발생
- 메모리 사용량 증가
- RAC 환경에서 인스턴스 간 번호 차이
- 순차성 보장 불가

## 적절한 Cache 크기 선정

- 트랜잭션 빈도 고려
- 결번 허용 정도
- RAC 노드 수
- 메모리 제약사항

## 코드/쿼리 예시

```sql
-- CACHE 사용 (기본값 20)
CREATE SEQUENCE seq_default
  START WITH 1
  INCREMENT BY 1
  CACHE 20;

-- CACHE 크기 조정 (대용량 INSERT)
CREATE SEQUENCE seq_high_performance
  START WITH 1
  INCREMENT BY 1
  CACHE 1000;

-- NOCACHE 설정 (순차성 중요)
CREATE SEQUENCE seq_no_gap
  START WITH 1
  INCREMENT BY 1
  NOCACHE
  ORDER;

-- 기존 Sequence 수정
ALTER SEQUENCE seq_default CACHE 500;

-- Sequence 캐시 상태 확인
SELECT sequence_name, cache_size, last_number
FROM user_sequences
WHERE sequence_name = 'SEQ_DEFAULT';
```

## 참고 자료

- Oracle Sequence Performance Tuning
- Best Practices for Sequence in RAC
