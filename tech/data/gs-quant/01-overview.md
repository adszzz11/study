---
date: 2026-08-24
tags: [tech]
type: tech-tool-study
status: draft
---

# GS Quant Overview

## What

GS Quant는 quantitative finance를 위한 Python toolkit이자 Goldman Sachs Marquee API client다. 금융상품을 `Instrument`로 표현하고, `PricingContext`에서 `price()` 또는 `calc()`를 실행하며, `Dataset`과 `DataContext`로 시계열을 조회한다. 이 abstraction은 `Portfolio`와 backtesting에도 이어진다.

| Layer | 핵심 object | 역할 |
|---|---|---|
| Domain | `Priceable`, `Instrument`, `Portfolio` | 계산 대상과 계층 구조 표현 |
| Risk | `RiskMeasure` | `Price`, `IRDelta`, `IRVega` 등 계산 요청 명세 |
| Execution | `PricingContext`, `HistoricalPricingContext` | valuation 조건, batching, async, cache 관리 |
| Data | `Dataset`, `DataContext` | dataset facade와 조회 기간 관리 |
| Connection | `GsSession` | OAuth token, environment, HTTP/WebSocket 연결 관리 |
| Strategy | `Trigger`, `Action`, `Strategy`, engine | declarative backtesting 구성 |
| Agent | `gs_quant.mcp`, `gs_quant.skills` | experimental MCP server/client와 tool discovery |

## Why

일반적인 quant workflow는 asset class별 instrument model, market data API, pricing, Greeks, portfolio aggregation, backtesting이 분리되기 쉽다. 연구 notebook과 production platform의 model이 다르면 같은 전략을 다시 구현해야 한다.

GS Quant는 다음 흐름을 하나의 Python domain model로 묶는다.

```text
Instrument 정의
  -> market convention resolve
  -> Dataset으로 data 조회
  -> PricingContext에서 price/risk 계산
  -> Portfolio aggregation
  -> 같은 abstraction으로 backtest
```

- 함수마다 valuation date와 market location을 전달하지 않고 context scope로 관리한다.
- 여러 `price()`·`calc()` 호출을 한 context에서 모아 dispatch할 수 있다.
- instrument와 risk measure를 portfolio와 strategy에서도 재사용한다.
- 공개 statistical package와 institutional backend client를 한 package에서 제공한다.

Goldman Sachs는 관련 analytics tooling을 내부의 1,000명 이상 quantitative developers가 사용한다고 설명한다. 다만 공개 package를 설치하는 것과 기관 backend에 접근하는 것은 별개의 권한 문제다.

## 핵심 특징

### 1. Domain object layer

`Priceable`은 가격이나 risk를 계산할 수 있는 공통 abstraction이다. 이를 구현하는 `Instrument`에는 `EqOption`, `FXOption`, `IRSwap`, `IRSwaption`과 credit·commodity product가 포함된다. 여러 instrument는 `Portfolio`로 묶어 같은 계산 interface를 쓸 수 있다.

Instrument는 `"13m"`, `"atm+40"` 같은 market-friendly relative parameter를 받을 수 있다. `resolve()`는 이 표현을 실제 날짜, strike, product default convention으로 구체화한다.

### 2. Context-driven execution

```python
from gs_quant.markets import PricingContext

with PricingContext(pricing_date=valuation_date):
    price_future = instrument.price()
    delta_future = instrument.calc(risk_measure)

price = price_future.result()
delta = delta_future.result()
```

context block 내부 호출은 block 종료 시 dispatch될 수 있고 결과는 `Future`로 다룬다. 장시간 계산은 `is_batch=True`, 호출자가 기다리지 않고 다른 일을 계속해야 한다면 `is_async=True`를 검토한다.

### 3. Data와 local analytics

`Dataset(dataset_id)`는 다음 facade를 제공한다.

| Method | 용도 |
|---|---|
| `get_data()` | 기간과 dimension 조건으로 table 조회 |
| `get_data_series()` | 특정 field의 시계열 조회 |
| `get_data_last()` | 기준 시점 이전 최신 관측값 조회 |
| `get_coverage()` | dataset coverage 확인 |

`gs_quant.timeseries`에는 date alignment, returns, volatility, correlation, statistics, econometrics, technical analysis 등이 있다. 직접 만든 `pandas.Series`에는 credentials 없이도 일부 함수를 적용할 수 있다.

### 4. Declarative backtesting

| Component | 질문 |
|---|---|
| `Trigger` | 언제 action을 실행하는가? |
| `Action` | 어떤 instrument를 만들거나 매매·hedge하는가? |
| `Strategy` | trigger와 action을 어떻게 조합하는가? |
| Calculation Engine | 어떤 방식으로 valuation·simulation하는가? |
| Backtest | 날짜별 portfolio와 risk 결과는 무엇인가? |

대표 trigger는 `PeriodicTrigger`, `MktTrigger`, `StrategyRiskTrigger`다. `GenericEngine`은 GS risk API를 사용하므로 공식 예제 다수는 initialized `GsSession`과 entitlement를 요구한다.

### 5. Experimental MCP

2026년 repository에는 `gs_quant.mcp`와 `gs_quant.skills`가 포함되어 있다. `pip install "gs-quant[mcp]"`로 optional dependencies를 설치하며 FastMCP server/client, tool auto-discovery, tag/key filtering, streamable HTTP, CLI, REPL, custom tool 등록을 제공한다.

> [!WARNING]
> MCP layer는 **Experimental**이다. API, CLI, configuration이 바뀔 수 있다. `local` authentication mode는 하나의 session을 모든 request가 공유하므로 multi-user deployment에는 적합하지 않다.

## 공개 범위와 경계

| 항목 | credentials 없이 | Marquee credentials/entitlement 필요 가능성 |
|---|---:|---:|
| package source 열람 | 가능 | 불필요 |
| 직접 만든 Series의 일부 analytics | 가능 | 불필요 |
| proprietary dataset 조회 | 불가 | 높음 |
| GS pricing model과 risk infrastructure | 불가 | 높음 |
| Security Master 기반 자산 조회 | 제한 | 높음 |
| 공식 server-backed backtest 예제 | 대체로 불가 | 높음 |

OAuth client ID와 secret은 Goldman Sachs 고객이 Marquee Developer Site에서 발급받는다. secret은 notebook, source code, vault에 기록하지 않고 environment variable이나 secret manager로 주입한다.

## Sources

- https://developer.gs.com/docs/gsquant/
- https://developer.gs.com/docs/gsquant/getting-started/
- https://developer.gs.com/docs/gsquant/pricing-and-risk/instruments/
- https://developer.gs.com/docs/gsquant/pricing-and-risk/measures/
- https://developer.gs.com/docs/gsquant/pricing-and-risk/pricing-context/
- https://developer.gs.com/docs/gsquant/data/data-environment/datasets/
- https://developer.gs.com/docs/gsquant/pricing-and-risk/backtesting/
- https://github.com/goldmansachs/gs-quant/tree/master/gs_quant/mcp

