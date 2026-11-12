---
date: 2026-11-12
tags: [tech]
type: tech-tool-study
status: draft
---

# Overview: OCaml-first Trading Platform

> [[tech/infra/jane-street-technology-ecosystem/README|목차]] · [[tech/infra/jane-street-technology-ecosystem/02-ecosystem|다음: Ecosystem]]

## What

Jane Street는 global electronic market maker이며, 거래·research·engineering이 공유하는 in-house software platform을 핵심 경쟁력으로 둔다. 공개 정보에서 보이는 대표 stack은 OCaml의 `Base` → `Core` → `Async`, incremental computation, internal web UI용 `Bonsai`, 그리고 profiling tool `magic-trace`다.

## Why

Market making은 noisy data에서 신호를 찾는 것만으로 끝나지 않는다. regime change, 주문·리스크의 상태 변화, 자신이 시장에 미치는 영향, 예측 불가능한 latency를 동시에 다룬다. 따라서 type system은 illegal state를 줄이고, low-latency infrastructure는 timely decision을 돕고, observability는 드문 incident의 원인을 재구성한다.

## 핵심 특징

| 영역 | 접근 | 의도 |
|---|---|---|
| Domain logic | OCaml, ADT, module/functor, immutable data | 복잡한 상태·boundary를 type로 표현 |
| Runtime | `Async`와 `Deferred` | non-blocking I/O와 event-driven workflow |
| UI | `Incremental`, `Bonsai` | 바뀐 dependency만 다시 계산 |
| Performance | low-latency networking, compiler/system work | tail latency와 throughput 동시 관리 |
| Diagnosis | `magic-trace`, `perf` | incident 직전 call flow와 system metric 연결 |
| Research | Python + ML infrastructure | analysis/training과 real-time serving의 역할 분리 |

## 계층을 읽는 법

```text
Base        minimal, predictable stdlib replacement
  └─ Core   richer production conventions and APIs
       └─ Async  Deferred-based concurrency and I/O
            └─ application: market data, risk, operations
```

`Base`와 `Core`는 단지 편의 library가 아니라 API design, error handling, time, containers에 대한 opinionated production vocabulary다. `Async_kernel`은 portable concurrency core로서 JavaScript 등 다른 환경에서도 활용될 수 있다.

> [!NOTE]
> OxCaml mode system은 scope, portability, sharing, linearity를 type checking에 더 강하게 반영하려는 extension이다. 공식 문서가 일부 기능의 넓은 도입이 진행 중임을 밝히므로, 안정적인 OCaml과 같은 성숙도로 가정하지 않는다.

## Sources

- https://www.janestreet.com/technology/
- https://www.janestreet.com/what-we-do/overview/
- https://github.com/janestreet/base
- https://github.com/janestreet/core
- https://github.com/janestreet/async_kernel
