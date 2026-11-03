---
date: 2026-11-03
tags: [tech]
type: tech-tool-study
status: draft
---

# Ecosystem: 대안과 검증 비교

> [[tech/data/algorithmic-option-buying/README|목차로 돌아가기]] · [[tech/data/algorithmic-option-buying/03-references|다음: References]]

| 접근 | 장점 | 핵심 약점 | 적합한 검증 |
|---|---|---|---|
| Discretionary price action | 맥락 판단이 빠름 | 재현성·감사 가능성이 낮음 | 거래 일지와 사전 정의 setup |
| Rule-based option buying | 진입·청산·손실 한도를 자동 검증 | regime 변화와 overfitting | out-of-sample, walk-forward |
| Futures/spot directional trade | Greeks·IV·Theta가 없어 구조가 단순 | 손실 제한이 option premium처럼 내재적이지 않음 | 동일 signal의 risk-adjusted 비교 |
| Short-premium option strategy | 시간가치가 유리할 수 있음 | tail risk·margin·복잡성이 큼 | stress test와 margin 시뮬레이션 |
| Buy-and-hold / ETF | 운용 부담·거래비용이 낮음 | 단기 방향성·event trade 목적에는 부적합 | 장기 benchmark 대비 성과 |

## Option Buying이 추가하는 변수

| 변수 | 의미 | 같은 방향 예측에도 달라질 수 있는 결과 |
|---|---|---|
| Delta | 기초자산 가격 변화 민감도 | 계약의 즉시 가격 반응이 달라진다. |
| Gamma | Delta 변화 민감도 | 큰 가격 이동에서 exposure가 빠르게 변한다. |
| Theta | 시간 경과 민감도 | 가격이 멈춰도 premium이 줄 수 있다. |
| Vega | IV 변화 민감도 | IV 하락이 방향 이익을 상쇄할 수 있다. |
| Spread/liquidity | 거래 가능한 호가의 질 | backtest 중간가격보다 실제 fill이 나빠질 수 있다. |

## 선택 기준

- 단순한 directional signal의 유효성부터 검증하려면 먼저 spot/futures proxy를 사용해 signal 자체를 분리한다.
- payoff 비대칭과 정해진 premium risk가 필요하면 option buying을 검토하되, Greeks와 execution cost를 모형에 넣는다.
- short premium은 option buying의 대체재가 아니라 margin 및 tail-risk 구조가 다른 전략군이다.

## Sources

- https://www.cboe.com/insights/posts/learning-the-greeks-an-experts-perspective
- https://www.theocc.com/company-information/documents-and-archives/options-disclosure-document
