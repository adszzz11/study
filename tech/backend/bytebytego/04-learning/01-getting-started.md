---
date: 2026-09-20
tags: [tech]
type: tech-tool-study
status: draft
---

# Getting Started: System Design 첫 바퀴

## 목표

URL shortener 하나를 선택해 request path, data path, bottleneck, trade-off를 설명할 수 있게 한다. 처음에는 완전한 구현보다 **한 장의 설계도와 근거**를 만든다.

## 1. 컴포넌트 순서대로 훑기

```text
Client → HTTP/API → Load Balancer → App → Cache → Database
                                  └→ Queue → Worker
Client ← CDN (static content)
```

- `HTTP/API`: request/response contract와 authentication을 정의한다.
- `Load Balancer`: 다수 application instance로 요청을 분산한다.
- `Cache`: hot read를 cache-aside로 빠르게 처리한다.
- `Database`: source of truth와 durability를 책임진다.
- `Queue/Worker`: 느리거나 재시도 가능한 작업을 비동기화한다.
- `CDN`: 정적·cacheable content의 origin 부하와 latency를 줄인다.

## 2. URL shortener 설계 노트

| 항목 | 첫 질문 | 예시 결정 |
| --- | --- | --- |
| API | 생성·redirect contract는? | `POST /urls`, `GET /{code}` |
| data model | 무엇을 영속화하는가? | `code`, `long_url`, `created_at`, `expires_at` |
| estimate | QPS와 storage는? | read-heavy 여부와 TTL을 명시 |
| cache | miss와 invalidation은? | Redis cache-aside, TTL |
| protection | abuse는? | IP/user rate limiting |
| ID | 충돌 없는 short code는? | Snowflake-like ID 또는 UUID 후 encoding |

```text
POST /urls → API → DB write
GET /abc123 → cache hit → 302 redirect
             cache miss → DB → cache populate → 302 redirect
```

## 3. 선택을 문장으로 설명하기

같은 요구사항에 대해 다음을 고르고 이유를 latency, availability, cost로 설명한다.

- SQL vs NoSQL: transaction/query 요구와 access pattern은 무엇인가?
- synchronous vs asynchronous: 사용자 응답을 기다려야 하는가?
- strong vs eventual consistency: 오래된 읽기가 허용되는가?

## 완료 기준

- [ ] API와 data model을 적었다.
- [ ] QPS, storage, read/write 비율을 가정으로 명시했다.
- [ ] cache miss와 DB 장애 시 동작을 설명했다.
- [ ] 선택 하나 이상을 수치 또는 요구사항으로 정당화했다.

다음: [[02-deep-dive]] · 프로젝트 확장: [[../05-projects]]

## Sources

- https://bytebytego.com/guides/system-design-blueprint-the-ultimate-guide/
- https://bytebytego.com/guides/learn-cache/
- https://blog.bytebytego.com/p/ep46-step-by-step-guide-on-system
