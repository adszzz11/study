---
date: 2026-08-24
tags: [tech]
type: tech-tool-study
status: draft
---

# Getting Started: 설치와 Local Analytics

> [[../README|목차로 돌아가기]] · [[02-deep-dive|다음: Deep Dive]]

## 학습 목표

첫 단계에서는 Marquee credentials 없이 package 구조와 local time series analytics를 익힌다. 그다음 credentials가 있는 경우에만 session 연결을 별도 검증한다.

- 공개 package와 proprietary backend의 경계를 설명한다.
- isolated Python environment에 `gs-quant`를 설치한다.
- 직접 만든 `pandas.Series`에 local analytics를 적용한다.
- 결과의 index alignment와 missing value를 점검한다.
- credential을 source code나 notebook에 저장하지 않는다.

## 1. 설치

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install "gs-quant==2.1.3"
```

MCP를 실험할 때만 optional extra를 설치한다.

```bash
python -m pip install "gs-quant[mcp]==2.1.3"
```

> [!NOTE]
> `2.1.3`은 조사 기준일에 확인된 version이다. 새 환경에서는 [[../03-references|References]]의 PyPI와 Releases에서 최신판과 breaking change를 먼저 확인한다.

설치를 확인한다.

```bash
python -c "import gs_quant; print(gs_quant.__version__)"
python -m pip show gs-quant
```

## 2. Credential-free 실습

공식 Getting Started의 방향처럼 직접 만든 series로 시작한다. API surface는 version에 따라 달라질 수 있으므로 현재 설치 version의 docstring도 함께 확인한다.

```python
import numpy as np
import pandas as pd

rng = np.random.default_rng(seed=42)
index = pd.bdate_range("2026-01-02", periods=100)
returns = pd.Series(rng.normal(0, 0.01, len(index)), index=index)
prices = 100 * (1 + returns).cumprod()

print(prices.head())
print(prices.index.is_monotonic_increasing)
print(prices.isna().sum())
```

그다음 `gs_quant.timeseries`의 함수 signature를 확인하고 22-business-day realized volatility 같은 analytics를 적용한다.

```python
from gs_quant import timeseries as ts

help(ts.volatility)

# 설치한 version의 signature에 맞춰 window를 전달한다.
realized_vol = ts.volatility(prices, 22)
print(realized_vol.dropna().tail())
```

### 결과 점검

| 점검 항목 | 질문 |
|---|---|
| Index | business date가 정렬되고 중복되지 않았는가? |
| Window | 22 observations인지 22 calendar days인지 확인했는가? |
| Missing values | warm-up 구간과 실제 data gap을 구분했는가? |
| Units | decimal return, percent, annualized volatility를 구분했는가? |
| Reproducibility | random seed, package version, input range를 기록했는가? |

## 3. API 구조 탐색

```python
from gs_quant.data import Dataset
from gs_quant.markets import PricingContext
from gs_quant.session import GsSession

print(Dataset.__doc__)
print(PricingContext.__doc__)
print(GsSession.__doc__)
```

이 단계에서는 class를 import하는 것과 Goldman Sachs backend를 호출하는 것을 구분한다. `Dataset`을 생성할 수 있어도 특정 dataset을 조회할 entitlement가 있다는 뜻은 아니다.

## 4. Credentials가 있을 때만 session 연결

credential 이름과 scope는 조직 설정 및 공식 authentication 문서를 확인한다. 아래는 secret을 code에 직접 넣지 않는 구조 예시다.

```python
import os

from gs_quant.session import Environment, GsSession

client_id = os.environ["GSQ_CLIENT_ID"]
client_secret = os.environ["GSQ_CLIENT_SECRET"]

GsSession.use(
    Environment.PROD,
    client_id=client_id,
    client_secret=client_secret,
)
```

```bash
# shell history와 process exposure 정책을 확인한 뒤 조직의 secret manager를 우선 사용한다.
export GSQ_CLIENT_ID="..."
export GSQ_CLIENT_SECRET="..."
```

> [!WARNING]
> 실제 client secret을 Obsidian vault, Git repository, notebook output, screenshot에 남기지 않는다. environment variable 예시도 local 개발 편의를 위한 최소 구조이며 production에서는 secret manager를 우선한다.

## 5. 첫 주 체크리스트

- [ ] Python virtual environment를 만들었다.
- [ ] 설치 version과 조사 기준 version을 기록했다.
- [ ] 직접 만든 `Series`로 local analytics를 실행했다.
- [ ] window, annualization, missing value 의미를 확인했다.
- [ ] `Dataset`, `PricingContext`, `GsSession`의 책임을 구분한다.
- [ ] credentials와 entitlement 없이는 어떤 예제가 실패하는지 설명할 수 있다.
- [ ] secret이 vault와 Git working tree에 없음을 확인했다.

## 자주 만나는 문제

| 증상 | 먼저 확인할 것 |
|---|---|
| import error | virtual environment 활성화, 설치 package, Python compatibility |
| 함수 argument error | 설치 version의 signature와 현재 공식 API 문서 |
| authentication error | client ID/secret, environment, OAuth 설정 |
| permission/empty result | dataset·model entitlement와 query dimensions |
| 예상과 다른 volatility | return definition, window, annualization, missing value |

## Sources

- https://developer.gs.com/docs/gsquant/getting-started/
- https://developer.gs.com/docs/gsquant/api/timeseries.html
- https://developer.gs.com/docs/gsquant/authentication/gs-session/
- https://pypi.org/project/gs-quant/

