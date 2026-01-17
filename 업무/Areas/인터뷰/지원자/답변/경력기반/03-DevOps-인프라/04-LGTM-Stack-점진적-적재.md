# LGTM Stack 도입 시 리소스 부족 문제를 '점진적 적재 방식'으로 해결했다고 했는데, 구체적인 전략은?

## 답변

기존에 사용하던 ELK(Elasticsearch, Logstash, Kibana) 스택은 강력하지만 **리소스 소비가 매우 높았습니다**. 특히 Elasticsearch가 메모리를 대량으로 사용하고, 인덱싱 과정에서 CPU와 디스크 I/O가 급증하여 온프레미스 환경에서는 운영 부담이 컸습니다.

LGTM Stack(Loki, Grafana, Tempo, Mimir)은 Grafana Labs에서 제공하는 클라우드 네이티브 관측성 스택으로, ELK 대비 **훨씬 적은 리소스로 유사한 기능을 제공**합니다. 하지만 모든 컴포넌트를 한 번에 도입하면 러닝 커브와 설정 복잡도가 높아지므로, **점진적 적재(Incremental Loading) 방식**으로 단계별로 전환했습니다.

핵심 전략은 **중요도와 리소스 효율성이 높은 순서대로 도입**하되, 기존 시스템과 병행 운영하며 안정성을 검증한 후 단계적으로 전환하는 것이었습니다.

## 핵심 키워드

- LGTM Stack (Loki, Grafana, Tempo, Mimir)
- 리소스 최적화
- 점진적 도입
- 비용 효율
- 데이터 보관 정책

## LGTM Stack 구성

### L - Loki (로그)
- **역할**: 로그 수집 및 저장 (Elasticsearch 대체)
- **특징**:
  - 로그를 인덱싱하지 않고 레이블(Label) 기반으로 저장하여 **스토리지 비용 90% 절감**
  - Prometheus와 동일한 레이블 쿼리 언어(LogQL) 사용
  - S3/MinIO 같은 오브젝트 스토리지 백엔드 지원
- **구성 요소**:
  - **Promtail**: 로그 수집 에이전트 (Filebeat 대체)
  - **Loki**: 로그 저장 및 쿼리 엔진
  - **Compactor**: 오래된 로그 압축 및 보관

### G - Grafana (시각화)
- **역할**: 통합 관측성 대시보드 (Kibana 대체)
- **특징**:
  - Loki, Tempo, Mimir, Prometheus 등 모든 데이터 소스 통합
  - 알림 규칙 설정 및 PagerDuty 연동
  - 사용자별 대시보드 템플릿 공유
- **장점**:
  - ELK는 로그 전용이지만, Grafana는 메트릭/로그/트레이스 모두 통합
  - JSON 기반 대시보드 버전 관리 가능 (Git으로 관리)

### T - Tempo (분산 추적)
- **역할**: 분산 트랜잭션 추적 (Jaeger/Zipkin 대체)
- **특징**:
  - **메타데이터만 인덱싱**, 트레이스 데이터는 오브젝트 스토리지 저장으로 비용 절감
  - OpenTelemetry 네이티브 지원
  - Trace ID로 로그와 메트릭 연관성 추적 가능
- **사용 사례**:
  - 마이크로서비스 간 요청 흐름 추적
  - 병목 구간 식별 (어느 서비스에서 지연 발생?)

### M - Mimir (메트릭)
- **역할**: 장기 메트릭 저장 (Prometheus 장기 저장소)
- **특징**:
  - Prometheus 데이터를 장기 보관 (기본 Prometheus는 15일 권장)
  - 수평 확장 가능 (Prometheus는 단일 서버)
  - **PromQL 완벽 호환**
- **도입 배경**:
  - 금융권 규제로 **6개월~1년간 메트릭 보관 필요**
  - Prometheus 단독으로는 디스크 부족 문제 발생

## 점진적 적재 전략

### 1단계: Grafana + Prometheus (기존 인프라 통합) - Week 1-2

#### 목표
- 기존 Prometheus 메트릭을 Grafana로 시각화
- Kibana 없이 메트릭만 먼저 Grafana에서 확인 가능하게 함

#### 작업
```yaml
# docker-compose.yml
version: '3.8'
services:
  grafana:
    image: grafana/grafana:10.2.0
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
      - GF_AUTH_ANONYMOUS_ENABLED=true
    volumes:
      - grafana-data:/var/lib/grafana
      - ./grafana/provisioning:/etc/grafana/provisioning

  prometheus:
    image: prom/prometheus:v2.48.0
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus/prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus-data:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.retention.time=15d'  # 15일 보관

volumes:
  grafana-data:
  prometheus-data:
```

#### 효과
- 개발자들이 Grafana UI에 익숙해짐
- Prometheus 메트릭으로 CPU, 메모리, 요청 수 등 모니터링 시작

### 2단계: Loki 도입 (로그 경량화) - Week 3-6

