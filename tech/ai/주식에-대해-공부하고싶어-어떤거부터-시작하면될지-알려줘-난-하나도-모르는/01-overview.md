---
date: 2026-06-09
tags:
  - tech
  - ai
  - stock
  - investing
  - overview
type: tech-tool-study
parent: "[[README]]"
---

# 주식 투자와 자동화 AI - 개요

> [[README|목차로 돌아가기]] | [[02-ecosystem|다음: 생태계]]

---

## 1. What - 주식이란?

> **한 줄 정의**: `stock`은 기업의 일부 소유권이고, 주식 투자는 그 소유권을 사고팔거나 보유하면서 성장, 배당, 가격 변동 수익을 기대하는 활동이다.

### 초보자가 먼저 알아야 할 핵심 개념

- `stock`: 회사의 지분이다. 주식을 산다는 것은 그 회사의 아주 작은 일부를 소유한다는 뜻이다.
- `share`: 주식의 단위다. 예를 들어 A회사 주식 1주, 10주처럼 센다.
- `ETF`(Exchange-Traded Fund): 여러 주식, 채권, 원자재 등을 묶어 거래소에서 주식처럼 사고파는 상품이다.
- `index`: 시장이나 특정 산업의 흐름을 나타내는 지표다. 예: S&P 500, Nasdaq 100.
- `dividend`: 회사가 이익 일부를 주주에게 나누어 주는 배당이다.
- `risk`: 손실 가능성이다. 수익 가능성만 보면 안 되고, 얼마까지 잃을 수 있는지를 함께 봐야 한다.
- `time horizon`: 돈을 언제 쓸지에 대한 투자 기간이다. 1년 뒤 쓸 돈과 20년 뒤 쓸 돈은 투자 방식이 달라야 한다.

### 가장 중요한 출발점

초보자는 "무슨 종목을 사야 해?"보다 아래 질문을 먼저 해야 한다.

| 질문 | 이유 |
|---|---|
| 이 돈을 언제 쓸 예정인가? | `time horizon`이 짧으면 손실 회복 시간이 부족하다. |
| 한 종목이 반토막 나도 버틸 수 있는가? | 단일 종목은 `concentration risk`가 크다. |
| 여러 자산에 나누어 투자했는가? | `diversification`은 기본적인 위험 관리 방법이다. |
| 수수료와 세금, 환율을 고려했는가? | 실제 수익률은 화면의 가격 변동과 다르다. |
| 전략을 과거 데이터로 검증했는가? | 감정적 매매를 줄이고 실패 조건을 확인할 수 있다. |

---

## 2. Why - 왜 순서가 중요한가?

### 초보자가 자주 하는 실수

- 뉴스나 유튜브에서 본 종목을 바로 산다.
- 한 종목에 큰 금액을 몰아넣는다.
- 손실이 나면 이유 없이 물타기한다.
- `backtest` 없이 자동매매부터 만들려고 한다.
- 수수료, `slippage`, 세금, 환율, 체결 실패를 무시한다.
- AI가 만든 신호를 검증 없이 매수/매도 결정으로 사용한다.

### 올바른 시작 순서

```text
투자 기초 -> 데이터 이해 -> 단순 전략 -> 백테스트 -> 리스크 관리 -> paper trading -> AI 보조 -> 소액 live
```

| 단계 | 배울 것 | 초보자 기준 목표 |
|---|---|---|
| 투자 기초 | stock, ETF, index, risk | 무엇을 사고 있는지 설명할 수 있다. |
| 계좌/주문 | market order, limit order, spread | 주문이 어떻게 체결되는지 안다. |
| 위험 관리 | diversification, position sizing | 한 번의 실수로 계좌가 망가지지 않게 한다. |
| 데이터 | OHLCV, adjusted close | 가격 데이터의 의미와 함정을 안다. |
| 전략 | moving average, rebalancing | 감정이 아니라 규칙으로 실험한다. |
| 검증 | backtest, out-of-sample | 과거 수익률 착시를 줄인다. |
| 자동화 | paper trading, monitoring | 실제 돈 없이 주문 로직을 검증한다. |

---

## 3. 주식 자동화 AI란?

> **한 줄 정의**: 주식 자동화 AI는 가격, 거래량, 재무제표, 뉴스 같은 데이터를 받아 전략 또는 모델로 신호를 만들고, 백테스트와 리스크 통제를 거쳐 주문과 모니터링까지 연결하는 시스템이다.

### 전체 아키텍처

