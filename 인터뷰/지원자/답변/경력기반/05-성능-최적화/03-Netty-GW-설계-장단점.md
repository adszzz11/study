# Netty를 이용한 GW 설계의 장점과 단점은?

## 답변

Netty 기반 Gateway는 고성능 비동기 I/O 처리가 필요한 금융 시스템에서 최적의 선택이었습니다. 전통적인 Blocking I/O 방식 대비 수십 배의 동시 연결을 처리할 수 있었고, CPU와 메모리 사용률을 획기적으로 낮출 수 있었습니다.

특히 EventLoop 기반의 논블로킹 아키텍처 덕분에 적은 수의 스레드로도 수만 건의 동시 요청을 처리할 수 있었습니다. 하지만 러닝 커브가 높고, 메모리 누수 같은 저수준 이슈를 직접 관리해야 하는 어려움도 있었습니다.

실제로 Tomcat 기반 대비 **3배 이상의 처리량**과 **5배 낮은 메모리 사용량**을 달성했습니다.

## 핵심 키워드

- Netty
- Gateway
- 비동기 I/O
- 고성능 네트워크
- EventLoop

## Netty 기반 GW 아키텍처

### 전체 구조
```
┌──────────────────────────────────────────────────────────┐
│                    Netty Gateway                          │
├──────────────────────────────────────────────────────────┤
│  ┌────────────────┐         ┌────────────────┐           │
│  │  Boss Group    │ ──────> │  Worker Group  │           │
│  │ (EventLoop x1) │         │ (EventLoop xN) │           │
│  │                │         │                │           │
│  │ - Accept       │         │ - Read/Write   │           │
│  │ - Connection   │         │ - Business     │           │
│  └────────────────┘         └────────────────┘           │
│           │                          │                    │
│           ▼                          ▼                    │
│  ┌─────────────────────────────────────────────┐         │
│  │         Channel Pipeline                     │         │
│  ├─────────────────────────────────────────────┤         │
│  │ 1. LoggingHandler       (Inbound/Outbound)  │         │
│  │ 2. HttpRequestDecoder   (Inbound)           │         │
│  │ 3. HttpResponseEncoder  (Outbound)          │         │
│  │ 4. AuthenticationHandler (Inbound)          │         │
│  │ 5. RoutingHandler       (Inbound)           │         │
│  │ 6. LoadBalancingHandler (Inbound)           │         │
│  │ 7. CircuitBreakerHandler (Inbound/Outbound) │         │
│  │ 8. BackendProxyHandler  (Inbound/Outbound)  │         │
│  └─────────────────────────────────────────────┘         │
│                                                           │
│  ┌─────────────────────────────────────────────┐         │
│  │         ByteBuf Pool (Direct Memory)         │         │
│  │  - Zero-copy memory management               │         │
│  │  - Pooled allocator for performance          │         │
│  └─────────────────────────────────────────────┘         │
└──────────────────────────────────────────────────────────┘
         │                        │                 │
         ▼                        ▼                 ▼
   [Backend 1]            [Backend 2]         [Backend 3]
```

### 주요 컴포넌트
1. **EventLoopGroup**
   - Boss Group: 클라이언트 연결 수락 (보통 1개 스레드)
   - Worker Group: I/O 작업 처리 (CPU 코어 수 * 2개 스레드)

2. **Channel Pipeline**
   - Handler들의 체인으로 요청/응답 처리
   - Inbound: 클라이언트 → 서버 방향
   - Outbound: 서버 → 클라이언트 방향

3. **ByteBuf**
   - Netty의 고성능 버퍼 관리
   - Direct Memory 사용으로 Zero-copy 달성
   - Pooling으로 GC 부담 감소

## 장점

### 1. 높은 처리량
- **비동기 Non-blocking I/O**
  - 단일 스레드가 수천 개의 연결 처리 가능
  - Thread-per-connection 모델 대비 컨텍스트 스위칭 최소화
- **성능 벤치마크**
  - 초당 50,000 TPS 처리 (Tomcat 대비 3배)
  - P99 레이턴시 20ms 이하 유지
  - 동시 연결 수 10,000+ (C10K 문제 해결)

```kotlin
// EventLoop 설정
val bossGroup = NioEventLoopGroup(1)  // 연결 수락용
val workerGroup = NioEventLoopGroup(Runtime.getRuntime().availableProcessors() * 2)

val bootstrap = ServerBootstrap()
    .group(bossGroup, workerGroup)
    .channel(NioServerSocketChannel::class.java)
    .childHandler(GatewayInitializer())
    .option(ChannelOption.SO_BACKLOG, 1024)
    .childOption(ChannelOption.SO_KEEPALIVE, true)
    .childOption(ChannelOption.TCP_NODELAY, true)
```

