---
date: 2026-11-03
tags: [tech]
type: tech-tool-study
status: draft
---

# 시작하기: 한 Setup을 측정 가능한 규칙으로

> [[tech/data/algorithmic-option-buying/README|목차로 돌아가기]] · [[tech/data/algorithmic-option-buying/04-learning/02-deep-dive|다음: Deep Dive]]

## 학습 목표

- Call/Put, strike, expiry, premium, ITM/ATM/OTM을 payoff 관점에서 설명한다.
- Delta, Theta, Vega, IV가 같은 underlying 이동의 option P&L을 바꾸는 이유를 확인한다.
- 하나의 price-action setup을 수치화하고 paper trading으로만 관찰한다.

## 1. Payoff와 계약의 기본값

| 항목 | 질문 |
|---|---|
| Underlying | 어느 지수·주식의 signal인가? |
| Call/Put | 상승 또는 하락 가설에 맞는 권리인가? |
| Strike/expiry | moneyness와 잔존기간은 무엇인가? |
| Premium | 최대로 잃을 수 있는 금액과 quantity는 얼마인가? |
| Liquidity | bid-ask spread, volume, OI가 최소 기준을 통과하는가? |

간단한 long call의 만기 손익은 개념적으로 다음과 같다.

```text
payoff = max(underlying_at_expiry - strike, 0)
P&L    = payoff - premium_paid - transaction_costs
```

만기 전 P&L은 이 식만으로 충분하지 않다. IV, 남은 시간, Greeks, 실제 호가와 fill을 함께 봐야 한다.

## 2. 한 가지 Setup만 정의하기

예시는 교육용 후보이며 성과 주장이 아니다. timeframe과 data source를 고정한다.

```yaml
name: vwap_breakout_retest_long
timeframe: 5m
entry:
  - close > vwap
  - high > prior_20_bar_high
  - next_3_bar_low >= prior_20_bar_high - 0.1 * ATR_14
invalidation:
  - close < prior_20_bar_high - 0.1 * ATR_14
exit:
  - underlying_stop
  - premium_stop
  - time_stop: 30m
```

정의 후에는 각 bar가 종료된 시점에만 계산했는지, `prior_20_bar_high`에 현재 bar를 잘못 포함하지 않았는지 확인한다.

## 3. Paper Observation 표

| timestamp | signal | 계약 후보 | Delta/Theta/Vega | bid-ask | 결론 |
|---|---|---|---|---|---|
| bar close | 조건 충족 여부 | expiry·strike | snapshot 값 | 절대값·비율 | enter / reject |

최소 20개 이상의 관찰을 모아 signal, 계약 선택, risk rejection의 이유를 함께 기록한다. 실제 주문 대신 calculator 또는 paper broker를 사용한다.

## 체크리스트

- [ ] payoff diagram과 premium-at-risk를 설명할 수 있다.
- [ ] setup의 entry·invalidation·exit·time stop이 숫자로 정의되어 있다.
- [ ] option quote와 underlying bar의 timestamp를 함께 저장했다.
- [ ] spread·slippage·fee를 무시한 결과를 성과로 해석하지 않는다.
- [ ] 실거래 전에 [[tech/data/algorithmic-option-buying/03-references|References]]의 disclosure와 정책을 검토한다.

## Sources

- https://www.theocc.com/company-information/documents-and-archives/options-disclosure-document
- https://www.cboe.com/insights/posts/learning-the-greeks-an-experts-perspective
- https://www.nseindia.com/option-chain
