---
date: 2026-09-20
tags: [tech]
type: tech-tool-study
status: draft
---

# ByteByteGo Projects

## 권장 실습 환경

TypeScript/Node.js 또는 Python/FastAPI, PostgreSQL, Redis, Kafka/SQS 계열, Docker, OpenTelemetry 조합으로 시작한다. AI 프로젝트에는 embedding, vector database, RAG, LLM evals, tracing, guardrails, cost/latency 측정을 추가한다.

## 1. URL Shortener

- Redis `cache-aside`, PostgreSQL 또는 DynamoDB, rate limiter, Snowflake/UUID 기반 ID, metrics를 구현한다.
- 검증: cache hit ratio, p95 redirect latency, collision 처리, DB fallback을 측정한다.
- 확장: expiration, custom alias, abuse detection을 추가한다.

## 2. Notification Platform

- API Gateway, queue, worker, provider adapter, retry/DLQ, per-user preference를 구현한다.
- `at-least-once delivery`에서 idempotency key로 중복을 처리한다.
- 검증: provider timeout, worker 재시작, poison message, 순서 보장 필요 여부를 테스트한다.

## 3. Mini Search / RAG Service

- 문서 ingestion, embedding, vector DB, retrieval, citation response, offline eval dataset, cost/latency dashboard를 구성한다.
- 검증: retrieval quality, citation coverage, prompt-injection test case, token cost를 기록한다.

## 4. System-design Decision Record 저장소

각 설계를 ADR처럼 축적한다.

```markdown
# Decision: cache-aside 도입
## Requirements / Estimate
## Diagram
## Options and Trade-offs
## Failure Modes
## Metrics
## Migration / Rollback Plan
```

## Sources

- https://bytebytego.com/guides/system-design-blueprint-the-ultimate-guide/
- https://bytebytego.com/guides/learn-cache/
- https://blog.bytebytego.com/p/our-new-book-generative-ai-system
