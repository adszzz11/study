---
date: 2026-08-24
tags: [tech]
type: tech-tool-study
status: draft
---

# GS Quant References

## 공식 진입점

| 자료 | URL | 읽을 이유 |
|---|---|---|
| GitHub repository | https://github.com/goldmansachs/gs-quant | source, examples, issue, package 구조 확인 |
| GS Quant documentation | https://developer.gs.com/docs/gsquant/ | 전체 기능 지도와 공식 개요 |
| Getting Started | https://developer.gs.com/docs/gsquant/getting-started/ | local analytics와 초기 workflow |
| PyPI | https://pypi.org/project/gs-quant/ | 현재 package와 release history 확인 |
| GitHub Releases | https://github.com/goldmansachs/gs-quant/releases | release note와 변경점 확인 |

## Authentication과 execution

| 자료 | URL | 핵심 질문 |
|---|---|---|
| `GsSession` authentication | https://developer.gs.com/docs/gsquant/authentication/gs-session/ | OAuth credential과 environment를 어떻게 설정하는가? |
| Instruments | https://developer.gs.com/docs/gsquant/pricing-and-risk/instruments/ | instrument와 relative parameter는 어떻게 표현하는가? |
| Measures | https://developer.gs.com/docs/gsquant/pricing-and-risk/measures/ | price와 risk request를 어떻게 명세하는가? |
| PricingContext | https://developer.gs.com/docs/gsquant/pricing-and-risk/pricing-context/ | date, market, async, batch, cache를 어떻게 scope로 묶는가? |

## Data와 analytics

| 자료 | URL | 핵심 질문 |
|---|---|---|
| Datasets guide | https://developer.gs.com/docs/gsquant/data/data-environment/datasets/ | dataset schema, coverage, daily/intraday 차이는 무엇인가? |
| Dataset API | https://developer.gs.com/docs/gsquant/api/classes/gs_quant.data.Dataset.html | 조회 method와 parameter는 무엇인가? |
| Timeseries API | https://developer.gs.com/docs/gsquant/api/timeseries.html | 로컬에서 사용할 수 있는 analytics는 무엇인가? |

## Backtesting과 MCP

| 자료 | URL | 핵심 질문 |
|---|---|---|
| Backtesting guide | https://developer.gs.com/docs/gsquant/pricing-and-risk/backtesting/ | Trigger, Action, Strategy, engine을 어떻게 조합하는가? |
| MCP source/README | https://github.com/goldmansachs/gs-quant/tree/master/gs_quant/mcp | server, client, auth mode, CLI는 어떻게 구성되는가? |
| `pyproject.toml` | https://github.com/goldmansachs/gs-quant/blob/master/pyproject.toml | `mcp` extra와 optional dependencies는 무엇인가? |

## 추천 읽기 순서

```text
1. 공식 Overview와 Getting Started
2. Timeseries API로 credential-free 범위 확인
3. Authentication 문서로 entitlement 경계 확인
4. Instruments -> Measures -> PricingContext
5. Datasets guide -> Dataset API
6. Backtesting guide
7. MCP README와 pyproject.toml
8. Releases에서 현재 version의 breaking changes 확인
```

## 조사 메모

- 기준일: **2026-08-24**
- 대상: `goldmansachs/gs-quant`; 동명의 Knowledge Graph 논문 제외
- 확인된 최신 release: PyPI `2.1.3`, 2026-08-07
- license: Apache-2.0
- 최신 정보는 설치 전에 PyPI와 Releases를 다시 확인한다.
- documentation example이 실행되지 않으면 package version, authentication, scope, dataset/model entitlement를 차례로 확인한다.

## Sources

- https://github.com/goldmansachs/gs-quant
- https://developer.gs.com/docs/gsquant/
- https://pypi.org/project/gs-quant/
- https://github.com/goldmansachs/gs-quant/releases

