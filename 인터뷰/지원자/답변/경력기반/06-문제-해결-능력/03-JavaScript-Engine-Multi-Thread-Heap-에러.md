# JavaScript Engine Load 시 multi-thread heap 탈취 에러는 어떻게 재현하고 검증했나요?

## 답변

서버 사이드에서 JavaScript 코드를 실행하기 위해 Nashorn 엔진을 사용하는 중, 멀티스레드 환경에서 간헐적으로 "IllegalStateException: Context is already closed" 또는 "concurrent heap access" 에러가 발생했습니다. 이는 하나의 ScriptEngine 인스턴스를 여러 스레드가 동시에 사용하면서 발생한 thread-safety 문제였습니다.

재현을 위해 JMeter로 동시 100개 요청을 보내는 부하 테스트를 수행했고, 단일 ScriptEngine을 공유하는 환경에서 에러 재현율이 약 15%였습니다. Thread dump와 스택 트레이스 분석 결과, 여러 스레드가 동일한 Engine의 internal state를 동시에 수정하려다 충돌하는 것을 확인했습니다.

해결 방법으로 세 가지를 검토했습니다:
1. ThreadLocal을 사용한 스레드별 Engine 격리
2. Object Pool 패턴으로 Engine 인스턴스 관리
3. 동기화(synchronized) 처리

ThreadLocal 방식은 스레드 수만큼 Engine이 생성되어 메모리 효율이 떨어지고, 동기화 방식은 성능 저하가 심했습니다. 최종적으로 Apache Commons Pool2를 사용한 Engine Pool을 구현했습니다. 초기 10개, 최대 50개의 Engine을 Pool로 관리하여 Thread-safety를 보장하면서도 메모리 효율성을 확보했습니다.

결과적으로 에러는 완전히 제거되었고, 동기화 방식 대비 응답 시간도 70% 개선되었습니다.

## 핵심 키워드

- JavaScript Engine
- Multi-thread
- Heap 메모리
- Thread Safety
- 동시성 문제

## 문제 상황

### 사용 기술
- JavaScript Engine: **Nashorn** (JDK 8~14 내장 JavaScript 엔진)
- 사용 목적: 사용자 정의 비즈니스 로직을 JavaScript로 작성하여 동적 실행
- 런타임: Java 8, Spring Boot 2.x
- 배포 환경: Tomcat 9 (스레드 풀 200)

### 에러 증상
```
java.lang.IllegalStateException: Context is already closed
    at jdk.nashorn.internal.runtime.Context.checkNotEnv(Context.java:395)
    at jdk.nashorn.internal.runtime.ScriptFunction.makeBoundFunction(ScriptFunction.java:699)

// 또는
java.lang.ArrayIndexOutOfBoundsException: Concurrent heap access detected
    at jdk.nashorn.internal.runtime.PropertyMap.getProperty(PropertyMap.java:123)
```

**발생 패턴:**
- 부하 테스트 시 15-20% 확률로 발생
- 단일 요청에서는 발생하지 않음 (동시성 문제)
- 에러 발생 시 해당 요청뿐 아니라 다른 요청도 영향 받음
- 서버 재시작 전까지 간헐적 에러 계속 발생

## 재현 방법

### 테스트 환경 구성
```xml
<!-- pom.xml -->
<dependencies>
    <dependency>
        <groupId>org.openjdk.nashorn</groupId>
        <artifactId>nashorn-core</artifactId>
        <version>15.4</version>
    </dependency>
</dependencies>
```

### 재현 코드
```java
// 문제가 있는 코드 - 싱글톤 ScriptEngine 공유
@Service
public class JavaScriptExecutor {
    // 모든 스레드가 공유하는 단일 엔진 - 문제의 원인!
    private static final ScriptEngine engine =
        new ScriptEngineManager().getEngineByName("nashorn");

    public Object execute(String script, Map<String, Object> context)
            throws ScriptException {
        // 여러 스레드가 동시에 같은 engine 인스턴스 사용
        Bindings bindings = engine.createBindings();
        context.forEach(bindings::put);

        // 동시 실행 시 internal state 충돌 발생
        return engine.eval(script, bindings);
    }
}

// 재현 테스트 코드
@Test
public void testConcurrentExecution() throws Exception {
    JavaScriptExecutor executor = new JavaScriptExecutor();
    String script = "function calculate(x) { return x * 2; } calculate(value);";

    ExecutorService threadPool = Executors.newFixedThreadPool(100);
    CountDownLatch latch = new CountDownLatch(100);
    AtomicInteger errorCount = new AtomicInteger(0);

    // 100개 스레드에서 동시 실행
    for (int i = 0; i < 100; i++) {
        final int value = i;
        threadPool.submit(() -> {
            try {
                Map<String, Object> context = new HashMap<>();
                context.put("value", value);
                executor.execute(script, context);
            } catch (Exception e) {
                errorCount.incrementAndGet();
                e.printStackTrace();
            } finally {
                latch.countDown();
            }
        });
    }

    latch.await(10, TimeUnit.SECONDS);
    threadPool.shutdown();

    System.out.println("Error rate: " + errorCount.get() + "/100");
    // 결과: Error rate: 15/100 (약 15% 에러 발생)
}
```

