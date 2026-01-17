# Oracle RAC 환경에서의 개발 경험은?

## 답변

[여기에 답변 작성]

## 핵심 키워드

- Oracle RAC (Real Application Clusters)
- 고가용성 (High Availability)
- Load Balancing
- Failover
- Cache Fusion
- 인스턴스 간 동기화

## RAC 환경 특징

- 다중 인스턴스 구조
- 공유 스토리지 사용
- 자동 장애 조치 (Failover)
- 부하 분산 (Load Balancing)

## 개발 시 고려사항

- 커넥션 풀 설정
- Sequence 캐시 설정
- 인스턴스 친화성 (Instance Affinity)
- Global Lock 및 동시성 제어
- 애플리케이션 레벨 Failover 처리

## RAC 관련 이슈

- Cache Coherency 문제
- GCS (Global Cache Service) 부하
- 인스턴스 간 데이터 동기화 지연
- Connection Failover 처리

## 코드/쿼리 예시

```sql
-- RAC 인스턴스 확인
SELECT inst_id, instance_name, host_name, status
FROM gv$instance;

-- 현재 세션의 인스턴스 확인
SELECT instance_name FROM v$instance;

-- RAC 연결 문자열 (JDBC)
-- jdbc:oracle:thin:@(DESCRIPTION=
--   (ADDRESS_LIST=
--     (ADDRESS=(PROTOCOL=TCP)(HOST=host1)(PORT=1521))
--     (ADDRESS=(PROTOCOL=TCP)(HOST=host2)(PORT=1521))
--     (LOAD_BALANCE=ON)
--     (FAILOVER=ON))
--   (CONNECT_DATA=(SERVICE_NAME=orcl)))

-- Sequence Cache 설정 (RAC 환경)
CREATE SEQUENCE order_seq
  START WITH 1
  INCREMENT BY 1
  CACHE 1000
  ORDER;
```

## 참고 자료

- Oracle RAC Administration Guide
- RAC Best Practices for Developers
