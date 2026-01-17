# LG메시지허브 토큰 만료 문제를 Round-Robin으로 해결했다고 했는데, 더 나은 방법은 없었나요?

## 답변

LG메시지허브 API를 사용하여 문자 발송 서비스를 구현하던 중, 토큰 만료로 인한 API 호출 실패가 빈번하게 발생했습니다. LG메시지허브는 토큰 유효 시간이 1시간으로 짧고, 만료된 토큰으로 요청 시 실패 응답을 반환하는 구조였습니다.

당시 상황은 단일 토큰을 사용하여 모든 요청을 처리했기 때문에, 토큰 만료 시점에 대량의 문자 발송이 실패하는 문제가 있었습니다. 특히 야간 배치 작업으로 수만 건의 문자를 발송할 때 토큰 갱신 시점에 수 분간 발송이 중단되었습니다.

해결책으로 여러 토큰을 미리 발급받아 Round-Robin 방식으로 순환 사용하는 방법을 선택했습니다. 5개의 토큰을 10분 간격으로 발급받아 Pool에 저장하고, 요청 시마다 순차적으로 토큰을 선택하여 사용했습니다. 이렇게 하면 하나의 토큰이 만료되어도 다른 토큰들이 유효하므로 서비스 중단 없이 지속적으로 API를 호출할 수 있었습니다.

더 나은 방법으로는 Token Auto-Refresh(만료 5분 전 자동 갱신), Event-driven Refresh(401 에러 시 즉시 갱신), 또는 Circuit Breaker 패턴 도입이 있었습니다. 하지만 당시 빠른 구현이 필요했고, LG메시지허브 API가 다중 토큰 사용을 허용했기 때문에 Round-Robin 방식이 가장 간단하고 효과적이었습니다.

결과적으로 토큰 만료로 인한 실패율이 15%에서 0%로 개선되었고, 배치 작업도 안정적으로 수행되었습니다. 다만 이후에는 토큰 갱신 로직을 개선하여 단일 토큰 + Auto-Refresh 방식으로 전환할 계획입니다.

## 핵심 키워드

- 토큰 관리
- Round-Robin
- Token Refresh
- 세션 관리
- 부하 분산

## 문제 상황

### LG메시지허브 API 특성
- **토큰 기반 인증**: 모든 API 요청에 Bearer Token 필요
- **짧은 유효 시간**: 토큰 유효 기간 1시간
- **하드 만료**: 토큰 만료 시 Graceful degradation 없이 즉시 실패 (401 Unauthorized)
- **토큰 갱신 방법**: 별도의 인증 API 호출로 새 토큰 발급
- **Rate Limit**: 인증 API는 분당 10회 제한

**API 사용 패턴:**
```java
// 문자 발송 API 호출
POST /api/v1/message/send
Headers:
  Authorization: Bearer {access_token}
Body:
  {
    "receiver": "01012345678",
    "message": "테스트 메시지"
  }
```

### 토큰 만료 이슈

**발생 상황:**
1. **초기 구현**: 단일 토큰을 1시간 사용 후 만료 시 갱신
2. **문제 발생 시점**: 토큰 만료 직전부터 갱신 완료까지 (약 2-3초)
3. **영향 범위**: 해당 시간 동안의 모든 API 요청 실패

**구체적 에러:**
```json
// 만료된 토큰으로 요청 시
{
  "status": 401,
  "error": "Unauthorized",
  "message": "Token expired",
  "code": "AUTH_TOKEN_EXPIRED"
}
```

**비즈니스 임팩트:**
- 대량 문자 발송 시 수백~수천 건 실패
- 야간 배치 작업 중 토큰 만료로 작업 중단
- 실패한 메시지 재발송 비용 증가
- 고객 불만 (중요 알림 미도착)

**로그 분석:**
```bash
# 시간대별 실패율 분석
2024-10-15 13:59:45 - SUCCESS (token1)
2024-10-15 13:59:55 - SUCCESS (token1)
2024-10-15 14:00:05 - FAIL: Token expired
2024-10-15 14:00:15 - FAIL: Token expired
2024-10-15 14:00:25 - FAIL: Token expired
2024-10-15 14:00:35 - SUCCESS (token2) - 새 토큰 발급 완료
# 약 30초간 모든 요청 실패
```

## Round-Robin 솔루션

