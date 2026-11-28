---
date: 2026-11-12
tags: [tech]
type: tech-tool-study
status: draft
---

# Ecosystem: 대안과 비교

> [[tech/infra/jane-street-technology-ecosystem/README|목차]] · [[tech/infra/jane-street-technology-ecosystem/03-references|다음: References]]

## 경쟁·대안 지형

| 대상 | 중심 언어/접근 | Jane Street와의 차이 |
|---|---|---|
| Jane Street | OCaml, functional programming, in-house platform | language·library·compiler·performance tool까지 수직 통합 성격이 강하다. |
| Hudson River Trading | C++/Python quantitative trading으로 널리 알려짐 | 같은 low-latency quant 영역이지만 Jane Street는 공개 OCaml ecosystem 존재감이 크다. |
| Jump Trading | C++/systems engineering·trading infrastructure | ultra-low-latency 경쟁군; `Base/Core/Async/Bonsai` 공개 stack이 차별점이다. |
| Citadel Securities | 대규모 electronic market making | 시장 기능은 가깝지만 공개 개발 platform보다 execution 조직으로 더 알려져 있다. |
| OCaml stdlib + Lwt/Eio | 범용 stdlib 및 concurrency 대안 | `Base/Core/Async`는 opinionated production stack이며 concurrency model도 다르다. |
| `perf` | Linux sampling/performance analysis | `magic-trace`는 Intel PT control-flow history를 보완적으로 제공한다. |

## Concurrency 선택

| 모델 | 강점 | 주의점 |
|---|---|---|
| `Async` / `Deferred` | Jane Street library와 자연스러운 결합, event loop 중심 I/O | 프로젝트 전반의 scheduler/abstraction 선택에 영향 |
| Lwt | 넓은 OCaml ecosystem, cooperative promise style | Async API와 직접 호환되지 않음 |
| Eio | effect 기반 structured concurrency 지향 | 기존 Async codebase와 migration 비용 존재 |

서로를 “더 빠른 것”으로 단순 비교하지 않는다. cancellation, resource lifetime, library compatibility, 팀의 debugging model까지 포함해 판단한다.

## Profiler 선택

`perf`는 CPU, scheduler, cache 등 Linux system-level 사실을 폭넓게 수집한다. `magic-trace`는 supported Intel Processor Trace 환경에서 특정 시점 바로 전의 control flow를 세밀하게 탐색하는 데 유리하다. latency incident에는 둘을 함께 두고, trace 가능성·CPU overhead·hardware/VM 제약을 먼저 확인한다.

## Sources

- https://github.com/janestreet/async_kernel
- https://github.com/janestreet/magic-trace
- https://ocaml.org/docs/concurrency
- https://perf.wiki.kernel.org/
