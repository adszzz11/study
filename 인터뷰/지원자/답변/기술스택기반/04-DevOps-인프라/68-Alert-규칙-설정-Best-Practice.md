# Alert 규칙 설정의 Best Practice는?

## 답변

[여기에 답변 작성]

## 핵심 키워드

- Alerting
- Alert Rules
- Severity Levels
- Alert Fatigue
- SLO/SLI
- Runbook
- Alert Routing
- Silence

## Alert 설계 원칙

### Actionable
-

### Meaningful
-

### Context-rich
-

## Severity Level 정의

### Critical
-

### Warning
-

### Info
-

## Alert Threshold 설정

### 고정 임계값 vs 동적 임계값
-

### for 절 활용
-

## Alert Fatigue 방지

-

## SLO 기반 알림

-

## Runbook 작성

-

## 설정 예시

### Prometheus Alert Rules
```yaml
groups:
  - name: infrastructure_critical
    interval: 30s
    rules:
      # 노드 다운
      - alert: InstanceDown
        expr: up == 0
        for: 5m
        labels:
          severity: critical
          component: infrastructure
        annotations:
          summary: "Instance {{ $labels.instance }} is down"
          description: |
            Instance {{ $labels.instance }} of job {{ $labels.job }} has been down for more than 5 minutes.
            Current value: {{ $value }}
          runbook_url: "https://runbooks.example.com/InstanceDown"
          dashboard_url: "https://grafana.example.com/d/node-exporter"

      # 높은 CPU 사용률
      - alert: HighCPUUsage
        expr: |
          100 - (avg by (instance) (irate(node_cpu_seconds_total{mode="idle"}[5m])) * 100) > 80
        for: 10m
        labels:
          severity: warning
          component: infrastructure
        annotations:
          summary: "High CPU usage on {{ $labels.instance }}"
          description: |
            CPU usage on {{ $labels.instance }} is above 80% for more than 10 minutes.
            Current value: {{ $value | humanizePercentage }}
          runbook_url: "https://runbooks.example.com/HighCPUUsage"

      # 메모리 부족
      - alert: HighMemoryUsage
        expr: |
          (1 - (node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes)) * 100 > 90
        for: 5m
        labels:
          severity: critical
          component: infrastructure
        annotations:
          summary: "High memory usage on {{ $labels.instance }}"
          description: |
            Memory usage on {{ $labels.instance }} is above 90%.
            Available: {{ with query "node_memory_MemAvailable_bytes{instance=\"" }}{{ . | first | value | humanize1024 }}{{ end }}
            Total: {{ with query "node_memory_MemTotal_bytes{instance=\"" }}{{ . | first | value | humanize1024 }}{{ end }}

  - name: application_critical
    interval: 30s
    rules:
      # 높은 에러율
      - alert: HighErrorRate
        expr: |
          (
            sum(rate(http_requests_total{status=~"5.."}[5m])) by (job)
            /
            sum(rate(http_requests_total[5m])) by (job)
          ) * 100 > 5
        for: 5m
        labels:
          severity: critical
          component: application
        annotations:
          summary: "High error rate on {{ $labels.job }}"
          description: |
            Error rate on {{ $labels.job }} is {{ $value | humanizePercentage }}.
            Threshold: 5%
          runbook_url: "https://runbooks.example.com/HighErrorRate"

      # 높은 레이턴시 (P95)
      - alert: HighLatency
        expr: |
          histogram_quantile(0.95,
            sum(rate(http_request_duration_seconds_bucket[5m])) by (job, le)
          ) > 1
        for: 10m
        labels:
          severity: warning
          component: application
        annotations:
          summary: "High latency on {{ $labels.job }}"
          description: |
            P95 latency on {{ $labels.job }} is {{ $value }}s.
            Threshold: 1s

      # API 가용성 (SLO)
      - alert: SLOViolation
        expr: |
          (
            sum(rate(http_requests_total{status!~"5.."}[30d]))
            /
            sum(rate(http_requests_total[30d]))
          ) < 0.999
        labels:
          severity: critical
          component: slo
        annotations:
          summary: "SLO violation: 99.9% availability"
          description: |
            30-day availability is {{ $value | humanizePercentage }}.
            SLO target: 99.9%
            Error budget consumed!

  - name: application_warning
    interval: 1m
    rules:
      # 디스크 사용률
      - alert: DiskSpaceWarning
        expr: |
          (1 - node_filesystem_avail_bytes / node_filesystem_size_bytes) * 100 > 80
        for: 5m
        labels:
          severity: warning
          component: infrastructure
        annotations:
          summary: "Disk space warning on {{ $labels.instance }}"
          description: |
            Disk usage on {{ $labels.instance }} {{ $labels.mountpoint }} is above 80%.
            Current: {{ $value | humanizePercentage }}

      - alert: DiskSpaceCritical
        expr: |
          (1 - node_filesystem_avail_bytes / node_filesystem_size_bytes) * 100 > 90
        for: 5m
        labels:
          severity: critical
          component: infrastructure
        annotations:
          summary: "Disk space critical on {{ $labels.instance }}"
          description: |
            Disk usage on {{ $labels.instance }} {{ $labels.mountpoint }} is above 90%.
            Current: {{ $value | humanizePercentage }}
            Available: {{ with query "node_filesystem_avail_bytes" }}{{ . | first | value | humanize1024 }}{{ end }}
```

