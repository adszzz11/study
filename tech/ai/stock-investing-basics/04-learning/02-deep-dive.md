---
date: 2026-06-09
tags:
  - tech
  - ai
  - stock
  - learning
  - deep-dive
type: tech-tool-study
parent: "[[../README]]"
---

# 주식 투자와 자동화 AI - 심화

> [[01-getting-started|이전: 시작하기]] | [[../README|목차로 돌아가기]] | [[../05-projects|다음: 프로젝트]]

---

## 1. 자동화 AI의 핵심은 모델보다 운영이다

주식 자동화 AI를 만들 때 많은 사람이 먼저 `LSTM`, `Transformer`, `Reinforcement Learning` 같은 모델을 떠올린다. 하지만 실제로는 아래 문제가 더 먼저다.

- 데이터가 정확한가?
- 과거 데이터에 미래 정보가 섞이지 않았는가?
- 거래 비용을 반영했는가?
- 손실 제한이 있는가?
- 주문이 실패하면 어떻게 되는가?
- broker API 장애가 나면 멈출 수 있는가?
- 사람이 나중에 판단할 수 있게 로그가 남는가?

```text
좋은 모델 < 좋은 데이터 + 검증 가능한 전략 + 강한 리스크 관리 + 안정적인 실행
```

---

## 2. Data Quality

### 가격 데이터에서 확인할 것

| 항목 | 질문 |
|---|---|
| `adjusted close` | split/dividend 조정이 반영되었는가? |
| `timezone` | 거래소 시간 기준이 맞는가? |
| `missing data` | 휴장일, 데이터 누락, 비정상 값이 처리되었는가? |
| `corporate actions` | split, dividend, merger가 반영되었는가? |
| `survivorship` | 상장폐지 종목이 빠져 있지 않은가? |
| `latency` | 실시간 데이터라면 지연 시간이 어느 정도인가? |

### 데이터 파이프라인 예시

```text
raw market data
-> validation
-> corporate action adjustment
-> feature calculation
-> feature store
-> strategy/model
-> backtest/live execution
```

---

## 3. Bias 방지

### Look-ahead Bias

미래에 알 수 있는 정보를 과거 의사결정에 사용하면 백테스트가 과장된다.

```python
# 잘못된 예: 오늘 종가를 보고 오늘 포지션을 잡는 효과가 날 수 있음
signal = (close.rolling(20).mean() > close.rolling(60).mean()).astype(int)
strategy_return = signal * close.pct_change()

# 개선: 신호는 다음 거래일부터 적용
position = signal.shift(1).fillna(0)
strategy_return = position * close.pct_change()
```

### Survivorship Bias

현재 살아남은 종목만 대상으로 과거를 보면 실패한 기업이 빠진다. 그러면 전략이 실제보다 좋아 보인다.

### Overfitting

한 데이터에서 파라미터를 계속 바꾸며 최고 수익률만 고르면 미래 성능이 떨어질 가능성이 크다.

| 방지 방법 | 설명 |
|---|---|
| `train/test split` | 일부 기간으로 전략을 만들고 다른 기간에서 검증 |
| `out-of-sample` | 전략 개발에 쓰지 않은 데이터로 평가 |
| `walk-forward` | 시간 순서를 지키며 반복 검증 |
| 단순한 규칙 유지 | 설명 가능한 전략부터 시작 |
| 거래 비용 반영 | fee, spread, slippage를 반드시 포함 |

---

## 4. Risk Overlay

`risk overlay`는 모델이 만든 매수/매도 신호 위에 추가되는 안전장치다.

### 기본 리스크 규칙

| 규칙 | 예시 |
|---|---|
| position sizing | 한 종목 비중 최대 5-10% |
| sector cap | 한 섹터 비중 최대 25% |
| max drawdown limit | 전략 손실이 -10%면 중단 |
| daily loss limit | 하루 손실이 -2%면 모든 신규 주문 중단 |
| cash buffer | 현금 5-20% 유지 |
| leverage ban | 초보 단계에서는 leverage 금지 |
| kill switch | 비정상 조건에서 모든 자동 주문 중단 |

