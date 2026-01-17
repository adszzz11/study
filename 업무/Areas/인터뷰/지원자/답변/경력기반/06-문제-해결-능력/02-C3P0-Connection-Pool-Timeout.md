# C3P0 Connection Pool의 timeout 문제를 어떻게 발견했고, setQueryTimeout 외에 고려한 다른 해결책은?

## 답변

트래픽이 증가하면서 간헐적으로 "Could not get JDBC Connection" 에러가 발생하고 응답 시간이 급격히 느려지는 문제가 있었습니다. 모니터링 결과 C3P0 Connection Pool의 모든 커넥션이 점유된 상태에서 새로운 요청이 타임아웃되는 것을 발견했습니다.

문제를 발견한 과정은 다음과 같습니다. 먼저 애플리케이션 로그에서 JDBC Connection timeout 에러가 빈번하게 발생하는 것을 확인했고, C3P0의 JMX MBean을 통해 실시간 커넥션 상태를 모니터링했습니다. numBusyConnections가 maxPoolSize(20)에 계속 도달해 있고, numIdleConnections는 0인 상태가 지속되었습니다. Thread dump 분석 결과, 대부분의 스레드가 JDBC connection을 얻기 위해 대기 중이었습니다.

해결책으로 여러 옵션을 검토했습니다:
1. setQueryTimeout으로 쿼리 실행 시간 제한
2. C3P0 Pool 설정 최적화 (maxPoolSize 증가, timeout 조정)
3. HikariCP로 마이그레이션
4. DB 레벨 timeout 설정

최종적으로 복합적인 접근을 선택했습니다. 즉시 조치로는 C3P0 설정을 조정했고(maxPoolSize 50, checkoutTimeout 5000ms), 근본 해결을 위해 느린 쿼리를 튜닝하고 setQueryTimeout을 적용했습니다. 중장기적으로는 HikariCP로 마이그레이션을 계획했는데, HikariCP는 성능과 안정성 면에서 C3P0보다 우수하기 때문입니다.

결과적으로 평균 응답 시간이 800ms에서 200ms로 개선되었고, connection timeout 에러는 완전히 사라졌습니다.

## 핵심 키워드

- C3P0 Connection Pool
- Connection Timeout
- Query Timeout
- Connection Leak
- Pool 튜닝

## 문제 발견 과정

### 증상
- 간헐적인 "Could not get JDBC Connection" 에러 발생
- 특정 시간대(점심시간 12-1시)에 응답 시간 급증
- 애플리케이션은 정상이지만 DB 접근이 안 되는 상황
- 서버 재시작 시 일시적으로 정상화되나 곧 재발

### 모니터링 지표
```java
// C3P0 JMX MBean 확인 결과
numConnections: 20        // 전체 커넥션 수
numBusyConnections: 20    // 사용 중인 커넥션 (최대치!)
numIdleConnections: 0     // 유휴 커넥션 없음
numThreadsAwaitingCheckout: 35  // 커넥션 대기 중인 스레드
```

**주요 발견 사항:**
- 모든 커넥션이 사용 중이고 반환되지 않음
- 35개 스레드가 커넥션을 얻기 위해 대기 중
- checkoutTimeout(3초) 초과하여 에러 발생

### 분석 방법

**1. 로그 분석**
```bash
# Connection timeout 에러 패턴 확인
grep "Could not get JDBC Connection" application.log | wc -l
# 결과: 점심시간대 100건 이상 발생

# 특정 시간대 집중 발생 확인
grep "Could not get JDBC Connection" application.log | awk '{print $1}' | uniq -c
```

**2. Thread Dump 분석**
```bash
jstack [PID] > thread_dump.txt
```
분석 결과: 80% 이상의 스레드가 `com.mchange.v2.resourcepool.BasicResourcePool.awaitAvailable()` 에서 대기 중

