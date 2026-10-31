---
date: 2026-08-24
tags: [tech]
type: tech-tool-study
status: draft
---

# GS Quant Cheatsheet

## 한눈에 보기

```text
Instrument/Portfolio --calc(RiskMeasure)--> PricingContext --> Future --> Result
Dataset ------------get_data/series------> DataContext ----> DataFrame/Series
Trigger + Action -------------------------> Strategy ------> Engine --> Backtest
```

## 설치

```bash
python -m pip install "gs-quant==2.1.3"
python -m pip install "gs-quant[mcp]==2.1.3"  # experimental MCP가 필요할 때만
```

## 핵심 object

| Object | 기억할 역할 |
|---|---|
| `Priceable` | price/risk 계산 가능한 공통 abstraction |
| `Instrument` | 금융상품 specification |
| `Portfolio` | instrument의 계층적 collection |
| `RiskMeasure` | 계산 요청의 명세 |
| `Dataset` | dataset query facade |
| `Strategy` | trigger와 action의 조합 |

## Context

| Context | Scope |
|---|---|
| `GsSession` | OAuth, environment, HTTP/WebSocket |
| `DataContext` | query 기간과 interval |
| `PricingContext` | pricing/market date, location, async, batch, cache |
| `HistoricalPricingContext` | 여러 valuation date의 pricing/risk |

```python
with PricingContext(pricing_date=valuation_date):
    price_future = instrument.price()
    risk_future = instrument.calc(risk_measure)

price = price_future.result()
risk = risk_future.result()
```

## Dataset methods

| Method | 결과 |
|---|---|
| `get_data()` | 조건에 맞는 table |
| `get_data_series()` | 한 field의 time series |
| `get_data_last()` | 기준 시점 이전 최신 관측값 |
| `get_coverage()` | entity/dimension coverage |

```text
큰 query: coverage -> fields 최소화 -> date/entity chunk -> merge -> validate
제한: API response 약 100MB
```

## Backtesting DSL

| Component | 역할 |
|---|---|
| `Trigger` | 언제 실행할지 결정 |
| `PeriodicTrigger` | 일정 기반 |
| `MktTrigger` | 시장 조건 기반 |
| `StrategyRiskTrigger` | risk threshold 기반 |
| `Action` | instrument 생성·매매·hedge |
| `Strategy` | trigger/action 구성 |
| Engine | valuation/simulation |
| Backtest | date별 portfolio/risk 결과 |

## Credentials 경계

```text
credentials 없이 가능:
- source 열람
- 직접 만든 pandas.Series의 일부 gs_quant.timeseries analytics

일반적으로 credentials + entitlement 필요:
- proprietary datasets
- GS pricing models / risk infrastructure
- Security Master
- server-backed backtesting examples
```

## MCP

| 항목 | 규칙 |
|---|---|
| 상태 | Experimental |
| 설치 | `gs-quant[mcp]` |
| `local` auth | 단일 shared session; single-user 전용 |
| `passthrough` auth | per-user session 전달 |
| production | version pin + adapter + integration test |

## 재현성 checklist

- [ ] `gs-quant`와 Python version
- [ ] input data source/snapshot
- [ ] pricing date와 market-data date/location
- [ ] original 및 resolved instrument
- [ ] risk measure와 units
- [ ] window와 annualization convention
- [ ] entitlement와 backend dependency
- [ ] async/batch/cache 설정
- [ ] partial failure와 retry 결과

## Troubleshooting 순서

```text
Import -> version/environment
Auth -> client credential/environment
Permission -> entitlement
Empty data -> coverage/dimensions/date/timezone
Wrong number -> units/window/alignment/market context
Slow job -> batching/async/query size
MCP issue -> experimental API/version/auth mode/tool filter
```

## Sources

- https://developer.gs.com/docs/gsquant/
- https://developer.gs.com/docs/gsquant/getting-started/
- https://developer.gs.com/docs/gsquant/pricing-and-risk/pricing-context/
- https://developer.gs.com/docs/gsquant/api/classes/gs_quant.data.Dataset.html
- https://developer.gs.com/docs/gsquant/pricing-and-risk/backtesting/
- https://github.com/goldmansachs/gs-quant/tree/master/gs_quant/mcp

