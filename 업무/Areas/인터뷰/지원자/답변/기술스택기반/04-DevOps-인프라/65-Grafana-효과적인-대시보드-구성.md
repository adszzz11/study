# Grafana에서 효과적인 대시보드 구성 방법은?

## 답변

[여기에 답변 작성]

## 핵심 키워드

- Grafana Dashboard
- Panel
- Variables
- Annotations
- Alerting
- Data Source
- PromQL
- LogQL

## 대시보드 설계 원칙

### 계층적 구성
-

### 사용자별 대시보드
-

## Panel 종류와 활용

### Time Series
-

### Stat
-

### Gauge
-

### Table
-

### Heatmap
-

### Logs
-

## Variables 활용

-

## Annotations

-

## Alert 설정

-

## 설정 예시

### Dashboard JSON (기본 구조)
```json
{
  "dashboard": {
    "title": "Application Monitoring",
    "tags": ["production", "myapp"],
    "timezone": "browser",
    "refresh": "30s",
    "panels": [
      {
        "id": 1,
        "type": "timeseries",
        "title": "Request Rate",
        "targets": [
          {
            "expr": "rate(http_requests_total{app=\"myapp\"}[5m])",
            "legendFormat": "{{method}} {{status}}"
          }
        ]
      }
    ]
  }
}
```

### Variables 설정
```json
{
  "templating": {
    "list": [
      {
        "name": "namespace",
        "type": "query",
        "datasource": "Prometheus",
        "query": "label_values(kube_pod_info, namespace)",
        "multi": true,
        "includeAll": true
      },
      {
        "name": "pod",
        "type": "query",
        "datasource": "Prometheus",
        "query": "label_values(kube_pod_info{namespace=~\"$namespace\"}, pod)",
        "multi": true,
        "refresh": 2
      }
    ]
  }
}
```

### PromQL 쿼리 예시
```promql
# CPU 사용률
rate(container_cpu_usage_seconds_total{namespace="$namespace", pod="$pod"}[5m]) * 100

# 메모리 사용률
container_memory_usage_bytes{namespace="$namespace", pod="$pod"} /
container_spec_memory_limit_bytes{namespace="$namespace", pod="$pod"} * 100

# HTTP 요청 수 (5분 평균)
sum(rate(http_requests_total{namespace="$namespace"}[5m])) by (status)

# P95 레이턴시
histogram_quantile(0.95,
  sum(rate(http_request_duration_seconds_bucket[5m])) by (le)
)

# Error Rate
sum(rate(http_requests_total{status=~"5.."}[5m])) /
sum(rate(http_requests_total[5m])) * 100
```

### LogQL 쿼리 예시
```logql
# 에러 로그 필터
{namespace="$namespace", pod=~"$pod"} |= "error" | json

# 로그 레벨별 카운트
sum by (level) (count_over_time({namespace="$namespace"}[5m]))

# 특정 패턴 추출
{app="myapp"} | pattern `<_> level=<level> msg="<message>"`

# 메트릭 변환
sum(rate({app="myapp"} |= "error" [5m])) by (pod)
```

### Alert Rule 설정
```yaml
# Grafana Alert Rule (YAML)
groups:
  - name: application_alerts
    interval: 1m
    rules:
      - alert: HighErrorRate
        expr: |
          sum(rate(http_requests_total{status=~"5.."}[5m])) /
          sum(rate(http_requests_total[5m])) * 100 > 5
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High error rate detected"
          description: "Error rate is {{ $value }}%"

      - alert: HighMemoryUsage
        expr: |
          container_memory_usage_bytes /
          container_spec_memory_limit_bytes * 100 > 90
        for: 10m
        labels:
          severity: critical
        annotations:
          summary: "High memory usage on {{ $labels.pod }}"
```

### Terraform으로 대시보드 관리
```hcl
resource "grafana_dashboard" "myapp" {
  config_json = file("${path.module}/dashboards/myapp.json")
  folder      = grafana_folder.myapp.id
}

resource "grafana_folder" "myapp" {
  title = "MyApp"
}

resource "grafana_data_source" "prometheus" {
  type = "prometheus"
  name = "Prometheus"
  url  = "http://prometheus:9090"

  json_data {
    http_method = "POST"
  }
}
```

### 대시보드 베스트 프랙티스
```json
{
  "dashboard": {
    "editable": false,
    "graphTooltip": 1,
    "links": [
      {
        "title": "Related Logs",
        "url": "/d/logs-dashboard"
      }
    ],
    "panels": [
      {
        "title": "Golden Signals",
        "type": "row",
        "collapsed": false,
        "panels": [
          {
            "title": "Latency (P50, P95, P99)",
            "type": "timeseries"
          },
          {
            "title": "Traffic (Requests/sec)",
            "type": "timeseries"
          },
          {
            "title": "Errors (Error Rate %)",
            "type": "timeseries"
          },
          {
            "title": "Saturation (CPU/Memory %)",
            "type": "timeseries"
          }
        ]
      }
    ]
  }
}
```

## 참고 자료

-
