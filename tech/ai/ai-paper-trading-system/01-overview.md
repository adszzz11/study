---
date: 2026-11-03
tags: [tech]
type: tech-tool-study
status: draft
---

# Overview: AI Paper Trading과 Risk Guard

> [[tech/ai/ai-paper-trading-system/README|목차로 돌아가기]]

## What

AI Paper Trading 시스템은 AI가 시장 요약, 전략 가설, parameter 후보, 코드 patch를 **제안**하고, 독립된 검증 계층이 주문과 위험을 통제하는 모의 거래 환경이다. AI의 자기수정은 운영 source를 직접 바꾸는 행위가 아니라 sandbox experiment 또는 Pull Request로 격리한다.

```text
Market Data → Feature / Signal → AI Strategy Lab → Order Proposal
                   │                  │                 │
                   │                  └→ Failure Ledger ▼
                   └──────────────────────→ Immutable Risk Guard
                                                   │
                                        Paper Broker / Execution
                                                   │
                                      Fills · P/L · Audit Event
```

## Why

- **과적합**: 과거 수익이 미래 성과를 보장하지 않는다.
- **look-ahead bias**: 당시 알 수 없었던 데이터가 signal에 섞이면 backtest가 부풀려진다.
- **execution gap**: simulator의 fill·liquidity 가정은 실제 시장과 다르다.
- **automation failure**: stale data, API error, 중복 주문, 무한 재시도가 손실과 운영 장애를 키울 수 있다.

따라서 AI의 창의성과 broker의 주문 권한을 같은 process에 두지 않는다.

## 특징

| 구성요소 | 책임 | AI가 변경할 수 없는 것 |
|---|---|---|
| AI Strategy Lab | 분석, 가설, patch 제안 | broker credential, production deploy |
| Immutable Risk Guard | 주문 검증·차단·kill switch | daily loss와 exposure 한도 |
| Execution Adapter | 승인된 주문만 broker로 전달 | paper/live endpoint 분리 |
| Failure Ledger | run·주문·실패 원인의 append-only 기록 | 과거 audit event |
| Promotion Gate | 검증 단계와 human approval 강제 | 승인 전 전략 승격 |

`Risk Guard`는 최소한 `max_daily_loss`, `max_drawdown`, `max_position_notional`, `max_order_rate`, symbol allowlist, market-hours, stale-data 조건을 확인한다. 하나라도 위반하면 신규 주문을 거절하고 필요 시 미체결 주문 취소와 cooldown 또는 kill switch를 실행한다.

## Sources

- https://www.instagram.com/reel/DfPDCU-Ma2R/
- https://docs.alpaca.markets/us/v1.4.2/docs/paper-trading
- https://docs.alpaca.markets/us/docs/getting-started-with-trading-api
