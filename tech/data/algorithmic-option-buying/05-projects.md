---
date: 2026-11-03
tags: [tech]
type: tech-tool-study
status: draft
---

# Projects: 연구에서 Paper Execution까지

> [[tech/data/algorithmic-option-buying/README|목차로 돌아가기]] · [[tech/data/algorithmic-option-buying/cheatsheet|다음: Cheatsheet]]

## 1. Option-chain Research Notebook

OI, change in OI, volume, IV, bid-ask spread를 timestamp별로 수집·시각화한다. signal 시점의 계약 후보가 실제로 유동성 조건을 만족했는지 분석한다.

**완료 기준**: raw snapshot, 정규화 schema, quote freshness report, 선택/제외 근거 chart가 있다.

## 2. Price-action Rule Backtester

VWAP, 고저점 돌파, retest 중 한 setup을 명문화한다. spot·future·option-buying 결과를 동일한 entry timestamp와 비용 가정 아래 비교한다.

**완료 기준**: parameter registry, point-in-time replay, fee/spread/slippage, OOS·walk-forward report가 있다.

## 3. Greeks-aware Risk Dashboard

포지션별 premium at risk, Delta, Gamma, Theta, Vega, expiry concentration, daily drawdown을 표시한다.

**완료 기준**: limit breach가 주문 전 `reject`로 나타나며, stale data와 kill switch 상태가 명확하다.

## 4. Paper Execution Service

`signal → risk gate → simulated fill → immutable audit log` 흐름을 구현한다. broker API는 충분한 검증 뒤 별도 adapter로 교체한다.

**완료 기준**: duplicate event 방지, partial fill, reject, cancel, replay가 테스트된다.

## 5. Regime Monitor

realized volatility 대비 IV, 이벤트 일정, expiry proximity, spread 악화를 감지해 신규 진입을 차단한다.

**완료 기준**: 차단 사유가 signal 결과와 분리되어 log·dashboard에 남는다.

## 기술스택 요약

- 데이터: broker/exchange API, OHLCV, option chain, OI·IV·Greeks 시계열 저장
- 분석: Python, pandas/Polars, NumPy, vectorized backtesting, walk-forward evaluation
- 서비스: FastAPI signal/risk service, PostgreSQL 또는 TimescaleDB, Redis event queue
- 운영: Docker, structured logging, alerting, kill switch, 주문·체결 audit trail
- 준수: 배포 시점의 SEBI retail-algo, 거래소, broker 정책을 재검증

## Sources

- https://www.nseindia.com/option-chain
- https://www.sebi.gov.in/legal/circulars/feb-2025/safer-participation-of-retail-investors-in-algorithmic-trading_91614.html
