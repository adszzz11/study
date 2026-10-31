---
date: 2026-11-01
tags: [tech]
type: tech-tool-study
status: draft
---

# Deep Dive: SLO, traces, saturation

## 1. SLI/SLO와 error budget

예를 들어 `30일 동안 요청의 99.9%가 300 ms 미만`을 latency SLO로 정의한다. 0.1%가 error budget이며, 짧은 기간에 빠르게 소진되는 burn rate는 page, 느리게 소진되는 경우는 ticket 또는 investigation으로 분리한다. 단순 CPU alert보다 사용자 영향과 대응 우선순위가 명확해진다.

## 2. Trace-to-log drill-down

OTel SDK 또는 auto-instrumentation을 도입하고 Collector에 export한다. log record에 trace ID/span ID를 포함하면 다음 경로를 연결할 수 있다.

```text
SLO breach → slow route trace → dependency span → correlated logs
           → pod/host metrics → pool, queue, CPU, I/O 가설 검증
```

Collector에서 PII redaction을 먼저 적용하고, high-volume trace는 head 또는 tail sampling 정책으로 조절한다. 오류와 고지연 trace는 보존 확률을 높이는 것이 일반적이다.

## 3. Saturation 실험

load test로 RPS를 점진적으로 높인다. 각 단계에서 P99, queue depth, waiting time, thread/connection pool, CPU, memory를 함께 기록한다.

| 관찰 | 가능한 해석 | 다음 확인 |
|---|---|---|
| P99·error 동시 상승 | timeout 또는 saturation | queue, pool wait, dependency latency |
| error만 상승, P99 정상 | 빠른 실패 | deploy, validation, dependency status |
| queue 지속 증가 | 도착률 > 처리율 | worker 수, service time, backpressure |
| GC 후 heap 최저점 상승 | leak 가능성 | heap profile, object growth |

## 4. Deploy와 incident

deploy 직후 warm-up curve와 평소 baseline을 문서화한다. 회복 추세가 없는 latency 상승은 rollback 조건으로 둔다. incident 후에는 최초 이상, alert, 대응 시작, 복구 시각을 timeline으로 만들고, missing signal·runbook·capacity·test 항목을 action item으로 남긴다.

## Sources

- https://sre.google/sre-book/service-level-objectives/
- https://sre.google/workbook/error-budget-policy/
- https://opentelemetry.io/docs/
- https://grafana.com/docs/opentelemetry/collector/
