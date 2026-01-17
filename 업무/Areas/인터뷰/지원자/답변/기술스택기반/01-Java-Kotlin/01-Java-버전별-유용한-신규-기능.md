# Java 7에서 21까지 버전업하면서 가장 유용했던 신규 기능은?

## 답변

저는 실무에서 Java 7부터 시작해서 현재 Java 21까지 다양한 버전을 경험했습니다. 각 버전마다 유용한 기능들이 있었지만, 실제 프로덕션 코드에서 **생산성과 코드 품질에 가장 큰 영향**을 준 기능들을 중심으로 말씀드리겠습니다.

가장 임팩트가 컸던 기능은:
1. **Java 8: Stream API와 Lambda** - 코드 가독성과 함수형 프로그래밍
2. **Java 11: Local Variable Type Inference (var)** - 보일러플레이트 감소
3. **Java 17: Record와 Sealed Class** - 불변 객체와 타입 안정성
4. **Java 21: Virtual Thread** - 동시성 프로그래밍 패러다임 전환

## 핵심 키워드

- Java 버전별 주요 기능
- 실무 적용 경험
- 생산성 향상
- 코드 품질 개선

## 버전별 주요 기능

### Java 8 (2014) - 가장 혁신적인 변화

#### 1. Lambda Expression & Stream API
```java
// Before Java 8
List<User> activeUsers = new ArrayList<>();
for (User user : users) {
    if (user.isActive() && user.getAge() >= 18) {
        activeUsers.add(user);
    }
}
Collections.sort(activeUsers, new Comparator<User>() {
    @Override
    public int compare(User u1, User u2) {
        return u1.getName().compareTo(u2.getName());
    }
});

// After Java 8
List<User> activeUsers = users.stream()
    .filter(User::isActive)
    .filter(user -> user.getAge() >= 18)
    .sorted(Comparator.comparing(User::getName))
    .collect(Collectors.toList());
```

**실무 적용:**
- 대용량 거래 데이터 필터링 로직 40% 라인 수 감소
- 병렬 스트림을 활용한 배치 처리 성능 2배 향상

#### 2. Optional
```java
// Before Java 8 - Null 체크 지옥
public String getUserEmail(String userId) {
    User user = userRepository.findById(userId);
    if (user != null) {
        Email email = user.getEmail();
        if (email != null) {
            return email.getValue();
        }
    }
    return "unknown@example.com";
}

// After Java 8
public String getUserEmail(String userId) {
    return userRepository.findById(userId)
        .map(User::getEmail)
        .map(Email::getValue)
        .orElse("unknown@example.com");
}
```

**효과:**
- NullPointerException 발생 80% 감소
- 코드 가독성 대폭 향상

#### 3. Default Method (Interface)
```java
public interface PaymentGateway {
    PaymentResult process(Payment payment);

    // Java 8부터 가능
    default boolean validate(Payment payment) {
        return payment.getAmount() > 0 && payment.getUser() != null;
    }
}
```

**장점:** 기존 인터페이스에 메서드 추가 시 구현체 수정 불필요

### Java 11 (2018) - LTS 버전

#### 1. Local Variable Type Inference (var)
```java
// Before
Map<String, List<Transaction>> userTransactions =
    new HashMap<String, List<Transaction>>();

// After
var userTransactions = new HashMap<String, List<Transaction>>();

// 특히 Stream에서 유용
var activeAdultUsers = users.stream()
    .filter(user -> user.isActive() && user.getAge() >= 18)
    .collect(Collectors.toList());
```

**주의사항:**
- 타입이 명확하지 않은 경우 사용 지양
- 가독성을 해치지 않는 선에서 사용

#### 2. String 메서드 개선
```java
// isBlank() - 공백 문자 체크
if (email.isBlank()) {
    throw new IllegalArgumentException("Email is required");
}

// lines() - 문자열을 라인별로 스트림 처리
String multiline = "line1\nline2\nline3";
multiline.lines()
    .filter(line -> !line.isEmpty())
    .forEach(System.out::println);

// strip() - 유니코드 공백도 제거
String cleaned = "  hello  ".strip();
```

#### 3. HTTP Client (Standard)
```java
// Before - Apache HttpClient 의존성 필요
// After - Java 11 기본 제공
var client = HttpClient.newHttpClient();
var request = HttpRequest.newBuilder()
    .uri(URI.create("https://api.example.com/users"))
    .header("Content-Type", "application/json")
    .POST(HttpRequest.BodyPublishers.ofString(json))
    .build();

var response = client.send(request, HttpResponse.BodyHandlers.ofString());
```

### Java 17 (2021) - 현재 주력 LTS

#### 1. Record (불변 데이터 클래스)
```java
// Before Java 17
public class Point {
    private final int x;
    private final int y;

    public Point(int x, int y) {
        this.x = x;
        this.y = y;
    }

    public int getX() { return x; }
    public int getY() { return y; }

    @Override
    public boolean equals(Object o) { ... }
    @Override
    public int hashCode() { ... }
    @Override
    public String toString() { ... }
}

// After Java 17
public record Point(int x, int y) {}
```

**실무 적용:**
- DTO 클래스 작성 시간 90% 감소
- 불변 객체 자동 보장으로 Thread-Safe

```java
// 실제 프로젝트 예시
public record TransactionEvent(
    String txnId,
    String userId,
    BigDecimal amount,
    LocalDateTime timestamp
) {
    // Compact Constructor로 Validation 가능
    public TransactionEvent {
        if (amount.compareTo(BigDecimal.ZERO) <= 0) {
            throw new IllegalArgumentException("Amount must be positive");
        }
    }
}
```

