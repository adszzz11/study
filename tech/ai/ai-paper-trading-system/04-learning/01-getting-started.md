---
date: 2026-11-03
tags: [tech]
type: tech-tool-study
status: draft
---

# 시작하기: 안전한 Paper Trading 최소 경로

> [[tech/ai/ai-paper-trading-system/README|목차로 돌아가기]] · [[tech/ai/ai-paper-trading-system/04-learning/02-deep-dive|다음: Deep Dive]]

## 목표

단순 EMA crossover를 비용·슬리피지 가정과 함께 backtest하고, Paper 주문 전에는 반드시 `RiskGuard.validate()`를 거치게 만든다. 이 단계에서 live credential과 실제 자본은 사용하지 않는다.

## 1. 재현 가능한 Backtest

OHLCV의 시간 정렬, timezone, 결측치와 signal 시점을 먼저 검증한다. 같은 bar의 종가를 보고 같은 종가에 체결했다고 가정하지 않는다.

```python
def net_return(entry, exit_, fee_rate=0.0005, slippage=0.0005):
    buy = entry * (1 + slippage)
    sell = exit_ * (1 - slippage)
    return (sell * (1 - fee_rate)) / (buy * (1 + fee_rate)) - 1

# signal은 t에서 계산하고, 주문 가격은 다음 거래 가능 bar(t+1)로 모델링한다.
```

EMA short/long, 수수료, slippage, data range, strategy hash를 결과와 함께 저장한다. in-sample 최적화 뒤에는 반드시 별도 out-of-sample 구간을 둔다.

## 2. Paper Credential 격리

Alpaca Paper 계정의 key만 환경변수로 제공하고 source, notebook, 로그에 넣지 않는다. Paper와 live endpoint·key를 같은 `.env`에 섞지 않는다.

```bash
export ALPACA_PAPER_API_KEY='paper-only-key'
export ALPACA_PAPER_SECRET_KEY='paper-only-secret'
export ALPACA_BASE_URL='https://paper-api.alpaca.markets'
```

환경변수 값은 예시이며 실제 secret을 shell history나 repository에 기록하지 않는다.

## 3. 주문 직전 Guard 호출

```python
decision = guard.validate(order=proposal, portfolio=portfolio, now=now)
if not decision.allowed:
    ledger.append({"event": "order_rejected", "reason": decision.reason})
    return

broker.submit_order(decision.order)
```

`validate`는 종목 allowlist, market hours, stale data, order rate, position notional, daily loss와 drawdown을 확인해야 한다. Guard 실패를 예외로 무시하거나 AI가 limit을 수정해 재시도하게 해서는 안 된다.

## 4. 첫 테스트

- 일일 손실 한도 초과 시 신규 주문이 거절되는가?
- kill switch가 미체결 주문을 취소하고 cooldown으로 전환하는가?
- stale-data와 중복 client order ID가 차단되는가?
- 거절 이유, request ID, strategy version이 ledger에 기록되는가?

## Sources

- https://docs.alpaca.markets/us/v1.4.2/docs/paper-trading
- https://docs.alpaca.markets/us/docs/authentication
