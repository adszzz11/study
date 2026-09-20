---
date: 2026-08-24
tags: [tech]
type: tech-tool-study
status: draft
---

# GS Quant Projects

## 프로젝트 선택표

| 단계 | 프로젝트 | Credentials | 핵심 산출물 |
|---|---|---:|---|
| 입문 | Local Volatility Lab | 불필요 | 재현 가능한 volatility notebook |
| 초급 | Analytics Comparison | 불필요 | GS Quant와 직접 계산 비교표 |
| 중급 | Dataset Query Planner | 설계는 불필요, 실행은 필요 | coverage·chunking plan |
| 심화 | Portfolio Risk Snapshot | 필요 | price/risk matrix와 metadata |
| 심화 | Declarative Strategy | 대체로 필요 | trigger/action/engine 설계와 backtest |
| 실험 | Read-only MCP Tool | backend 호출 시 필요 | filtered tool server와 security checklist |

## 1. Local Volatility Lab

직접 생성하거나 공개적으로 사용 가능한 price series를 대상으로 rolling realized volatility를 계산한다.

### 요구사항

- random seed 또는 input data source 기록
- 22일과 66일 window 비교
- missing date와 outlier 처리 전후 비교
- package version, Python version, 실행일 기록
- 직접 계산한 benchmark와 결과 대조

```text
data load
  -> index validation
  -> return calculation
  -> rolling volatility
  -> annualization check
  -> chart/table
  -> reproducibility note
```

### 완료 기준

- [ ] warm-up `NaN`과 data gap을 구분했다.
- [ ] window가 observations인지 calendar days인지 명시했다.
- [ ] annualization convention을 기록했다.
- [ ] credentials 없이 재실행할 수 있다.

## 2. Analytics Comparison

같은 series에 대해 `gs_quant.timeseries` 결과와 `pandas`/NumPy 직접 계산을 비교한다.

| 비교 항목 | 검증 질문 |
|---|---|
| Returns | simple return인가 log return인가? |
| Volatility | sample/std convention과 annualization factor는? |
| Correlation | date alignment와 missing value policy는? |
| Window | fixed observations와 date window가 같은가? |

결과가 다르면 “library가 틀렸다”가 아니라 default convention, alignment, units부터 비교한다.

## 3. Dataset Query Planner

실제 data를 내려받기 전에 한 dataset의 조회 계획을 설계한다.

```yaml
dataset_id: DATASET_ID
frequency: daily-or-intraday
entities:
  - ENTITY_1
fields:
  - FIELD_1
range:
  start: YYYY-MM-DD
  end: YYYY-MM-DD
chunking:
  by: month
entitlement_checked: false
validation:
  - coverage
  - duplicate-index
  - missing-boundary
  - schema-drift
  - timezone
```

API의 약 100MB response limit을 넘지 않도록 date와 entity를 분할하고, chunk 재시도와 deduplication 규칙을 문서화한다.

## 4. Portfolio Risk Snapshot

entitlement가 있는 환경에서 여러 instrument를 `Portfolio`로 묶고 price와 risk measure를 같은 valuation context에서 계산한다.

### 산출물

- instrument specification과 resolved representation
- portfolio hierarchy
- price/risk result matrix
- valuation date, market date/location
- package version과 entitlement scope 메모
- partial failure와 retry 기록

| Instrument | Price | Risk measure 1 | Risk measure 2 | Status |
|---|---:|---:|---:|---|
| Instrument A | — | — | — | pending |
| Instrument B | — | — | — | pending |

> [!WARNING]
> 결과를 투자 판단에 사용하기 전 model assumptions, market data timestamp, entitlement 범위, 독립 검증 절차를 확인한다. 이 프로젝트의 목적은 SDK 학습이지 투자 조언 생성이 아니다.

## 5. Declarative Strategy

월별 roll 또는 risk threshold hedge 전략을 `Trigger + Action + Strategy`로 표현한다.

```text
PeriodicTrigger(monthly)
  -> AddTradeAction(relative instrument)
  -> resolve at configured time
  -> GenericEngine valuation
  -> portfolio/risk by date
```

### 검증 항목

- look-ahead bias가 없는가?
- trigger가 어떤 timestamp의 data를 보는가?
- relative instrument가 언제 resolve되는가?
- transaction cost와 liquidity assumption이 있는가?
- failed valuation date를 제외하고 성과를 과대평가하지 않는가?

## 6. Read-only MCP Tool

experimental `gs_quant.mcp`로 local analytics 또는 허용된 read-only query만 노출한다.

### Guardrail

- tool allowlist와 tag/key filter 적용
- write/trade 성격 action 제외
- credential과 result log redaction
- single-user라면 `local`, multi-user라면 per-user isolation 검토
- dependency version pinning
- upgrade 전 contract/integration test

관련 설계는 [[tech/ai/model-context-protocol-mcp/05-projects|MCP Projects]]도 참고한다.

## Sources

- https://developer.gs.com/docs/gsquant/api/timeseries.html
- https://developer.gs.com/docs/gsquant/data/data-environment/datasets/
- https://developer.gs.com/docs/gsquant/pricing-and-risk/pricing-context/
- https://developer.gs.com/docs/gsquant/pricing-and-risk/backtesting/
- https://github.com/goldmansachs/gs-quant/tree/master/gs_quant/mcp

