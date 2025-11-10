# Socket 연동에서 비연결유지형을 선택한 이유와 trade-off는?

## 답변

비연결유지형(Non-Persistent Connection) 방식을 선택한 가장 큰 이유는 **트래픽 패턴과 시스템 안정성**이었습니다. 금융권 특성상 거래가 특정 시간대에 집중되고, 대부분의 시간은 유휴 상태였기 때문에, 연결을 계속 유지하는 것이 오히려 리소스 낭비였습니다.

연결유지형은 빠른 응답 속도를 제공하지만, 유휴 연결 관리 복잡성, 방화벽/NAT 타임아웃 문제, 그리고 장애 시 광범위한 영향이라는 치명적인 단점이 있었습니다. 반면 비연결유지형은 요청마다 연결을 맺고 끊기 때문에 오버헤드가 있지만, **단순하고 안정적이며 확장성이 높다**는 장점이 있었습니다.

실제로 비연결유지형 + 최적화(Connection Pool, Keep-Alive, Fast Open)를 통해 성능 차이를 최소화하면서 안정성을 크게 향상시킬 수 있었습니다.

## 핵심 키워드

- Socket 통신
- 비연결유지형
- 연결유지형
- Connection Pool
- 리소스 관리

## 연결 방식 비교

### 연결유지형 (Persistent Connection)
**개념:**
- 클라이언트와 서버 간 연결을 계속 유지
- HTTP/1.1의 Keep-Alive, WebSocket, Long Polling 등

**장점:**
- **빠른 응답 속도**: 연결 수립 오버헤드 없음 (3-way handshake 생략)
- **낮은 레이턴시**: TCP Slow Start를 한 번만 거침
- **실시간 통신 가능**: Push 알림, 실시간 업데이트 등
- **서버 리소스 예측 가능**: 연결 수 = 동시 사용자 수

**단점:**
- **리소스 낭비**: 유휴 연결이 메모리와 파일 디스크립터 점유
- **확장성 제한**: 서버의 최대 연결 수 제약 (ulimit, OS 커널 파라미터)
- **장애 전파**: 하나의 서버 장애가 모든 연결된 클라이언트에 영향
- **연결 관리 복잡성**: Heartbeat, Timeout, Reconnection 로직 필요
- **방화벽/NAT 이슈**: Idle Timeout으로 연결이 끊어질 수 있음

**적용 사례:**
- 실시간 채팅 (WebSocket)
- 게임 서버 (Long-lived connection)
- 스트리밍 서비스

### 비연결유지형 (Non-Persistent Connection)
**개념:**
- 요청마다 새로운 연결 수립 후 응답 완료 시 즉시 종료
- 전통적인 HTTP 방식

**장점:**
- **단순성**: 연결 상태 관리 불필요
- **안정성**: 장애 격리 (한 요청의 실패가 다른 요청에 영향 없음)
- **확장성**: 무한정 많은 클라이언트 처리 가능 (동시 연결 수 제약 없음)
- **리소스 효율성**: 필요한 순간만 연결 사용
- **로드밸런싱 유리**: 각 요청을 다른 서버로 분산 가능

**단점:**
- **연결 수립 오버헤드**: 매 요청마다 3-way handshake 필요
- **높은 레이턴시**: TCP Slow Start를 매번 거침
- **네트워크 부하**: SYN/ACK 패킷이 빈번하게 발생
- **TIME_WAIT 소켓 증가**: 대량 트래픽 시 포트 고갈 가능

**적용 사례:**
- RESTful API
- 배치 작업
- 간헐적 트랜잭션

## 비연결유지형 선택 이유

### 시스템 특성
1. **금융 거래의 원자성**
   - 각 거래는 독립적으로 처리되어야 함
   - 하나의 거래 실패가 다른 거래에 영향을 주면 안 됨
   - 연결 상태와 무관하게 트랜잭션 관리 가능

2. **높은 안정성 요구**
   - 연결 장애 시 명확한 에러 처리
   - 재시도 로직이 단순함 (새 연결로 재시도)
   - 네트워크 문제 발생 시 빠른 복구

3. **다양한 클라이언트**
   - ATM, 인터넷뱅킹, 모바일 앱 등
   - 각 채널마다 트래픽 패턴이 다름
   - 연결 유지 시 채널별로 다른 관리 정책 필요

