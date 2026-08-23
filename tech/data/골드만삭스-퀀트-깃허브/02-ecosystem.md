---
date: 2026-08-24
tags: [tech]
type: tech-tool-study
status: draft
---

# GS Quant Ecosystem 비교

## Positioning

GS Quant의 차별점은 pure analytics library, standalone pricing engine, raw vendor API 중 하나만 제공하는 것이 아니라 Python domain model을 통해 이 층들을 연결한다는 점이다. 대신 server-backed 기능의 실질적 가치는 Marquee 계약과 entitlement에 크게 좌우된다.

## 접근 방식 비교

| 선택지 | 중심 역할 | 강점 | 제약 | 적합한 상황 |
|---|---|---|---|---|
| **GS Quant** | cross-asset domain model + Marquee client | instrument/risk/data/backtest abstraction 통합 | proprietary backend는 credentials와 entitlement 필요 | Marquee 사용자, institutional workflow |
| **pandas + NumPy/SciPy** | general-purpose local analytics | 자유도, 넓은 생태계, backend 종속 없음 | 금융상품 convention과 risk model을 직접 설계 | 자체 data/model 연구, 가벼운 분석 |
| **QuantLib** | open-source pricing/model engine | pricing algorithm과 term structure를 로컬에서 통제 | market data와 production workflow는 별도 구축 | model 구현·검증, 독립적인 pricing engine |
| **직접 만든 vendor REST client** | raw API access | endpoint를 직접 통제, dependency가 작을 수 있음 | object model, batching, retry, schema를 직접 관리 | 좁고 안정된 endpoint만 필요한 service |
| **일반 backtesting framework** | strategy simulation | retail data source와 strategy 예제가 풍부할 수 있음 | institutional derivative risk와 model 연결이 약할 수 있음 | equities 중심 전략 연구 |

> [!NOTE]
> 이 표는 architecture와 사용 목적의 비교다. 동일한 data entitlement, asset-class coverage, model 정확도를 전제로 한 benchmark가 아니다.

## GS Quant 내부 선택지

### Local analytics vs server-backed analytics

| 기준 | Local `gs_quant.timeseries` | Marquee-backed data/pricing/risk |
|---|---|---|
| 입력 | 직접 준비한 `pandas.Series` 등 | GS dataset, instrument, market context |
| credentials | 일부 기능은 불필요 | 일반적으로 필요 |
| 재현성 | 입력 data와 package version에 좌우 | entitlement, backend model/data version도 영향 |
| 주요 용도 | returns, volatility, correlation, alignment | pricing, Greeks, portfolio risk, proprietary data |
| 시작 난이도 | 낮음 | session과 권한 확인 필요 |

### Sync vs async vs batch

| Mode | 선택 기준 | 주의점 |
|---|---|---|
| 기본 context | 짧은 interactive 계산 | block 종료와 result materialization 시점 이해 |
| `is_async=True` | caller가 계산 중 다른 일을 계속해야 함 | `Future` 상태와 오류 처리 필요 |
| `is_batch=True` | 장시간 또는 큰 계산 | 즉시 응답을 기대하지 말고 job lifecycle 고려 |

### MCP authentication mode

| Mode | session model | 적합성 |
|---|---|---|
| `local` | 모든 request가 단일 session 공유 | single-user local experiment |
| `passthrough` | 사용자별 credential/session 전달 | per-user service 검토 |

`local` mode를 multi-user server에 쓰면 사용자 격리가 깨질 수 있으므로 피한다. MCP 자체도 experimental이므로 interface 변경을 흡수할 adapter와 version pinning이 필요하다.

## 선택 가이드

```text
Marquee entitlement가 있는가?
├─ Yes
│  ├─ cross-asset pricing/risk/data 통합이 필요한가? -> GS Quant 우선 검토
│  └─ model implementation을 완전히 통제해야 하는가? -> QuantLib/자체 engine 병행
└─ No
   ├─ 로컬 통계 분석만 필요한가? -> pandas/NumPy/SciPy 또는 gs_quant.timeseries
   ├─ open-source pricing engine이 필요한가? -> QuantLib 검토
   └─ GS proprietary 기능이 목적이었는가? -> 계약·entitlement 확인 전 구현 보류
```

## Dependency와 운영 관점

- research notebook에서는 package version, input data snapshot, valuation date를 함께 기록한다.
- production에서는 OAuth secret을 code나 Obsidian vault에 저장하지 않는다.
- dataset API 응답은 약 100MB 제한이 있으므로 기간·entity별 chunking을 설계한다.
- relative parameter를 썼다면 재현 가능한 결과를 위해 `resolve()` 결과도 보관한다.
- experimental MCP를 사용하면 `gs-quant` version을 pin하고 upgrade test를 별도로 둔다.

## Sources

- https://github.com/goldmansachs/gs-quant
- https://developer.gs.com/docs/gsquant/
- https://developer.gs.com/docs/gsquant/api/timeseries.html
- https://developer.gs.com/docs/gsquant/pricing-and-risk/pricing-context/
- https://github.com/goldmansachs/gs-quant/tree/master/gs_quant/mcp
- https://github.com/goldmansachs/gs-quant/blob/master/pyproject.toml

