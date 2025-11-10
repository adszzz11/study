# Kotlin을 주 언어로 사용하는 이유는? Java와 비교했을 때 실무에서 느낀 장단점은?

## 답변

저는 2022년부터 Kotlin을 주 언어로 사용하기 시작했고, 현재는 신규 프로젝트의 90% 이상을 Kotlin으로 개발하고 있습니다.

Kotlin을 선택한 가장 큰 이유는 **생산성과 안정성의 균형**입니다. Java의 장황한 보일러플레이트 코드를 줄이면서도, 정적 타입 언어의 안정성은 유지하고, Null 안정성을 언어 차원에서 지원받을 수 있기 때문입니다.

실무에서는 **코드 작성 시간이 30% 단축**되었고, **NullPointerException이 90% 감소**했으며, **코드 가독성이 크게 향상**되었습니다. 다만 팀 전체의 러닝커브와 Java 라이브러리 interop 시 일부 주의사항이 있었습니다.

## 핵심 키워드

- Kotlin
- Null Safety
- 간결성 (Conciseness)
- Java Interoperability
- 코루틴 (Coroutines)
- 함수형 프로그래밍
- Extension Function

## Kotlin 선택 배경

### 1. 프로젝트 요구사항
- 선불통합관리서비스는 안정성이 최우선
- 금융 도메인 특성상 Null 처리가 매우 중요
- 대용량 트래픽 처리를 위한 비동기 프로그래밍 필요
- 빠른 개발 속도와 유지보수성 요구

### 2. Kotlin의 장점이 잘 맞았던 이유
- **Null Safety**: 금융 시스템에서 치명적인 NPE 사전 차단
- **Coroutine**: 대용량 트래픽을 효율적으로 처리
- **간결한 문법**: 3명의 작은 팀에서 빠른 개발 가능
- **Java 호환성**: 기존 Spring 생태계 그대로 활용

## Java 대비 장점

### 1. Null Safety (가장 큰 장점!)

```kotlin
// Java - Null 체크 지옥
public String getUserEmail(String userId) {
    User user = userRepository.findById(userId);
    if (user != null) {
        Email email = user.getEmail();
        if (email != null) {
            String value = email.getValue();
            if (value != null) {
                return value;
            }
        }
    }
    return "unknown@example.com";
}

// Kotlin - 안전한 호출 연산자
fun getUserEmail(userId: String): String {
    return userRepository.findById(userId)
        ?.email
        ?.value
        ?: "unknown@example.com"
}
```

**실무 효과:**
- NullPointerException 발생 90% 감소
- Null 처리 코드 70% 감소
- 컴파일 타임에 Null 가능성 체크

### 2. 간결한 문법

```kotlin
// Java - Data Class
public class TransactionDto {
    private final String id;
    private final BigDecimal amount;
    private final LocalDateTime createdAt;

    public TransactionDto(String id, BigDecimal amount, LocalDateTime createdAt) {
        this.id = id;
        this.amount = amount;
        this.createdAt = createdAt;
    }

    public String getId() { return id; }
    public BigDecimal getAmount() { return amount; }
    public LocalDateTime getCreatedAt() { return createdAt; }

    @Override
    public boolean equals(Object o) { ... }  // 10줄
    @Override
    public int hashCode() { ... }  // 5줄
    @Override
    public String toString() { ... }  // 5줄
}
// 총 50줄

// Kotlin - Data Class
data class TransactionDto(
    val id: String,
    val amount: BigDecimal,
    val createdAt: LocalDateTime
)
// 총 5줄 (90% 감소!)
```

**실무 효과:**
- DTO 클래스 작성 시간 95% 단축
- 코드 라인 수 평균 40% 감소
- 유지보수성 향상

### 3. Extension Function

```kotlin
// 기존 클래스에 메서드 추가 (클래스 수정 없이!)
fun BigDecimal.toKoreanWon(): String {
    return "${this.setScale(0, RoundingMode.HALF_UP).toPlainString()}원"
}

fun String.maskEmail(): String {
    val parts = this.split("@")
    if (parts.size != 2) return this
    val masked = parts[0].take(3) + "***"
    return "$masked@${parts[1]}"
}

// 사용
val amount = BigDecimal("10000")
println(amount.toKoreanWon())  // "10,000원"

val email = "user@example.com"
println(email.maskEmail())  // "use***@example.com"
```

**실무 효과:**
- 유틸리티 클래스 불필요
- 코드 가독성 향상
- 도메인 로직을 도메인 객체에 응집

### 4. 코루틴 (Coroutines)

