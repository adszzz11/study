---
date: 2026-11-12
tags: [tech]
type: tech-tool-study
status: draft
---

# Deep Dive: Incremental, Bonsai, OxCaml, Tracing

> [[tech/infra/jane-street-technology-ecosystem/README|목차]] · [[tech/infra/jane-street-technology-ecosystem/05-projects|다음: Projects]]

## Incremental computation

`Incremental`은 dependency graph에서 input이 변했을 때 그 변경에 의존하는 node만 재계산한다. 예를 들어 가격 하나가 바뀌면 해당 instrument, portfolio aggregate, 관련 risk widget만 invalidation 대상이 된다. 이는 “모든 것을 매 tick 다시 계산”하는 구현과 대비해 latency와 UI noise를 낮출 수 있다.

```text
price[A] ─┐
          ├→ position[A] → portfolio delta → risk panel
fx rate ─┘
price[B] ───────────────→ position[B] ────────┘
```

graph identity, cutoff/equality, stale data 처리와 side effect 경계를 명확히 해야 한다. incremental engine이 market data correctness를 자동으로 보장하지는 않는다.

## Bonsai UI

`Bonsai`는 Incremental 위에 declarative web UI를 구성한다. view와 state transition을 명시하고, live market-data UI에서 필요한 selective recomputation을 활용한다. browser 연결 전 model을 독립적으로 test하여 business rule과 rendering을 분리한다.

## OxCaml modes

mode system은 `local`, `portable`, `once` 같은 성질을 통해 값의 scope, allocation, thread sharing/portability, linear usage를 type level에서 표현하려는 방향이다. 실험 순서는 다음이 안전하다.

1. 작은 allocation-sensitive function에서 annotation을 읽고 compiler error를 기록한다.
2. thread/parallel boundary에 넘길 값의 portability 제약을 확인한다.
3. stable OCaml fallback과 benchmark를 유지한다.
4. 지원 상태·migration 비용이 확인되기 전 production foundation으로 확장하지 않는다.

## Latency incident tracing

1. request ID와 monotonic timestamp로 slow path를 재현한다.
2. `perf`로 CPU scheduling, syscall, cache 등 broad symptom을 먼저 확인한다.
3. hardware와 kernel 조건을 만족할 때 `magic-trace`로 incident 직전 call timeline을 조사한다.
4. trace는 sensitive code path를 노출할 수 있으므로 retention/access policy를 적용한다.

> [!WARNING]
> `magic-trace`는 Intel Processor Trace와 Linux 환경 제약이 있다. VM passthrough와 CPU generation을 사전에 검증하고, unsupported host에서 “trace가 비어 있음”을 application bug로 단정하지 않는다.

## Sources

- https://github.com/janestreet/incremental
- https://github.com/janestreet/bonsai
- https://oxcaml.org/documentation/modes/intro/
- https://github.com/janestreet/magic-trace
