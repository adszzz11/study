---
date: 2026-07-31
tags: [tech]
type: tech-tool-study
status: draft
---

# OmniRoute Cheatsheet

## Install & Run

```bash
# npm
npm install -g omniroute
omniroute

# diagnostics
omniroute doctor

# Docker: local-only port + persistent data
docker run -d \
  --name omniroute \
  --restart unless-stopped \
  --stop-timeout 40 \
  -p 127.0.0.1:20128:20128 \
  -v omniroute-data:/app/data \
  diegosouzapw/omniroute:latest
```

| 항목 | 기본값 |
|---|---|
| Dashboard | `http://localhost:20128` |
| API base URL | `http://localhost:20128/v1` |
| Client auth | `Authorization: Bearer <endpoint-key>` |
| Storage | SQLite/WAL |
| License | MIT |

## Security first

```bash
# 값을 출력한 뒤 secret manager에 보관
openssl rand -hex 32
```

```text
STORAGE_ENCRYPTION_KEY=<secret>
```

> [!WARNING]
> `STORAGE_ENCRYPTION_KEY`가 없으면 민감 정보는 plaintext passthrough mode다. “Local-first”여도 external provider로 route된 prompt와 output은 upstream으로 전달된다.

## Core API

```bash
# Models
curl http://localhost:20128/v1/models \
  -H "Authorization: Bearer YOUR_OMNIROUTE_KEY"

# Chat
curl -i http://localhost:20128/v1/chat/completions \
  -H "Authorization: Bearer YOUR_OMNIROUTE_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "auto",
    "messages": [{"role": "user", "content": "Hello"}]
  }'

# Streaming
curl --no-buffer http://localhost:20128/v1/chat/completions \
  -H "Authorization: Bearer YOUR_OMNIROUTE_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "auto/fast",
    "stream": true,
    "messages": [{"role": "user", "content": "Hello"}]
  }'
```

| Endpoint | 용도 |
|---|---|
| `/v1/chat/completions` | Chat Completions |
| `/v1/responses` | Responses API |
| `/v1/messages` | Anthropic-compatible messages |
| `/v1/models` | model catalog |
| `/v1/embeddings` | embeddings |
| `/v1/images/generations` | image generation |
| `/v1/audio/*` | audio |
| `/v1/search` | search |
| `/v1/rerank` | reranking |
| `/v1/moderations` | moderation |
| `/v1/ws` | WebSocket bridge |

## Auto model IDs

| Model | 최적화 방향 |
|---|---|
| `auto` | balanced, LKGP |
| `auto/coding` | coding quality |
| `auto/fast` | latency |
| `auto/cheap` | token cost |
| `auto/offline` | quota headroom |
| `auto/smart` | quality + exploration |
| `auto/coding:fast` | coding candidate + latency tier |
| `auto/reasoning:pro` | reasoning candidate + premium tier |
| `auto/multimodal:free` | multimodal candidate + free tier |

> Category/tier filter는 일치하는 candidate가 없을 때 fail-open할 수 있다. capability가 hard constraint라면 실제 candidate와 decision을 확인한다.

## 19 strategies

| 분류 | Strategies |
|---|---|
| 순서/분산 | `priority`, `fill-first`, `weighted`, `round-robin`, `random`, `strict-random` |
| 부하/상태 | `p2c`, `least-used`, `headroom`, `reset-window`, `reset-aware` |
| 비용/문맥 | `cost-optimized`, `context-optimized`, `cache-optimized` |
| 연속성 | `lkgp`, `context-relay` |
| 동적 | `auto` |
| 고급 실행 | `fusion`, `pipeline` |

## Useful headers

| Header | 방향 | 용도 |
|---|---|---|
| `Authorization: Bearer ...` | Request | client API key |
| `Idempotency-Key` | Request | 짧은 window의 request deduplication |
| `X-Session-Id` | Request | sticky session key |
| `X-OmniRoute-No-Cache: true` | Request | cache bypass |
| `x-omniroute-no-memory: true` | Request | memory/skills injection bypass |
| `X-OmniRoute-Decision` | Response | strategy, provider, latency routing trace |
| `X-OmniRoute-Cache` | Response | `HIT` 또는 `MISS` |
| `X-OmniRoute-Idempotent` | Response | deduplicated 여부 |
| `X-OmniRoute-Version` | Response | serving build version |

설치 version에 따라 header와 허용 값이 바뀔 수 있으므로 API Reference를 최종 기준으로 삼는다.

## OpenAI SDK

```python
from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:20128/v1",
    api_key="YOUR_OMNIROUTE_KEY",
)

result = client.chat.completions.create(
    model="auto/coding",
    messages=[{"role": "user", "content": "Review this function."}],
)

print(result.choices[0].message.content)
```

## Failure model

```text
1. Connection/account
   └─ same provider, another account
2. Combo/model
   └─ another provider or model
3. System
   └─ retry, cooldown, circuit breaker, lockout, dedup
```

## Debug order

```text
401 → endpoint API key / Bearer header
  ↓
empty models → provider connection / OAuth / catalog
  ↓
429 → quota / reset window / candidate connections
  ↓
5xx → upstream health / circuit / fallback log
  ↓
stream break → SSE client / reverse-proxy buffering
  ↓
wrong route → candidate pool / pricing / latency / health
```

## Production checklist

- [ ] version pin
- [ ] `STORAGE_ENCRYPTION_KEY`
- [ ] SQLite + encryption key 분리 backup
- [ ] loopback 또는 TLS reverse proxy
- [ ] dashboard/management route 보호
- [ ] scoped API key와 log redaction
- [ ] streaming/tool call/structured output test
- [ ] account/model/system failure injection
- [ ] p95/p99, error, fallback depth alert
- [ ] upstream terms와 data handling 검토
- [ ] upgrade rollback drill

## Sources

- https://github.com/diegosouzapw/OmniRoute
- https://github.com/diegosouzapw/OmniRoute/blob/release/v3.8.50/docs/reference/API_REFERENCE.md
- https://github.com/diegosouzapw/OmniRoute/blob/release/v3.8.50/docs/routing/AUTO-COMBO.md
- https://github.com/diegosouzapw/OmniRoute/blob/release/v3.8.50/SECURITY.md

