---
date: 2026-11-01
tags: [tech]
type: tech-tool-study
status: draft
---

# 서버 모니터링 참고 자료

## 원문

1. [서버 모니터링 분석 가이드](https://kciter.so/posts/server-monitoring-analysis-guide/) — symptom-first 분석 흐름의 출발점

## Metrics와 Prometheus

2. [Prometheus Overview](https://prometheus.io/docs/introduction/overview/) — data model, PromQL, pull architecture
3. [Prometheus Histograms and Summaries](https://prometheus.io/docs/practices/histograms/) — percentile과 histogram 기반 집계

## OpenTelemetry와 Collector

4. [OpenTelemetry Documentation](https://opentelemetry.io/docs/) — SDK, Collector, instrumentation
5. [OpenTelemetry Signals](https://opentelemetry.io/docs/concepts/signals/) — metrics, logs, traces의 역할
6. [Grafana Alloy Documentation](https://grafana.com/docs/alloy/latest/) — OTel/Prometheus collector distribution
7. [Grafana OTel Collector production setup](https://grafana.com/docs/opentelemetry/collector/) — production pipeline 권고

## Reliability와 alerting

8. [Google SRE: Service Level Objectives](https://sre.google/sre-book/service-level-objectives/) — SLI, SLO, error budget
9. [Google SRE: Error Budget Policy](https://sre.google/workbook/error-budget-policy/) — release·reliability 의사결정

## 읽는 순서

원문 → Prometheus Overview/Histograms → OTel Signals → SRE SLO → Grafana Collector 순서로 읽으면, signal 설계에서 수집 pipeline과 alert policy까지 이어진다.