### 구현 방법
```java
@Service
public class LGMessageHubTokenManager {
    private static final int TOKEN_POOL_SIZE = 5;
    private static final int TOKEN_REFRESH_INTERVAL_MINUTES = 10;
    private static final int TOKEN_VALIDITY_MINUTES = 60;

    private final List<TokenInfo> tokenPool = new CopyOnWriteArrayList<>();
    private final AtomicInteger currentIndex = new AtomicInteger(0);
    private final ReentrantLock refreshLock = new ReentrantLock();

    @PostConstruct
    public void initializeTokenPool() {
        // 초기 토큰 5개 발급 (10분 간격으로 생성 시간 분산)
        for (int i = 0; i < TOKEN_POOL_SIZE; i++) {
            String token = issueToken();
            TokenInfo tokenInfo = new TokenInfo(
                token,
                LocalDateTime.now().plusMinutes(i * TOKEN_REFRESH_INTERVAL_MINUTES),
                LocalDateTime.now().plusMinutes(TOKEN_VALIDITY_MINUTES)
            );
            tokenPool.add(tokenInfo);
        }

        // 주기적 토큰 갱신 스케줄러
        scheduleTokenRefresh();
    }

    /**
     * Round-Robin 방식으로 토큰 선택
     */
    public String getToken() {
        int index = currentIndex.getAndUpdate(i -> (i + 1) % TOKEN_POOL_SIZE);
        TokenInfo tokenInfo = tokenPool.get(index);

        // 만료된 토큰인 경우 즉시 갱신
        if (tokenInfo.isExpired()) {
            log.warn("Token {} is expired, refreshing immediately", index);
            refreshToken(index);
            tokenInfo = tokenPool.get(index);
        }

        return tokenInfo.getToken();
    }

    /**
     * 주기적으로 토큰 갱신 (만료 10분 전)
     */
    @Scheduled(fixedRate = 600000) // 10분마다
    public void scheduleTokenRefresh() {
        for (int i = 0; i < tokenPool.size(); i++) {
            TokenInfo tokenInfo = tokenPool.get(i);

            // 만료 10분 전이면 갱신
            if (tokenInfo.willExpireIn(10)) {
                refreshToken(i);
            }
        }
    }

    private void refreshToken(int index) {
        refreshLock.lock();
        try {
            TokenInfo oldToken = tokenPool.get(index);
            String newToken = issueToken();
            TokenInfo newTokenInfo = new TokenInfo(
                newToken,
                LocalDateTime.now(),
                LocalDateTime.now().plusMinutes(TOKEN_VALIDITY_MINUTES)
            );

            tokenPool.set(index, newTokenInfo);
            log.info("Token {} refreshed successfully", index);
        } catch (Exception e) {
            log.error("Failed to refresh token {}", index, e);
        } finally {
            refreshLock.unlock();
        }
    }

    /**
     * LG메시지허브 인증 API 호출
     */
    private String issueToken() {
        RestTemplate restTemplate = new RestTemplate();

        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_JSON);

        Map<String, String> body = new HashMap<>();
        body.put("username", lgConfig.getUsername());
        body.put("password", lgConfig.getPassword());

        HttpEntity<Map<String, String>> request = new HttpEntity<>(body, headers);

        ResponseEntity<AuthResponse> response = restTemplate.postForEntity(
            lgConfig.getAuthUrl(),
            request,
            AuthResponse.class
        );

        return response.getBody().getAccessToken();
    }
}

/**
 * 토큰 정보 클래스
 */
@Data
@AllArgsConstructor
class TokenInfo {
    private String token;
    private LocalDateTime issuedAt;
    private LocalDateTime expiresAt;

    public boolean isExpired() {
        return LocalDateTime.now().isAfter(expiresAt);
    }

    public boolean willExpireIn(int minutes) {
        return LocalDateTime.now()
            .isAfter(expiresAt.minusMinutes(minutes));
    }
}

/**
 * 메시지 발송 서비스
 */
@Service
public class MessageService {
    @Autowired
    private LGMessageHubTokenManager tokenManager;

    public void sendMessage(String receiver, String message) {
        String token = tokenManager.getToken(); // Round-Robin으로 토큰 선택

        RestTemplate restTemplate = new RestTemplate();
        HttpHeaders headers = new HttpHeaders();
        headers.setBearerAuth(token);
        headers.setContentType(MediaType.APPLICATION_JSON);

        Map<String, String> body = new HashMap<>();
        body.put("receiver", receiver);
        body.put("message", message);

        HttpEntity<Map<String, String>> request = new HttpEntity<>(body, headers);

        try {
            restTemplate.postForEntity(
                lgConfig.getMessageUrl(),
                request,
                MessageResponse.class
            );
            log.info("Message sent successfully to {}", receiver);
        } catch (HttpClientErrorException e) {
            if (e.getStatusCode() == HttpStatus.UNAUTHORIZED) {
                log.error("Token expired, retry with new token");
                // 재시도 로직
            }
        }
    }
}
```

