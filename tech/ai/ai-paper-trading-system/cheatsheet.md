---
date: 2026-11-03
tags: [tech]
type: tech-tool-study
status: draft
---

# Cheatsheet: AI Paper Trading Risk Guard

> [[tech/ai/ai-paper-trading-system/README|목차로 돌아가기]]

## 운영 원칙

| 해야 할 것 | 하지 말 것 |
|---|---|
| AI는 proposal과 analysis로 제한 | AI에게 broker credential·배포 권한 부여 |
| Guard를 별도 boundary로 실행 | strategy가 broker를 직접 호출 |
| paper/live key와 endpoint 분리 | 같은 config에서 mode만 바꿔 live 전환 |
| 비용·slippage·out-of-sample 반영 | 수수료 없는 in-sample 수익만 비교 |
| append-only ledger와 request ID 보존 | 실패·거절 event를 버리기 |

## Order 전 Checklist

```text
[ ] Paper endpoint와 paper-only credential인가?
[ ] Market data가 fresh하고 timestamp가 정상인가?
[ ] Symbol이 allowlist에 있는가?
[ ] Position notional / order rate 한도 내인가?
[ ] daily loss와 drawdown 한도 내인가?
[ ] client order ID가 중복되지 않는가?
[ ] 승인 또는 거절 event를 ledger에 기록하는가?
```

## 기본 흐름

```python
proposal = strategy.propose(snapshot)
result = guard.validate(proposal, portfolio, snapshot)
if result.allowed:
    execution.submit(result.order)
else:
    ledger.append(result.audit_event)
```

## 관측 지표

- equity, realized/unrealized P&L, max drawdown
- rejected/canceled orders, risk-gate hit, cooldown 상태
- stale-data 시간, broker request ID, API error/retry 횟수
- strategy hash, data version, prompt/model version, seed

## Sources

- https://docs.alpaca.markets/us/docs/getting-started-with-trading-api
- https://docs.alpaca.markets/us/v1.4.2/docs/paper-trading
