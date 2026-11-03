---
date: 2026-11-03
tags: [tech]
type: tech-tool-study
status: draft
---

# Deep Dive: 불변 Guard와 Promotion 설계

> [[tech/ai/ai-paper-trading-system/README|목차로 돌아가기]] · [[tech/ai/ai-paper-trading-system/05-projects|Projects]]

## Immutable Boundary

전략 process는 `OrderProposal`만 만들고 broker client를 직접 import하지 않는다. Guard만 broker adapter를 호출할 수 있게 dependency와 credential을 분리한다. limit configuration은 versioned·reviewed artifact로 제공하며 AI service account에 write 권한을 주지 않는다.

```text
AI / Strategy ──proposal──> Guard ──approved order──> Broker Adapter
       │                       │
       └──── no credentials ───┴── limits · kill switch · audit
```

## Guard 정책 예시

| 검사 | 차단 예시 | 조치 |
|---|---|---|
| `max_daily_loss` | realized + unrealized loss가 한도 초과 | 신규 주문 거절, cooldown |
| `max_drawdown` | equity peak 대비 하락 초과 | kill switch, human review |
| `max_position_notional` | 단일 symbol exposure 초과 | quantity 축소 또는 거절 |
| `max_order_rate` | 짧은 구간의 반복 주문 | rate-limit, deduplicate |
| data freshness | quote/bar가 허용 시간보다 오래됨 | 주문 거절, data alert |

정책 평가에 쓰는 portfolio와 market data도 timestamp와 source를 audit event에 남겨야 한다.

## Failure Ledger

append-only ledger에는 experiment와 execution을 함께 남긴다.

```json
{
  "strategy_version": "ema-v3",
  "git_sha": "abc1234",
  "prompt_model": "reviewer-v1",
  "data_range": "2025-01-01..2026-01-01",
  "seed": 42,
  "event": "order_rejected",
  "reason": "max_daily_loss",
  "max_drawdown": 0.031,
  "broker_request_id": "..."
}
```

SQLite로 시작해도 좋지만, 전략 hash, parameters, data version, fill, 비용, P/L, failure reason의 연결이 끊기지 않아야 한다. MLflow는 experiment lineage와 artifact를 추적하는 보완 수단이다.

## Promotion Gate

1. sandbox backtest: 비용·slippage·편향 검사를 포함한다.
2. walk-forward / out-of-sample: 학습·선택에 쓰지 않은 기간으로 확인한다.
3. Paper 기간: 예상치 못한 API, data, order lifecycle 오류를 관측한다.
4. human approval: 결과와 risk impact를 검토해 제한적으로 승격한다.

AI patch는 각 gate의 입력·출력과 승인자를 남기며, 어느 단계에서도 Guard 설정·broker credential·감사 기록을 수정할 수 없다.

## Sources

- https://mlflow.org/docs/latest/ml/tracking/
- https://docs.alpaca.markets/us/docs/getting-started-with-trading-api
- https://www.quantconnect.com/docs/v2/writing-algorithms/reality-modeling/brokerages/key-concepts