#### 목표
- ELK와 병행 운영하며 Loki의 안정성 검증
- 중요도가 낮은 로그(개발/스테이징)부터 Loki로 전환

#### 작업
```yaml
# Promtail 설정 (로그 수집 에이전트)
# promtail-config.yml
server:
  http_listen_port: 9080

positions:
  filename: /tmp/positions.yaml

clients:
  - url: http://loki:3100/loki/api/v1/push

scrape_configs:
  - job_name: system
    static_configs:
      - targets:
          - localhost
        labels:
          job: varlogs
          __path__: /var/log/*.log

  - job_name: containers
    docker_sd_configs:
      - host: unix:///var/run/docker.sock
    relabel_configs:
      - source_labels: ['__meta_docker_container_name']
        target_label: 'container'
      - source_labels: ['__meta_docker_container_log_stream']
        target_label: 'stream'
```

```yaml
# Loki 설정
# loki-config.yml
auth_enabled: false

server:
  http_listen_port: 3100

ingester:
  lifecycler:
    ring:
      kvstore:
        store: inmemory
      replication_factor: 1
  chunk_idle_period: 5m
  chunk_retain_period: 30s

schema_config:
  configs:
    - from: 2024-01-01
      store: boltdb-shipper
      object_store: filesystem
      schema: v11
      index:
        prefix: index_
        period: 24h

storage_config:
  boltdb_shipper:
    active_index_directory: /loki/index
    cache_location: /loki/boltdb-cache
  filesystem:
    directory: /loki/chunks

# 보관 정책: 30일 후 삭제
limits_config:
  retention_period: 720h  # 30일

chunk_store_config:
  max_look_back_period: 720h

table_manager:
  retention_deletes_enabled: true
  retention_period: 720h
```

#### 리소스 비교 (운영 환경 기준)

| 항목 | Elasticsearch | Loki | 절감율 |
|-----|---------------|------|--------|
| 메모리 | 16GB (JVM Heap 8GB) | 2GB | **87.5%** |
| CPU | 4 vCPU (인덱싱 부하) | 1 vCPU | **75%** |
| 디스크 | 500GB (인덱스 + 로그) | 100GB (압축된 로그만) | **80%** |
| 쿼리 속도 | 빠름 (인덱스 기반) | 중간 (레이블 기반 스캔) | - |

#### 전환 순서
1. **개발 환경 로그**: Loki로 전환 (1주차)
2. **스테이징 환경 로그**: Loki로 전환 (2주차)
3. **프로덕션 비중요 로그** (access log, debug log): Loki로 전환 (3주차)
4. **프로덕션 중요 로그** (error log, audit log): ELK와 Loki 동시 적재 후 검증 (4-6주차)

### 3단계: Mimir 도입 (메트릭 장기 보관) - Week 7-10

#### 목표
- Prometheus의 15일 제한을 넘어 **6개월간 메트릭 보관**
- 금융권 감사 요구사항 충족 (과거 데이터 조회 가능)

#### 작업
```yaml
# Prometheus - Mimir 연동 (Remote Write)
# prometheus.yml
global:
  scrape_interval: 15s

remote_write:
  - url: http://mimir:9009/api/v1/push
    queue_config:
      capacity: 10000
      max_shards: 50

scrape_configs:
  - job_name: 'trading-api'
    static_configs:
      - targets: ['trading-api:8080']
```

```yaml
# Mimir 설정 (단일 노드 모드)
# mimir-config.yml
target: all

server:
  http_listen_port: 9009

ingester:
  ring:
    kvstore:
      store: memberlist
    replication_factor: 1

blocks_storage:
  backend: s3
  s3:
    endpoint: minio:9000
    bucket_name: mimir-blocks
    access_key_id: minioadmin
    secret_access_key: minioadmin
    insecure: true

  tsdb:
    dir: /data/ingester

compactor:
  data_dir: /data/compactor
  compaction_interval: 30m

# 6개월 보관 정책
limits:
  max_global_series_per_user: 300000
  ingestion_rate: 10000

# 자동 압축 및 다운샘플링
compactor:
  compaction_interval: 1h
  deletion_delay: 2h
```

#### 효과
- **스토리지 최적화**: 오래된 데이터는 자동 압축 (1분 → 5분 → 1시간 다운샘플링)
- **비용 절감**: MinIO (S3 호환 스토리지) 사용으로 기존 디스크 대비 50% 비용 절감
- **규제 준수**: 6개월간 모든 거래 관련 메트릭 보관 가능

### 4단계: Tempo 도입 (분산 추적) - Week 11-14

#### 목표
- 마이크로서비스 간 요청 흐름 추적
- 로그와 트레이스 연관성 확보 (Trace ID 기반)

