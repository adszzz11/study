---
date: 2026-11-03
tags: [tech]
type: tech-tool-study
status: draft
---

# Ecosystem: 도구와 대안 비교

> [[tech/ai/ai-paper-trading-system/README|목차로 돌아가기]] · [[tech/ai/ai-paper-trading-system/03-references|References]]

| 선택지 | 강점 | 적합한 경우 | 주의점 |
|---|---|---|---|
| Alpaca Trading API + 자체 Guard | Paper 계정·주문·portfolio API, Python 친화적 | 미국 주식/crypto 중심의 직접 구축 | Paper fill은 실제 유동성을 완전히 재현하지 않는다 |
| QuantConnect LEAN | backtest·paper·brokerage abstraction 통합 | 다자산 연구와 framework 기반 운영 | 기본 Paper 모델에 slippage가 없을 수 있어 현실 모델 보강이 필요하다 |
| Freqtrade | crypto bot, stoploss·drawdown protection | crypto 중심 rule-based bot | AI code 변경보다 protection 설정·검증을 우선한다 |
| FinRL | RL 기반 quantitative research | RL agent 실험과 학습 pipeline | 연구 성과가 live 성과를 보장하지 않으며 execution guard가 별도 필요하다 |
| Alpaca Trading API MCP | AI client에서 account/data/order tool 사용 | AI-assisted analysis 또는 제한된 paper workflow | toolset 최소 권한과 인간 승인 흐름이 필요하다 |

## 선택 기준

1. broker와 자산군을 먼저 고른다. 시작점은 Paper 전용 key와 endpoint가 명확한 Alpaca가 단순하다.
2. 연구 규모가 커지면 LEAN 또는 FinRL을 사용하더라도, 주문 직전 Guard는 framework 밖의 독립 boundary로 남긴다.
3. bot framework의 stoploss는 유용하지만, 일일 손실·주문 빈도·stale-data 같은 운영 규칙까지 대체한다고 가정하지 않는다.
4. AI tool integration은 read-only analysis부터 시작하고 order tool은 allowlist·approval·audit이 준비된 뒤 최소 권한으로 연다.

## Sources

- https://docs.alpaca.markets/us/docs/trading-api-mcp
- https://www.quantconnect.com/docs/v2/cloud-platform/live-trading/brokerages/quantconnect-paper-trading
- https://docs.freqtrade.io/en/2022.12/plugins/
- https://www.finrl.ai/
