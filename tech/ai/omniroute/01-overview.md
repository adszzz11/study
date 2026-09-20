---
date: 2026-07-31
tags: [tech]
type: tech-tool-study
status: draft
---

# OmniRoute Overview

## What

OmniRoute는 여러 LLM provider와 account를 단일 OpenAI-compatible API 뒤에 배치하는 self-hosted AI gateway다. application은 하나의 `/v1/*` endpoint만 호출하고, OmniRoute가 provider별 authentication, request/response translation, streaming, routing, fallback, usage logging을 처리한다.

주요 interface는 다음과 같다.

| 영역 | Endpoint 예시 | 역할 |
|---|---|---|
| Text | `/v1/chat/completions`, `/v1/responses`, `/v1/messages` | OpenAI·Responses·Anthropic 계열 호환 |
| Discovery | `/v1/models` | 연결된 model 및 virtual route 조회 |
| Retrieval | `/v1/embeddings`, `/v1/search`, `/v1/rerank` | embedding, search, reranking |
| Media | `/v1/images/generations`, `/v1/audio/*` | image와 audio 작업 |
| Safety | `/v1/moderations` | moderation 요청 |
| Streaming | SSE, `/v1/ws` | streaming 및 WebSocket bridge |

## Why

AI application이나 coding agent가 provider를 직접 호출하면 integration과 운영 상태가 client에 누적된다.

| 문제 | 직접 연동 시 결과 | OmniRoute의 접근 |
|---|---|---|
| API dialect 차이 | schema, role, tool call, reasoning 처리 분기 | request/response normalization |
| quota와 rate limit | account 하나의 소진이 workflow 중단으로 연결 | account selection과 quota preflight |
| 장애와 성능 편차 | static endpoint에 종속 | health·latency 기반 routing과 fallback |
| credential 분산 | client마다 key와 OAuth session 관리 | connection layer와 local persistence |
| 비용 가시성 부족 | provider dashboard를 따로 확인 | usage·cost·latency telemetry 통합 |
| client 재설정 | provider를 바꿀 때마다 base URL/model 변경 | 하나의 `/v1` endpoint와 alias/combo 사용 |

## 핵심 개념

### Connection

`Connection`은 provider에 접근하는 실제 credential 단위다. 하나의 provider에 여러 OAuth account 또는 API key connection을 둘 수 있다. 따라서 routing target은 단순한 `provider + model`이 아니라 다음과 같이 이해해야 한다.

```text
target = provider + model + connection/account
```

### Combo

`Combo`는 여러 target과 execution policy를 묶은 route다. 단순 fallback chain부터 load distribution, cost optimization, multi-model orchestration까지 표현한다.

| 목적 | Strategy |
|---|---|
| 순서와 분산 | `priority`, `fill-first`, `weighted`, `round-robin`, `random` |
| 부하와 상태 | `p2c`, `least-used`, `headroom`, `reset-aware` |
| 비용과 문맥 | `cost-optimized`, `context-optimized`, `cache-optimized` |
| 연속성 | `lkgp`, `context-relay` |
| 동적 선택 | `auto` |
| 고급 실행 | `fusion`, `pipeline` |

`fusion`은 여러 model에 병렬 질의한 뒤 judge model이 결과를 합성한다. `pipeline`은 한 step의 output을 다음 step의 input으로 넘긴다. 둘 다 일반 fallback보다 비용과 latency가 커지므로 명시적으로 선택하는 orchestration 기능으로 본다.

### Auto-Combo

`auto`, `auto/coding`, `auto/fast`, `auto/cheap`, `auto/offline` 같은 virtual model ID는 저장된 combo 없이 현재 연결을 후보 pool로 만든다.

```json
{
  "model": "auto/coding",
  "messages": [
    {"role": "user", "content": "이 TypeScript 오류를 분석해줘."}
  ]
}
```

