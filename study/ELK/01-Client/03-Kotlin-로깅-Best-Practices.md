---
tags:
  - ELK/Client
  - Kotlin
  - BestPractices
  - 로깅
  - 보안
created: 2025-10-06
updated: 2025-10-06
---

# Kotlin 로깅 Best Practices

> [!tip] 개요
> Kotlin + Spring Boot에서 효과적이고 안전한 로깅을 위한 모범 사례

## 🎯 로깅 레벨 가이드

### 레벨별 사용 기준

| 레벨 | 용도 | 예시 |
|------|------|------|
| **ERROR** | 에러 발생 (즉시 조치 필요) | DB 연결 실패, 외부 API 오류 |
| **WARN** | 경고 (잠재적 문제) | 느린 쿼리, Deprecated API 사용 |
| **INFO** | 중요 비즈니스 이벤트 | 사용자 로그인, 주문 생성 |
| **DEBUG** | 디버깅 정보 | 메서드 진입/종료, 변수 값 |
| **TRACE** | 상세한 추적 정보 | 루프 내부, SQL 쿼리 |

### 권장 설정

```kotlin
// Production
logging.level.root=INFO
logging.level.com.example.myapp=INFO

// Staging
logging.level.root=DEBUG
logging.level.com.example.myapp=DEBUG

// Development
logging.level.root=DEBUG
logging.level.com.example.myapp=TRACE
```

---

## ✅ Do: 해야 할 것

### 1. Lazy 평가 사용

```kotlin
// ✅ 좋은 예
log.debug { "User data: $user" }

// ❌ 나쁜 예
log.debug("User data: $user")  // 로그 레벨이 꺼져있어도 문자열 생성
```

### 2. 구조화된 로깅

```kotlin
import net.logstash.logback.argument.StructuredArguments.*

// ✅ 좋은 예: 검색 가능한 필드
log.info(
    "Order created",
    kv("orderId", order.id),
    kv("userId", user.id),
    kv("amount", order.totalAmount)
)

// ❌ 나쁜 예: 문자열로만 기록
log.info("Order ${order.id} created by user ${user.id} with amount ${order.totalAmount}")
```

### 3. MDC 활용

```kotlin
// ✅ 좋은 예: 요청별 추적 가능
MDC.put("requestId", requestId)
log.info { "Processing request" }
MDC.clear()

// 모든 로그에 requestId가 자동 포함
```

### 4. Exception 로깅

```kotlin
// ✅ 좋은 예: 스택 트레이스 포함
try {
    riskyOperation()
} catch (e: Exception) {
    log.error(e) { "Failed to process order: ${order.id}" }
}

// ❌ 나쁜 예: 스택 트레이스 없음
catch (e: Exception) {
    log.error { "Error: ${e.message}" }
}
```

### 5. 의미 있는 메시지

```kotlin
// ✅ 좋은 예: 컨텍스트 포함
log.info { "Payment processed successfully for order ${orderId} in ${duration}ms" }

// ❌ 나쁜 예: 모호함
log.info { "Success" }
```

---

## ❌ Don't: 하지 말아야 할 것

### 1. 민감한 정보 로깅 금지

```kotlin
// ❌ 절대 금지
log.info { "User login: password=${user.password}" }
log.debug { "Credit card: ${payment.cardNumber}" }
log.info { "API Key: ${config.apiKey}" }

// ✅ 올바른 방법
log.info { "User login successful: userId=${user.id}" }
log.info { "Payment processed: last4=${payment.cardLast4}" }
```

### 2. 과도한 로깅 금지

```kotlin
// ❌ 나쁜 예: 루프마다 로깅
users.forEach { user ->
    log.debug { "Processing user: $user" }
}

// ✅ 좋은 예: 요약 정보만
log.debug { "Processing ${users.size} users" }
```

### 3. 프로덕션에서 DEBUG/TRACE 금지

```kotlin
// ❌ 나쁜 예
// application-prod.yml
logging.level.root=DEBUG  # 성능 저하!

// ✅ 좋은 예
logging.level.root=INFO
```

---

## 🔒 보안 고려사항

### 민감 정보 목록

> [!danger] 로그에서 제외해야 할 정보
> - 비밀번호, PIN
> - 신용카드 번호
> - 주민등록번호, 여권번호
> - API 키, 토큰
> - 세션 ID (일부만 표시)
> - 개인 식별 정보 (PII)

### 안전한 로깅 예시