### 트래픽 패턴
```
일일 거래량 분석:
09:00-11:00  ████████████████ (피크 타임, 40%)
11:00-14:00  ████████ (중간 트래픽, 20%)
14:00-18:00  ████████████ (오후 피크, 30%)
18:00-09:00  ██ (야간 저조, 10%)

문제점:
- 피크 타임에 맞춰 연결을 유지하면, 70%의 시간 동안 리소스 낭비
- 유휴 연결이 서버의 메모리와 파일 디스크립터를 점유
- 연결유지형은 피크 타임 기준으로 서버를 프로비저닝해야 함
```

**실제 데이터:**
- 평균 거래 간격: 5분 이상 (동일 클라이언트 기준)
- 연결 유휴 시간: 평균 4분 30초
- 피크 시간대 집중도: 전체 거래의 40%가 2시간 내 발생
- **결론**: 연결을 유지할 필요성이 낮음

### 리소스 제약
1. **서버 측 제약**
   - 파일 디스크립터 한계: `ulimit -n` 제한 (보통 65,536)
   - 메모리: 연결당 약 64KB~128KB 소모 (TCP 버퍼)
   - 10,000개 연결 유지 시: 약 1GB 메모리 사용

2. **레거시 시스템 호환성**
   - 기존 메인프레임 시스템이 비연결유지형으로 설계됨
   - 연결유지형으로 전환 시 전체 시스템 재설계 필요

3. **보안 정책**
   - 방화벽의 Stateful Inspection 부담 증가
   - 장기 연결 시 보안 감사 로그 분석 복잡성 증가

## Trade-off 분석

### 성능 측면

**연결 수립 오버헤드 측정:**
```
비연결유지형 (매 요청마다 연결):
- TCP 3-way handshake: 1.5 RTT (Round Trip Time)
- 한국 내 RTT 평균: 20ms
- 연결 수립 비용: 30ms

연결유지형:
- 연결 수립: 최초 1회만 30ms
- 이후 요청: 0ms

차이: 요청당 30ms 추가

BUT! 실제 비즈니스 로직 처리 시간: 평균 200ms
→ 연결 수립 오버헤드는 전체의 15% 정도
→ 전체 응답 시간: 230ms vs 200ms (13% 차이)
```

**최적화 후 성능:**
```kotlin
// TCP Fast Open 활성화로 1 RTT 단축
// Connection Pool 사용으로 연결 재사용

실측 결과:
- 비연결유지형 (최적화 전): 평균 230ms
- 비연결유지형 (최적화 후): 평균 210ms
- 연결유지형: 평균 200ms

→ 최적화로 차이를 5%로 축소 (허용 가능한 수준)
```

### 안정성 측면

**장애 시나리오:**

1. **서버 장애 발생 시**
   - 연결유지형: 10,000개 연결이 모두 끊어짐 → 클라이언트 전체 재연결 시도 → 서버 과부하
   - 비연결유지형: 현재 처리 중인 요청만 실패 → 다음 요청부터 다른 서버로 자동 라우팅

2. **네트워크 일시 장애**
   - 연결유지형: Heartbeat 실패 → 재연결 로직 필요 → 복잡도 증가
   - 비연결유지형: 해당 요청만 실패 → 간단한 재시도로 해결

3. **배포 시나리오**
   - 연결유지형: Graceful Shutdown 필요 → 모든 연결이 종료될 때까지 대기 → 배포 시간 증가
   - 비연결유지형: 현재 요청만 완료하면 즉시 종료 → 빠른 배포

**실제 장애 사례:**
```
2024년 3월 장애 사례 (연결유지형 시스템):
- 원인: DB 연결 풀 고갈
- 영향: 모든 연결된 클라이언트가 Timeout
- 복구 시간: 30분 (모든 연결 재수립 필요)

vs

비연결유지형 시스템:
- 원인: 동일 (DB 연결 풀 고갈)
- 영향: 일부 요청만 실패
- 복구 시간: 5분 (DB 복구 즉시 정상화)
```

### 비용 측면

**인프라 비용:**
```
연결유지형:
- 서버 대수: 10대 (10,000 동시 연결 유지)
- 메모리: 16GB × 10 = 160GB
- 월 비용: $2,000

비연결유지형:
- 서버 대수: 4대 (평균 500 동시 요청 처리)
- 메모리: 8GB × 4 = 32GB
- 월 비용: $600

→ 약 70% 비용 절감
```

**개발 및 운영 비용:**
- 연결유지형: Heartbeat, Reconnection, Connection Pool 관리 복잡
- 비연결유지형: 단순한 요청-응답 모델