```kotlin
// Java - CompletableFuture (복잡)
public CompletableFuture<List<ApiResponse>> callMultipleApis(List<String> urls) {
    List<CompletableFuture<ApiResponse>> futures = urls.stream()
        .map(url -> CompletableFuture.supplyAsync(() -> callApi(url)))
        .collect(Collectors.toList());

    return CompletableFuture.allOf(futures.toArray(new CompletableFuture[0]))
        .thenApply(v -> futures.stream()
            .map(CompletableFuture::join)
            .collect(Collectors.toList()));
}

// Kotlin - Coroutine (간결하고 직관적)
suspend fun callMultipleApis(urls: List<String>): List<ApiResponse> = coroutineScope {
    urls.map { url ->
        async { callApi(url) }
    }.awaitAll()
}
```

**실무 효과:**
- 비동기 코드를 동기 코드처럼 작성
- Thread 생성 오버헤드 없이 수백만 개의 코루틴 실행 가능
- 구조적 동시성으로 메모리 누수 방지

### 5. Smart Cast

```kotlin
// Java
if (obj instanceof String) {
    String str = (String) obj;  // 명시적 캐스팅 필요
    System.out.println(str.length());
}

// Kotlin - Smart Cast
if (obj is String) {
    println(obj.length)  // 자동으로 String으로 캐스팅됨!
}

// when과 함께 사용 (매우 강력)
fun processPayment(method: PaymentMethod) = when (method) {
    is CreditCard -> processCreditCard(method.cardNumber)  // 자동 캐스팅
    is BankTransfer -> processBankTransfer(method.accountNumber)  // 자동 캐스팅
    is MobilePayment -> processMobilePayment(method.phoneNumber)  // 자동 캐스팅
}
```

### 6. Default Parameter & Named Arguments

```kotlin
// Java - 오버로딩 지옥
public void createUser(String name) {
    createUser(name, "default@example.com", 0);
}

public void createUser(String name, String email) {
    createUser(name, email, 0);
}

public void createUser(String name, String email, int age) {
    // 실제 구현
}

// Kotlin - Default Parameter
fun createUser(
    name: String,
    email: String = "default@example.com",
    age: Int = 0
) {
    // 실제 구현
}

// Named Arguments로 가독성 향상
createUser(
    name = "홍길동",
    email = "hong@example.com"  // age는 기본값 사용
)
```

## Java 대비 단점

### 1. 러닝커브

**문제:**
- 팀원들이 Kotlin 문법과 관용구를 익히는데 시간 필요
- 특히 고급 기능(inline, reified, DSL 등)은 이해하기 어려움

**해결:**
- Kotlin 스터디 진행 (2주)
- Code Review를 통한 Best Practice 공유
- Java에서 점진적으로 전환 (신규 클래스부터 Kotlin으로)

### 2. 컴파일 속도

**문제:**
- Java보다 컴파일 속도가 10~15% 느림
- 대규모 프로젝트에서 체감됨

**해결:**
- Gradle Build Cache 활성화
- Incremental Compilation 활용
- 불필요한 allopen, noarg 플러그인 제거

```kotlin
// build.gradle.kts
kotlin {
    incremental = true  // 증분 컴파일
}
```

### 3. Java 라이브러리 Interop 시 주의사항

**문제:**
- Java 라이브러리가 반환하는 null을 Kotlin이 감지 못함
- Platform Type (String!) 으로 추론되어 런타임 NPE 가능

```kotlin
// Java 라이브러리
public class JavaLibrary {
    public String getValue() {
        return null;  // Nullable이지만 애노테이션 없음
    }
}

// Kotlin에서 사용
val value = JavaLibrary().getValue()  // String! (Platform Type)
println(value.length)  // NPE 발생 가능!
```

**해결:**
```kotlin
// 1. Safe call 사용
val length = JavaLibrary().getValue()?.length

// 2. @Nullable/@NotNull 애노테이션 요청
// 또는 Wrapper 클래스 작성
class SafeJavaLibrary(private val lib: JavaLibrary) {
    fun getValue(): String? = lib.getValue()
}
```

### 4. 빌드 파일 크기 증가

**문제:**
- Kotlin 표준 라이브러리 포함으로 JAR 파일 크기 증가 (약 1.5MB)
- 람다/인라인 함수 사용 시 추가 바이트코드 생성

**영향:**
- 실무에서는 큰 문제 아님 (전체 JAR이 50MB 이상)
- Lambda/Cloud Function 같은 환경에서는 고려 필요

### 5. Checked Exception 없음

**문제:**
- Java의 Checked Exception을 강제하지 않음
- 예외 처리를 놓칠 수 있음

