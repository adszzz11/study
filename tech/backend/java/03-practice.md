---
date: 2025-01-18
tags:
  - tech
  - practice
  - java
  - performance
  - debugging
parent: "[[README]]"
---

# Java - 실무 적용

> ⬅️ [[02-core|이전: JVM 심화]] | ➡️ [[04-advanced|다음: 고급]]

---

## 1. 성능 최적화

### JVM 옵션 설정

```bash
# 프로덕션 권장 설정 (4GB 힙 기준)
java \
  -Xms4g -Xmx4g \                    # 힙 크기 고정
  -XX:+UseG1GC \                     # G1 GC 사용
  -XX:MaxGCPauseMillis=200 \         # 목표 STW 시간
  -XX:+HeapDumpOnOutOfMemoryError \  # OOM 시 덤프
  -XX:HeapDumpPath=/var/log/heap.hprof \
  -Xlog:gc*:file=/var/log/gc.log:time \
  -jar application.jar
```

### 메모리 크기 산정

| 애플리케이션 유형 | 힙 크기 | GC 권장 |
|-----------------|--------|---------|
| 소규모 서비스 | 512MB~2GB | G1 GC |
| 일반 웹 서비스 | 2GB~8GB | G1 GC |
| 대용량 처리 | 8GB~32GB | G1 GC / ZGC |
| 초저지연 필요 | 16GB+ | ZGC |

### String 최적화

```java
// Bad: 매번 새 객체 생성
String result = "";
for (int i = 0; i < 1000; i++) {
    result += i;  // O(n²)
}

// Good: StringBuilder 사용
StringBuilder sb = new StringBuilder();
for (int i = 0; i < 1000; i++) {
    sb.append(i);  // O(n)
}
String result = sb.toString();

// String Interning
String s1 = new String("hello").intern();
String s2 = "hello";
System.out.println(s1 == s2);  // true
```

### Collection 선택

```java
// 읽기 위주 → ArrayList
List<User> users = new ArrayList<>();

// 삽입/삭제 빈번 → LinkedList
List<Task> tasks = new LinkedList<>();

// 빠른 조회 → HashMap
Map<Long, User> userMap = new HashMap<>();

// 순서 보장 → LinkedHashMap
Map<String, Object> orderedMap = new LinkedHashMap<>();

// 정렬 필요 → TreeMap
Map<String, Integer> sortedMap = new TreeMap<>();

// 동시성 → ConcurrentHashMap
Map<String, Session> sessions = new ConcurrentHashMap<>();
```

---

## 2. 프로파일링

### JFR (Java Flight Recorder)

```bash
# JFR 활성화하여 실행
java -XX:StartFlightRecording=duration=60s,filename=recording.jfr \
     -jar application.jar

# 실행 중 녹화 시작
jcmd <pid> JFR.start duration=60s filename=recording.jfr

# 분석
jfr print --events CPULoad,GarbageCollection recording.jfr
```

### jstat - GC 모니터링

```bash
# GC 통계 (1초 간격, 10회)
jstat -gc <pid> 1000 10

# 출력 예시
# S0C   S1C   S0U   S1U   EC    EU    OC      OU      MC     MU
# 2048  2048  0     1024  16384 8192  40960   20480   4480   4200

# 주요 지표
# S0C/S1C: Survivor 용량
# EC: Eden 용량
# OC: Old 용량
# GCT: 총 GC 시간
```

### Async Profiler

```bash
# CPU 프로파일링
./profiler.sh -d 30 -f cpu.html <pid>

# 메모리 할당 프로파일링
./profiler.sh -e alloc -d 30 -f alloc.html <pid>

# Flame Graph 생성
./profiler.sh -d 30 -f flamegraph.svg <pid>
```

---

## 3. 디버깅

### Heap Dump 분석

```bash
# Heap Dump 생성
jmap -dump:format=b,file=heap.hprof <pid>

# OOM 시 자동 덤프
-XX:+HeapDumpOnOutOfMemoryError
-XX:HeapDumpPath=/path/to/dump

# MAT (Memory Analyzer Tool)로 분석
# - Dominator Tree: 메모리 점유 객체
# - Leak Suspects: 누수 의심 지점
# - Histogram: 클래스별 인스턴스 수
```

### Thread Dump 분석

```bash
# Thread Dump 생성
jstack <pid> > thread_dump.txt

# 여러 번 캡처 (3회, 5초 간격)
for i in 1 2 3; do jstack <pid> >> thread_dump.txt; sleep 5; done
```

