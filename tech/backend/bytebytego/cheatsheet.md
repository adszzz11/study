---
date: 2026-09-20
tags: [tech]
type: tech-tool-study
status: draft
---

# ByteByteGo Cheatsheet

## 4-step 답변 순서

```text
1. Scope: requirements, scale, SLA, constraints
2. High-level: API, components, data flow
3. Deep dive: hot path, data model, partitioning, failure
4. Wrap-up: trade-offs, metrics, migration, next risks
```

## Capacity Estimation

| 항목 | 빠른 질문 |
| --- | --- |
| traffic | average/peak QPS와 read:write 비율은? |
| storage | record size × writes/day × retention은? |
| bandwidth | payload × QPS는? |
| latency | p50/p95/p99 목표는? |
| availability | RTO/RPO와 허용 장애 범위는? |

## Component 선택

| 필요 | 대표 선택지 | 반드시 설명할 trade-off |
| --- | --- | --- |
| read latency 절감 | CDN, Redis cache | staleness, invalidation, hot key |
| durable query | SQL | schema, transaction, scale-out 비용 |
| flexible access pattern | NoSQL | consistency, secondary index, modeling |
| async workload | queue + worker | ordering, retry, duplicate, DLQ |
| unique ID | Snowflake/UUID | ordering, coordination, size |
| scale-out | sharding/replication | rebalancing, cross-shard query, lag |

## Failure Checklist

- [ ] timeout, retry, exponential backoff, retry budget가 있는가?
- [ ] consumer와 API가 idempotent한가?
- [ ] queue lag, DLQ, replay 방법을 운영 가능한가?
- [ ] database/cache/provider 장애 시 degraded mode가 있는가?
- [ ] logs, metrics, traces와 alert의 owner가 정해졌는가?
- [ ] data migration과 rollback이 가능한가?

## AI/RAG Checklist

- [ ] ingestion source/version/access control을 보존하는가?
- [ ] chunking·retrieval 품질을 offline eval로 측정하는가?
- [ ] citation과 unsupported answer 정책이 있는가?
- [ ] prompt-injection red team과 data/instruction 분리가 있는가?
- [ ] model latency, token cost, trace를 수집하는가?

## Sources

- https://blog.bytebytego.com/p/ep46-step-by-step-guide-on-system
- https://bytebytego.com/guides/system-design-blueprint-the-ultimate-guide/
- https://live.bytebytego.com/courses/ai-evals