### 장점
- **서비스 중단 없음**: 하나의 토큰이 만료되어도 다른 토큰 사용 가능
- **간단한 구현**: 복잡한 로직 없이 인덱스만 순환
- **부하 분산**: 여러 토큰에 요청이 분산되어 Rate Limit 우회 가능
- **즉시 적용 가능**: 기존 코드 최소 수정으로 도입

### 단점
- **메모리 사용 증가**: 토큰 5개 유지 (미미한 수준)
- **토큰 발급 API 호출 증가**: 초기 5회 + 주기적 갱신
- **불필요한 토큰**: 트래픽이 적을 때도 5개 유지
- **복잡도 증가**: 토큰 상태 관리 필요
- **근본 해결 아님**: 갱신 타이밍 로직 개선이 더 나은 방법

## 대안 솔루션 비교

### 1. Token Auto-Refresh
**설명:** 토큰 만료 5-10분 전에 자동으로 갱신

```java
@Service
public class AutoRefreshTokenManager {
    private String currentToken;
    private LocalDateTime expiresAt;

    @Scheduled(fixedRate = 60000) // 1분마다 체크
    public void checkAndRefresh() {
        if (LocalDateTime.now().isAfter(expiresAt.minusMinutes(5))) {
            // 만료 5분 전이면 갱신
            refreshToken();
        }
    }

    private synchronized void refreshToken() {
        String newToken = issueToken();
        this.currentToken = newToken;
        this.expiresAt = LocalDateTime.now().plusMinutes(60);
        log.info("Token auto-refreshed");
    }

    public String getToken() {
        return currentToken;
    }
}
```

**장점:**
- 단일 토큰만 관리하므로 간단
- 메모리 효율적
- 토큰 만료 전에 미리 갱신하여 실패 방지

**단점:**
- 갱신 중 짧은 시간 동안 Lock 필요
- 갱신 실패 시 백업 토큰 없음

### 2. Token Pool 관리
**설명:** Pool에서 유효한 토큰만 관리, 필요 시 동적 생성

```java
@Service
public class TokenPoolManager {
    private final Queue<TokenInfo> validTokens = new ConcurrentLinkedQueue<>();
    private final int MIN_TOKENS = 2;

    public String getToken() {
        // 유효한 토큰 찾기
        TokenInfo tokenInfo = validTokens.poll();

        while (tokenInfo != null && tokenInfo.isExpired()) {
            tokenInfo = validTokens.poll(); // 만료된 토큰 제거
        }

        if (tokenInfo == null) {
            // 유효한 토큰 없으면 새로 발급
            tokenInfo = new TokenInfo(issueToken(), LocalDateTime.now().plusMinutes(60));
        }

        String token = tokenInfo.getToken();
        validTokens.offer(tokenInfo); // 다시 Queue에 넣기

        // Pool 크기 유지
        ensureMinimumTokens();

        return token;
    }

    @Scheduled(fixedRate = 600000)
    private void ensureMinimumTokens() {
        while (validTokens.size() < MIN_TOKENS) {
            TokenInfo newToken = new TokenInfo(
                issueToken(),
                LocalDateTime.now().plusMinutes(60)
            );
            validTokens.offer(newToken);
        }
    }
}
```

**장점:**
- 동적으로 토큰 수 조절
- 만료된 토큰 자동 제거
- 유연한 확장 가능

**단점:**
- Queue 동기화 오버헤드
- 구현 복잡도 높음

### 3. Event-driven Refresh
**설명:** 401 에러 발생 시 즉시 토큰 갱신 후 재시도

```java
@Service
public class EventDrivenTokenManager {
    private String currentToken;

    public <T> T callWithToken(Supplier<T> apiCall) {
        try {
            return apiCall.get();
        } catch (HttpClientErrorException e) {
            if (e.getStatusCode() == HttpStatus.UNAUTHORIZED) {
                // 401 에러 시 즉시 갱신
                log.warn("Token expired, refreshing...");
                refreshToken();

                // 재시도
                return apiCall.get();
            }
            throw e;
        }
    }

    private synchronized void refreshToken() {
        this.currentToken = issueToken();
    }

    public String getToken() {
        return currentToken;
    }
}

// 사용 예
messageService.callWithToken(() -> sendMessage(receiver, message));
```

**장점:**
- 실제 에러 발생 시에만 갱신 (리소스 효율적)
- 자동 재시도로 개발자 편의성 높음