```
# Thread Dump 분석 포인트
"http-nio-8080-exec-1" #15 daemon prio=5 os_prio=0 tid=0x00007f...
   java.lang.Thread.State: BLOCKED (on object monitor)
        at com.example.Service.process(Service.java:45)
        - waiting to lock <0x000000076b4a1234> (a java.lang.Object)
        - locked <0x000000076b4a5678> (a java.lang.Object)
        at com.example.Controller.handle(Controller.java:23)

# BLOCKED: 락 대기 중
# WAITING: 조건 대기 중
# TIMED_WAITING: 시간 제한 대기
# RUNNABLE: 실행 중 또는 실행 가능
```

### 원격 디버깅

```bash
# 서버에서 디버그 모드로 실행
java -agentlib:jdwp=transport=dt_socket,server=y,suspend=n,address=*:5005 \
     -jar application.jar

# IDE에서 Remote Debug 연결
# Host: server-ip, Port: 5005
```

---

## 4. 로깅 Best Practices

### SLF4J + Logback

```java
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class UserService {
    private static final Logger log = LoggerFactory.getLogger(UserService.class);

    public User findUser(Long id) {
        log.debug("Finding user with id: {}", id);  // 파라미터 바인딩

        try {
            User user = repository.findById(id);
            log.info("User found: {}", user.getName());
            return user;
        } catch (Exception e) {
            log.error("Failed to find user: {}", id, e);  // 예외 스택트레이스
            throw e;
        }
    }
}
```

### logback.xml 설정

```xml
<configuration>
    <appender name="FILE" class="ch.qos.logback.core.rolling.RollingFileAppender">
        <file>logs/application.log</file>
        <rollingPolicy class="ch.qos.logback.core.rolling.TimeBasedRollingPolicy">
            <fileNamePattern>logs/application.%d{yyyy-MM-dd}.log</fileNamePattern>
            <maxHistory>30</maxHistory>
        </rollingPolicy>
        <encoder>
            <pattern>%d{yyyy-MM-dd HH:mm:ss.SSS} [%thread] %-5level %logger{36} - %msg%n</pattern>
        </encoder>
    </appender>

    <root level="INFO">
        <appender-ref ref="FILE" />
    </root>
</configuration>
```

---

## 5. 실무 코드 패턴

### Connection Pool 설정 (HikariCP)

```yaml
# application.yml
spring:
  datasource:
    hikari:
      maximum-pool-size: 10
      minimum-idle: 5
      idle-timeout: 300000      # 5분
      max-lifetime: 1800000     # 30분
      connection-timeout: 30000 # 30초
```

### 비동기 처리

```java
@Service
public class AsyncService {

    @Async
    public CompletableFuture<User> fetchUserAsync(Long id) {
        User user = userRepository.findById(id);
        return CompletableFuture.completedFuture(user);
    }
}

// 호출
CompletableFuture<User> future1 = asyncService.fetchUserAsync(1L);
CompletableFuture<User> future2 = asyncService.fetchUserAsync(2L);

// 병렬 실행 후 결과 수집
List<User> users = Stream.of(future1, future2)
    .map(CompletableFuture::join)
    .collect(Collectors.toList());
```

### 예외 처리 패턴

```java
// Custom Exception
public class BusinessException extends RuntimeException {
    private final ErrorCode errorCode;

    public BusinessException(ErrorCode errorCode) {
        super(errorCode.getMessage());
        this.errorCode = errorCode;
    }
}

// Global Exception Handler
@RestControllerAdvice
public class GlobalExceptionHandler {

    @ExceptionHandler(BusinessException.class)
    public ResponseEntity<ErrorResponse> handleBusinessException(BusinessException e) {
        return ResponseEntity
            .status(e.getErrorCode().getStatus())
            .body(new ErrorResponse(e.getErrorCode()));
    }
}
```

---

## 6. 체크리스트

### 운영 전 점검

- [ ] JVM 힙 크기 적절히 설정 (-Xms, -Xmx)
- [ ] GC 알고리즘 선택 완료
- [ ] GC 로그 활성화
- [ ] HeapDumpOnOutOfMemoryError 설정
- [ ] Connection Pool 크기 검토
- [ ] 로깅 레벨 및 로테이션 설정

### 성능 점검

- [ ] 응답시간 P99 < 200ms 확인
- [ ] GC Pause Time < 200ms
- [ ] Heap 사용량 70% 미만 유지
- [ ] Thread 수 적정 범위 내

---

## 다음 단계

> [!tip] 다음으로
> 실무 기법을 익혔다면 [[04-advanced|고급]]에서 Java 21 신기능과 고급 패턴을 학습하세요.

---

## References

- [HikariCP Configuration](https://github.com/brettwooldridge/HikariCP)
- [JFR Documentation](https://docs.oracle.com/en/java/javase/17/jfapi/)
- [Async Profiler](https://github.com/jvm-profiling-tools/async-profiler)
