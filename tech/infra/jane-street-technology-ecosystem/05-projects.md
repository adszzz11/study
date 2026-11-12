---
date: 2026-11-12
tags: [tech]
type: tech-tool-study
status: draft
---

# Projects: 적용 과제

> [[tech/infra/jane-street-technology-ecosystem/README|목차]] · [[tech/infra/jane-street-technology-ecosystem/cheatsheet|다음: Cheatsheet]]

| 프로젝트 | 구현 범위 | 완료 기준 |
|---|---|---|
| Real-time risk dashboard | mock market-data stream을 `Async`로 받고, `Incremental`로 risk metric, `Bonsai`로 UI 구성 | 한 가격 변경이 관련 panel만 업데이트되고 test로 확인됨 |
| Latency incident lab | 느린 RPC/queue consumer를 의도적으로 만들고 `perf`/`magic-trace` 비교 | root cause 가설, evidence, hardware 조건을 incident report에 기록 |
| Typed order-state engine | ADT로 주문 lifecycle과 illegal transition 모델링 | invalid transition이 compile-time 또는 API boundary에서 차단됨 |
| Regime-aware forecasting sandbox | Python feature/model training과 OCaml inference workflow boundary 설계 | data contract, model version, latency budget, fallback 명시 |
| Compiler/type-safety study | OxCaml mode annotation 실험 | 잡힌 오류·제한·stable fallback을 표로 기록 |

## 권장 진행: Risk Dashboard

1. deterministic mock price feed와 timestamp를 만든다.
2. position, FX rate, limit을 immutable model로 정의한다.
3. price 변경과 portfolio risk recomputation의 dependency를 test한다.
4. stale feed·invalid price·out-of-order event 정책을 추가한다.
5. view rendering latency와 update count를 측정한다.

## 평가 기준

- correctness: 수치 단위, timestamp, state transition을 재현 가능하게 검증하는가?
- performance: median뿐 아니라 tail latency와 queue growth를 관찰하는가?
- operability: log, metric, trace의 correlation key가 있는가?
- safety: simulated data와 credential-free setup을 유지하는가?

## Sources

- https://github.com/janestreet/async
- https://github.com/janestreet/incremental
- https://github.com/janestreet/bonsai
- https://github.com/janestreet/magic-trace