후보 scoring에는 health와 circuit-breaker state, quota headroom, token cost, p95 latency, task fit, stability, account tier, context-window affinity, connection density, reset-window affinity 등이 관여한다. 이는 “항상 가장 좋은 model”을 보장하는 benchmark가 아니라 현재 관측값과 policy로 target을 고르는 heuristic이다.

## Request lifecycle

```text
1. Client authentication
2. Request shape / role / parameter normalization
3. Alias, direct model, Combo 또는 Auto-Combo 해석
4. Quota preflight와 healthy candidate 선별
5. Connection/account 선택
6. Provider request translation과 upstream 호출
7. Retry / cooldown / circuit breaker / fallback
8. Response normalization과 streaming
9. Usage / cost / latency / decision 기록
```

예를 들어 OpenAI SDK가 보내는 `developer` role을 upstream이 이해하는 `system` role로 바꾸거나, OpenAI의 `json_schema`를 Gemini의 `responseSchema`로 변환할 수 있다. 엄격한 OpenAI SDK가 거부할 수 있는 추가 field를 정리하는 response sanitization도 compatibility layer의 책임이다.

## 3-layer resilience

| Layer | 실패 예 | 대응 |
|---|---|---|
| Connection/account | 특정 account quota 소진, token 만료 | 같은 provider의 다른 connection 선택 |
| Combo/model | provider 장애, model unavailable | 다른 provider 또는 model로 fallback |
| System | 일시 오류, 반복 요청, 장애 확산 | retry, cooldown, circuit breaker, lockout, deduplication |

Quota preflight, P2C selection, exponential backoff, anti-thundering-herd mutex, 3-state circuit breaker, last-known-good route가 함께 동작한다. runtime state는 memory에 유지하면서 SQLite에 write-through하고 cold start 때 복원한다.

## Persistence와 observability

주 저장소는 `better-sqlite3` 기반 SQLite/WAL이다.

- provider connection, API key, alias, combo, pricing, settings
- usage history, call/proxy log, audit log, MCP call log
- budget, fallback chain, lockout, circuit-breaker state
- p50/p95/p99 latency와 cost telemetry
- memory용 FTS5와 vector embedding

SQLite는 single-node와 local deployment를 단순하게 만든다. 반면 high-availability multi-replica 환경에서는 database sharing, state consistency, failover를 별도로 설계하고 검증해야 한다.

## 특징과 한계

### 특징

- OAuth subscription account를 API-key provider와 같은 routing pool에 포함
- OpenAI-compatible endpoint를 중심으로 Anthropic·Gemini dialect까지 translation
- quota, health, cost, latency를 함께 보는 Combo와 Auto-Combo
- local dashboard, SQLite persistence, usage/cost/latency telemetry
- optional guardrails, compression, memory, MCP, A2A를 같은 runtime에서 제공
- MIT license와 self-hosted deployment

### 한계와 주의

- provider 수와 free-tier 수는 release마다 변하며 프로젝트 측 집계다.
- unofficial integration은 upstream 약관, account 정책, authentication 안정성을 직접 검토해야 한다.
- translation layer가 모든 provider-specific semantic을 완전히 동일하게 만들지는 않는다.
- gateway는 새로운 single point of failure가 될 수 있으므로 backup, health check, upgrade rollback이 필요하다.
- local gateway를 사용해도 external upstream으로 보낸 data는 local에만 머물지 않는다.
- built-in guardrail은 best-effort heuristic이며 완전한 prompt-injection firewall이 아니다.

## Sources

- https://github.com/diegosouzapw/OmniRoute
- https://github.com/diegosouzapw/OmniRoute/blob/release/v3.8.50/docs/architecture/ARCHITECTURE.md
- https://github.com/diegosouzapw/OmniRoute/blob/release/v3.8.50/docs/reference/API_REFERENCE.md
- https://github.com/diegosouzapw/OmniRoute/blob/release/v3.8.50/docs/routing/AUTO-COMBO.md
- https://github.com/diegosouzapw/OmniRoute/blob/release/v3.8.50/docs/architecture/RESILIENCE_GUIDE.md

