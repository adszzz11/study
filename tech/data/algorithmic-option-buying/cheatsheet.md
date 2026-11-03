---
date: 2026-11-03
tags: [tech]
type: tech-tool-study
status: draft
---

# Cheatsheet: Option Buying Research와 주문 전 점검

> [[tech/data/algorithmic-option-buying/README|목차로 돌아가기]]

## 핵심 용어

| 용어 | 빠른 정의 |
|---|---|
| Call / Put | 기초자산을 매수 / 매도할 권리 |
| Strike | 권리가 기준으로 삼는 가격 |
| Expiry | 계약 만기 시점 |
| Premium | option buyer가 지급하는 대가; long option의 최대 손실 기준 |
| ITM / ATM / OTM | 현재 underlying 대비 strike의 상대 위치 |
| IV | 시장 가격에서 역산된 기대 변동성 참조값 |
| Delta / Gamma | 가격 민감도 / Delta 변화 민감도 |
| Theta / Vega | 시간 경과 민감도 / IV 변화 민감도 |

## 주문 전 Gate

```text
[ ] signal은 closed bar와 point-in-time data만 사용한다
[ ] quote timestamp가 stale하지 않다
[ ] expiry, strike, right, quantity가 명시됐다
[ ] bid-ask spread·volume·OI 기준을 통과했다
[ ] premium-at-risk와 daily loss limit 안에 있다
[ ] Delta/Gamma/Theta/Vega 및 expiry concentration을 확인했다
[ ] event/expiry-day 정책과 kill switch를 확인했다
[ ] order·fill·reject를 audit log로 연결할 correlation ID가 있다
```

## 검증 최소 요건

| 항목 | 포함할 것 |
|---|---|
| Data | option-chain snapshot, contract rollover, timestamp alignment |
| Cost | premium, spread, slippage, commission, tax |
| Evaluation | holdout, out-of-sample, walk-forward, benchmark |
| Execution | partial fill, reject, retry, cancellation, stale-data handling |
| Governance | broker/exchange eligibility, API policy, kill switch, audit trail |

## 기억할 원칙

- underlying 방향이 맞아도 Theta·IV·spread 때문에 option P&L은 다를 수 있다.
- Reel은 검증된 전략 명세가 아니다. 규칙과 결과는 독립적으로 재현·검증한다.
- 실주문 전에는 [[tech/data/algorithmic-option-buying/03-references|References]]의 risk disclosure와 최신 정책을 다시 확인한다.

## Sources

- https://www.investor.gov/introduction-investing/general-resources/news-alerts/alerts-bulletins/investor-bulletins-63
- https://www.cboe.com/insights/posts/learning-the-greeks-an-experts-perspective
- https://www.theocc.com/company-information/documents-and-archives/options-disclosure-document
