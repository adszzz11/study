---
date: 2026-11-03
tags: [tech]
type: tech-tool-study
status: draft
---

# References: 검증 출처

> [[tech/ai/ai-paper-trading-system/README|목차로 돌아가기]]

## Primary Source

1. [Instagram 원본 릴 — lazy_owen](https://www.instagram.com/reel/DfPDCU-Ma2R/) — AI가 손실 뒤 전략 코드를 개선하는 Paper Trading 발상.

## Broker와 Execution

2. [Alpaca Paper Trading](https://docs.alpaca.markets/us/v1.4.2/docs/paper-trading) — simulator의 범위와 fill 가정 확인.
3. [Alpaca Authentication](https://docs.alpaca.markets/us/docs/authentication) — paper/live endpoint와 credential 분리.
4. [Alpaca Portfolio History API](https://docs.alpaca.markets/us/reference/getaccountportfoliohistory-1) — equity·P/L 관측 데이터.
5. [Alpaca Trading API MCP](https://docs.alpaca.markets/us/docs/trading-api-mcp) — toolset filtering과 paper 기본값.
6. [Alpaca Trading API 시작하기](https://docs.alpaca.markets/us/docs/getting-started-with-trading-api) — request ID 보존과 API 운영 참고.

## Research와 Guard

7. [QuantConnect Paper Trading](https://www.quantconnect.com/docs/v2/cloud-platform/live-trading/brokerages/quantconnect-paper-trading)
8. [QuantConnect Reality Modeling / Brokerage Model](https://www.quantconnect.com/docs/v2/writing-algorithms/reality-modeling/brokerages/key-concepts)
9. [Freqtrade Protections](https://docs.freqtrade.io/en/2022.12/plugins/)
10. [FinRL](https://www.finrl.ai/)
11. [MLflow Tracking](https://mlflow.org/docs/latest/ml/tracking/) — parameter, code version, metric, artifact의 run 단위 기록.

문서의 API 세부 사항, simulator 행동, credential scope는 구현 직전에 다시 확인한다.