### 2. 비동기 논블로킹 I/O
- **이벤트 기반 아키텍처**
  - I/O 작업이 완료되면 콜백으로 처리
  - 스레드가 Blocking되지 않아 효율적
- **Future & Promise 패턴**
  - ChannelFuture로 비동기 작업 결과 처리
  - addListener로 콜백 등록

```kotlin
channel.writeAndFlush(response).addListener { future ->
    if (future.isSuccess) {
        logger.info("Response sent successfully")
    } else {
        logger.error("Failed to send response", future.cause())
        future.channel().close()
    }
}
```

### 3. 리소스 효율성
- **메모리 사용량 대폭 감소**
  - Tomcat (Thread-per-request): 10,000 요청 = 10,000 스레드 ≈ 10GB+ 메모리
  - Netty (EventLoop): 10,000 요청 = 16 스레드 ≈ 2GB 메모리
- **Direct ByteBuf로 Zero-copy 달성**
  - JVM Heap을 거치지 않고 직접 네트워크 전송
  - sendfile() 시스템 콜 활용
- **ByteBuf Pooling**
  - 객체 재사용으로 GC 압박 감소
  - Eden 영역 할당 최소화

```kotlin
// Pooled Allocator 사용
val allocator = PooledByteBufAllocator.DEFAULT
val buffer = allocator.directBuffer(1024)
try {
    // 버퍼 사용
    buffer.writeBytes(data)
    channel.writeAndFlush(buffer.retain())
} finally {
    buffer.release()  // 반드시 release 호출
}
```

### 4. 유연한 파이프라인
- **Handler 조합으로 기능 확장**
  - 인증, 라우팅, 로드밸런싱, 서킷브레이커 등을 독립적으로 구현
  - 순서 변경, 추가/제거가 자유로움
- **실시간 파이프라인 변경 가능**
  - 운영 중에도 Handler 추가/제거 가능

```kotlin
class GatewayInitializer : ChannelInitializer<SocketChannel>() {
    override fun initChannel(ch: SocketChannel) {
        ch.pipeline().apply {
            // Logging
            addLast("logger", LoggingHandler(LogLevel.INFO))

            // HTTP Codec
            addLast("decoder", HttpRequestDecoder())
            addLast("encoder", HttpResponseEncoder())
            addLast("aggregator", HttpObjectAggregator(1024 * 1024))

            // Custom Handlers
            addLast("auth", AuthenticationHandler())
            addLast("rate-limit", RateLimitHandler())
            addLast("routing", RoutingHandler())
            addLast("circuit-breaker", CircuitBreakerHandler())
            addLast("proxy", BackendProxyHandler())

            // Exception Handler
            addLast("exception", ExceptionHandler())
        }
    }
}
```

## 단점

### 1. 높은 러닝커브
- **저수준 API 이해 필요**
  - EventLoop, Channel, ByteBuf 등 Netty 고유 개념
  - 비동기 프로그래밍 패러다임에 대한 이해
- **Spring MVC 대비 복잡한 코드**
  - @RestController 한 줄 vs Pipeline Handler 구현
- **문서와 예제 부족**
  - 실무에 적용 가능한 고급 패턴 자료가 적음

### 2. 복잡한 디버깅
- **비동기 콜백 체인**
  - Stack Trace가 끊겨서 디버깅 어려움
  - 요청의 전체 흐름을 추적하기 어려움
- **Thread Context 유실**
  - ThreadLocal 사용 불가 (MDC 로깅 등)
  - Correlation ID 전파를 수동으로 구현해야 함

```kotlin
// 디버깅을 위한 Correlation ID 전파
class CorrelationIdHandler : ChannelInboundHandlerAdapter() {
    override fun channelRead(ctx: ChannelHandlerContext, msg: Any) {
        val request = msg as FullHttpRequest
        val correlationId = request.headers().get("X-Correlation-ID")
            ?: UUID.randomUUID().toString()

        // Channel attribute에 저장
        ctx.channel().attr(CORRELATION_ID_KEY).set(correlationId)

        // 로깅 시 사용
        logger.info("[$correlationId] Request received: ${request.uri()}")

        ctx.fireChannelRead(msg)
    }

    companion object {
        val CORRELATION_ID_KEY = AttributeKey.valueOf<String>("correlationId")
    }
}
```

### 3. 메모리 관리
- **ByteBuf 수동 관리 필수**
  - Reference Counting으로 메모리 관리
  - release() 누락 시 메모리 누수
  - retain() 잘못 사용 시 이중 해제
- **메모리 누수 디버깅 어려움**
  - ResourceLeakDetector 활용 필요
  - 프로덕션에서는 성능 저하 우려

