---
date: 2026-06-09
tags:
  - tech
  - ai
  - stock
  - learning
  - beginner
type: tech-tool-study
parent: "[[../README]]"
---

# 주식 투자와 자동화 AI - 시작하기

> [[../README|목차로 돌아가기]] | [[02-deep-dive|다음: 심화]]

---

## 1. 초보자 학습 원칙

초보자는 `AI 자동매매`부터 시작하면 거의 반드시 잘못된 실험을 하게 된다. 올바른 순서는 아래와 같다.

```text
투자 기초 -> 데이터 -> 백테스트 -> 리스크 -> paper trading -> AI
```

### 첫 4주 학습 계획

| 주차 | 목표 | 할 일 |
|---|---|---|
| 1주차 | 주식/ETF 이해 | stock, ETF, index, dividend, risk 정리 |
| 2주차 | 가격 데이터 읽기 | OHLCV, adjusted close, volatility 확인 |
| 3주차 | 단순 전략 실험 | 20-day/60-day moving average backtest |
| 4주차 | 자동화 전 점검 | 수수료, slippage, paper trading 로그 설계 |

---

## 2. 실습 1 - ETF와 개별 주식 비교

### 목표

`SPY`, `QQQ`, 관심 기업 1개를 놓고 5년 가격 그래프, 최대 낙폭, 연평균 수익률을 비교한다.

### 비교 항목

| 항목 | 설명 |
|---|---|
| `annual return` | 1년 평균 수익률 |
| `volatility` | 가격 흔들림 정도 |
| `max drawdown` | 고점 대비 최대 하락폭 |
| `correlation` | 두 자산이 비슷하게 움직이는 정도 |

### Python 예시

```python
import yfinance as yf
import pandas as pd

tickers = ["SPY", "QQQ", "AAPL"]
prices = yf.download(tickers, period="5y", auto_adjust=True)["Close"]

returns = prices.pct_change().dropna()

annual_return = (1 + returns.mean()) ** 252 - 1
annual_volatility = returns.std() * (252 ** 0.5)

running_max = prices.cummax()
drawdown = prices / running_max - 1
max_drawdown = drawdown.min()

summary = pd.DataFrame({
    "annual_return": annual_return,
    "annual_volatility": annual_volatility,
    "max_drawdown": max_drawdown,
})

print(summary)
```

> [!note]
> `yfinance`는 학습용으로 쓰기 쉽지만, 실거래 시스템의 공식 market data로 가정하면 안 된다. 운영 단계에서는 데이터 권한, 지연, 누락, 조정 가격 정책을 확인해야 한다.

---

## 3. 실습 2 - 단순 이동평균 전략 만들기

### 전략 규칙

```text
if 20-day moving average > 60-day moving average:
    buy or hold
else:
    cash
```

### 확인할 것

- 수수료를 넣었는가?
- `slippage`를 넣었는가?
- 종가를 보고 같은 종가에 매수하는 오류가 없는가?
- `train/test split`을 했는가?
- ETF 적립식 투자와 비교했는가?

### Python 예시

```python
import yfinance as yf
import pandas as pd

symbol = "SPY"
price = yf.download(symbol, period="10y", auto_adjust=True)["Close"]

ma20 = price.rolling(20).mean()
ma60 = price.rolling(60).mean()

signal = (ma20 > ma60).astype(int)
position = signal.shift(1).fillna(0)

daily_return = price.pct_change().fillna(0)
strategy_return = position * daily_return

fee = 0.0005
turnover = position.diff().abs().fillna(0)
strategy_return = strategy_return - turnover * fee

equity_curve = (1 + strategy_return).cumprod()
buy_and_hold = (1 + daily_return).cumprod()

print({
    "strategy_final": float(equity_curve.iloc[-1]),
    "buy_hold_final": float(buy_and_hold.iloc[-1]),
})
```

---

## 4. 실습 3 - 잘못된 backtest 찾기

### 체크리스트

| 문제 | 설명 | 예시 |
|---|---|---|
| `look-ahead bias` | 미래 데이터를 과거 의사결정에 사용 | 오늘 종가를 보고 오늘 종가에 매수 |
| `survivorship bias` | 살아남은 종목만 사용 | 상장폐지 종목 제외 |
| `data snooping` | 같은 데이터로 반복 최적화 | 가장 잘 나온 파라미터만 선택 |
| 수수료 누락 | 실제 비용 미반영 | fee 0으로 백테스트 |
| `slippage` 누락 | 원하는 가격에 항상 체결된다고 가정 | 유동성 낮은 종목에서 문제 |
| corporate action 누락 | split/dividend 반영 안 함 | adjusted price 미사용 |

### 좋은 질문

- 이 전략은 왜 돈을 벌어야 하는가?
- 같은 규칙이 다른 기간에도 작동하는가?
- 거래 비용을 넣어도 남는가?
- 전략이 ETF 장기 보유보다 나은가?
- 손실이 길어질 때 중단 기준이 있는가?

---

## 5. 실습 4 - paper trading

`paper trading`은 실제 돈 없이 broker API로 주문 생성, 취소, 체결 흐름을 시험하는 단계다.

### 저장해야 할 로그

```text
timestamp
strategy_version
ticker
signal
order_type
requested_qty
requested_price
submitted_order_id
filled_qty
filled_price
status
error_message
portfolio_value
risk_checks
```

### 최소 운영 기간

- 최소 1개월, 가능하면 3개월 이상
- 시장이 상승/하락/횡보하는 구간을 모두 겪어보는 것이 좋다.
- 주문 실패, 데이터 누락, API 지연, 잘못된 포지션 계산이 있었는지 확인한다.

---

## 6. 실습 5 - AI 붙이기

처음에는 LLM에게 "살까 말까?"를 묻지 않는다. 대신 아래처럼 검증 가능한 보조 업무부터 맡긴다.

| LLM 작업 | 입력 | 출력 |
|---|---|---|
| 공시 요약 | 10-K risk factors | 핵심 리스크 bullet |
| 뉴스 분류 | 기사 제목/본문 | positive/negative/neutral |
| 리스크 체크 | 포트폴리오 상태 | 경고 목록 |
| 신호 검증 | strategy output | JSON schema 통과 여부 |

### Structured signal 예시

```json
{
  "ticker": "SPY",
  "signal": "hold",
  "confidence": 0.62,
  "reasons": [
    "20-day moving average is above 60-day moving average",
    "position size is within risk limit"
  ],
  "risk_flags": [
    "market volatility is elevated"
  ]
}
```

관련 구현 흐름은 [[../../codex/README]], [[../../langchain-crewai/README]], [[../../litellm/README]]를 참고한다.

---

## 다음 단계

> [!tip] 다음으로
> 기본 실습을 끝냈다면 [[02-deep-dive|심화]]에서 bias, risk overlay, execution 구조를 더 깊게 보자.