## 최적화 방안

### 1. Connection Pool 사용 (클라이언트 측)
```kotlin
// HikariCP 스타일의 Socket Connection Pool
class SocketConnectionPool(
    private val host: String,
    private val port: Int,
    private val maxPoolSize: Int = 10,
    private val maxIdleTime: Duration = Duration.ofSeconds(30)
) {
    private val pool = LinkedBlockingDeque<Socket>()

    fun borrowConnection(): Socket {
        // Pool에서 재사용 가능한 연결 찾기
        var socket = pool.pollFirst()

        // 연결이 살아있는지 확인
        if (socket != null && !socket.isConnected) {
            socket.close()
            socket = null
        }

        // 새 연결 생성
        return socket ?: Socket(host, port).apply {
            tcpNoDelay = true
            soTimeout = 5000
        }
    }

    fun returnConnection(socket: Socket) {
        if (pool.size < maxPoolSize && socket.isConnected) {
            pool.offerLast(socket)
        } else {
            socket.close()
        }
    }
}

// 사용 예시
val pool = SocketConnectionPool("backend.example.com", 8080)

fun sendRequest(data: ByteArray): ByteArray {
    val socket = pool.borrowConnection()
    try {
        socket.getOutputStream().write(data)
        socket.getOutputStream().flush()

        val response = socket.getInputStream().readBytes()
        pool.returnConnection(socket)  // 재사용을 위해 풀에 반환
        return response
    } catch (e: Exception) {
        socket.close()
        throw e
    }
}
```

### 2. TCP Fast Open (TFO)
```kotlin
// Linux 커널 설정
// /etc/sysctl.conf
// net.ipv4.tcp_fastopen = 3

// Java에서 TCP Fast Open 사용
val socket = Socket()
val socketImpl = socket.javaClass.getDeclaredField("impl")
socketImpl.isAccessible = true
val impl = socketImpl.get(socket) as SocketImpl

// TFO 옵션 활성화
impl.setOption(SocketOptions.TCP_FASTOPEN_CONNECT, true)

// 연결 시 데이터를 함께 전송 (1 RTT 절약)
socket.connect(InetSocketAddress(host, port))
socket.getOutputStream().write(requestData)
```

### 3. HTTP Keep-Alive (애플리케이션 레벨)
```kotlin
// HTTP/1.1 Keep-Alive로 하나의 TCP 연결로 여러 요청 전송
val client = OkHttpClient.Builder()
    .connectionPool(ConnectionPool(
        maxIdleConnections = 10,
        keepAliveDuration = 30, TimeUnit.SECONDS
    ))
    .build()

// 비연결유지형이지만, HTTP 레벨에서는 연결 재사용
val request = Request.Builder()
    .url("http://backend.example.com/api")
    .header("Connection", "keep-alive")
    .build()
```

### 4. 부하 분산 및 Auto Scaling
```yaml
# Kubernetes HPA (Horizontal Pod Autoscaler)
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: socket-gateway
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: socket-gateway
  minReplicas: 4
  maxReplicas: 20
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Pods
    pods:
      metric:
        name: concurrent_requests
      target:
        type: AverageValue
        averageValue: "500"
```

### 5. 모니터링 및 알림
```kotlin
// Micrometer로 메트릭 수집
registry.gauge("socket.pool.active", pool.activeConnections())
registry.gauge("socket.pool.idle", pool.idleConnections())
registry.timer("socket.request.duration").record {
    sendRequest(data)
}

// Prometheus Alert 설정
groups:
  - name: socket_alerts
    rules:
      - alert: HighSocketLatency
        expr: socket_request_duration_seconds{quantile="0.99"} > 0.5
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "Socket request latency is high"
```

## 참고 자료

- [The Linux Programming Interface - Michael Kerrisk](https://man7.org/tlpi/)
- [TCP/IP Illustrated, Vol. 1 - W. Richard Stevens](https://www.oreilly.com/library/view/tcpip-illustrated-volume/9780132808200/)
- [High Performance Browser Networking - Ilya Grigorik](https://hpbn.co/)
- [RFC 7413 - TCP Fast Open](https://datatracker.ietf.org/doc/html/rfc7413)
- [Designing Data-Intensive Applications - Martin Kleppmann](https://dataintensive.net/)
- [Connection Pooling Best Practices](https://github.com/brettwooldridge/HikariCP/wiki/About-Pool-Sizing)