**3. 느린 쿼리 식별**
- MySQL Slow Query Log 활성화
- 5초 이상 실행되는 쿼리 다수 발견
- 특정 리포트 쿼리가 인덱스 없이 Full Table Scan 수행

**4. Connection Leak 의심**
```java
// Connection 미반환 코드 패턴 발견
Connection conn = dataSource.getConnection();
try {
    // query 실행
} catch (Exception e) {
    // Connection close 없음 - 예외 발생 시 leak!
}
```

## 해결책 비교

### 1. setQueryTimeout
**장점:**
- 코드 레벨에서 쿼리 실행 시간 제어 가능
- 무한 대기하는 쿼리 방지
- 즉시 적용 가능, 간단한 수정

**단점:**
- 근본 원인(느린 쿼리) 해결은 아님
- 정상적으로 오래 걸리는 쿼리도 중단될 수 있음
- 모든 DAO/Repository에 일일이 적용 필요

**구현 예시:**
```java
@Transactional
public List<User> findUsers() {
    Query query = entityManager.createQuery("SELECT u FROM User u");
    query.setHint("javax.persistence.query.timeout", 5000); // 5초
    return query.getResultList();
}
```

### 2. Connection Pool 설정 조정
```properties
# 기존 설정
c3p0.maxPoolSize=20
c3p0.minPoolSize=5
c3p0.acquireIncrement=5
c3p0.maxIdleTime=1800
c3p0.checkoutTimeout=3000

# 개선된 설정
c3p0.maxPoolSize=50                # 20 → 50 증가
c3p0.minPoolSize=10                # 최소 연결 유지
c3p0.acquireIncrement=5            # 동시 증가량
c3p0.maxIdleTime=600               # 유휴 연결 빠르게 정리 (10분)
c3p0.checkoutTimeout=5000          # 타임아웃 증가 (5초)
c3p0.idleConnectionTestPeriod=300  # 5분마다 연결 테스트
c3p0.testConnectionOnCheckout=false  # 성능을 위해 false
c3p0.testConnectionOnCheckin=true    # 반환 시 검증
c3p0.maxConnectionAge=3600         # 1시간마다 연결 재생성
c3p0.unreturnedConnectionTimeout=300  # Leak 감지 (5분)
c3p0.debugUnreturnedConnectionStackTraces=true  # Leak 디버깅
```

**장점:**
- 빠르게 적용 가능
- 트래픽 증가에 대응

**단점:**
- DB 서버 부하 증가 가능성
- 메모리 사용량 증가
- 근본 문제 해결은 아님

### 3. HikariCP로 마이그레이션
**장점:**
- 현재 가장 빠르고 안정적인 Connection Pool
- Spring Boot 2.x 기본 채택
- 더 나은 성능 (레이턴시 최소화)
- Connection leak detection 내장
- 간단한 설정

**단점:**
- 마이그레이션 시간 소요
- 기존 C3P0 설정과 호환성 검토 필요
- 테스트 필요

**마이그레이션 예시:**
```xml
<!-- pom.xml -->
<dependency>
    <groupId>com.zaxxer</groupId>
    <artifactId>HikariCP</artifactId>
    <version>5.0.1</version>
</dependency>
```

```properties
# application.properties
spring.datasource.hikari.maximum-pool-size=50
spring.datasource.hikari.minimum-idle=10
spring.datasource.hikari.connection-timeout=5000
spring.datasource.hikari.idle-timeout=600000
spring.datasource.hikari.max-lifetime=1800000
spring.datasource.hikari.leak-detection-threshold=60000  # 1분
```

### 4. Database Timeout 설정
```sql
-- MySQL
SET GLOBAL wait_timeout = 600;  -- 10분
SET GLOBAL interactive_timeout = 600;

-- 또는 my.cnf 설정
[mysqld]
wait_timeout = 600
interactive_timeout = 600
max_connections = 200  -- Connection Pool 크기 고려하여 설정
```

**장점:**
- DB 레벨에서 전역적으로 적용
- 좀비 연결 방지

