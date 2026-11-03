---
date: 2026-11-03
tags: [tech]
type: tech-tool-study
status: draft
---

# Overview: Algo Price Action Option Buying

> [[tech/data/algorithmic-option-buying/README|목차로 돌아가기]] · [[tech/data/algorithmic-option-buying/02-ecosystem|다음: Ecosystem]]

## What

Algo Price Action 기반 option buying은 OHLCV, option chain, OI, IV, Greeks로부터 관찰 가능한 조건을 만들고, 조건이 충족될 때 Call 또는 Put을 **매수**하는 규칙 기반 workflow다. 핵심은 차트의 서술을 entry·invalidation·exit·time stop으로 바꾸는 데 있다.

```text
관찰: "VWAP 위로 전고점 돌파 후 지지"
규칙: close > VWAP AND high > prior_N_bar_high
      AND retest_low >= prior_N_bar_high - tolerance
주문: liquidity filter를 통과한 계약만 매수
무효화: underlying close < retest_low 또는 premium stop
```

## Why

- **재현성**: 같은 timestamp와 입력이면 같은 signal이 나와야 backtest와 review가 가능하다.
- **계약 선택**: underlying의 bullish/bearish signal만으로는 expiry, strike, moneyness, spread, IV가 다른 실제 P&L을 설명할 수 없다.
- **위험 제한**: option buyer의 손실은 premium까지일 수 있으나 premium 전액 손실은 실제 가능한 결과다.
- **감사 가능성**: signal, risk decision, order, fill, reject, retry를 event log로 남기면 연구와 운영을 분리해 검토할 수 있다.

## 핵심 특징

| Layer | 입력 | 산출 | 반드시 점검할 것 |
|---|---|---|---|
| Price action | OHLCV, VWAP, swing | breakout/retest·trend signal | timeframe, lookback, 미래 데이터 누수 |
| Option selection | chain, OI, IV, Greeks | expiry·strike·수량 | bid-ask, volume, moneyness, stale quote |
| Risk gate | position, premium, Greeks | allow/reject 및 size | 일일 손실, 동시 포지션, expiry-day 제한 |
| Execution/audit | order/fill/reject | 상태 전이와 log | idempotency, partial fill, slippage |
| Validation | point-in-time data | OOS 결과 | fees, tax, rollover, survivorship bias |

## 설계 원칙

1. signal은 underlying 기준으로 먼저 정의하고 option selection을 별도 함수로 둔다.
2. risk gate는 signal보다 우선한다. 통과하지 못한 주문은 좋은 setup처럼 보여도 제출하지 않는다.
3. research 결과와 live/paper execution log를 같은 schema로 저장한다.
4. 규정, broker API 정책, 거래소 계약 사양은 구현 시점에 다시 확인한다.

## Sources

- https://www.investor.gov/introduction-investing/general-resources/news-alerts/alerts-bulletins/investor-bulletins-63
- https://www.nseindia.com/option-chain
- https://www.cboe.com/insights/posts/learning-the-greeks-an-experts-perspective