```kotlin
// Java
public void readFile(String path) throws IOException {  // 명시적
    Files.readAllBytes(Paths.get(path));
}

// Kotlin
fun readFile(path: String) {  // IOException 명시 안 함
    Files.readAllBytes(Paths.get(path))
}
```

**해결:**
```kotlin
// @Throws로 명시적 표현
@Throws(IOException::class)
fun readFile(path: String) {
    Files.readAllBytes(Paths.get(path))
}

// Result 타입 사용
fun readFile(path: String): Result<ByteArray> = runCatching {
    Files.readAllBytes(Paths.get(path))
}
```

## 실무 적용 사례

### Case 1: 금융 거래 검증 로직

```kotlin
// Kotlin의 when, sealed class, extension으로 깔끔한 도메인 로직
sealed class TransactionValidationResult {
    object Valid : TransactionValidationResult()
    data class Invalid(val reason: String) : TransactionValidationResult()
}

fun Transaction.validate(): TransactionValidationResult = when {
    amount <= BigDecimal.ZERO ->
        Invalid("금액은 0보다 커야 합니다")
    userId.isBlank() ->
        Invalid("사용자 ID는 필수입니다")
    createdAt.isAfter(LocalDateTime.now()) ->
        Invalid("미래 시간으로 거래할 수 없습니다")
    else ->
        Valid
}

// 사용
val result = transaction.validate()
when (result) {
    is Valid -> processTransaction(transaction)
    is Invalid -> throw ValidationException(result.reason)
}
```

### Case 2: 대용량 배치 처리 (코루틴 활용)

```kotlin
// 10,000건의 거래를 병렬로 처리
suspend fun processBatchTransactions(transactions: List<Transaction>) = coroutineScope {
    transactions
        .chunked(100)  // 100건씩 묶음
        .map { chunk ->
            async {
                chunk.forEach { transaction ->
                    processTransaction(transaction)
                }
            }
        }
        .awaitAll()
}

// 처리 시간: 10분 → 2분 (80% 개선)
```

### Case 3: DSL을 활용한 쿼리 작성

```kotlin
// QueryDSL과 Kotlin의 조합
fun findTransactions(builder: TransactionQueryBuilder.() -> Unit): List<Transaction> {
    return TransactionQueryBuilder()
        .apply(builder)
        .build()
        .fetch()
}

// 사용 - 매우 직관적!
val transactions = findTransactions {
    userId eq "user123"
    amount greaterThan BigDecimal("1000")
    createdAt between (startDate to endDate)
    status in listOf(COMPLETED, PENDING)
}
```

## 성과 및 효과

### 정량적 효과
- **개발 속도**: 30% 향상 (보일러플레이트 감소)
- **버그 감소**: NPE 90% 감소, 전체 버그 40% 감소
- **코드 라인**: 평균 40% 감소
- **테스트 커버리지**: 85% → 92% 향상 (테스트 작성이 쉬워짐)

### 정성적 효과
- 코드 리뷰 시간 단축 (가독성 향상)
- 신입 개발자 온보딩 시간 단축 (직관적인 문법)
- 유지보수성 향상 (명확한 의도 표현)

## 마이그레이션 전략

### 점진적 전환
1. **신규 클래스부터 Kotlin으로 작성**
2. **테스트 코드를 Kotlin으로 먼저 전환** (부담 없음)
3. **Util 성 클래스 전환** (의존성 적음)
4. **핵심 도메인 로직 전환** (Kotlin의 장점 극대화)
5. **레거시 코드는 유지** (무리한 전환 금지)

### 혼용 전략
```kotlin
// Kotlin과 Java 혼용 가능
// Kotlin Service → Java Repository 호출
@Service
class TransactionService(
    private val transactionRepository: TransactionRepository  // Java 클래스
) {
    fun getTransaction(id: String): Transaction? {
        return transactionRepository.findById(id).orElse(null)
    }
}
```

## 참고 자료

- [Kotlin 공식 문서](https://kotlinlang.org/docs/home.html)
- [Kotlin for Java Developers - Coursera](https://www.coursera.org/learn/kotlin-for-java-developers)
- [Effective Kotlin - Marcin Moskała](https://kt.academy/book/effectivekotlin)
- [Kotlin in Action - Dmitry Jemerov](https://www.manning.com/books/kotlin-in-action)
- [Spring Kotlin 가이드](https://spring.io/guides/tutorials/spring-boot-kotlin/)
- [우아한형제들 - Kotlin 도입기](https://techblog.woowahan.com/2520/)
