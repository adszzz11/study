---
date: 2026-11-03
tags: [tech]
type: tech-tool-study
status: draft
---

# Projects: 적용 과제

> [[tech/ai/ai-paper-trading-system/README|목차로 돌아가기]]

## 1. Minimum Paper Bot

Alpaca Paper API, EMA/RSI signal, SQLite ledger, Telegram 또는 Slack alert를 연결한다. 완료 조건은 Paper 전용 credential, 비용 포함 backtest, 모든 order event의 기록이다.

## 2. Immutable Risk Guard

일일 손실, portfolio drawdown, 종목당 exposure, 주문 빈도와 kill switch를 독립 Python package 또는 service로 구현한다. 전략 process가 Guard를 우회하는 integration test를 추가한다.

## 3. Failure Ledger Dashboard

전략별 out-of-sample 성과, drawdown, rejection reason, AI proposal-to-result을 시각화한다. 성공률만 보여주지 말고 block·cancel·stale-data 이벤트를 같은 화면에서 비교한다.

## 4. AI Research Reviewer

LLM은 거래 로그를 요약하고 개선안을 JSON schema로 제안한다. 이 component에는 broker credential과 주문 API 권한을 주지 않으며, 제안은 sandbox experiment로만 전달한다.

## 5. Promotion Pipeline

GitHub Actions 같은 CI에서 backtest, walk-forward, 최소 Paper 기간, risk regression을 검사한다. 모든 통과가 있어도 human approval 전에는 strategy version을 승격하지 않는다.

## Sources

- https://docs.alpaca.markets/us/v1.4.2/docs/paper-trading
- https://mlflow.org/docs/latest/ml/tracking/
