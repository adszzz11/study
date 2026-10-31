---
date: 2026-11-01
tags: [tech]
type: tech-tool-study
status: draft
---

# Getting Started: RED와 기본 dashboard

## 목표

서비스 하나에서 사용자 영향 지표와 기반 resource 지표를 같은 dashboard에 배치하고, error-rate alert 하나를 만든다.

## 1. Application instrumentation

request counter, error counter, latency histogram을 instrument한다. label은 `service`, `route`, `method`, `status_code`처럼 제한된 값만 사용한다. `user_id`, request ID처럼 무한히 늘어나는 값은 metric label로 쓰지 않는다.

```text
http_requests_total{service, route, method, status_code}
http_request_duration_seconds_bucket{service, route, le}
```

## 2. RED dashboard

- **Rate**: RPS와 traffic 급락/급증
- **Errors**: `5xx / total requests` error ratio
- **Duration**: P50/P95/P99 latency

Prometheus histogram의 P99 예시는 다음과 같다.

```promql
histogram_quantile(
  0.99,
  sum by (le) (rate(http_request_duration_seconds_bucket[5m]))
)
```

route별로 볼 때는 `sum by (le, route)`로 확장한다. histogram은 여러 instance를 aggregate할 수 있어 SLO·fleet dashboard에 적합하다.

## 3. 기반 지표 추가

- Host: CPU mode, memory, disk usage/I/O, network, process/file descriptor
- DB: connection pool usage/wait, query latency
- Cache: hit ratio, eviction, memory
- Runtime: GC pause와 GC 후 heap 최저점

## 4. 첫 alert

사용자 영향이 있는 error ratio에 alert을 건다. 임계치와 duration은 서비스 baseline과 SLO에 맞춰 조정한다.

```yaml
- alert: ApiHighErrorRatio
  expr: |
    sum(rate(http_requests_total{status_code=~"5.."}[5m]))
    / sum(rate(http_requests_total[5m])) > 0.02
  for: 10m
  labels:
    severity: page
  annotations:
    summary: API 5xx error ratio is above 2% for 10 minutes
```

## 완료 기준

- [ ] RPS, error ratio, P50/P95/P99가 하나의 dashboard에 있다.
- [ ] host/DB/cache signal을 drill-down할 수 있다.
- [ ] test traffic에서 alert과 notification 경로를 검증했다.
- [ ] alert에 dashboard·runbook URL 또는 대응 문맥을 붙였다.

## Sources

- https://prometheus.io/docs/practices/histograms/
- https://prometheus.io/docs/introduction/overview/
