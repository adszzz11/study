---
date: 2026-06-09
tags:
  - tech
  - ai
  - stock
  - cheatsheet
  - trading-ai
type: tech-tool-study
parent: "[[README]]"
---

# 주식 투자와 자동화 AI - 치트시트

> [[README|목차로 돌아가기]]

---

## 초보자 시작 순서

```text
1. stock, ETF, index, dividend 이해
2. risk, diversification, time horizon 이해
3. market order, limit order, spread, slippage 이해
4. OHLCV, adjusted close 읽기
5. ETF와 개별 주식 5년 성과 비교
6. moving average 같은 단순 전략 backtest
7. fee, slippage, train/test split 적용
8. paper trading으로 주문 로그 수집
9. LLM은 요약/분류/검증부터 사용
10. live trading은 소액 + kill switch 이후
```

---

## 핵심 용어

| 용어 | 영문 | 설명 |
|---|---|---|
| 주식 | `stock` | 기업의 일부 소유권 |
| 주 | `share` | 주식 수량 단위 |
| ETF | `exchange-traded fund` | 여러 자산을 묶어 주식처럼 거래하는 상품 |
| 지수 | `index` | 시장/섹터 흐름을 나타내는 지표 |
| 배당 | `dividend` | 회사가 이익 일부를 주주에게 지급 |
| 위험 | `risk` | 손실 가능성 |
| 분산 | `diversification` | 종목, 산업, 국가, 자산군을 나누는 것 |
| 투자 기간 | `time horizon` | 돈을 언제 쓸지 |
| 변동성 | `volatility` | 가격이 흔들리는 정도 |
| 최대 낙폭 | `max drawdown` | 고점 대비 최대 하락폭 |
| 백테스트 | `backtest` | 과거 데이터로 전략을 실험 |
| 모의투자 | `paper trading` | 실제 돈 없이 주문 로직을 시험 |
| 미끄러짐 | `slippage` | 예상 가격과 실제 체결 가격 차이 |
| 스프레드 | `bid/ask spread` | 매수 호가와 매도 호가 차이 |

---

## 자동화 AI 아키텍처 한 장 요약

```text
Data
  OHLCV, quotes, trades, SEC filings, news

Storage/Feature
  Parquet/S3, PostgreSQL/TimescaleDB, returns, volatility, RSI

Research/Model
  rule-based baseline, ML, DL/RL, LLM summarization

Backtest
  event-driven, fees, slippage, spread, corporate actions

Risk
  position sizing, max drawdown, daily loss limit, kill switch

Execution
  broker API, paper trading, order validation, retry, idempotency

Monitoring
  PnL, exposure, failed order, latency, data gap, model drift
```

---

## Backtest 체크리스트

- [ ] 신호를 다음 거래일부터 적용했다.
- [ ] adjusted price를 사용했다.
- [ ] fee를 넣었다.
- [ ] slippage를 넣었다.
- [ ] spread와 liquidity를 고려했다.
- [ ] train/test split을 했다.
- [ ] out-of-sample 성능을 확인했다.
- [ ] survivorship bias를 고려했다.
- [ ] buy-and-hold와 비교했다.
- [ ] max drawdown을 확인했다.

---

## Paper Trading 체크리스트

- [ ] paper/live API key를 분리했다.
- [ ] 주문 생성/취소/체결 로그를 저장한다.
- [ ] rejected/partial fill을 처리한다.
- [ ] retry가 중복 주문을 만들지 않는다.
- [ ] daily loss limit이 있다.
- [ ] kill switch가 있다.
- [ ] 실패 주문이 알림으로 온다.
- [ ] 최소 1-3개월 로그를 모은다.

---

## LLM 사용 원칙

| 좋은 사용 | 피해야 할 사용 |
|---|---|
| SEC filing 요약 | LLM 말만 믿고 매수 |
| 뉴스 분류 | 감성 점수만으로 주문 |
| 리스크 체크리스트 생성 | 손실 제한 없는 자동매매 |
| JSON signal validation | schema 없는 자유문장 주문 |
| tool calling으로 데이터 조회 | 출처 없는 숫자 사용 |

### Structured signal schema

```json
{
  "ticker": "SPY",
  "signal": "hold",
  "confidence": 0.62,
  "reasons": [
    "20-day moving average is above 60-day moving average"
  ],
  "risk_flags": [
    "market volatility is elevated"
  ]
}
```

---

## 초보자 금지 목록

- leverage
- margin trading
- options/futures
- 검증 없는 단타 자동매매
- 한 종목 몰빵
- 수수료 없는 백테스트
- paper trading 없는 live trading
- kill switch 없는 자동 주문

---

## 참고 링크

- [SEC Investor.gov Stocks FAQ](https://www.investor.gov/introduction-investing/investing-basics/investment-products/stocks)
- [FINRA Risk](https://www.finra.org/investors/investing/investing-basics/risk)
- [FINRA ETFs/ETPs](https://www.finra.org/investors/investing/investment-products/exchange-traded-funds-and-products)
- [SEC EDGAR Search](https://www.sec.gov/edgar/search-and-access)
- [Alpaca Paper Trading Docs](https://docs.alpaca.markets/us/docs/paper-trading)
- [QuantConnect LEAN](https://www.quantconnect.com/docs/v2/writing-algorithms/key-concepts/algorithm-engine)
- [VectorBT Docs](https://vectorbt.dev/)
- [Backtrader Docs](https://backtrader.readthedocs.io/en/latest/)

---

## 관련 노트

- [[study/tech/ai/codex/README]]
- [[study/tech/ai/langchain-crewai/README]]
- [[study/tech/ai/litellm/README]]
- [[study/tech/ai/agent-orchestration/README]]
