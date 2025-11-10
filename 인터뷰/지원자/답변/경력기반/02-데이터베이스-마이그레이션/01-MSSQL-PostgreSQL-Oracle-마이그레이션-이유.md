# MSSQL → PostgreSQL → Oracle 순으로 마이그레이션한 이유는? 처음부터 Oracle을 선택하지 않은 이유는?

## 답변

금융 선불결제 시스템을 운영하면서 3단계에 걸친 데이터베이스 마이그레이션을 진행했습니다. 각 단계마다 명확한 기술적, 비즈니스적 이유가 있었으며, 처음부터 Oracle을 선택하지 않은 것은 비용 대비 효과와 조직의 기술 성숙도를 고려한 전략적 결정이었습니다.

초기에는 MSSQL로 시작했지만 라이선스 비용 부담과 오픈소스 전환 필요성으로 PostgreSQL로 마이그레이션했고, 이후 수백만 건의 트랜잭션 처리와 복잡한 금융 쿼리 성능 문제로 최종적으로 Oracle로 전환하게 되었습니다.

## 핵심 키워드

- 데이터베이스 마이그레이션
- 라이선스 비용
- 성능 요구사항
- 기술적 제약사항
- 단계적 전환

## 각 단계별 선택 이유

### MSSQL (초기)

**선택 배경:**
- 초기 시스템 구축 시 Microsoft 생태계 기반 인프라 사용 (Windows Server, .NET 기반 레거시 시스템 연동)
- 사내 DBA 팀의 MSSQL 운영 경험 보유
- 빠른 프로토타이핑과 개발 생산성 (SSMS, Visual Studio 통합)

**한계점 발견:**
- **라이선스 비용**: 코어당 라이선스 비용이 서버 증설 시마다 기하급수적으로 증가
- **플랫폼 종속성**: Windows Server 기반 운영으로 컨테이너화 및 클라우드 전환에 제약
- **오픈소스 전환 정책**: 회사 차원의 TCO 절감 및 벤더 종속성 탈피 전략

### PostgreSQL (중기)

**마이그레이션 이유:**
- **라이선스 비용 제로**: 오픈소스로 연간 수억 원의 라이선스 비용 절감
- **표준 SQL 준수**: ANSI SQL 표준을 잘 따르며 MSSQL에서 마이그레이션이 상대적으로 용이
- **확장성과 유연성**: JSONB, 커스텀 데이터 타입, 다양한 Extension 지원
- **컨테이너화 지원**: Docker/Kubernetes 환경에서 운영 용이

**예상하지 못한 문제점:**
- **MVCC 구조와 Vacuum 오버헤드**: 금융 거래 데이터의 빈번한 UPDATE/DELETE로 인한 테이블 Bloat 발생
- **Autovacuum 성능 저하**: 수백만 건의 트랜잭션 처리 중 Vacuum으로 인한 I/O 경합과 레이턴시 증가
- **복잡한 쿼리 성능**: 통계 집계, 정산 배치에서 Oracle 대비 옵티마이저 성능 차이 체감
- **엔터프라이즈 지원 부족**: 금융권에서 요구하는 기술 지원과 SLA 보장의 어려움

```sql
-- PostgreSQL에서 발생한 Vacuum 문제 예시
-- 일일 거래 테이블 (약 500만 건/일)
SELECT
    schemaname,
    tablename,
    n_live_tup,
    n_dead_tup,
    last_autovacuum,
    ROUND(100 * n_dead_tup / NULLIF(n_live_tup + n_dead_tup, 0), 2) AS dead_ratio
FROM pg_stat_user_tables
WHERE tablename = 'payment_transactions'
ORDER BY n_dead_tup DESC;

-- dead_ratio가 30% 이상 지속적으로 발생하여 쿼리 성능 저하
```

### Oracle (최종)

**최종 전환 결정 이유:**

1. **엔터프라이즈 성능 요구사항**
   - 초당 수천 건의 결제 트랜잭션 처리
   - 복잡한 집계 쿼리 (정산, 통계, 리포팅) 성능 개선 필요
   - Real Application Clusters (RAC)를 통한 고가용성 확보

2. **옵티마이저 성능**
   - Cost-Based Optimizer의 우수한 실행 계획 생성
   - Hint 기반의 세밀한 튜닝 가능
   - Parallel Query 처리 성능

3. **금융권 표준 준수**
   - 금융 거래 시스템에서 검증된 안정성
   - 규제 준수 및 감사 요구사항 충족 (Audit Vault, Flashback)
   - 24/7 엔터프라이즈 기술 지원

