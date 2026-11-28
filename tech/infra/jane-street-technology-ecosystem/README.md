---
date: 2026-11-12
tags: [tech]
type: tech-tool-study
status: draft
---

# Jane Street 기술 생태계

> **한 줄 정의**: Jane Street는 OCaml 중심 functional programming, ultra-low-latency infrastructure, quantitative research/ML을 결합해 global electronic market making을 수행하는 기술 주도 trading firm이다.

## Overview

Jane Street의 공개 기술 생태계는 단일 제품이 아니라 시장 데이터·주문·리스크·운영 UI를 정확하고 빠르게 다루기 위한 수직 통합된 platform이다. 중심 축은 `Base`/`Core`의 production-oriented OCaml library, `Async`의 event-driven concurrency, `Incremental`·`Bonsai`의 변경 전파 UI, 그리고 `magic-trace`·OxCaml 같은 performance/type-safety 연구다. Python은 data analysis, visualization, ML workflow에서 병행된다.

```text
market data → model / risk → order workflow → internal UI
     │             │              │              │
  Async I/O    OCaml types    low latency   Incremental + Bonsai
     └────────── observability: perf + magic-trace ──────────┘
```

## Learning Path

- [ ] [[tech/infra/jane-street-technology-ecosystem/01-overview|Overview]] — What/Why와 architecture
- [ ] [[tech/infra/jane-street-technology-ecosystem/02-ecosystem|Ecosystem]] — trading firm, OCaml concurrency, profiler 비교
- [ ] [[tech/infra/jane-street-technology-ecosystem/03-references|References]] — 공식 문서와 repository 읽기 순서
- [ ] [[tech/infra/jane-street-technology-ecosystem/04-learning/01-getting-started|시작하기]] — OCaml, `dune`, `Base/Core`, `Async` 첫 실습
- [ ] [[tech/infra/jane-street-technology-ecosystem/04-learning/02-deep-dive|Deep Dive]] — Incremental, Bonsai, OxCaml, tracing
- [ ] [[tech/infra/jane-street-technology-ecosystem/05-projects|Projects]] — dashboard·latency·type-state 프로젝트
- [ ] [[tech/infra/jane-street-technology-ecosystem/cheatsheet|Cheatsheet]] — stack과 판단 기준 빠른 복습

## When To Use

- typed functional design으로 복잡한 order/risk state transition을 모델링할 때
- low-latency event-driven service와 correctness를 함께 다뤄야 할 때
- 입력 일부의 변경만 계산·UI에 반영하는 internal dashboard를 만들 때
- Linux/Intel PT 환경에서 latency spike의 precise control-flow history를 조사할 때
- Python research/ML과 OCaml real-time workflow의 경계를 설계할 때

## When Not To Use

- 공개 repository만으로 Jane Street의 proprietary trading platform이나 market data를 재현하려 할 때
- 팀이 OCaml 학습 비용을 감당할 수 없고 일반적인 CRUD web service만 빠르게 만들 때
- `magic-trace`를 ARM, 비지원 Intel CPU, 또는 제한적인 VM에서 주 profiler로 삼을 때
- OxCaml의 실험적/도입 중인 기능을 검증 없이 production 기본값으로 채택할 때

## Related Notes

- [[MOCs/Index]]
- [[MOCs/Infra]]
- [[tech/infra/space-secure-agent-runtime/README|Secure Agent Runtime]]

## Sources

- https://www.janestreet.com/technology/
- https://www.janestreet.com/what-we-do/overview/
- https://www.janestreet.com/join-jane-street/machine-learning/
- https://github.com/janestreet
- https://oxcaml.org/documentation/modes/intro/
