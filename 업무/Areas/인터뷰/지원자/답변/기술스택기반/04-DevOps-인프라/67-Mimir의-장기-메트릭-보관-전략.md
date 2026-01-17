# Mimir의 장기 메트릭 보관 전략은?

## 답변

[여기에 답변 작성]

## 핵심 키워드

- Mimir
- Long-term Storage
- Compaction
- Retention Policy
- Object Storage
- Downsampling
- Recording Rules
- Query Federation

## Mimir 아키텍처

### 주요 컴포넌트
-

### 저장 계층
-

## Retention 정책

### Block Retention
-

### Compaction
-

## Downsampling

### 왜 필요한가
-

### 구현 방법
-

## Recording Rules 활용

-

## Cost Optimization

### Storage Tiering
-

### Query Optimization
-

## 설정 예시

### Mimir Configuration
```yaml
# mimir.yaml
multitenancy_enabled: false

server:
  http_listen_port: 8080
  grpc_listen_port: 9095

# 분산 컴포넌트
distributor:
  pool:
    health_check_ingesters: true

ingester:
  lifecycler:
    ring:
      kvstore:
        store: consul
        consul:
          host: consul:8500
      replication_factor: 3

  # WAL 설정
  wal:
    enabled: true
    dir: /data/ingester-wal
    checkpoint_duration: 2h

# 장기 보관 설정
blocks_storage:
  backend: s3

  s3:
    endpoint: s3.amazonaws.com
    bucket_name: mimir-blocks
    access_key_id: ${S3_ACCESS_KEY}
    secret_access_key: ${S3_SECRET_KEY}

  tsdb:
    # Block 생성 주기
    block_ranges_period: [2h, 12h, 24h]
    retention_period: 0  # 무제한 (삭제는 compactor가 담당)
    ship_interval: 1m
    head_compaction_interval: 5m

  bucket_store:
    sync_dir: /data/tsdb-sync
    max_chunk_pool_bytes: 12884901888  # 12GB

    # 청크 캐시
    chunks_cache:
      backend: memcached
      memcached:
        addresses: memcached:11211
        max_item_size: 1048576
        timeout: 200ms

    # 인덱스 캐시
    index_cache:
      backend: memcached
      memcached:
        addresses: memcached:11211
        max_item_size: 5242880

    # 메타데이터 캐시
    metadata_cache:
      backend: memcached
      memcached:
        addresses: memcached:11211
        max_item_size: 1048576

# Compactor 설정
compactor:
  data_dir: /data/compactor
  sharding_ring:
    kvstore:
      store: consul
      consul:
        host: consul:8500

  # Compaction 설정
  compaction_interval: 30m
  cleanup_interval: 15m

  # Retention 정책 (tenant별로 다르게 설정 가능)
  deletion_delay: 12h
  max_compaction_time: 24h

# Limits 설정
limits:
  # Ingestion limits
  ingestion_rate: 100000
  ingestion_burst_size: 200000

  # Query limits
  max_query_lookback: 720h  # 30일
  max_query_length: 721h
  max_query_parallelism: 32

  # Storage limits
  max_global_series_per_user: 10000000
  max_global_series_per_metric: 0

  # Retention (테넌트별)
  compactor_blocks_retention_period: 2160h  # 90일

# Query Frontend
query_frontend:
  log_queries_longer_than: 10s
  compress_responses: true

  results_cache:
    backend: memcached
    memcached:
      addresses: memcached:11211
      timeout: 500ms
```

### Prometheus Recording Rules (Downsampling)
```yaml
# prometheus-rules.yaml
groups:
  - name: downsampling_5m
    interval: 5m
    rules:
      # 5분 평균
      - record: http_request_duration_seconds:rate5m
        expr: rate(http_request_duration_seconds_sum[5m]) / rate(http_request_duration_seconds_count[5m])

      - record: http_requests:rate5m
        expr: sum(rate(http_requests_total[5m])) by (job, status)

      # CPU 사용률 5분 평균
      - record: node_cpu:usage5m
        expr: avg(rate(node_cpu_seconds_total{mode!="idle"}[5m])) by (instance)

  - name: downsampling_1h
    interval: 1h
    rules:
      # 1시간 평균
      - record: http_request_duration_seconds:rate1h
        expr: rate(http_request_duration_seconds_sum[1h]) / rate(http_request_duration_seconds_count[1h])

      - record: http_requests:rate1h
        expr: sum(rate(http_requests_total[1h])) by (job, status)

  - name: aggregations
    interval: 1m
    rules:
      # 사전 집계
      - record: instance:node_memory_usage:ratio
        expr: |
          (node_memory_MemTotal_bytes - node_memory_MemAvailable_bytes)
          / node_memory_MemTotal_bytes

      - record: instance:node_disk_usage:ratio
        expr: |
          (node_filesystem_size_bytes - node_filesystem_avail_bytes)
          / node_filesystem_size_bytes
```

### Retention by Tenant (Multi-tenancy)
```yaml
# Per-tenant limits
overrides:
  tenant1:
    compactor_blocks_retention_period: 4320h  # 180일
    max_global_series_per_user: 20000000

  tenant2:
    compactor_blocks_retention_period: 720h   # 30일
    max_global_series_per_user: 5000000
```

### Kubernetes Deployment
```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: mimir-ingester
spec:
  serviceName: mimir-ingester
  replicas: 3
  template:
    spec:
      containers:
      - name: ingester
        image: grafana/mimir:latest
        args:
          - -config.file=/etc/mimir/mimir.yaml
          - -target=ingester
        volumeMounts:
        - name: data
          mountPath: /data
        - name: config
          mountPath: /etc/mimir
        resources:
          requests:
            memory: 4Gi
            cpu: 2
          limits:
            memory: 8Gi
            cpu: 4
  volumeClaimTemplates:
  - metadata:
      name: data
    spec:
      accessModes: ["ReadWriteOnce"]
      resources:
        requests:
          storage: 100Gi
```

### Query를 위한 Grafana Data Source
```yaml
apiVersion: 1

datasources:
  - name: Mimir
    type: prometheus
    access: proxy
    url: http://mimir-query-frontend:8080/prometheus
    jsonData:
      httpMethod: POST
      timeInterval: 30s
      # 장기 쿼리를 위한 설정
      customQueryParameters: 'max_source_resolution=0'
```

### Cost Optimization Query 예시
```promql
# 원본 데이터 대신 recording rule 사용
# ❌ 비효율적 (30일간 raw data 쿼리)
rate(http_requests_total[30d])

# ✅ 효율적 (pre-aggregated data 사용)
http_requests:rate1h

# 오래된 데이터는 낮은 해상도로 조회
# 최근 1시간: 원본 데이터
rate(http_requests_total[5m])

# 1일 전: 5분 집계 데이터
http_requests:rate5m offset 1d

# 30일 전: 1시간 집계 데이터
http_requests:rate1h offset 30d
```

## 참고 자료

-