```text
Data Layer
- Market data: OHLCV, real-time quote, trades
- Fundamental data: SEC EDGAR 10-K/10-Q/8-K
- Alternative data: news, earnings calendar, sentiment

Storage/Feature Layer
- PostgreSQL/TimescaleDB 또는 Parquet/S3
- feature store: returns, volatility, moving average, RSI, macro indicators

Research/Model Layer
- rule-based baseline
- ML: XGBoost, LightGBM, RandomForest
- DL/RL: LSTM, Transformer, Reinforcement Learning
- LLM agent: filing/news summarization, tool calling, structured signal generation

Backtest Layer
- event-driven backtest 권장
- fees, slippage, spread, liquidity, corporate actions 반영
- look-ahead bias, survivorship bias 방지

Risk Layer
- position sizing
- max drawdown limit
- stop-loss/take-profit
- sector exposure cap
- daily loss limit
- kill switch

Execution Layer
- broker API: Alpaca, Interactive Brokers, QuantConnect/LEAN
- paper trading first
- live trading은 order validation, retry, idempotency, audit log 필수

Monitoring Layer
- dashboard, alerts, PnL, exposure, failed order, latency
- model drift, data gap, abnormal volatility 감지
```

### 자동화는 무엇을 잘하는가?

- 반복적인 데이터 수집과 정리
- 규칙 기반 전략의 일관된 실행
- 여러 종목의 조건 동시 확인
- 뉴스, 공시, 재무제표 요약
- 리스크 한도 초과 감지
- 주문 로그와 체결 로그 저장

### 자동화가 해결하지 못하는 것

- 미래 수익 보장
- 잘못된 데이터로 만든 잘못된 전략
- 시장 급변, 거래 정지, 유동성 부족
- 과최적화된 `backtest` 착시
- 규제, 세금, broker 정책 확인
- 투자자의 손실 감내 능력

> [!warning]
> 자동화는 수익만 자동화하지 않는다. 손실, 실수, 잘못된 주문도 자동화할 수 있다.

---

## 4. 초보자용 핵심 특징

### 먼저 배울 것

| 개념 | 영문 용어 | 초보자 설명 |
|---|---|---|
| 주식 | `stock` | 회사의 일부 소유권 |
| ETF | `exchange-traded fund` | 여러 자산을 묶어 주식처럼 거래하는 상품 |
| 분산 | `diversification` | 여러 종목, 산업, 국가, 자산군으로 나누는 것 |
| 변동성 | `volatility` | 가격이 흔들리는 정도 |
| 최대 낙폭 | `max drawdown` | 고점 대비 얼마나 크게 빠졌는지 |
| 포지션 크기 | `position sizing` | 한 종목에 얼마를 넣을지 정하는 것 |
| 백테스트 | `backtest` | 과거 데이터로 전략을 시험하는 것 |
| 모의투자 | `paper trading` | 실제 돈 없이 주문 로직을 시험하는 것 |

### 처음에는 피할 것

- `leverage` 사용
- 옵션, 선물, 마진 거래
- 하루에도 여러 번 사고파는 초단타
- 검증 없는 AI 매수/매도 추천
- "확실한 수익"처럼 말하는 전략

---

## 5. 자동화 AI에서 LLM의 적절한 역할

LLM은 처음부터 "매수/매도 결정자"로 쓰기보다 보조 분석 도구로 쓰는 편이 안전하다.

| 역할 | 좋은 사용 예 | 주의점 |
|---|---|---|
| Filing summarization | SEC 10-K/10-Q 핵심 위험 요약 | 원문 출처와 섹션을 남겨야 한다. |
| News classification | 호재/악재/중립 분류 | 감성 점수만으로 주문하면 위험하다. |
| Checklist generation | 리스크 체크리스트 생성 | 최종 판단은 규칙과 검증 로직이 해야 한다. |
| Structured signal validation | JSON schema로 신호 형식 검증 | 신호의 수익성 검증은 별도 backtest가 필요하다. |
| Tool calling | 가격, 공시, 포트폴리오 조회 도구 호출 | 도구 응답 실패와 지연을 처리해야 한다. |

관련 구현 방식은 [[study/tech/ai/langchain-crewai/README]], [[study/tech/ai/codex/README]], [[study/tech/ai/openrouter]]와 함께 보면 좋다.

---

## 6. 규제와 운영 주의

- 미국 시장 자동화 매매를 하려면 broker별 `margin`, `day trading`, `pattern day trader`, 주문 제한 정책을 확인해야 한다.
- 2026년 SEC의 `SR-FINRA-2025-017` 승인처럼 margin/day-trading 관련 규칙은 바뀔 수 있다.
- live trading 전에 최소 1-3개월 이상 `paper trading` 로그를 모으고, 체결 실패와 데이터 누락을 확인한다.
- 자동 주문 시스템에는 `kill switch`, `audit log`, `order validation`, `retry`, `idempotency`가 필요하다.

---

## 다음 단계

> [!tip] 다음으로
> 개념을 이해했다면 [[02-ecosystem|생태계와 관련 도구 비교]]를 살펴보자.

---

## References

- [SEC Investor.gov Stocks FAQ](https://www.investor.gov/introduction-investing/investing-basics/investment-products/stocks)
- [FINRA Risk](https://www.finra.org/investors/investing/investing-basics/risk)
- [FINRA ETFs/ETPs](https://www.finra.org/investors/investing/investment-products/exchange-traded-funds-and-products)
- [SEC SR-FINRA-2025-017](https://www.sec.gov/rules-regulations/self-regulatory-organization-rulemaking/sr-finra-2025-017)