#### 작업
```yaml
# Tempo 설정
# tempo-config.yml
server:
  http_listen_port: 3200

distributor:
  receivers:
    otlp:
      protocols:
        grpc:
          endpoint: 0.0.0.0:4317
        http:
          endpoint: 0.0.0.0:4318

ingester:
  trace_idle_period: 10s
  max_block_duration: 5m

storage:
  trace:
    backend: s3
    s3:
      endpoint: minio:9000
      bucket: tempo-traces
      access_key: minioadmin
      secret_access_key: minioadmin
      insecure: true

# 7일 보관 (트레이스는 단기 보관)
compactor:
  compaction:
    block_retention: 168h  # 7일
```

```java
// Spring Boot 애플리케이션 - OpenTelemetry 설정
// build.gradle
dependencies {
    implementation 'io.opentelemetry:opentelemetry-api:1.32.0'
    implementation 'io.opentelemetry.instrumentation:opentelemetry-spring-boot-starter:1.32.0'
}

// application.yml
otel:
  service:
    name: trading-api
  exporter:
    otlp:
      endpoint: http://tempo:4317
  traces:
    sampler:
      probability: 0.1  # 10%만 샘플링 (리소스 절약)
```

#### Trace ID로 로그 연관
```yaml
# Promtail에서 Trace ID 추출
# promtail-config.yml
scrape_configs:
  - job_name: containers
    pipeline_stages:
      - regex:
          expression: '.*trace_id=(?P<trace_id>[0-9a-f]+)'
      - labels:
          trace_id:
```

**효과**: Grafana에서 로그 확인 시 Trace ID 클릭하면 전체 요청 흐름 시각화

## 리소스 최적화 방법

### 1. 보관 기간 차등 적용
```yaml
# 데이터 타입별 보관 정책
- 로그 (Loki):
  - ERROR 로그: 90일
  - INFO 로그: 30일
  - DEBUG 로그: 7일

- 메트릭 (Mimir):
  - 비즈니스 메트릭 (거래량, 금액): 6개월 (1분 해상도)
  - 인프라 메트릭 (CPU, 메모리): 3개월 (5분 다운샘플링)

- 트레이스 (Tempo):
  - 샘플링률: 10% (모든 요청 추적 시 비용 과다)
  - 보관 기간: 7일
```

### 2. 압축 및 다운샘플링
```yaml
# Loki 압축 설정
compactor:
  working_directory: /loki/compactor
  compaction_interval: 10m
  retention_enabled: true
  retention_delete_delay: 2h
```

**효과**: 30일 동안 압축률 평균 85% (100GB → 15GB)

### 3. 오브젝트 스토리지 활용
- **MinIO (S3 호환)**: 온프레미스에서 저렴한 스토리지 클래스 사용
- **Glacier 전환**: 90일 이상 로그는 콜드 스토리지로 자동 이동

### 4. 샘플링 및 필터링
```yaml
# Promtail - 불필요한 로그 필터링
scrape_configs:
  - job_name: containers
    pipeline_stages:
      - drop:
          source: "filename"
          expression: ".*healthcheck.*"  # 헬스체크 로그 제외
      - drop:
          source: "level"
          expression: "DEBUG"  # 프로덕션에서 DEBUG 로그 제외
```

## 효과 및 결과

### 비용 절감
| 항목 | Before (ELK) | After (LGTM) | 절감율 |
|-----|-------------|--------------|--------|
| **서버 대수** | 5대 (ES 3대, LS 1대, KB 1대) | 2대 (All-in-One) | **60%** |
| **메모리** | 총 48GB | 총 8GB | **83%** |
| **스토리지** | 2TB | 400GB | **80%** |
| **월 비용** | $500 (서버 + 디스크) | $150 | **70% 절감** |

### 성능 개선
| 지표 | Before | After | 개선율 |
|-----|--------|-------|--------|
| 로그 검색 속도 | 2-5초 | 1-3초 | **40% 향상** |
| 대시보드 로딩 | 10초 | 3초 | **70% 향상** |
| 디스크 쓰기 속도 | 500MB/s (인덱싱) | 100MB/s (압축) | **80% 감소** |

### 개발자 경험 개선
- **단일 UI**: Kibana + Grafana 2개 → Grafana 1개로 통합
- **연관성 추적**: 로그 → 트레이스 → 메트릭 원클릭 이동
- **쿼리 언어 통일**: LogQL, PromQL로 일관된 문법

### 금융권 규제 준수
- 6개월간 거래 관련 메트릭 보관 완료
- 감사 추적 가능 (Trace ID 기반 전체 흐름 재현)
- 데이터 유출 방지 (온프레미스 MinIO 사용)

## 참고 자료

- [Grafana Loki Documentation](https://grafana.com/docs/loki/latest/)
- [Grafana Tempo Documentation](https://grafana.com/docs/tempo/latest/)
- [Grafana Mimir Documentation](https://grafana.com/docs/mimir/latest/)
- [OpenTelemetry - Distributed Tracing](https://opentelemetry.io/docs/concepts/signals/traces/)
- [LogQL Query Language](https://grafana.com/docs/loki/latest/logql/)
- [Prometheus Remote Write Specification](https://prometheus.io/docs/prometheus/latest/storage/#remote-storage-integrations)
