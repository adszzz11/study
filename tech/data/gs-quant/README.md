---
date: 2026-08-24
tags: [tech]
type: tech-tool-study
status: draft
---

# GS Quant: 골드만삭스 퀀트 GitHub

> **한 줄 정의**: **GS Quant**는 Goldman Sachs quants가 개발·유지하는 Apache-2.0 기반 Python quantitative finance toolkit으로, 로컬 금융 통계 분석과 Goldman Sachs Marquee의 market data·derivatives pricing·risk API를 하나의 객체 모델로 연결한다.

## Overview

GS Quant는 `Instrument`, `Portfolio`, `RiskMeasure` 같은 domain object와 `GsSession`, `DataContext`, `PricingContext` 같은 scoped context를 결합한다. 같은 Python workflow 안에서 time series analytics, market data 조회, derivatives pricing, portfolio risk, backtesting을 다룰 수 있다.

```text
Python application / Notebook / Agent
                │
     Instrument · Portfolio · Strategy
                │
 Session ─ DataContext ─ PricingContext
                │
   Dataset / Risk / Backtest API clients
                │
 Goldman Sachs Marquee services
 market data · pricing · risk · reports
```

공개 범위를 오해하지 않는 것이 중요하다. package source와 일부 `gs_quant.timeseries` analytics는 공개되어 있지만, Goldman Sachs의 proprietary datasets, pricing models, Security Master, risk infrastructure에는 일반적으로 Marquee application credentials와 entitlement가 필요하다. 즉, “Goldman Sachs 데이터와 모델의 무료 공개”가 아니라 **공개 SDK + 제한된 institutional backend** 구조다.

> [!NOTE]
> 조사 기준은 **2026-08-24**다. 이 노트는 동명의 2026년 Knowledge Graph 논문 `GS-Quant`가 아니라 공식 [`goldmansachs/gs-quant`](https://github.com/goldmansachs/gs-quant) repository를 다룬다. 확인된 최신 PyPI release는 `2.1.3`(2026-08-07)이다.

## Learning Path

- [ ] [[01-overview|Overview]] — What/Why, 공개 범위, 핵심 architecture 파악
- [ ] [[02-ecosystem|Ecosystem]] — QuantLib, pandas/SciPy, vendor API와 비교
- [ ] [[03-references|References]] — 공식 문서와 source code 읽는 순서 정리
- [ ] [[04-learning/01-getting-started|Getting Started]] — 설치와 local time series analytics 실습
- [ ] [[04-learning/02-deep-dive|Deep Dive]] — session, pricing, data, backtesting, MCP 이해
- [ ] [[05-projects|Projects]] — entitlement 유무에 맞는 미니 프로젝트 수행
- [ ] [[cheatsheet|Cheatsheet]] — 핵심 object, context, 선택 기준 빠르게 복습

## When To Use

- Python에서 금융 시계열 분석과 institutional pricing/risk workflow를 같은 domain model로 연결할 때
- `EqOption`, `FXOption`, `IRSwap`, `IRSwaption` 등 여러 asset class를 공통 interface로 다룰 때
- `Portfolio` 단위 risk aggregation과 historical valuation이 필요할 때
- Marquee credentials와 적절한 dataset/model entitlement가 이미 있을 때
- `Trigger`와 `Action`을 조합하는 declarative backtesting을 연구할 때
- experimental MCP layer로 quant 기능을 agent tool로 노출하는 실험을 할 때

## When Not To Use

- Goldman Sachs proprietary data나 pricing model을 무료로 사용할 목적일 때
- credentials 없이 market data, Security Master, server-side pricing 예제를 그대로 재현하려 할 때
- 완전히 open-source인 pricing engine과 model implementation 자체가 필요할 때
- 단순한 `pandas` 변환이나 몇 개의 통계 함수만 필요해 dependency를 최소화해야 할 때
- MCP의 안정적인 장기 API compatibility가 필수인 production system일 때
- `local` MCP authentication mode를 multi-user service에 배포하려 할 때

## Related Notes

- [[MOCs/Index]]
- [[MOCs/Data]]
- [[tech/ai/model-context-protocol-mcp/README|Model Context Protocol (MCP)]]
- [[tech/data/dolt/README|Dolt]]

## Sources

- https://github.com/goldmansachs/gs-quant
- https://developer.gs.com/docs/gsquant/
- https://developer.gs.com/docs/gsquant/getting-started/
- https://developer.gs.com/docs/gsquant/authentication/gs-session/
- https://pypi.org/project/gs-quant/
- https://github.com/goldmansachs/gs-quant/releases

