---
date: 2026-11-12
tags: [tech]
type: tech-tool-study
status: draft
---

# Cheatsheet: Jane Street Stack

> [[tech/infra/jane-street-technology-ecosystem/README|목차]]

| 항목 | 기억할 점 |
|---|---|
| `Base` | predictable한 OCaml stdlib replacement |
| `Core` | `Base` 위의 richer production library |
| `Async` | `Deferred` 중심 non-blocking I/O/event loop |
| `Incremental` | dependency 변경분만 재계산 |
| `Bonsai` | Incremental 기반 declarative web UI |
| `magic-trace` | Intel PT 기반 control-flow history; `perf`와 보완 관계 |
| OxCaml | allocation, portability, sharing 등을 type로 더 표현하려는 extension |
| Python | research, analysis, visualization, ML에 병행 |

## 빠른 판단

```text
복잡한 domain state?      → ADT + pattern matching
여러 I/O 완료를 연결?     → Async Deferred, timeout/backpressure도 설계
입력 일부만 바뀜?         → Incremental dependency graph
live internal UI?          → Bonsai + model/view test 분리
latency spike 원인?        → perf 먼저, 조건 충족 시 magic-trace 보완
OxCaml 도입?              → 작은 실험 + stable OCaml fallback 유지
```

## 주의할 함정

- low latency는 평균값이 아니라 tail latency, queueing, system contention까지 본다.
- type safety는 stale market data, 잘못된 unit, 운영 권한을 자동으로 해결하지 않는다.
- `magic-trace`의 결과와 가능 여부는 CPU, Linux/kernel, VM 설정에 좌우된다.
- 공개 repository는 회사 내부 trading system 전체가 아니다.

## Sources

- https://www.janestreet.com/technology/
- https://github.com/janestreet
- https://github.com/janestreet/magic-trace
- https://oxcaml.org/documentation/modes/intro/
