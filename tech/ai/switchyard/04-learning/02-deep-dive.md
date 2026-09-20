---
date: 2026-08-15
tags: [tech]
type: tech-tool-study
status: draft
---

# Switchyard Deep Dive

> [[01-getting-started|이전: Getting Started]] · [[../README|목차]] · [[../05-projects|다음: Projects]]

## Routing As A Decision System

Intelligent routing은 단순 load balancing이 아니다. 입력, trajectory state, judge verdict, policy threshold, session state가 target 선택에 영향을 준다. 따라서 평균 latency만 보지 말고 quality, cost, escalation, failure를 함께 평가해야 한다.

```text
request
  ├─ session affinity hit ───────────────→ pinned target
  └─ no affinity
       ├─ capability classifier ─────────→ efficient or capable
       ├─ escalation: efficient result
       │     └─ judge ───────────────────→ accept or rerun capable
       ├─ custom schema verdict ─────────→ policy-selected target
       └─ stage signals ─────────────────→ efficient or capable

invalid / unparseable verdict ───────────→ strong/default fallback
```

## LLM Classifier Modes

### Capability routing

Judge가 weak model이 요청을 해결할 확률 `p_solve`를 추정한다. threshold 이상이면 efficient target, 미만이면 capable target을 고른다.

설계 포인트:

- threshold는 비용 선호도가 아니라 evaluation set의 quality/cost frontier로 정한다.
- judge 자체의 latency와 token cost를 전체 비용에 포함한다.
- language, codebase size, tool availability별 calibration drift를 분리해 본다.
- parse failure가 strong/default로 가는지 failure injection으로 확인한다.

### Escalation routing

먼저 weak model을 호출하고 judge가 결과를 평가한다. 부족하면 strong model로 전체 요청을 재실행한다. quality-first cascade에는 유용하지만 worst-case latency와 token cost가 `weak + judge + strong`으로 늘어난다.

적합한 경우:

- weak result 자체를 평가할 수 있는 rubric이 있음
- 대부분 요청은 weak model로 해결되고 재실행 비율이 낮음
- tail latency보다 품질과 평균 비용을 중시함

### Custom routing

JSON Schema verdict와 policy로 두 개 이상의 target을 선택한다. 예를 들어 `risk`, `domain`, `needs_tools`, `context_pressure`를 verdict field로 정의할 수 있다. schema는 작고 결정 가능하게 유지하고, 허용되지 않은 값과 누락 field의 fallback을 명시한다.

## Stage Router

`stage_router`는 한 prompt만 분류하지 않고 agent trajectory에서 진행 상태를 추론한다.

| 신호 | 일반적 해석 | 후보 tier |
|---|---|---|
| critical error | 즉각적인 복구·추론 필요 | `capable` 강제 |
| 반복 작업, 같은 오류, 진전 부재 | agent가 stuck 상태 | `capable` |
| read/search/exploration 중심 | 문제 이해와 전략 수립 | `capable` |
| 최근 write/edit가 지속 | 계획이 정해진 production 단계 | `efficient` |
| 모호한 신호 | picker default 또는 optional classifier | policy에 따름 |

`efficient_first`는 cost-first, `capable_first`는 quality-first다. 공식 문서가 제안하는 `confidence_threshold = 0.5`는 시작점일 뿐이며 workload별 calibration이 필요하다. `capable_first`는 아직 benchmark되지 않은 experimental option으로 다룬다.

### Trajectory pitfalls

- tool name이 달라지면 read/write/error signal mapping이 깨질 수 있다.
- edit 횟수가 많아도 잘못된 방향으로 진행 중일 수 있다.
- session boundary가 너무 넓으면 이전 task의 stage가 새 task에 누출된다.
- compacted context나 provider별 tool trace 변환이 signal을 제거할 수 있다.

## Session Affinity

첫 routing decision을 이후 turn에 재사용하면 judge 호출과 model switching을 줄이고 cache locality를 높일 수 있다. 반면 초기에 잘못 선택한 tier가 고정될 수 있다.

검토 항목:

- session key의 source와 tenant isolation
- TTL, explicit reset, task boundary
- critical error가 affinity를 override하는 조건
- prompt cache와 model-specific conversation state의 호환성
- stats/log에 session ID를 남길 때 privacy와 cardinality

## Protocol Fidelity Tests

translation layer는 happy-path text보다 edge case에서 가치가 갈린다.

| 영역 | test case |
|---|---|
| Streaming | delta 순서, stop reason, usage-only final event, disconnect |
| Tool calls | parallel call, partial JSON arguments, call/result ID 보존 |
| Responses | reasoning item과 final-answer item 분리, multi-item output |
| Anthropic | content block 순서, tool result, error envelope |
| Usage | input/output/cache token, retry·escalation 중복 계산 |
| Errors | auth, rate limit, timeout, context overflow의 status/envelope mapping |

golden fixture를 protocol별로 만들고 다음 invariant를 검사한다.

```text
decode(inbound) → neutral types → encode(upstream)
decode(upstream) → neutral types → encode(client)
```

모든 provider field가 round-trip될 필요는 없지만 application이 의존하는 semantics는 반드시 보존되어야 한다.

## Observability And Evaluation

### Minimum telemetry

- client-facing route와 실제 serving target
- algorithm, tier, verdict, fallback reason
- end-to-end latency와 각 model/judge call latency
- input/output/cache token과 retry/escalation call count
- session affinity hit/miss
- translation, parse, upstream, context-overflow error

### Evaluation matrix

| 지표 | 질문 |
|---|---|
| Quality | capable-only baseline 대비 task success가 얼마나 유지되는가? |
| Cost | judge와 retry까지 포함해 request당 비용이 줄었는가? |
| Latency | median뿐 아니라 p95/p99와 escalation tail은 어떤가? |
| Safety | invalid verdict가 weak model로 fail-open하지 않는가? |
| Stability | 같은 session에서 불필요한 tier thrashing이 있는가? |
| Attribution | response, header, span, JSONL, billing의 model이 일치하는가? |

## Rollout Strategy

1. `passthrough`로 protocol parity와 telemetry를 검증한다.
2. production trace를 redaction한 evaluation set을 만든다.
3. `random` 또는 shadow decision으로 baseline을 수집한다.
4. router decision만 기록하고 실제 serving target은 고정한다.
5. low-risk traffic에 bounded canary를 적용한다.
6. quality, cost, latency guardrail을 통과하면 비율을 늘린다.
7. known issue와 version upgrade마다 regression suite를 다시 실행한다.

## Sources

- [LLM Classifier Routing](https://github.com/NVIDIA-NeMo/Switchyard/blob/main/docs/routing_algorithms/llm_classifier_routing.md)
- [Stage-Router Routing](https://github.com/NVIDIA-NeMo/Switchyard/blob/main/docs/routing_algorithms/stage_router_routing.md)
- [Protocol crate](https://github.com/NVIDIA-NeMo/Switchyard/blob/main/crates/protocol/README.md)
- [`libsy` README](https://github.com/NVIDIA-NeMo/Switchyard/blob/main/crates/libsy/README.md)