```kotlin
data class User(
    val id: Long,
    val email: String,
    val password: String,  // ⚠️ 민감 정보
    val name: String
) {
    // toString()에서 민감 정보 제외
    override fun toString(): String =
        "User(id=$id, email=${email.maskEmail()}, name=$name)"

    fun toLogString(): String =
        "User(id=$id, email=${email.maskEmail()})"
}

// 이메일 마스킹
fun String.maskEmail(): String {
    val parts = this.split("@")
    if (parts.size != 2) return "***"

    val local = parts[0]
    val domain = parts[1]

    val maskedLocal = if (local.length <= 2) {
        "***"
    } else {
        local.substring(0, 2) + "***"
    }

    return "$maskedLocal@$domain"
}

// 사용
log.info { "User registered: ${user.toLogString()}" }
// 출력: User(id=123, email=jo***@example.com)
```

---

## ⚡ 성능 최적화

### 1. 비동기 Appender

```xml
<appender name="ASYNC" class="ch.qos.logback.classic.AsyncAppender">
    <appender-ref ref="FILE"/>
    <queueSize>512</queueSize>
    <discardingThreshold>0</discardingThreshold>
</appender>
```

### 2. 조건부 로깅

```kotlin
// ✅ 좋은 예: 로그 레벨 확인
if (log.isDebugEnabled) {
    val expensiveData = computeExpensiveData()
    log.debug { "Data: $expensiveData" }
}

// 또는 Lazy 평가 (자동으로 확인)
log.debug { computeExpensiveData() }
```

### 3. 샘플링

```kotlin
// 대량의 요청 중 일부만 로깅
if (Random.nextInt(100) < 10) {  // 10%만
    log.debug { "Sampled request: $request" }
}
```

---

## 📝 로깅 패턴

### Controller

```kotlin
@RestController
class OrderController(private val orderService: OrderService) {

    private val log = KotlinLogging.logger {}

    @PostMapping("/orders")
    fun createOrder(@RequestBody request: CreateOrderRequest): Order {
        log.info { "Creating order: items=${request.items.size}" }

        val order = orderService.create(request)

        log.info(
            "Order created successfully",
            kv("orderId", order.id),
            kv("userId", order.userId),
            kv("amount", order.totalAmount)
        )

        return order
    }
}
```

### Service

```kotlin
@Service
class OrderService {

    private val log = KotlinLogging.logger {}

    fun create(request: CreateOrderRequest): Order {
        log.debug { "Validating order request" }

        validateRequest(request)

        log.debug { "Saving order to database" }
        val order = orderRepository.save(request.toEntity())

        log.info { "Order saved: orderId=${order.id}" }

        return order
    }
}
```

### Exception Handler

```kotlin
@RestControllerAdvice
class GlobalExceptionHandler {

    private val log = KotlinLogging.logger {}

    @ExceptionHandler(BusinessException::class)
    fun handleBusinessException(e: BusinessException): ResponseEntity<ErrorResponse> {
        log.warn(e) {
            "Business exception occurred: ${e.message}"
        }

        return ResponseEntity
            .status(HttpStatus.BAD_REQUEST)
            .body(ErrorResponse(e.message))
    }

    @ExceptionHandler(Exception::class)
    fun handleException(e: Exception): ResponseEntity<ErrorResponse> {
        log.error(e) {
            "Unexpected error occurred: ${e.message}"
        }

        return ResponseEntity
            .status(HttpStatus.INTERNAL_SERVER_ERROR)
            .body(ErrorResponse("Internal server error"))
    }
}
```

---

## 🧪 테스트에서의 로깅

```kotlin
class OrderServiceTest {

    // 테스트에서는 로그 레벨을 낮춤
    @BeforeAll
    fun setup() {
        val logger = LoggerFactory.getLogger("com.example") as ch.qos.logback.classic.Logger
        logger.level = Level.WARN
    }

    @Test
    fun `should create order`() {
        // 테스트 중 불필요한 로그 출력 방지
        val order = orderService.create(request)
        assertThat(order.id).isNotNull()
    }
}
```

---

## 📋 체크리스트

### 코드 리뷰시 확인사항

- [ ] Lazy 평가 사용 (`log.info { }`)
- [ ] 민감한 정보 필터링
- [ ] 구조화된 로깅 (StructuredArguments)
- [ ] Exception 스택 트레이스 포함
- [ ] 의미 있는 로그 메시지
- [ ] 적절한 로그 레벨
- [ ] MDC 사용 (요청 추적)
- [ ] 과도한 로깅 없음

### 프로덕션 배포 전

- [ ] 로그 레벨 INFO 이상
- [ ] 비동기 Appender 사용
- [ ] 민감 정보 제거 확인
- [ ] 로그 파일 로테이션 설정
- [ ] Elasticsearch 연결 확인

---

## 🔗 관련 문서

- [[01-Kotlin-SpringBoot-로깅-설정|← Kotlin 로깅 설정]]
- [[../02-Server/02-Logstash-파이프라인|Logstash 파이프라인 →]]

---

#ELK/Client #BestPractices #Kotlin #보안 #성능최적화