4. **고급 기능 활용**
   - Partitioning: 일/월 단위 파티션으로 쿼리 성능 대폭 향상
   - Materialized View: 정산/통계 데이터 사전 집계
   - Advanced Compression: 스토리지 비용 절감 (약 60% 압축률)

```sql
-- Oracle Partitioning 예시
CREATE TABLE payment_transactions (
    transaction_id    NUMBER PRIMARY KEY,
    transaction_date  DATE NOT NULL,
    amount            NUMBER(15,2),
    status            VARCHAR2(20),
    ...
) PARTITION BY RANGE (transaction_date)
INTERVAL (NUMTODSINTERVAL(1, 'DAY'))
(
    PARTITION p_initial VALUES LESS THAN (DATE '2023-01-01')
)
COMPRESS FOR OLTP;

-- 파티션 프루닝으로 쿼리 성능 10배 이상 개선
SELECT SUM(amount)
FROM payment_transactions
WHERE transaction_date BETWEEN DATE '2024-01-01' AND DATE '2024-01-31';
```

## 처음부터 Oracle을 선택하지 않은 이유

### 1. 초기 비용 부담
- Oracle 라이선스 비용은 MSSQL보다 훨씬 높음 (프로세서당 수천만 원)
- 초기 스타트업 단계에서는 투자 대비 효과를 정당화하기 어려움
- 트래픽과 데이터 규모가 작을 때는 오버스펙

### 2. 단계적 검증 필요
- PostgreSQL을 통해 오픈소스 DB 운영 경험 축적
- 마이그레이션 프로세스, 데이터 정합성 검증 노하우 확보
- 조직의 DB 전환 역량 검증 후 Oracle 전환으로 리스크 최소화

### 3. 기술 스택 검증
- PostgreSQL 마이그레이션을 통해 SQL 표준화 작업 선행
- 애플리케이션 레이어의 DB 종속성 제거 (JPA, MyBatis 추상화)
- 마이그레이션 도구 및 프로세스 검증 (AWS DMS, pgloader 등)

### 4. 비즈니스 성장 단계
```
단계 1 (MSSQL): 초기 구축 및 빠른 출시 (거래량: ~10만 건/일)
단계 2 (PostgreSQL): 비용 최적화 및 확장 (거래량: ~100만 건/일)
단계 3 (Oracle): 엔터프라이즈 안정성 (거래량: ~500만 건/일)
```

각 단계에서 비즈니스 요구사항과 DB 선택이 일치했으며, 처음부터 Oracle을 선택했다면 초기 과도한 투자와 미숙한 운영으로 오히려 리스크가 컸을 것입니다.

## 마이그레이션 과정에서 얻은 교훈

### 1. 점진적 마이그레이션의 중요성
- 한 번에 완벽한 DB를 선택하기보다는 단계별로 요구사항에 맞춰 전환
- 각 단계에서 축적된 마이그레이션 경험이 다음 전환의 리스크 감소

### 2. 데이터베이스 중립적 설계
```java
// DB 종속성을 줄이는 설계 패턴 적용
@Entity
@Table(name = "payment_transactions")
public class PaymentTransaction {
    @Id
    @GeneratedValue(strategy = GenerationType.SEQUENCE,
                    generator = "payment_seq")
    @SequenceGenerator(name = "payment_seq",
                       sequenceName = "payment_transaction_seq")
    private Long id;

    // DB 특화 기능 최소화, 표준 JPA 사용
}
```

### 3. 성능 테스트의 중요성
- PostgreSQL 도입 전 충분한 부하 테스트를 하지 않아 Vacuum 문제를 뒤늦게 발견
- Oracle 전환 전 3개월간 PoC 진행하여 실제 워크로드 검증
- nGrinder를 활용한 실전 트래픽 시뮬레이션 필수

### 4. 비용 vs 성능 트레이드오프
- 오픈소스가 항상 정답은 아니며, 엔터프라이즈 요구사항에서는 상용 DB의 가치가 있음
- 라이선스 비용보다 다운타임, 성능 저하로 인한 비즈니스 손실이 더 클 수 있음
- 금융 시스템에서는 안정성과 성능이 최우선 가치

### 5. 조직의 기술 역량 고려
- 각 DB마다 필요한 전문 지식이 다름 (PostgreSQL: Vacuum 튜닝, Oracle: RAC, Partitioning)
- DBA 팀의 학습 곡선과 외부 지원 가능성 고려
- 커뮤니티 활성도와 레퍼런스 사례 검토

## 참고 자료

- PostgreSQL Documentation: MVCC and Vacuum
- Oracle Database Concepts: Partitioning Guide
- AWS Database Migration Best Practices
- "Database Reliability Engineering" by Laine Campbell & Charity Majors