#### 2. Sealed Class (봉인된 클래스)
```java
// 허용된 서브클래스만 상속 가능
public sealed interface PaymentMethod
    permits CreditCard, DebitCard, BankTransfer {
}

public final class CreditCard implements PaymentMethod { ... }
public final class DebitCard implements PaymentMethod { ... }
public final class BankTransfer implements PaymentMethod { ... }

// Pattern Matching과 함께 사용
public String processPayment(PaymentMethod method) {
    return switch (method) {
        case CreditCard cc -> "Processing credit card: " + cc.getCardNumber();
        case DebitCard dc -> "Processing debit card: " + dc.getCardNumber();
        case BankTransfer bt -> "Processing bank transfer: " + bt.getAccountNumber();
        // 컴파일러가 모든 케이스 체크 - default 불필요!
    };
}
```

**효과:**
- 타입 안정성 향상
- 런타임 에러 → 컴파일 타임 에러로 전환

#### 3. Pattern Matching for switch
```java
// Before
if (obj instanceof String) {
    String s = (String) obj;
    System.out.println(s.length());
} else if (obj instanceof Integer) {
    Integer i = (Integer) obj;
    System.out.println(i * 2);
}

// After Java 17
switch (obj) {
    case String s -> System.out.println(s.length());
    case Integer i -> System.out.println(i * 2);
    case null -> System.out.println("null value");
    default -> System.out.println("Unknown type");
}
```

### Java 21 (2023) - 최신 LTS

#### 1. Virtual Thread (Project Loom)
```java
// Before - Platform Thread (무겁고 비쌈)
ExecutorService executor = Executors.newFixedThreadPool(100);
for (int i = 0; i < 10000; i++) {
    executor.submit(() -> {
        // I/O 작업
    });
}

// After - Virtual Thread (가볍고 효율적)
try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
    for (int i = 0; i < 10000; i++) {
        executor.submit(() -> {
            // I/O 작업 - 수백만 개도 가능!
        });
    }
}
```

**성능 테스트 결과:**
- 동시 요청 처리량 10배 향상 (1,000 TPS → 10,000 TPS)
- 메모리 사용량 70% 감소
- 특히 I/O Bound 작업에서 효과적

**실무 적용 계획:**
- 외부 API 호출이 많은 정산 배치 시스템에 적용 예정
- WebFlux 대신 Virtual Thread + Spring MVC 조합 검토 중

#### 2. Sequenced Collections
```java
// Before - 첫/마지막 요소 접근이 불편
List<String> list = new ArrayList<>();
String first = list.get(0);
String last = list.get(list.size() - 1);

// After Java 21
String first = list.getFirst();
String last = list.getLast();
list.addFirst("element");
list.addLast("element");

// Reversed view
for (String item : list.reversed()) {
    System.out.println(item);
}
```

#### 3. String Templates (Preview)
```java
// Before
String message = String.format(
    "User %s made a transaction of %s at %s",
    userName, amount, timestamp
);

// After Java 21 (Preview)
String message = STR."""
    User \{userName} made a transaction of \{amount} at \{timestamp}
    """;
```

## 실제 프로젝트 적용 사례

### Case 1: 거래 데이터 처리 최적화 (Java 8 Stream)
```java
// 월별 거래 통계 생성
Map<YearMonth, BigDecimal> monthlyStats = transactions.stream()
    .collect(Collectors.groupingBy(
        txn -> YearMonth.from(txn.getTimestamp()),
        Collectors.reducing(
            BigDecimal.ZERO,
            Transaction::getAmount,
            BigDecimal::add
        )
    ));
```
- 처리 시간: 5초 → 2초 (60% 개선)
- 코드 라인: 50줄 → 8줄

### Case 2: DTO 간소화 (Java 17 Record)
```java
// API 응답 DTO
public record TransactionResponse(
    String txnId,
    String userId,
    BigDecimal amount,
    String status,
    LocalDateTime timestamp
) {
    public static TransactionResponse from(Transaction txn) {
        return new TransactionResponse(
            txn.getId(),
            txn.getUserId(),
            txn.getAmount(),
            txn.getStatus().name(),
            txn.getTimestamp()
        );
    }
}
```
- 보일러플레이트 코드 80% 감소
- 불변성 자동 보장

### Case 3: 비동기 처리 개선 (Java 21 Virtual Thread 예정)
```java
// 100개 외부 API 병렬 호출
try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
    List<CompletableFuture<ApiResponse>> futures = apiRequests.stream()
        .map(request -> CompletableFuture.supplyAsync(
            () -> callExternalApi(request),
            executor
        ))
        .toList();

    List<ApiResponse> responses = futures.stream()
        .map(CompletableFuture::join)
        .toList();
}
```
- 예상 효과: 처리 시간 10초 → 1초

## 참고 자료

- [Java 8 Features](https://docs.oracle.com/javase/8/docs/technotes/guides/language/enhancements.html)
- [Java 17 Features](https://openjdk.org/projects/jdk/17/)
- [Java 21 Features](https://openjdk.org/projects/jdk/21/)
- [Virtual Threads - JEP 444](https://openjdk.org/jeps/444)
- [Oracle Java SE Support Roadmap](https://www.oracle.com/java/technologies/java-se-support-roadmap.html)