### 주문 전 체크 예시

```python
def validate_order(order, portfolio, risk):
    checks = []

    if order.notional > portfolio.value * risk.max_position_ratio:
        checks.append("position size exceeds limit")

    if portfolio.daily_pnl < -portfolio.value * risk.max_daily_loss:
        checks.append("daily loss limit reached")

    if order.ticker in risk.blocked_tickers:
        checks.append("ticker is blocked")

    return {
        "approved": len(checks) == 0,
        "checks": checks,
    }
```

---

## 5. Execution Layer

실거래에서는 전략 신호와 실제 체결 사이에 많은 일이 생긴다.

```text
signal
-> risk validation
-> order creation
-> broker submit
-> accepted/rejected
-> partial fill/full fill/cancel
-> portfolio update
-> audit log
```

### 필수 개념

| 개념 | 설명 |
|---|---|
| `market order` | 현재 가능한 가격으로 즉시 체결을 시도 |
| `limit order` | 지정한 가격 또는 더 좋은 가격에서만 체결 |
| `stop order` | 특정 가격 도달 후 주문 활성화 |
| `spread` | bid와 ask의 차이 |
| `slippage` | 예상 가격과 실제 체결 가격의 차이 |
| `partial fill` | 주문 수량 일부만 체결 |
| `idempotency` | 같은 주문이 중복 실행되지 않게 하는 원칙 |

### Live 전 체크리스트

- [ ] paper trading에서 주문 로그를 1-3개월 이상 모았다.
- [ ] order validation이 있다.
- [ ] retry가 중복 주문을 만들지 않는다.
- [ ] failed order가 알림으로 온다.
- [ ] PnL, exposure, cash, open orders를 대시보드에서 볼 수 있다.
- [ ] broker의 margin/day-trading 정책을 확인했다.
- [ ] kill switch가 있다.

---

## 6. LLM Agent 설계

### 좋은 역할 분담

```text
LLM:
- 공시/뉴스 요약
- 리스크 체크리스트 생성
- 자연어 질문을 구조화된 쿼리로 변환
- JSON schema 기반 signal validation

Rule/Model:
- 실제 매수/매도 신호 생성
- position sizing
- risk limit 적용

Execution System:
- 주문 검증
- broker API 호출
- 체결 상태 추적
- audit log 저장
```

### LLM output schema 예시

```json
{
  "ticker": "AAPL",
  "document_type": "10-K",
  "summary": "The company reports risks related to supply chain concentration and regulatory pressure.",
  "risk_level": "medium",
  "citations": [
    {
      "source": "SEC EDGAR",
      "section": "Risk Factors"
    }
  ],
  "trade_recommendation": null
}
```

> [!note]
> `trade_recommendation`을 `null`로 둔 이유는 LLM 요약과 실제 주문 판단을 분리하기 위해서다.

관련 설계는 [[../../agent-orchestration/README]], [[../../codex/README]], [[../../langchain-crewai/README]]를 참고한다.

---

## 7. Monitoring

자동화 시스템은 만든 뒤가 더 중요하다.

| 모니터링 항목 | 봐야 하는 이유 |
|---|---|
| PnL | 손익 추적 |
| exposure | 특정 종목/섹터/자산군 쏠림 확인 |
| failed orders | 주문 실패 감지 |
| latency | 데이터/주문 지연 확인 |
| data gap | 가격 데이터 누락 확인 |
| model drift | 과거와 다른 데이터 분포 감지 |
| abnormal volatility | 급변장 자동 중단 판단 |
| audit log | 사후 분석과 오류 추적 |

### 알림 예시

```yaml
alerts:
  daily_loss_limit:
    threshold: -0.02
    action: "disable_new_orders"
  data_gap:
    threshold_minutes: 5
    action: "pause_strategy"
  failed_order:
    threshold_count: 1
    action: "notify"
  abnormal_volatility:
    threshold_zscore: 3
    action: "reduce_position"
```

---

## 다음 단계

> [!tip] 다음으로
> [[../05-projects|실전 프로젝트]]에서 작은 프로젝트부터 구현해보자.
