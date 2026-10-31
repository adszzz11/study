---
date: 2026-11-01
tags: [tech]
type: tech-tool-study
status: draft
---

# 서버 모니터링 분석 가이드: 개요

## What

서버 모니터링은 host resource만 보는 작업이 아니다. 사용자가 경험하는 request volume, latency, error를 먼저 확인하고, 그 변화와 CPU·memory·I/O·pool·dependency 지표를 상관분석하는 observability 실천이다.

## Why

현대 서비스는 application, VM/container, Kubernetes, DB, cache, 외부 API가 함께 동작한다. CPU threshold만으로 alert하면 원인과 증상을 혼동해 불필요한 호출을 만들거나 실제 영향을 놓칠 수 있다. SLI/SLO와 error budget은 무엇이 정상인지, 언제 조치해야 하는지를 사용자 영향으로 정의한다.

## 핵심 특징

- **Symptom-first**: traffic → latency(P95/P99) → error를 보고 원인을 좁힌다.
- **상관분석**: metrics, logs, traces를 timestamp·service·trace ID 같은 공통 metadata로 연결한다.
- **Tail 중심**: 평균 대신 percentile로 일부 사용자의 나쁜 경험을 드러낸다.
- **SLO-first alerting**: CPU 임계치보다 error rate, latency SLO burn을 우선 alert한다.
- **운영 피드백**: incident timeline과 postmortem으로 baseline·runbook·release gate를 갱신한다.

## 관찰 아키텍처

```text
Application / Host / DB / Cache / K8s
  └─ instrumentation · exporter · agent
       └─ Collector (enrich / redact / sample / batch / route)
            ├─ Metrics TSDB → PromQL → Grafana / Alertmanager
            ├─ Logs backend
            └─ Traces backend → dependency / root-cause analysis
                         └─ SLO dashboard · alert · incident · postmortem
```

Collector는 단순 전달기가 아니다. retry/buffer, resource enrichment, PII redaction, sampling, multi-destination routing을 중앙 정책으로 적용한다.

## 분석의 기본 순서

1. traffic 변화부터 본다. 급락했는데 backend가 조용하면 LB, DNS, gateway 단절도 의심한다.
2. latency와 error를 함께 비교한다. 둘 다 상승하면 timeout 또는 saturation, error만 상승하고 latency가 정상이면 즉시 실패하는 dependency·code·deploy를 가설로 둔다.
3. 관련 service trace와 log를 열고, host/DB/cache/pool/queue 지표로 가설을 검증한다.
4. 복구 후 최초 이상 시각부터 대응·복구까지 timeline을 재구성한다.

## Capacity와 saturation

Little's Law 관점에서 동시 처리량은 대략 `RPS × 평균 처리시간`이다. 도착률이 처리율을 지속적으로 넘으면 queue depth와 waiting time이 증가하고 timeout, memory pressure, OOM으로 이어진다. 따라서 thread/connection pool 사용량과 queue를 같이 봐야 한다.

Memory의 GC sawtooth 자체는 정상일 수 있다. GC 뒤의 **최저점**이 반복적으로 상승하는지가 leak의 더 유용한 신호다.

## Sources

- https://kciter.so/posts/server-monitoring-analysis-guide/
- https://sre.google/sre-book/service-level-objectives/
- https://opentelemetry.io/docs/concepts/signals/