### Alertmanager Configuration
```yaml
global:
  resolve_timeout: 5m
  slack_api_url: 'https://hooks.slack.com/services/XXX'

# 알림 라우팅
route:
  receiver: 'default'
  group_by: ['alertname', 'cluster', 'service']
  group_wait: 10s
  group_interval: 10s
  repeat_interval: 12h

  routes:
    # Critical 알림은 즉시 전송
    - match:
        severity: critical
      receiver: 'critical-alerts'
      group_wait: 0s
      repeat_interval: 4h
      continue: true

    # 업무 시간에만 경고
    - match:
        severity: warning
      receiver: 'warning-alerts'
      group_wait: 30s
      repeat_interval: 12h
      active_time_intervals:
        - business_hours

    # 인프라 알림은 별도 채널
    - match:
        component: infrastructure
      receiver: 'infrastructure-team'

    # 애플리케이션 알림
    - match:
        component: application
      receiver: 'dev-team'

# Inhibition rules (중복 알림 방지)
inhibit_rules:
  # InstanceDown이면 다른 알림 무시
  - source_match:
      alertname: InstanceDown
    target_match_re:
      alertname: (HighCPUUsage|HighMemoryUsage|DiskSpace.*)
    equal: ['instance']

  # Critical이 발생하면 Warning 무시
  - source_match:
      severity: critical
    target_match:
      severity: warning
    equal: ['alertname', 'instance']

# Receivers
receivers:
  - name: 'default'
    slack_configs:
      - channel: '#alerts'
        title: '{{ .Status | toUpper }}: {{ .GroupLabels.alertname }}'
        text: '{{ range .Alerts }}{{ .Annotations.description }}{{ end }}'

  - name: 'critical-alerts'
    slack_configs:
      - channel: '#alerts-critical'
        title: 'CRITICAL: {{ .GroupLabels.alertname }}'
        text: |
          {{ range .Alerts }}
          *Summary:* {{ .Annotations.summary }}
          *Description:* {{ .Annotations.description }}
          *Runbook:* {{ .Annotations.runbook_url }}
          *Dashboard:* {{ .Annotations.dashboard_url }}
          {{ end }}
        send_resolved: true

    pagerduty_configs:
      - service_key: 'YOUR_PAGERDUTY_KEY'
        description: '{{ .GroupLabels.alertname }}: {{ .GroupLabels.instance }}'

  - name: 'warning-alerts'
    slack_configs:
      - channel: '#alerts-warning'

  - name: 'infrastructure-team'
    email_configs:
      - to: 'infra-team@example.com'
        headers:
          Subject: '[{{ .Status }}] {{ .GroupLabels.alertname }}'

  - name: 'dev-team'
    slack_configs:
      - channel: '#dev-alerts'

# Time intervals
time_intervals:
  - name: business_hours
    time_intervals:
      - times:
        - start_time: '09:00'
          end_time: '18:00'
        weekdays: ['monday:friday']
```

### Grafana Alert Rules (Unified Alerting)
```yaml
apiVersion: 1

groups:
  - name: service_health
    interval: 1m
    rules:
      - uid: service_down
        title: Service Down
        condition: B
        data:
          - refId: A
            queryType: ''
            relativeTimeRange:
              from: 300
              to: 0
            datasourceUid: prometheus
            model:
              expr: up{job="myapp"}
              refId: A

          - refId: B
            queryType: ''
            relativeTimeRange:
              from: 0
              to: 0
            datasourceUid: __expr__
            model:
              type: classic_conditions
              refId: B
              conditions:
                - evaluator:
                    params: [0]
                    type: lt
                  operator:
                    type: and
                  query:
                    params: [A]
                  type: query

        noDataState: NoData
        execErrState: Error
        for: 5m
        annotations:
          description: 'Service {{ $labels.instance }} has been down for 5 minutes'
          runbook_url: 'https://runbooks.example.com/ServiceDown'
        labels:
          severity: critical
```

## 참고 자료

-
