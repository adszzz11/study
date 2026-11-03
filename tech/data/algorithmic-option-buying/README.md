---
date: 2026-11-03
tags: [tech]
type: tech-tool-study
status: draft
---

# Algo Price Action 기반 Option Buying 시스템

> **한 줄 정의**: Price action 신호를 규칙화하고 option-chain·Greeks·risk limit를 결합해 Call/Put을 매수하는 데이터 기반 파생상품 트레이딩 접근이다.

## Overview

이 노트는 `algopriceactiontrader`의 [공개 Reel](https://www.instagram.com/reel/DfFrvCWTijy/)이 언급한 `#optionbuying`, `#stockoptions`를 출발점으로 한다. 공개 caption에는 전략 규칙, 성과 검증, 시장, 진입 조건이 없으므로 특정 수익 전략이나 투자 권유로 해석하지 않는다.

Option buying은 최대 손실을 지불한 premium으로 제한할 수 있지만, 방향뿐 아니라 움직임의 **속도와 시점**이 중요하다. 만기가 가까워지면 Theta decay와 implied volatility(IV) 변화가 기초자산의 방향 예측과 다른 option P&L을 만들 수 있다. 따라서 signal 생성, 계약 선택, 위험 통제, 주문 자동화와 준수 요건을 서로 분리해 설계한다.

```text
Market data ──> Feature engine ──> Signal/rule engine ──> Risk gate ──> Broker API
 OHLCV, OI,       trend, support/     price-action        position,       order,
 option-chain,    resistance, VWAP,   breakout/retest,    premium,        fill,
 IV, Greeks       IV, Greeks          invalidation        Greeks, kill    audit trail
                                                                  │
                                          Research/backtest <──────┘
```

## Learning Path

- [ ] [[tech/data/algorithmic-option-buying/01-overview|Overview]] — What/Why와 계층별 책임 이해
- [ ] [[tech/data/algorithmic-option-buying/02-ecosystem|Ecosystem]] — 방향성 거래 대안 및 검증법 비교
- [ ] [[tech/data/algorithmic-option-buying/04-learning/01-getting-started|시작하기]] — payoff, Greeks, 한 가지 setup을 수치화
- [ ] [[tech/data/algorithmic-option-buying/04-learning/02-deep-dive|Deep Dive]] — point-in-time backtest와 risk/execution 설계
- [ ] [[tech/data/algorithmic-option-buying/05-projects|Projects]] — research부터 paper execution까지 단계별 구현
- [ ] [[tech/data/algorithmic-option-buying/cheatsheet|Cheatsheet]] — 주문 전 위험 점검표와 핵심 용어
- [ ] [[tech/data/algorithmic-option-buying/03-references|References]] — 원문, 규제, 거래소·교육 자료 확인

## When To Use

- 재현 가능한 price-action setup을 정의하고, option 계약 선택까지 데이터로 검증할 때
- premium-at-risk, Greeks, 유동성, 일일 drawdown 한도를 주문 전에 강제할 때
- spot/futures와 option buying의 비용 및 risk-adjusted 결과를 같은 signal로 비교할 때
- 실주문 전에 paper trading, event log, kill switch를 검증할 때

## When Not To Use

- Reel이나 차트의 인상만으로 검증 없는 수익을 기대할 때
- premium 전액 손실, bid-ask spread, slippage, IV/Theta 영향을 감당하거나 설명할 수 없을 때
- point-in-time option-chain 데이터 없이 과거 option 성과를 단정할 때
- broker·exchange의 최신 eligibility, API, 알고리즘 거래 준수 요건을 확인하지 않았을 때

## Related Notes

- [[MOCs/Index]]
- [[MOCs/Data]]
- [[tech/data/gs-quant/README|GS Quant]]

## Sources

- https://www.instagram.com/reel/DfFrvCWTijy/
- https://www.investor.gov/introduction-investing/general-resources/news-alerts/alerts-bulletins/investor-bulletins-63
- https://www.nseindia.com/option-chain
- https://www.sebi.gov.in/legal/circulars/feb-2025/safer-participation-of-retail-investors-in-algorithmic-trading_91614.html
- https://www.cboe.com/insights/posts/learning-the-greeks-an-experts-perspective
