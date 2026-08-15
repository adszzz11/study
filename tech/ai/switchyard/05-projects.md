---
date: 2026-08-15
tags: [tech]
type: tech-tool-study
status: draft
---

# Switchyard Projects

> [[04-learning/02-deep-dive|이전: Deep Dive]] · [[README|목차]] · [[cheatsheet|다음: Cheatsheet]]

## Project 1: Protocol Bridge Smoke Test

### Goal

Anthropic-compatible client의 요청을 OpenAI-compatible local backend로 보내며 text, streaming, tool call semantics가 보존되는지 검증한다.

### Scope

- `passthrough` route 하나
- `llm_client` 하나와 target 하나
- `/v1/messages` inbound → `openai_chat` upstream
- golden fixtures: text, streaming, single tool call, error envelope

### Done Criteria

- [ ] 네 fixture가 반복 실행 가능하다.
- [ ] tool call/result ID와 stop reason이 보존된다.
- [ ] response `model`, routing header, log target이 일치한다.
- [ ] timeout과 invalid key가 client-compatible error로 반환된다.

## Project 2: Weak/Strong Capability Router

### Goal

efficient model과 capable model을 `llm_classifier` capability mode로 선택하고 capable-only baseline 대비 quality/cost frontier를 측정한다.

### Dataset

| 유형 | 예시 | 기대 tier |
|---|---|---|
| 단순 변환 | format 변경, 짧은 extraction | efficient |
| 지역 수정 | 명확한 한 파일 bug fix | efficient 또는 capable |
| 복합 추론 | 여러 module root-cause 분석 | capable |
| 복구 | 실패한 tool trace와 반복 error | capable |
| 장문 context | 큰 repository와 긴 history | workload에 따라 측정 |

### Experiment

1. capable-only, efficient-only baseline을 수집한다.
2. classifier decision만 shadow로 기록한다.
3. threshold sweep으로 success, token, latency를 비교한다.
4. invalid verdict, judge timeout, rate limit을 주입한다.
5. fallback이 strong/default로 안전하게 작동하는지 확인한다.

### Done Criteria

- [ ] judge 비용을 포함한 total cost를 계산했다.
- [ ] threshold별 confusion matrix와 task success가 있다.
- [ ] p95 latency와 escalation rate를 기록했다.
- [ ] quality guardrail을 깨면 즉시 passthrough capable route로 되돌릴 수 있다.

## Project 3: Coding-Agent Stage Router

### Goal

coding session의 exploration, stuck, production 단계를 구분해 capable/efficient model을 전환한다.

### Design

```text
read/search + ambiguity ──→ capable
critical/repeated error ──→ capable
stable write/edit loop ───→ efficient
uncertain signal ─────────→ picker default or classifier
```

### Evaluation

- 동일한 task set을 capable-only, efficient-first, stage-router로 실행
- task completion, human review score, wall time, total token 비교
- tool name과 trace format이 바뀌어도 signal extraction이 유지되는지 확인
- session affinity on/off와 reset boundary 비교

> [!warning]
> `capable_first`는 공식 문서상 아직 benchmark되지 않은 experimental option이다. 초기 project에서는 `efficient_first`와 capable-only baseline부터 비교한다.

## Project 4: Observability Dashboard

### Goal

Prometheus metrics, OpenTelemetry span, `/v1/stats`, JSONL routing log를 하나의 evaluation view로 연결한다.

### Dashboard Panels

- route·target·algorithm별 request rate
- end-to-end 및 upstream p50/p95/p99 latency
- efficient/capable selection과 escalation ratio
- input/output/cache token, retry count, estimated cost
- classifier parse failure, context overflow, upstream error
- session affinity hit rate와 target switching

### Guardrails

- high-cardinality session ID는 metric label로 직접 쓰지 않는다.
- prompt/tool payload는 기본 수집하지 않고 필요한 경우 redact한다.
- response/header/log/billing attribution mismatch를 정기 검사한다.
- stats known issue가 dashboard에 주는 영향을 별도 annotation한다.

## Project 5: `libsy` Embedding Spike

### Goal

기존 Rust gateway에 routing algorithm을 내장하고 network proxy hop 없이 `Step::CallModel`을 처리한다.

### Host Responsibilities

- model HTTP call과 streaming transport
- secret, timeout, retry budget
- `Step::CallModel` 결과를 algorithm state machine에 반환
- trace propagation과 cancellation
- tenant/session isolation

### Decision Record

spike 종료 시 standalone server와 embedded library를 다음 기준으로 비교한다.

| 기준 | Standalone server | Embedded `libsy` |
|---|---|---|
| 배포 독립성 | 높음 | host release에 결합 |
| integration effort | 낮음 | 높음 |
| transport control | proxy boundary | host가 완전 통제 |
| network hop | 추가 | 없음 |
| failure isolation | process 단위 | host process와 공유 |

## Sources

- [Getting Started](https://github.com/NVIDIA-NeMo/Switchyard/blob/main/docs/getting_started.md)
- [LLM Classifier Routing](https://github.com/NVIDIA-NeMo/Switchyard/blob/main/docs/routing_algorithms/llm_classifier_routing.md)
- [Stage-Router Routing](https://github.com/NVIDIA-NeMo/Switchyard/blob/main/docs/routing_algorithms/stage_router_routing.md)
- [`libsy` README](https://github.com/NVIDIA-NeMo/Switchyard/blob/main/crates/libsy/README.md)

