---
date: 2026-11-01
tags: [tech]
type: tech-tool-study
status: draft
---

# 서버 모니터링 실전 프로젝트

## 1. Single VM API baseline

**목표**: Node Exporter + Prometheus + Grafana로 API, host, DB의 최소 운영 dashboard를 만든다.

- API에 request/error counter와 latency histogram을 추가한다.
- Node Exporter로 CPU, memory, disk, network를 수집한다.
- DB connection pool, query latency를 추가하고 error-rate alert을 테스트한다.
- 결과물: dashboard URL, alert rule, metric dictionary, 간단한 runbook.

## 2. SLO-first alerting

**목표**: availability·latency SLI를 histogram으로 만들고 multi-window burn-rate alert과 release gate를 구축한다.

- 30일 SLO와 error budget을 합의한다.
- fast/slow burn rate를 분리해 page와 ticket의 noise를 제어한다.
- deploy 뒤 SLO burn이 지속되면 rollback 또는 release 중단 조건을 검증한다.
- 결과물: SLO spec, PromQL recording/alert rules, incident drill 기록.

## 3. OTel migration

**목표**: proprietary agent를 OTel SDK/Collector로 점진 전환하고 signal correlation을 완성한다.

- 서비스 한 개에서 auto-instrumentation 또는 SDK를 시작한다.
- Collector에 redaction, sampling, retry/batch, routing을 정의한다.
- trace ID를 logs에 넣고 trace → log → host metric drill-down을 시연한다.
- 결과물: pipeline diagram, config review, migration checklist, 비용 baseline.

## 평가 기준

| 항목 | 질문 |
|---|---|
| 사용자 영향 | dashboard가 traffic·latency·error를 먼저 보여주는가? |
| 진단성 | 한 alert에서 trace, logs, resource signal로 이동할 수 있는가? |
| 안전성 | PII redaction·secret 제외·cardinality guardrail이 있는가? |
| 운영성 | alert이 action 가능한가, runbook과 owner가 있는가? |

## Sources

- https://kciter.so/posts/server-monitoring-analysis-guide/
- https://opentelemetry.io/docs/
- https://sre.google/sre-book/service-level-objectives/
