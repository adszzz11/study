---
date: 2026-11-03
tags: [tech]
type: tech-tool-study
status: draft
---

# Deep Dive: Point-in-time 검증과 Risk Gate

> [[tech/data/algorithmic-option-buying/README|목차로 돌아가기]] · [[tech/data/algorithmic-option-buying/05-projects|다음: Projects]]

## 1. Point-in-time Dataset

각 decision timestamp에는 그 순간 이용 가능했던 값만 쓴다. OHLCV bar의 close, option-chain snapshot, quote freshness, contract metadata를 함께 저장한다.

```text
decision_time
  ├─ underlying bar closed_at
  ├─ option quote received_at / exchange_timestamp
  ├─ selected expiry / strike / right
  ├─ bid / ask / LTP / volume / OI / IV / Greeks
  └─ risk inputs: position, daily P&L, limits
```

다음 편향을 명시적으로 검사한다.

- 현재 bar의 high/low를 종가 전에 사용한 look-ahead bias
- 만기·상장폐지 계약을 제거해 버리는 survivorship bias
- 만기 rollover와 corporate action을 무시하는 data discontinuity
- middle price fill, 수수료 누락, 부분체결 누락으로 인한 execution bias

## 2. 계약 선택과 Risk Gate

signal이 있어도 모든 계약이 거래 대상은 아니다. 예시는 broker와 시장 사양에 맞게 별도 설정한다.

```python
def allow_order(candidate, account, now):
    return (
        candidate.quote_age_seconds <= 2
        and candidate.bid_ask_spread_pct <= 0.05
        and candidate.volume >= candidate.min_volume
        and candidate.premium_at_risk <= account.max_trade_premium
        and account.daily_realized_plus_open_pnl > -account.daily_loss_limit
        and account.open_positions < account.max_open_positions
        and not account.kill_switch
    )
```

위 숫자는 추천값이 아니라 구조 예시다. expiry-day 차단, market-event window, IV/realized-volatility 조건, position Greeks concentration도 독립된 policy로 만든다.

## 3. 평가 순서

1. in-sample에서 signal 정의를 고정한다.
2. holdout/out-of-sample 기간에서 수정 없이 재실행한다.
3. 여러 시간 구간을 이동시키는 walk-forward로 regime 변화에 대한 민감도를 본다.
4. spot/futures proxy와 option buying을 동일한 signal, 비용 가정, risk budget에서 비교한다.
5. paper execution에서 order reject, stale data, partial fill, kill switch를 리허설한다.

## 4. 운영 경계

research service는 signal과 후보 계약을 만들고, execution adapter는 broker API 호출을 담당하게 분리한다. 모든 상태 전이는 correlation ID로 연결한다.

```text
signal_created → risk_approved/rejected → order_submitted
               → acknowledged/rejected → partially_filled/filled/cancelled
```

인도 시장 적용 시에는 SEBI의 retail algo framework와 implementation schedule, 거래소 및 broker의 최신 계정·등록·식별·감사 요건을 주문 연결 전 확인한다.

## Sources

- https://www.sebi.gov.in/legal/circulars/feb-2025/safer-participation-of-retail-investors-in-algorithmic-trading_91614.html
- https://www.sebi.gov.in/sebi_data/attachdocs/sep-2025/1759232056254.pdf
- https://www.nseindia.com/option-chain