**단점:**
- DB 서버 재시작 필요할 수 있음
- 다른 애플리케이션에도 영향
- Connection Pool 설정과 동기화 필요

## 최종 선택과 이유

**단계별 접근 방식 채택:**

### Phase 1: 즉시 조치 (1일)
1. **C3P0 Pool 크기 증설**: maxPoolSize 20 → 50
2. **Connection Leak 감지 활성화**:
   ```properties
   c3p0.unreturnedConnectionTimeout=300
   c3p0.debugUnreturnedConnectionStackTraces=true
   ```
3. **긴급 패치**: Connection 미반환 코드 수정
   ```java
   // try-with-resources로 변경
   try (Connection conn = dataSource.getConnection()) {
       // query 실행
   } // 자동으로 close됨
   ```

### Phase 2: 중기 개선 (1주)
1. **Slow Query 튜닝**:
   - 인덱스 추가: 리포트 쿼리 5초 → 0.5초로 개선
   - N+1 쿼리 문제 해결 (fetch join 적용)
2. **setQueryTimeout 적용**:
   - 모든 쿼리에 기본 10초 타임아웃 설정
   - 리포트성 쿼리는 30초로 별도 설정

### Phase 3: 장기 개선 (1개월)
1. **HikariCP로 마이그레이션**:
   - 성능 테스트 결과 평균 레이턴시 15% 감소
   - Leak detection 기능으로 조기 발견 가능
2. **모니터링 강화**:
   - Prometheus + Grafana로 Connection Pool 메트릭 실시간 모니터링
   - 알람 설정: Pool 사용률 80% 초과 시 경고

**선택 이유:**
- 즉각적인 안정화와 근본 원인 해결을 병행
- 단계적 접근으로 리스크 최소화
- HikariCP는 업계 표준이며 장기적으로 유지보수 유리

## 성능 개선 결과

### Before (개선 전)
- 평균 응답 시간: 800ms
- P95 응답 시간: 3500ms
- Connection timeout 에러: 일 100건 이상
- Peak time DB connection 사용률: 100%

### After (개선 후)
- 평균 응답 시간: 200ms (75% 개선)
- P95 응답 시간: 450ms (87% 개선)
- Connection timeout 에러: 0건
- Peak time DB connection 사용률: 60%

### 구체적 개선 사항
```
1. Pool 설정 최적화 효과
   - Connection 대기 시간: 평균 2.5초 → 0초
   - Pool exhausted 에러: 일 100건 → 0건

2. Slow Query 튜닝 효과
   - 리포트 쿼리: 5초 → 0.5초 (90% 개선)
   - N+1 쿼리 해결: 50개 쿼리 → 1개로 통합

3. HikariCP 마이그레이션 효과
   - Connection borrow 시간: 평균 5ms → 1ms
   - Memory footprint: 20% 감소
   - Leak detection으로 잠재적 문제 3건 조기 발견
```

### 모니터링 지표 (현재)
```yaml
HikariCP Metrics:
  - active_connections: 평균 15 (max 50)
  - idle_connections: 평균 10
  - pending_threads: 0
  - connection_timeout_rate: 0/min
  - connection_acquired_ns: p95 < 2ms
```

## 참고 자료

- C3P0 Documentation: https://www.mchange.com/projects/c3p0/
- HikariCP GitHub: https://github.com/brettwooldridge/HikariCP
- HikariCP is Fastest: https://github.com/brettwooldridge/HikariCP#checkered_flag-jmh-benchmarks
- Spring Boot HikariCP Configuration: https://docs.spring.io/spring-boot/docs/current/reference/html/application-properties.html#application-properties.data.spring.datasource.hikari
- Connection Pool Sizing: https://github.com/brettwooldridge/HikariCP/wiki/About-Pool-Sizing
- Troubleshooting Connection Pool: https://vladmihalcea.com/the-anatomy-of-connection-pooling/
