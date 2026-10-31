---
date: 2026-08-24
tags: [tech]
type: tech-tool-study
status: draft
---

# Deep Dive: Pricing, Data, Backtesting, MCP

> [[01-getting-started|이전: Getting Started]] · [[../README|목차로 돌아가기]] · [[../05-projects|다음: Projects]]

## 학습 목표

- context-driven execution의 scope와 lifecycle을 이해한다.
- relative instrument를 resolve하고 valuation 조건을 기록한다.
- 큰 dataset query를 coverage와 chunk 단위로 설계한다.
- declarative backtesting component를 구분한다.
- experimental MCP의 authentication mode와 운영 한계를 설명한다.

## 1. Instrument와 resolve

Instrument에는 maturity나 strike를 market convention으로 표현할 수 있다.

```text
입력: termination_date="13m", strike="atm+40"
          │
          ▼ resolve()
출력: concrete date, strike, defaults, conventions
```

relative parameter는 간결하지만 valuation date와 market data에 따라 concrete value가 달라질 수 있다. 연구 결과에는 원본 specification뿐 아니라 resolved instrument, pricing date, market location을 함께 기록한다.

```python
# 실제 constructor parameter는 product와 설치 version의 API 문서를 확인한다.
instrument = make_instrument_with_relative_parameters()
resolved = instrument.resolve()

print(resolved)
```

## 2. PricingContext와 Future

```python
from gs_quant.markets import PricingContext

with PricingContext(
    pricing_date=valuation_date,
    is_async=True,
):
    price_future = instrument.price()
    risk_future = instrument.calc(risk_measure)

price = price_future.result()
risk = risk_future.result()
```

### Context 선택표

| Context | 관리 대상 | 대표 사용 |
|---|---|---|
| `GsSession` | authentication, connection, environment | Marquee API 연결 |
| `DataContext` | start/end date, interval | time series query 범위 |
| `PricingContext` | pricing date, market date/location, async, batch, cache | 현재·특정 시점 pricing/risk |
| `HistoricalPricingContext` | 여러 valuation date | historical pricing/risk |

### 주의할 점

- context block을 벗어난 뒤 `Future.result()`를 materialize하는 흐름을 명시한다.
- interactive latency와 장시간 batch job을 같은 timeout 정책으로 처리하지 않는다.
- partial failure를 portfolio 전체 성공으로 오해하지 않는다.
- valuation date, market-data date, location을 결과 metadata에 남긴다.
- cache가 켜져 있다면 재계산 여부를 명확히 한다.

## 3. Dataset query 설계

Dataset은 공통 schema와 entitlement를 공유하는 time series collection이다. daily/date-based dataset과 intraday/time-based dataset의 index 의미가 다르므로 query 전에 schema와 coverage를 확인한다.

```python
from gs_quant.data import Dataset

dataset = Dataset("DATASET_ID")

coverage = dataset.get_coverage()
latest = dataset.get_data_last(as_of=as_of_time, assetId=asset_id)
series = dataset.get_data_series(
    "fieldName",
    start=start_date,
    end=end_date,
    assetId=asset_id,
)
```

> [!NOTE]
> 위 코드는 query shape를 보여주는 skeleton이다. 실제 dataset ID, field, dimension, timestamp parameter는 Dataset API와 dataset schema를 확인한다.

API 응답은 약 100MB 제한이 있으므로 큰 조회는 분할한다.

```text
coverage 확인
  -> 필요한 field/dimension만 선택
  -> date range chunking
  -> entity chunking
  -> 각 chunk 저장 및 검증
  -> deduplicate + sort + completeness check
```

| 검증 | 방법 |
|---|---|
| Coverage | 요청 entity가 dataset에 존재하는지 먼저 확인 |
| Boundary | chunk 경계의 누락·중복 검사 |
| Schema | field type과 date/time index 확인 |
| Entitlement | empty data와 permission failure를 구분 |
| Freshness | `get_data_last()`의 기준 시점과 timezone 기록 |

## 4. Declarative backtesting

```text
Trigger ── decides when ──┐
                          ├─> Strategy -> Calculation Engine -> Backtest
Action ── decides what ───┘                         │
                                        portfolio + risk by date
```

| Component | 예시 | 책임 |
|---|---|---|
| `PeriodicTrigger` | 매월 첫 영업일 | 일정 기반 실행 |
| `MktTrigger` | 시장 지표 threshold | market condition 기반 실행 |
| `StrategyRiskTrigger` | delta/vega 한도 | strategy risk 기반 실행 |
| `Action` | instrument 생성, trade, hedge | 상태 변경 |
| `Strategy` | trigger + action | declarative rule 묶음 |
| `GenericEngine` | GS risk API 활용 | valuation과 simulation |

backtest를 해석할 때는 look-ahead bias, market data availability, transaction cost, trigger evaluation timing, instrument resolve 시점을 함께 검증한다. server-backed engine은 session과 entitlement가 필요할 수 있다.

## 5. Experimental MCP

```bash
python -m pip install "gs-quant[mcp]==2.1.3"
```

MCP layer의 주요 범위는 FastMCP server/client, tool auto-discovery, tag/key filtering, streamable HTTP, CLI, interactive REPL, external package custom tool 등록이다.

### Deployment decision

| 질문 | 결정 |
|---|---|
| single-user local experiment인가? | `local` mode 검토 |
| 여러 사용자가 접속하는가? | `local` mode 금지, `passthrough`와 사용자 격리 검토 |
| stable production contract가 필요한가? | experimental API 앞에 adapter와 integration test 배치 |
| tool 권한을 줄여야 하는가? | tag/key filtering과 allowlist 적용 |
| credential이 tool log에 노출되는가? | request/response logging과 redaction 점검 |

관련 protocol 개념은 [[tech/ai/model-context-protocol-mcp/README|Model Context Protocol (MCP)]] 노트와 함께 본다.

## 심화 체크리스트

- [ ] relative instrument의 resolved 결과를 저장한다.
- [ ] valuation date, market date/location, package version을 기록한다.
- [ ] sync, async, batch를 workload에 맞게 선택한다.
- [ ] dataset coverage를 확인한 뒤 100MB 미만으로 query를 분할한다.
- [ ] backtest의 look-ahead bias와 transaction cost를 검토한다.
- [ ] MCP `local` mode를 multi-user로 배포하지 않는다.
- [ ] experimental interface 변경을 upgrade test로 감지한다.

## Sources

- https://developer.gs.com/docs/gsquant/pricing-and-risk/instruments/
- https://developer.gs.com/docs/gsquant/pricing-and-risk/measures/
- https://developer.gs.com/docs/gsquant/pricing-and-risk/pricing-context/
- https://developer.gs.com/docs/gsquant/data/data-environment/datasets/
- https://developer.gs.com/docs/gsquant/api/classes/gs_quant.data.Dataset.html
- https://developer.gs.com/docs/gsquant/pricing-and-risk/backtesting/
- https://github.com/goldmansachs/gs-quant/tree/master/gs_quant/mcp

