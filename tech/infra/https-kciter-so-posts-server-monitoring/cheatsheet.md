---
date: 2026-11-01
tags: [tech]
type: tech-tool-study
status: draft
---

# 서버 모니터링 Cheatsheet

## 장애 분석 순서

```text
Traffic → Latency (P95/P99) → Error
       → Trace/Logs → Dependency/Pool/Queue → Host/DB/Cache resource
```

| 증상 | 우선 가설 | 확인할 signal |
|---|---|---|
| traffic 급락, backend 정상 | LB/DNS/gateway 단절 | edge 4xx/5xx, routing, health check |
| P99·error 상승 | saturation/timeout | queue, pool wait, dependency latency |
| error만 상승 | 즉시 실패 | deploy, status code, dependency response |
| P99만 상승 | 느린 dependency/resource | trace span, DB query, I/O, CPU |
| heap 최저점 상승 | memory leak | GC 후 heap, heap profile, allocation |

## PromQL 조각

```promql
# RPS
sum(rate(http_requests_total[5m]))

# 5xx error ratio
sum(rate(http_requests_total{status_code=~"5.."}[5m]))
/ sum(rate(http_requests_total[5m]))

# Fleet P99 from a histogram
histogram_quantile(0.99,
  sum by (le) (rate(http_request_duration_seconds_bucket[5m])))
```

## Guardrails

- metric label에는 bounded cardinality만 사용한다. user ID, request ID는 금지한다.
- logs/traces는 Collector에서 PII·secret을 redaction한다.
- alert은 user impact와 명확한 owner/runbook에 연결한다.
- queue depth만 보지 말고 arrival rate, processing rate, waiting time을 함께 본다.
- 평균 latency만 보지 말고 P95/P99와 error를 함께 읽는다.

## SLO 용어

| 용어 | 의미 |
|---|---|
| SLI | 신뢰성을 재는 관측값 (예: 성공 요청 비율) |
| SLO | SLI의 목표 (예: 30일 99.9%) |
| Error budget | SLO가 허용하는 실패량 |
| Burn rate | error budget을 소진하는 속도 |

## Sources

- https://prometheus.io/docs/practices/histograms/
- https://opentelemetry.io/docs/concepts/signals/
- https://sre.google/sre-book/service-level-objectives/
