# Loki와 Elasticsearch의 차이점은?

## 답변

[여기에 답변 작성]

## 핵심 키워드

- Loki
- Elasticsearch
- Log Aggregation
- Indexing 방식
- Label
- 비용 효율성
- 쿼리 성능

## 아키텍처 차이

### Loki
-

### Elasticsearch
-

## Indexing 방식

### Loki
-

### Elasticsearch
-

## 쿼리 방식

### Loki (LogQL)
-

### Elasticsearch (DSL/Lucene)
-

## 성능 및 비용

### Loki
-

### Elasticsearch
-

## 사용 사례

### Loki가 적합한 경우
-

### Elasticsearch가 적합한 경우
-

## 설정 예시

### Loki Configuration
```yaml
auth_enabled: false

server:
  http_listen_port: 3100

ingester:
  lifecycler:
    address: 127.0.0.1
    ring:
      kvstore:
        store: inmemory
      replication_factor: 1
  chunk_idle_period: 5m
  chunk_retain_period: 30s

schema_config:
  configs:
    - from: 2020-05-15
      store: boltdb-shipper
      object_store: s3
      schema: v11
      index:
        prefix: loki_index_
        period: 24h

storage_config:
  boltdb_shipper:
    active_index_directory: /loki/index
    cache_location: /loki/boltdb-cache
  aws:
    s3: s3://region/bucket

limits_config:
  enforce_metric_name: false
  reject_old_samples: true
  reject_old_samples_max_age: 168h
```

### Promtail Configuration (Loki Agent)
```yaml
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

  - job_name: kubernetes
    kubernetes_sd_configs:
      - role: pod
    relabel_configs:
      - source_labels: [__meta_kubernetes_pod_label_app]
        target_label: app
      - source_labels: [__meta_kubernetes_namespace]
        target_label: namespace
```

### LogQL 쿼리 예시
```logql
# 기본 로그 스트림 선택
{app="myapp", env="production"}

# 필터링
{app="myapp"} |= "error"

# 정규식 필터
{app="myapp"} |~ "error|warning"

# 메트릭 쿼리
rate({app="myapp"}[5m])

# 집계
sum by (namespace) (rate({job="varlogs"}[5m]))
```

### Elasticsearch Configuration
```yaml
cluster.name: my-cluster
node.name: node-1

path.data: /var/lib/elasticsearch
path.logs: /var/log/elasticsearch

network.host: 0.0.0.0
http.port: 9200

discovery.seed_hosts: ["host1", "host2"]
cluster.initial_master_nodes: ["node-1", "node-2"]

# 메모리 설정
bootstrap.memory_lock: true

# 샤드 설정
index.number_of_shards: 3
index.number_of_replicas: 1
```

### Filebeat Configuration (Elasticsearch Agent)
```yaml
filebeat.inputs:
  - type: log
    enabled: true
    paths:
      - /var/log/*.log
    fields:
      app: myapp
      env: production

output.elasticsearch:
  hosts: ["elasticsearch:9200"]
  index: "myapp-%{+yyyy.MM.dd}"

setup.template.name: "myapp"
setup.template.pattern: "myapp-*"
```

### Elasticsearch Query DSL
```json
{
  "query": {
    "bool": {
      "must": [
        { "match": { "app": "myapp" } },
        { "match": { "level": "error" } }
      ],
      "filter": [
        { "range": { "@timestamp": { "gte": "now-1h" } } }
      ]
    }
  },
  "aggs": {
    "errors_over_time": {
      "date_histogram": {
        "field": "@timestamp",
        "interval": "5m"
      }
    }
  }
}
```

## 비용 비교

### 스토리지
- Loki:
- Elasticsearch:

### 운영 복잡도
- Loki:
- Elasticsearch:

## 참고 자료

-
