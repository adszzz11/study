---
date: 2026-06-09
tags:
  - tech
  - ai
  - stock
  - projects
  - trading-ai
type: tech-tool-study
parent: "[[README]]"
---

# 주식 투자와 자동화 AI - 실전 프로젝트

> [[README|목차로 돌아가기]] | [[cheatsheet|다음: 치트시트]]

---

## 1. 프로젝트 아이디어

| 프로젝트 | 난이도 | 학습 포인트 |
|---|---:|---|
| `Beginner Portfolio Tracker` | ⭐ | 보유 종목, 매수가, 현재가, 수익률, 비중, 섹터 노출 |
| `ETF Dollar-Cost Averaging Simulator` | ⭐ | 매월 일정 금액 투자, 장기 수익률, drawdown |
| `Backtest Lab` | ⭐⭐ | moving average, rebalancing, fee, slippage |
| `Paper Trading Logger` | ⭐⭐ | 주문 생성, 취소, 체결 로그 저장 |
| `SEC Filing Summarizer` | ⭐⭐ | EDGAR 문서 요약, LLM structured output |
| `Risk Dashboard` | ⭐⭐⭐ | exposure, daily loss, max drawdown, kill switch |
| `Trading AI Research Pipeline` | ⭐⭐⭐ | data -> features -> model -> backtest -> monitoring |

---

## 2. 프로젝트 1 - Beginner Portfolio Tracker

### 목표

내가 가진 자산이 어디에 얼마나 몰려 있는지 보는 대시보드를 만든다.

### 기능

- 보유 종목 입력
- 매수가, 수량, 현재가 표시
- 평가금액과 수익률 계산
- 종목별 비중 계산
- 섹터/국가/자산군 노출 표시
- 현금 비중 표시

### 데이터 구조 예시

```yaml
positions:
  - ticker: "SPY"
    quantity: 3
    average_price: 520.0
    asset_type: "ETF"
    sector: "broad_market"
  - ticker: "AAPL"
    quantity: 2
    average_price: 190.0
    asset_type: "stock"
    sector: "technology"
cash: 1000
```

### 배울 것

- portfolio value
- unrealized PnL
- allocation
- concentration risk

---

## 3. 프로젝트 2 - ETF Dollar-Cost Averaging Simulator

### 목표

매월 일정 금액을 ETF에 투자했을 때 결과를 시뮬레이션한다. 초보자에게 가장 교육 효과가 좋다.

### 기능

- ETF ticker 선택: `SPY`, `QQQ`, `VTI` 등
- 월 투자금 입력
- 기간 입력
- 최종 평가금액, 총 투자금, 수익률 계산
- 최대 낙폭 표시
- 일시불 투자와 비교

### 핵심 질문

- 장기 투자 중 손실 구간이 얼마나 길었는가?
- 매월 적립식 투자는 하락장에서 어떤 효과가 있었는가?
- ETF가 개별 주식보다 변동성이 낮았는가?

---

## 4. 프로젝트 3 - Backtest Lab

### 목표

단순 이동평균 전략을 만들고, 거래 비용과 `slippage`를 넣어본다.

### 최소 기능

- ticker 입력
- 기간 선택
- 20일/60일 moving average 계산
- 매수/현금 신호 생성
- 거래 비용 반영
- buy-and-hold와 비교
- max drawdown 계산

### 결과 표 예시

| Metric | Strategy | Buy & Hold |
|---|---:|---:|
| Final Value |  |  |
| Annual Return |  |  |
| Volatility |  |  |
| Max Drawdown |  |  |
| Number of Trades |  |  |

### 주의점

- 신호는 반드시 다음 거래일부터 적용한다.
- adjusted price를 사용한다.
- train/test split을 적용한다.
- 파라미터를 과도하게 최적화하지 않는다.

---

## 5. 프로젝트 4 - Paper Trading Logger

### 목표

Alpaca 같은 broker API의 paper trading 환경에서 주문 생성, 취소, 체결 로그를 저장한다.

### 프로젝트 구조 예시

```text
trading-ai/
├── config/
│   └── paper.yaml
├── data/
│   └── orders.parquet
├── src/
│   ├── data_feed.py
│   ├── strategy.py
│   ├── risk.py
│   ├── execution.py
│   ├── logger.py
│   └── monitor.py
└── notebooks/
    └── review_paper_trading.ipynb
```

### 필수 로그

| 필드 | 설명 |
|---|---|
| `strategy_version` | 어떤 전략이 주문을 냈는지 |
| `signal` | 매수/매도/보유 신호 |
| `risk_checks` | 주문 전 리스크 검증 결과 |
| `order_id` | broker 주문 ID |
| `status` | submitted, filled, canceled, rejected |
| `filled_price` | 실제 체결 가격 |
| `error_message` | 실패 원인 |

---

## 6. 프로젝트 5 - SEC Filing Summarizer

### 목표

SEC EDGAR에서 공시를 가져와 LLM으로 요약하되, 투자 추천이 아니라 리스크 요약만 만든다.

### 출력 schema

```json
{
  "company": "Example Inc.",
  "ticker": "EXM",
  "filing_type": "10-K",
  "summary": [
    "Revenue growth slowed compared with the prior year.",
    "The company reports supply chain concentration risk."
  ],
  "risk_factors": [
    {
      "topic": "supply_chain",
      "severity": "medium",
      "evidence": "Risk Factors section"
    }
  ],
  "trade_signal": null
}
```

### 관련 노트

- [[study/tech/ai/codex/README]]
- [[study/tech/ai/langchain-crewai/README]]
- [[study/tech/ai/llm-wiki-study/README]]

---

## 7. Best Practices

- 초보자는 ETF와 장기 분산 투자부터 이해한다.
- 단일 종목 자동매매보다 포트폴리오 추적과 리스크 대시보드부터 만든다.
- backtest에는 fee, slippage, spread, corporate actions를 넣는다.
- live trading 전 paper trading 로그를 최소 1-3개월 모은다.
- LLM은 매수/매도 결정자가 아니라 요약, 분류, 검증 도구로 먼저 사용한다.
- 모든 주문에는 audit log를 남긴다.
- `kill switch` 없이 live trading을 하지 않는다.

---

## 8. 실무 적용 시 고려사항

### 성능

- real-time trading이 아니라면 초반에는 초 단위 latency보다 데이터 정확성이 더 중요하다.
- 대량 파라미터 탐색은 VectorBT처럼 빠른 도구를 쓰고, live 후보는 event-driven backtest로 재검증한다.

### 보안

- broker API key는 코드에 저장하지 않는다.
- paper/live key를 분리한다.
- 주문 권한이 있는 key는 최소 권한으로 관리한다.

### 모니터링

- PnL, exposure, failed orders, data gap, latency를 추적한다.
- daily loss limit 도달 시 신규 주문을 중단한다.
- 비정상 변동성이나 데이터 누락이 있으면 전략을 멈춘다.

---

## 9. 배포 가이드

```text
1. notebook prototype
2. backtest script
3. paper trading service
4. dashboard + alerts
5. small live trading
6. post-trade review
```

live trading은 기술적으로 가능해졌다는 이유만으로 시작하지 않는다. 손실 한도, 운영 로그, broker 정책, 세금/규제 확인이 끝났을 때만 소액으로 시작한다.