### 재현 조건
1. **동시성 필수**: 단일 스레드에서는 절대 재현 안 됨
2. **최소 스레드 수**: 10개 이상의 동시 요청 필요
3. **ScriptEngine 공유**: 싱글톤 또는 static 인스턴스 사용 시
4. **반복 실행**: 한 번의 테스트로는 재현 안 될 수 있음 (확률적 발생)

**재현 환경:**
- JMeter: 100 threads, 1초 ramp-up, 10번 반복
- 또는 Gatling: constantUsersPerSec(100) during(30 seconds)

## 근본 원인 분석

### 1. Nashorn의 Thread-Safety 문제
Nashorn ScriptEngine은 **thread-safe하지 않습니다**. 공식 문서에도 명시되어 있습니다:
> "A single ScriptEngine instance is not guaranteed to be thread-safe."

### 2. Internal State 공유
```java
// Nashorn 내부 구조 (간략화)
class ScriptEngineImpl {
    private Context context;         // 스레드 간 공유되는 내부 상태
    private Global globalObject;     // 전역 객체
    private ScriptContext scriptCtx; // 스크립트 컨텍스트

    public Object eval(String script) {
        // 내부 상태를 읽고 쓰는 작업
        // 멀티스레드 환경에서 경쟁 조건(race condition) 발생
        context.compile(...);  // Thread A
        context.evaluate(...); // Thread B - 동시 접근 시 충돌!
    }
}
```

### 3. 스택 트레이스 분석
```
Thread-1: engine.eval() 호출
  → Context.compile() 진입
    → PropertyMap 수정 중...

Thread-2: 동시에 engine.eval() 호출
  → Context.compile() 진입
    → 같은 PropertyMap에 접근
      → ArrayIndexOutOfBoundsException 발생!
```

### 4. Heap Memory 충돌
JavaScript 엔진이 사용하는 힙 메모리 구조가 동시에 변경되면서 발생:
- Thread A가 heap에 객체 할당 중
- Thread B가 같은 위치에 접근하여 heap corruption 발생

## 해결 방법

### 1. ThreadLocal 사용
```java
@Service
public class ThreadLocalJavaScriptExecutor {
    // 각 스레드마다 독립적인 ScriptEngine 보유
    private static final ThreadLocal<ScriptEngine> engineThreadLocal =
        ThreadLocal.withInitial(() ->
            new ScriptEngineManager().getEngineByName("nashorn")
        );

    public Object execute(String script, Map<String, Object> context)
            throws ScriptException {
        ScriptEngine engine = engineThreadLocal.get();
        Bindings bindings = engine.createBindings();
        context.forEach(bindings::put);
        return engine.eval(script, bindings);
    }

    // 주의: ThreadLocal은 메모리 누수 위험이 있으므로 cleanup 필요
    public void cleanup() {
        engineThreadLocal.remove();
    }
}
```

**장점:**
- 구현이 간단
- Thread-safety 완벽 보장

**단점:**
- Tomcat 스레드 풀 200개면 Engine도 200개 생성
- 메모리 사용량 급증 (Engine당 약 10-20MB)
- ThreadLocal cleanup 누락 시 메모리 누수

### 2. Engine Pool 구성 (최종 선택)
```java
import org.apache.commons.pool2.BasePooledObjectFactory;
import org.apache.commons.pool2.PooledObject;
import org.apache.commons.pool2.impl.DefaultPooledObject;
import org.apache.commons.pool2.impl.GenericObjectPool;
import org.apache.commons.pool2.impl.GenericObjectPoolConfig;

// ScriptEngine Factory
public class ScriptEngineFactory extends BasePooledObjectFactory<ScriptEngine> {
    @Override
    public ScriptEngine create() throws Exception {
        return new ScriptEngineManager().getEngineByName("nashorn");
    }

    @Override
    public PooledObject<ScriptEngine> wrap(ScriptEngine engine) {
        return new DefaultPooledObject<>(engine);
    }

    @Override
    public void destroyObject(PooledObject<ScriptEngine> p) throws Exception {
        // Engine cleanup
        p.getObject().getBindings(ScriptContext.ENGINE_SCOPE).clear();
    }
}

// Pool 기반 Executor
@Service
public class PooledJavaScriptExecutor {
    private final GenericObjectPool<ScriptEngine> enginePool;

    public PooledJavaScriptExecutor() {
        GenericObjectPoolConfig<ScriptEngine> config = new GenericObjectPoolConfig<>();
        config.setMaxTotal(50);              // 최대 50개
        config.setMaxIdle(20);               // 최대 유휴 20개
        config.setMinIdle(10);               // 최소 유휴 10개
        config.setMaxWaitMillis(5000);       // 최대 대기 5초
        config.setTestOnBorrow(false);       // 성능을 위해 false
        config.setTestOnReturn(false);
        config.setBlockWhenExhausted(true);  // 대기

        this.enginePool = new GenericObjectPool<>(new ScriptEngineFactory(), config);
    }

    public Object execute(String script, Map<String, Object> context)
            throws Exception {
        ScriptEngine engine = null;
        try {
            engine = enginePool.borrowObject();  // Pool에서 빌림

            Bindings bindings = engine.createBindings();
            context.forEach(bindings::put);

            return engine.eval(script, bindings);
        } finally {
            if (engine != null) {
                enginePool.returnObject(engine);  // Pool에 반환
            }
        }
    }

    @PreDestroy
    public void destroy() {
        enginePool.close();
    }

    // 모니터링용
    public String getPoolStats() {
        return String.format(
            "Active: %d, Idle: %d, Waiters: %d",
            enginePool.getNumActive(),
            enginePool.getNumIdle(),
            enginePool.getNumWaiters()
        );
    }
}
```

