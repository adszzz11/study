# Tempo를 통한 분산 추적 구현 경험은?

## 답변

[여기에 답변 작성]

## 핵심 키워드

- Tempo
- Distributed Tracing
- OpenTelemetry
- Jaeger
- Trace ID
- Span
- Sampling
- Trace Context Propagation

## Tempo 아키텍처

### 주요 컴포넌트
-

### 저장 구조
-

## OpenTelemetry 통합

### Instrumentation
-

### Collector
-

## Trace Context Propagation

-

## Sampling 전략

### Head-based Sampling
-

### Tail-based Sampling
-

## Grafana 통합

### Trace to Logs
-

### Trace to Metrics
-

## 설정 예시

### Tempo Configuration
```yaml
server:
  http_listen_port: 3200

distributor:
  receivers:
    otlp:
      protocols:
        http:
        grpc:
    jaeger:
      protocols:
        thrift_http:
        grpc:

ingester:
  trace_idle_period: 10s
  max_block_bytes: 1_000_000
  max_block_duration: 5m

storage:
  trace:
    backend: s3
    s3:
      bucket: tempo-traces
      endpoint: s3.amazonaws.com
      access_key: ${S3_ACCESS_KEY}
      secret_key: ${S3_SECRET_KEY}
    wal:
      path: /var/tempo/wal
    pool:
      max_workers: 100
      queue_depth: 10000

compactor:
  compaction:
    block_retention: 720h  # 30 days

metrics_generator:
  registry:
    external_labels:
      source: tempo
  storage:
    path: /var/tempo/generator/wal
    remote_write:
      - url: http://prometheus:9090/api/v1/write
```

### OpenTelemetry Collector
```yaml
receivers:
  otlp:
    protocols:
      grpc:
        endpoint: 0.0.0.0:4317
      http:
        endpoint: 0.0.0.0:4318

processors:
  batch:
    timeout: 10s
    send_batch_size: 1024

  # Tail-based Sampling
  tail_sampling:
    decision_wait: 10s
    num_traces: 100
    policies:
      - name: errors
        type: status_code
        status_code: {status_codes: [ERROR]}
      - name: slow
        type: latency
        latency: {threshold_ms: 1000}
      - name: random
        type: probabilistic
        probabilistic: {sampling_percentage: 10}

exporters:
  otlp:
    endpoint: tempo:4317
    tls:
      insecure: true

  prometheus:
    endpoint: "0.0.0.0:8889"

service:
  pipelines:
    traces:
      receivers: [otlp]
      processors: [batch, tail_sampling]
      exporters: [otlp]
    metrics:
      receivers: [otlp]
      processors: [batch]
      exporters: [prometheus]
```

### Spring Boot Application (OpenTelemetry)
```yaml
# application.yml
management:
  tracing:
    enabled: true
    sampling:
      probability: 0.1  # 10% sampling

  otlp:
    tracing:
      endpoint: http://otel-collector:4318/v1/traces

# 또는 환경 변수로 설정
# OTEL_SERVICE_NAME=myapp
# OTEL_EXPORTER_OTLP_ENDPOINT=http://otel-collector:4318
# OTEL_TRACES_SAMPLER=parentbased_traceidratio
# OTEL_TRACES_SAMPLER_ARG=0.1
```

```java
// Manual Instrumentation
@Service
public class MyService {
    private final Tracer tracer;

    public MyService(Tracer tracer) {
        this.tracer = tracer;
    }

    public void doWork() {
        Span span = tracer.spanBuilder("custom-operation")
            .setSpanKind(SpanKind.INTERNAL)
            .startSpan();

        try (Scope scope = span.makeCurrent()) {
            span.setAttribute("user.id", "123");
            span.addEvent("Processing started");

            // 작업 수행
            processData();

            span.addEvent("Processing completed");
        } catch (Exception e) {
            span.recordException(e);
            span.setStatus(StatusCode.ERROR);
            throw e;
        } finally {
            span.end();
        }
    }
}
```

### Grafana Data Source 설정
```yaml
apiVersion: 1

datasources:
  - name: Tempo
    type: tempo
    access: proxy
    url: http://tempo:3200
    jsonData:
      tracesToLogs:
        datasourceUid: loki
        tags: ['job', 'instance', 'pod', 'namespace']
        mappedTags: [{ key: 'service.name', value: 'app' }]
        filterByTraceID: true
        filterBySpanID: false
      tracesToMetrics:
        datasourceUid: prometheus
        tags: [{ key: 'service.name', value: 'app' }]
        queries:
          - name: 'Sample query'
            query: 'sum(rate(tempo_spanmetrics_latency_bucket{$__tags}[5m]))'
      serviceMap:
        datasourceUid: prometheus
      search:
        hide: false
      nodeGraph:
        enabled: true
      lokiSearch:
        datasourceUid: loki
```

### TraceQL 쿼리 예시
```traceql
# 특정 서비스의 느린 요청
{service.name="myapp" && duration > 1s}

# 에러가 발생한 트레이스
{status=error}

# 특정 HTTP 상태 코드
{http.status_code=500}

# 복합 조건
{service.name="myapp" && http.method="POST" && duration > 500ms}

# Span 속성 검색
{span.http.url=~".*api/users.*"}
```

### Docker Compose 예시
```yaml
version: '3.8'

services:
  tempo:
    image: grafana/tempo:latest
    command: ["-config.file=/etc/tempo.yaml"]
    volumes:
      - ./tempo.yaml:/etc/tempo.yaml
      - tempo-data:/var/tempo
    ports:
      - "3200:3200"   # Tempo HTTP
      - "4317:4317"   # OTLP gRPC
      - "4318:4318"   # OTLP HTTP

  otel-collector:
    image: otel/opentelemetry-collector-contrib:latest
    command: ["--config=/etc/otel-collector.yaml"]
    volumes:
      - ./otel-collector.yaml:/etc/otel-collector.yaml
    ports:
      - "4317:4317"   # OTLP gRPC
      - "4318:4318"   # OTLP HTTP
    depends_on:
      - tempo

  grafana:
    image: grafana/grafana:latest
    ports:
      - "3000:3000"
    volumes:
      - ./grafana-datasources.yaml:/etc/grafana/provisioning/datasources/datasources.yaml
    depends_on:
      - tempo

volumes:
  tempo-data:
```

## 참고 자료

-
