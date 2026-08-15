---
date: 2026-08-15
tags: [tech]
type: tech-tool-study
status: draft
---

# Switchyard Cheatsheet

> [[05-projects|이전: Projects]] · [[README|목차]]

## Identity

| 항목 | 값 |
|---|---|
| Project | NVIDIA NeMo Switchyard |
| 기준 version | v0.2.0, 2026-08-10 |
| 성숙도 | pre-alpha / PyPI Alpha |
| 신규 구성 기준 | native TOML + `switchyard-server` |
| 핵심 역할 | protocol translation, intelligent routing, fallback, affinity, observability |

## Request Flow

```text
client protocol
  → decode to neutral Request
  → route algorithm
  → target + llm_client
  → encode upstream
  → decode response/stream
  → encode client protocol
```

## Configuration Vocabulary

| 이름 | 기억할 것 |
|---|---|
| `llm_clients` | endpoint, wire format, `api_key_env`, retry |
| `targets` | 실제 upstream model ID + `llm_client` |
| `routes` | client-facing model ID + algorithm |
| `api_key_env` | secret 값이 아니라 환경변수 **이름** |

## Algorithms

| Algorithm | 한 줄 선택 기준 |
|---|---|
| `passthrough` | translation baseline 또는 target 하나 |
| `random` | uniform/weighted traffic split |
| classifier capability | 요청 전 `p_solve`로 weak/strong 선택 |
| classifier escalation | weak 결과 평가 후 필요하면 strong 재실행 |
| classifier custom | JSON Schema verdict로 domain policy 적용 |
| `stage_router` | coding-agent trajectory의 탐색·오류·edit 단계 활용 |

### Safe Defaults

- invalid/unparseable classifier verdict → strong/default fallback
- stage router threshold 시작점 → `0.5`, 반드시 workload로 재보정
- `efficient_first` → cost-first
- `capable_first` → quality-first, 아직 experimental/unbenchmarked
- routing 추가 전 → `passthrough` parity test

## Endpoints

| Endpoint | 용도 |
|---|---|
| `/v1/chat/completions` | OpenAI Chat Completions-compatible |
| `/v1/responses` | OpenAI Responses-compatible |
| `/v1/messages` | Anthropic Messages-compatible |
| token counting endpoint | client-side token estimation 지원 |
| `GET /v1/models` | client-facing model discovery |
| `GET /health` | health check |
| `/metrics` | Prometheus metrics |
| `/v1/stats` | runtime routing statistics |
| `/v1/stats/reset` | statistics reset |

정확한 HTTP method와 token counting path는 실행 중인 v0.2.0 공식 문서 또는 binary help로 확인한다.

## Commands

```bash
# isolated install
python -m venv .venv
source .venv/bin/activate
python -m pip install 'nemo-switchyard==0.2.0'

# installed CLI surface 확인
switchyard --help
switchyard-server --help

# coding-agent launcher surface 확인
switchyard launch claude --help
switchyard launch codex --help
switchyard launch openclaw --help

# server smoke checks: PORT를 실제 값으로 교체
curl -fsS http://127.0.0.1:PORT/health
curl -fsS http://127.0.0.1:PORT/v1/models
curl -fsS http://127.0.0.1:PORT/metrics
curl -fsS http://127.0.0.1:PORT/v1/stats
```

## Protocol Formats

- `openai_chat`
- `openai_responses`
- `anthropic_messages`

반드시 시험할 edge case:

- streaming delta와 terminal event
- parallel/partial tool call과 call/result ID
- Responses reasoning/final-answer item
- prompt-cache token usage
- Anthropic error envelope
- context overflow, retry, client disconnect

## Observability Checklist

- [ ] client-facing route와 actual serving target
- [ ] algorithm, tier, verdict, fallback reason
- [ ] end-to-end/model/judge latency
- [ ] input/output/cache token
- [ ] retry와 escalation call count
- [ ] session affinity hit/miss
- [ ] response `model`, routing header, span, JSONL attribution 일치
- [ ] prompt/tool payload redaction과 retention policy

## Known Risks In v0.2.0

- client disconnect 뒤 buffered upstream 작업 지속 가능
- 일부 routing decision tier attribution 누락
- retry recovery counter 오류
- session ID stats 누락
- `main` 문서와 release binary 사이의 schema/CLI drift

## Rollout Ladder

```text
passthrough parity
  → offline evaluation
  → shadow decision
  → bounded canary
  → guardrail review
  → gradual rollout
```

## Sources

- [v0.2.0 Release](https://github.com/NVIDIA-NeMo/Switchyard/releases/tag/v0.2.0)
- [Core Concepts](https://github.com/NVIDIA-NeMo/Switchyard/blob/main/docs/core_concepts.md)
- [Getting Started](https://github.com/NVIDIA-NeMo/Switchyard/blob/main/docs/getting_started.md)
- [Routing documentation](https://github.com/NVIDIA-NeMo/Switchyard/tree/main/docs/routing_algorithms)