**단점:**
- 첫 번째 요청은 실패 (재시도 필요)
- 동시 다발적 요청 시 토큰 갱신 경쟁 조건

### 4. Circuit Breaker 패턴
**설명:** Resilience4j를 사용한 장애 격리

```java
@Service
public class CircuitBreakerTokenManager {
    private final CircuitBreaker circuitBreaker;
    private String currentToken;

    public CircuitBreakerTokenManager() {
        CircuitBreakerConfig config = CircuitBreakerConfig.custom()
            .failureRateThreshold(50)
            .waitDurationInOpenState(Duration.ofSeconds(10))
            .build();

        this.circuitBreaker = CircuitBreaker.of("lgMessageHub", config);
    }

    public String getToken() {
        return circuitBreaker.executeSupplier(() -> {
            if (isTokenExpired()) {
                refreshToken();
            }
            return currentToken;
        });
    }
}
```

**장점:**
- 장애 전파 방지
- 자동 복구 시도
- 모니터링 편리

**단점:**
- 추가 라이브러리 필요
- 학습 곡선

## 왜 Round-Robin을 선택했는가?

### 1. 빠른 문제 해결 필요
- 프로덕션에서 즉시 발생 중인 문제
- 간단한 구현으로 당일 배포 가능
- 검증된 패턴 (Redis Cluster 등에서 사용)

### 2. LG메시지허브 API 특성
- 다중 토큰 발급 허용 (계정당 제한 없음)
- 토큰 발급 API Rate Limit 여유 있음 (분당 10회)
- 토큰 크기 작음 (메모리 부담 적음)

### 3. 트래픽 패턴 고려
- 대량 배치 작업 위주
- 순간적으로 많은 요청 발생
- 여러 토큰으로 부하 분산 효과

### 4. 리스크 최소화
- 기존 코드 최소 수정
- Rollback 쉬움
- 사이드 이펙트 적음

## 개선 가능성

### 단기 개선 (1-2주)
1. **Hybrid 방식**: Round-Robin + Auto-Refresh 결합
   ```java
   // 각 토큰별로 만료 5분 전 자동 갱신
   // Round-Robin으로 선택 + 만료 임박 시 자동 갱신
   ```

2. **Fallback 로직 추가**:
   ```java
   // 선택된 토큰이 만료되었으면 다음 토큰 즉시 시도
   public String getToken() {
       for (int i = 0; i < TOKEN_POOL_SIZE; i++) {
           String token = getNextToken();
           if (!isExpired(token)) {
               return token;
           }
       }
       throw new AllTokensExpiredException();
   }
   ```

### 중기 개선 (1개월)
1. **Token Pool + Auto-Refresh 조합**:
   - 최소 2개 토큰 유지
   - 각 토큰 만료 5분 전 자동 갱신
   - 갱신 실패 시 백업 토큰 사용

2. **모니터링 강화**:
   - Prometheus 메트릭 수집
   - 토큰 사용 패턴 분석
   - 갱신 실패율 추적

### 장기 개선 (3개월)
1. **단일 토큰 + 완벽한 Auto-Refresh**:
   ```java
   // 만료 5분 전 비동기 갱신
   // 갱신 중에도 기존 토큰 사용
   // 갱신 완료 후 원자적 교체
   @Async
   public void refreshTokenAsync() {
       String newToken = issueToken();
       atomicReference.set(newToken);
   }
   ```

2. **Circuit Breaker 도입**:
   - Resilience4j 적용
   - 토큰 갱신 실패 시 자동 재시도
   - 장애 격리 및 빠른 실패

3. **Event-driven Architecture**:
   - Kafka/RabbitMQ로 토큰 갱신 이벤트 발행
   - 여러 인스턴스 간 토큰 공유
   - Redis에 토큰 캐싱

## 참고 자료

- Martin Fowler - Circuit Breaker Pattern: https://martinfowler.com/bliki/CircuitBreaker.html
- Resilience4j Documentation: https://resilience4j.readme.io/
- OAuth 2.0 Token Refresh Best Practices: https://datatracker.ietf.org/doc/html/rfc6749#section-1.5
- Spring @Scheduled Documentation: https://docs.spring.io/spring-framework/docs/current/javadoc-api/org/springframework/scheduling/annotation/Scheduled.html
- AtomicReference in Java: https://docs.oracle.com/javase/8/docs/api/java/util/concurrent/atomic/AtomicReference.html
- CopyOnWriteArrayList Thread-Safety: https://docs.oracle.com/javase/8/docs/api/java/util/concurrent/CopyOnWriteArrayList.html