**장점:**
- 메모리 효율적 (최대 50개로 제한)
- Thread-safety 보장
- 동적으로 Pool 크기 조절 가능
- 모니터링 가능

**단점:**
- 구현 복잡도 증가
- 추가 라이브러리 의존성

### 3. 동기화 처리 (비추천)
```java
@Service
public class SynchronizedJavaScriptExecutor {
    private static final ScriptEngine engine =
        new ScriptEngineManager().getEngineByName("nashorn");

    public synchronized Object execute(String script, Map<String, Object> context)
            throws ScriptException {
        // synchronized로 동시 접근 방지
        Bindings bindings = engine.createBindings();
        context.forEach(bindings::put);
        return engine.eval(script, bindings);
    }
}
```

**장점:**
- 구현이 매우 간단
- 메모리 효율적 (Engine 1개만 사용)

**단점:**
- **성능 저하 심각**: 모든 요청이 직렬화됨
- 병목 지점(bottleneck) 발생
- 동시 처리 불가능

## 검증 방법

### 1. 부하 테스트
```bash
# JMeter 테스트 시나리오
Thread Group:
  - Threads: 200
  - Ramp-up: 10초
  - Loop: 100회
  - Duration: 5분

Result:
  - ThreadLocal 방식: 0% 에러율, 평균 응답 120ms
  - Pool 방식: 0% 에러율, 평균 응답 125ms
  - Synchronized 방식: 0% 에러율, 평균 응답 450ms (너무 느림)
```

### 2. 메모리 사용량 측정
```java
// JVM 옵션
-Xms1024m -Xmx2048m
-XX:+PrintGCDetails

// 결과 (부하 테스트 중 최대 메모리)
- ThreadLocal 방식: 1.8GB (200개 Engine)
- Pool 방식: 1.2GB (50개 Engine)
- Synchronized 방식: 800MB (1개 Engine)
```

### 3. 안정성 테스트
```java
// 장시간 부하 테스트 (Soak Test)
// 8시간 동안 지속적으로 100 TPS 유지

Results after 8 hours:
- ThreadLocal: 0 errors, Memory 안정적
- Pool: 0 errors, Memory 안정적
- Synchronized: 0 errors, 하지만 응답 시간 계속 증가 (병목)
```

### 4. 코드 레벨 검증
```java
@Test
public void testThreadSafety() throws Exception {
    PooledJavaScriptExecutor executor = new PooledJavaScriptExecutor();

    int threadCount = 500;
    int iterations = 100;

    ExecutorService pool = Executors.newFixedThreadPool(threadCount);
    CountDownLatch latch = new CountDownLatch(threadCount * iterations);
    AtomicInteger errorCount = new AtomicInteger(0);

    for (int i = 0; i < threadCount * iterations; i++) {
        final int value = i;
        pool.submit(() -> {
            try {
                String script = "value * 2";
                Map<String, Object> context = Map.of("value", value);
                Object result = executor.execute(script, context);

                // 결과 검증
                if (!result.equals(value * 2)) {
                    errorCount.incrementAndGet();
                }
            } catch (Exception e) {
                errorCount.incrementAndGet();
            } finally {
                latch.countDown();
            }
        });
    }

    latch.await(60, TimeUnit.SECONDS);
    pool.shutdown();

    // 검증: 에러가 전혀 없어야 함
    assertEquals(0, errorCount.get());
    System.out.println("Pool stats: " + executor.getPoolStats());
}
```

## 참고 자료

- Nashorn Official Documentation: https://docs.oracle.com/en/java/javase/11/nashorn/
- JSR 223: Scripting for the Java Platform
- Apache Commons Pool Documentation: https://commons.apache.org/proper/commons-pool/
- Oracle: Multithreading and Scripting Engines: https://docs.oracle.com/javase/8/docs/technotes/guides/scripting/prog_guide/api.html#multithreading
- Effective Java 3rd Edition - Item 83: Use lazy initialization judiciously
- GraalVM JavaScript (Nashorn 대체): https://www.graalvm.org/javascript/
