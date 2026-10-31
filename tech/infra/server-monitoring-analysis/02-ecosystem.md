---
date: 2026-11-01
tags: [tech]
type: tech-tool-study
status: draft
---

# 서버 모니터링 에코시스템

## 선택 기준

도구보다 먼저 signal 범위(metrics/logs/traces), deployment 환경, retention, cardinality, 운영 인력, 데이터 egress와 비용을 정한다. OTel은 vendor-neutral instrumentation과 export 경로를 제공하므로 backend 교체 비용을 낮추는 기본 축이 된다.

| 선택지 | 강점 | 적합한 상황 | 유의점 |
|---|---|---|---|
| Prometheus + Grafana + Alertmanager | Pull metrics, PromQL, CNCF 생태계 | Kubernetes·자체 운영, metrics 중심 | logs/traces와 long-term storage를 별도 설계 |
| OTel Collector + Grafana Alloy + Loki/Tempo/Mimir | OTel·Prometheus pipeline 통합, vendor-neutral export | unified OSS observability, 점진 migration | backend별 retention·cardinality·비용 설계 필요 |
| Datadog | SaaS와 host/container/process 통합 visibility | 운영 인력이 적고 빠른 도입 | ingestion·retention 비용과 vendor dependence 검토 |
| New Relic | infra agent, APM, logs-in-context, cloud integration | full-stack SaaS observability | data model/NRQL 및 agent 정책 필요 |
| Elastic Observability | Elasticsearch 검색, logs 분석, APM, OTel ingest | log search·analytics 통합 | cluster·storage lifecycle 운영 비용 고려 |
| AWS CloudWatch | AWS resource와 native 통합 | AWS 중심 환경 | multi-cloud 및 정밀 trace/log 분석은 보완 도구 검토 |

## 구성 패턴

### OSS 중심

Prometheus가 exporter를 pull하고 Grafana가 dashboard를, Alertmanager가 notification을 담당한다. logs/traces는 Loki/Tempo 같은 backend를 붙이고, OTel Collector 또는 Grafana Alloy를 pipeline 경계로 둔다.

### SaaS 중심

Agent 또는 OTel Collector가 vendor backend로 전송한다. 초기 운영은 단순하지만 cardinality, trace sampling, log volume, retention이 비용의 주요 조절점이다.

### Hybrid

OTel SDK와 Collector로 instrumentation을 표준화하고 metrics 일부는 Prometheus, long-term analysis 또는 APM은 SaaS에 보낸다. 다중 export는 필요 signal만 routing해 중복 ingestion 비용을 피한다.

## 비교 후 결정 질문

- PromQL과 Kubernetes service discovery가 운영팀의 기본 역량인가?
- logs/traces의 검색 기간과 법적 보존 요건은 무엇인가?
- high-cardinality label과 trace sampling의 예산 상한은 얼마인가?
- vendor outage 또는 migration 때 application instrumentation을 유지할 수 있는가?

## Sources

- https://prometheus.io/docs/introduction/overview/
- https://grafana.com/docs/alloy/latest/
- https://docs.datadoghq.com/infrastructure/
- https://docs.newrelic.com/docs/infrastructure/introduction-infra-monitoring/
- https://www.elastic.co/docs/solutions/observability
- https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/WhatIsCloudWatch.html