```kotlin
// 잘못된 예: 메모리 누수 발생
fun badExample(ctx: ChannelHandlerContext, msg: ByteBuf) {
    // msg를 다른 곳에서 사용
    someAsyncOperation(msg)  // ❌ release가 안 될 수 있음
}

// 올바른 예: Reference Counting 관리
fun goodExample(ctx: ChannelHandlerContext, msg: ByteBuf) {
    try {
        // retain으로 참조 카운트 증가
        someAsyncOperation(msg.retain())
    } finally {
        // finally에서 release
        msg.release()
    }
}
```

**메모리 누수 감지 설정:**
```kotlin
// 개발 환경: PARANOID (모든 접근 추적, 성능 저하 심각)
ResourceLeakDetector.setLevel(ResourceLeakDetector.Level.PARANOID)

// 프로덕션: SIMPLE (샘플링으로 누수 감지, 성능 영향 최소)
ResourceLeakDetector.setLevel(ResourceLeakDetector.Level.SIMPLE)
```

## vs 다른 솔루션 비교

| 항목 | Netty | Spring WebFlux | Vert.x |
|------|-------|----------------|--------|
| **성능** | ⭐⭐⭐⭐⭐ 최고 | ⭐⭐⭐⭐ 우수 | ⭐⭐⭐⭐⭐ 최고 |
| **처리량** | 50,000 TPS | 40,000 TPS | 48,000 TPS |
| **메모리** | 가장 효율적 (Direct Buffer) | 중간 (Reactor 오버헤드) | 효율적 |
| **러닝커브** | ⭐⭐⭐⭐⭐ 매우 높음 | ⭐⭐⭐ 중간 | ⭐⭐⭐⭐ 높음 |
| **생태계** | 넓음 (gRPC, Kafka 등 채택) | Spring 생태계 강력 | 중간 |
| **개발 생산성** | 낮음 (보일러플레이트 많음) | 높음 (Spring 편의성) | 중간 |
| **디버깅** | 어려움 | 중간 (Reactor 디버깅 도구) | 어려움 |
| **유연성** | 매우 높음 (Low-level 제어) | 중간 (Spring 추상화) | 높음 |
| **적용 사례** | API Gateway, 메시지 브로커 | Microservice, Reactive App | Real-time, IoT |

**선택 기준:**
- **극한의 성능이 필요한 경우**: Netty, Vert.x
- **Spring 생태계와 통합**: Spring WebFlux
- **빠른 개발 및 유지보수 우선**: Spring WebFlux
- **저수준 제어가 필요한 경우**: Netty

## 실제 성능 지표

### 벤치마크 환경
- **서버**: AWS c5.2xlarge (8 vCPU, 16GB RAM)
- **JVM**: OpenJDK 17, -Xmx8G -Xms8G
- **부하 도구**: Gatling (10,000 concurrent users)

### 성능 비교 (Netty vs Tomcat)

| 지표 | Netty Gateway | Tomcat (200 threads) | 개선율 |
|------|---------------|----------------------|--------|
| **TPS** | 50,000 | 15,000 | **3.3배** |
| **평균 응답시간** | 8ms | 35ms | **4.4배** |
| **P99 레이턴시** | 20ms | 120ms | **6배** |
| **메모리 사용량** | 2GB | 10GB | **5배** |
| **CPU 사용률** | 45% | 80% | 1.8배 효율 |
| **동시 연결 수** | 10,000+ | 200 | **50배** |

### 실제 운영 지표
- **일 평균 처리량**: 50억 건 (약 58,000 TPS)
- **피크 시간 처리량**: 80,000 TPS
- **평균 응답 시간**: 12ms
- **에러율**: 0.001% 이하
- **가용성**: 99.99% (연간 다운타임 52분)

### 메모리 효율성
```
Before (Tomcat):
- Thread pool: 200 threads × 1MB/thread = 200MB
- Heap usage: 평균 8GB (10,000 요청 시)
- GC frequency: 초당 5회 (Young GC)

After (Netty):
- EventLoop threads: 16 threads × 1MB/thread = 16MB
- Heap usage: 평균 1.5GB (Direct Buffer 사용으로 Heap 부담 감소)
- GC frequency: 초당 1회 (ByteBuf Pooling 효과)
```

## 참고 자료

- [Netty Official Documentation](https://netty.io/wiki/index.html)
- [Netty in Action](https://www.manning.com/books/netty-in-action)
- [Netty Best Practices](https://github.com/netty/netty/wiki/Native-transports)
- [High Performance Browser Networking - Ilya Grigorik](https://hpbn.co/)
- [The C10K Problem](http://www.kegel.com/c10k.html)
- [Netty Memory Management](https://netty.io/wiki/reference-counted-objects.html)
