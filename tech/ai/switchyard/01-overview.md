---
date: 2026-08-15
tags: [tech]
type: tech-tool-study
status: draft
---

# Switchyard Overview

> [[README|목차]] · [[02-ecosystem|다음: Ecosystem]]

## What

NVIDIA NeMo Switchyard는 LLM client와 model backend 사이에 놓이는 traffic orchestration layer다. client에는 OpenAI 또는 Anthropic compatible API를 제공하고, 내부에서는 request를 provider-neutral representation으로 바꾼 다음 routing policy에 따라 target과 transport를 선택한다.

```text
OpenAI / Anthropic client
          ↓
switchyard-server endpoint
          ↓ decode
provider-neutral Request
          ↓ route algorithm
Target + LLM Client
          ↓ encode
OpenAI / Anthropic / OpenRouter / vLLM / Ollama / NIM
          ↓ decode + translate
client-compatible response / stream
```

여기서 Switchyard는 동명의 JBoss SOA framework나 network emulator가 아니라 **NVIDIA NeMo Switchyard**를 뜻한다.

## Why

하나의 고성능 model만 쓰면 단순 요청에도 비용과 latency가 커진다. 반대로 저가·소형 model만 쓰면 복잡한 reasoning, exploration, error recovery에서 성공률이 낮아진다. 요청 또는 agent trajectory에 따라 weak/efficient model과 strong/capable model을 선택하면 비용·속도·품질을 함께 조절할 수 있다.

Switchyard가 다루는 구체적인 문제는 다음과 같다.

- OpenAI Chat Completions, Responses, Anthropic Messages의 request, streaming, tool-call 형식 차이
- 특정 API semantics에 의존하는 coding agent와 실제 inference backend 사이의 결합
- task complexity나 오류 상태를 이해하지 못하는 단순 round-robin
- routing 도입 후 필요한 target, token, cache, retry, latency 관측
- proxy에 결합된 routing algorithm의 낮은 재사용성

## Architecture

### Configuration layers

| 계층 | 책임 | 예시 질문 |
|---|---|---|
| `llm_clients` | `base_url`, wire format, credential env, retry policy | 어떤 protocol로 어디에 연결하는가? |
| `targets` | upstream model ID와 `llm_client` 연결 | 실제 어떤 model을 serving하는가? |
| `routes` | client-facing model ID와 selection algorithm | 요청을 어느 target으로 보낼 것인가? |

여러 target은 하나의 transport 설정을 공유할 수 있고, 여러 route는 같은 target을 재사용할 수 있다. secret 값은 TOML에 직접 넣지 않고 `api_key_env`에 환경변수 이름만 지정한다.

### Execution forms

| 형태 | 특징 | 선택 기준 |
|---|---|---|
| `switchyard-server` | native Rust standalone HTTP proxy | 독립 gateway로 빠르게 도입 |
| `switchyard-libsy` | routing state machine을 Rust host에 내장 | 기존 gateway/runtime과 통합 |
| Python/PyO3 | Python에서 native algorithm 호출 또는 server in-process 실행 | Python experiment와 embedding |
| Agent launcher | local proxy와 Claude/Codex/OpenClaw 환경 설정 관리 | coding-agent 실험 |

`libsy`는 직접 HTTP request를 보내지 않는다. `Step::CallModel`을 host에 넘기고 host가 실행 결과를 되돌려주는 inversion-of-control 구조이므로 transport, secret, telemetry 정책을 host가 소유할 수 있다.

## Core Features

### Routing

| Algorithm | 동작 | 대표 용도 |
|---|---|---|
| `passthrough` | 항상 하나의 target 선택 | protocol bridge, baseline |
| `random` | uniform 또는 weighted split | A/B test, traffic sampling |
| `llm_classifier` capability | judge가 weak model의 성공 확률 `p_solve` 추정 | complexity routing |
| `llm_classifier` escalation | weak 결과를 평가하고 필요하면 strong으로 재실행 | quality-first cascade |
| `llm_classifier` custom | JSON Schema verdict와 policy로 2개 이상 target 선택 | domain-specific policy |
| `stage_router` | tool result, 오류, 탐색, edit 진행 신호로 agent stage 판단 | 긴 coding-agent trajectory |

Classifier verdict가 invalid하거나 parsing에 실패하면 strong/default target으로 fallback한다. Session affinity를 사용하면 첫 선택을 이후 turn에도 재사용해 judge 호출과 model switching을 줄일 수 있다.

### Protocol translation

`switchyard-protocol`은 conversation, instruction, content block, tool call/result, usage, routing decision, streaming event를 provider-neutral Rust type으로 표현한다. `switchyard-translation`은 다음 wire format을 상호 변환한다.

- `openai_chat`
- `openai_responses`
- `anthropic_messages`

v0.2.0은 streaming, tool trace, Responses reasoning/final-answer item, prompt-cache token usage, Anthropic error envelope 보존을 강화했다.

### Operations

- TLS, graceful shutdown, bounded upstream retry
- context-window overflow 시 다른 route target 시도
- `GET /health`, `GET /v1/models`, Prometheus `/metrics`
- GenAI semantic attributes 기반 OpenTelemetry spans
- `/v1/stats`, `/v1/stats/reset`
- optional per-session stats와 durable JSONL routing log
- response `model` 및 routing header에 실제 serving target 기록

## Maturity And Risks

v0.2.0은 2026-08-10 공개된 pre-alpha release이며 PyPI 상태는 Alpha다. `main`의 Unreleased changelog에서는 legacy `switchyard serve`, YAML route bundle, FastAPI endpoint, Python chain이 제거되었다. 새 실습은 **native TOML + `switchyard-server`** 기준으로 구성해야 한다.

공개된 known issues에는 다음이 포함된다.

- client disconnect 후 buffered upstream 작업이 계속될 수 있음
- 일부 routing decision의 tier attribution 누락
- retry recovery counter 오류
- session ID stats 누락

따라서 timeout, concurrency, cost ceiling을 외부에서도 제한하고, routing log와 provider billing을 대조해야 한다.

## Sources

- [v0.2.0 Changelog](https://github.com/NVIDIA-NeMo/Switchyard/blob/main/CHANGELOG.md)
- [Core Concepts](https://github.com/NVIDIA-NeMo/Switchyard/blob/main/docs/core_concepts.md)
- [Protocol crate](https://github.com/NVIDIA-NeMo/Switchyard/blob/main/crates/protocol/README.md)
- [`libsy` README](https://github.com/NVIDIA-NeMo/Switchyard/blob/main/crates/libsy/README.md)

