---
date: 2026-06-09
tags:
  - tech
  - ai
  - stock
  - references
  - trading-ai
type: tech-tool-study
parent: "[[README]]"
---

# 주식 투자와 자동화 AI - 참고자료

> [[02-ecosystem|이전: 생태계]] | [[README|목차로 돌아가기]] | [[04-learning/01-getting-started|다음: 시작하기]]

---

## 공식 투자 기초 자료

| 자료 | 용도 | 메모 |
|---|---|---|
| [SEC Investor.gov Stocks FAQ](https://www.investor.gov/introduction-investing/investing-basics/investment-products/stocks) | 주식의 기본 개념 | stock, shareholder, risk를 공식 설명으로 확인 |
| [FINRA Risk](https://www.finra.org/investors/investing/investing-basics/risk) | 투자 위험 이해 | asset allocation, diversification 관점 |
| [FINRA ETFs/ETPs](https://www.finra.org/investors/investing/investment-products/exchange-traded-funds-and-products) | ETF/ETP 이해 | ETF가 무엇이고 어떤 위험이 있는지 확인 |

---

## 공식 데이터/규제 자료

| 자료 | 용도 | 메모 |
|---|---|---|
| [SEC EDGAR Search](https://www.sec.gov/edgar/search-and-access) | 미국 기업 공시 검색 | 10-K, 10-Q, 8-K 기반 재무/리스크 분석 |
| [SEC SR-FINRA-2025-017](https://www.sec.gov/rules-regulations/self-regulatory-organization-rulemaking/sr-finra-2025-017) | 2026년 FINRA Rule 4210 변경 | day trading margin provisions와 intraday margin standard 확인 |

> [!warning]
> 규제, margin, day trading 정책은 시간이 지나며 바뀔 수 있다. 자동화 매매를 할 때는 broker와 규제기관의 최신 문서를 다시 확인해야 한다.

---

## Broker/API 자료

| 자료 | 용도 | 메모 |
|---|---|---|
| [Alpaca Paper Trading Docs](https://docs.alpaca.markets/us/docs/paper-trading) | 모의 주문 환경 | live 전 주문 생성/취소/체결 로그 검증 |
| [Alpaca Market Data API Docs](https://docs.alpaca.markets/us/docs/about-market-data-api) | market data 연동 | 데이터 권한, 범위, 요금 확인 필요 |
| [Alpaca SDKs and Tools](https://docs.alpaca.markets/us/docs/sdks-and-tools) | SDK 확인 | Python 등 개발 환경 연동 |

---

## Backtest/Algorithm Engine

| 자료 | 용도 | 메모 |
|---|---|---|
| [QuantConnect LEAN Algorithm Engine](https://www.quantconnect.com/docs/v2/writing-algorithms/key-concepts/algorithm-engine) | event-driven algorithm 구조 | backtest/live 연결 구조 학습 |
| [QuantConnect LEAN GitHub](https://github.com/quantconnect/lean) | open-source engine | 실제 엔진 구조 참고 |
| [VectorBT Docs](https://vectorbt.dev/) | 빠른 벡터화 백테스트 | parameter search, pandas/NumPy 친화 |
| [Backtrader Docs](https://backtrader.readthedocs.io/en/latest/) | Python 백테스트 학습 | 전략 객체 구조 이해 |

---

## OpenAI/LLM 자동화 자료

| 자료 | 용도 | 메모 |
|---|---|---|
| [OpenAI Function Calling](https://help.openai.com/en/articles/8555517-function-calling-in-the-openai-api) | 도구 호출 기반 자동화 | 가격 조회, 공시 조회, 주문 전 체크 도구 연결 |
| [OpenAI Structured Outputs](https://platform.openai.com/docs/guides/structured-outputs) | JSON schema 기반 출력 | trading signal 형식 검증에 사용 |

관련 노트:

- [[study/tech/ai/codex/README]]
- [[study/tech/ai/langchain-crewai/README]]
- [[study/tech/ai/litellm/README]]

---

## AI Trading 연구 자료

| 자료 | 용도 | 메모 |
|---|---|---|
| [FinRL-X 2026 paper](https://arxiv.org/abs/2603.21330) | AI-native quant architecture 참고 | 실거래 보장 아님 |
| [BacktestBench 2026 paper](https://arxiv.org/abs/2605.17937) | backtest 평가 이슈 참고 | bias와 평가 방식 확인 |

---

## 읽는 순서

```text
1. SEC Investor.gov Stocks FAQ
2. FINRA Risk
3. FINRA ETFs/ETPs
4. SEC EDGAR Search
5. VectorBT 또는 Backtrader Docs
6. Alpaca Paper Trading Docs
7. OpenAI Structured Outputs / Function Calling
8. QuantConnect LEAN
9. FinRL-X / BacktestBench
```

---

## 관련 노트

- [[study/tech/ai/llm-wiki-study/README]]
- [[study/tech/ai/agent-orchestration/README]]
- [[study/tech/data/cloudflare-r2/README]]
