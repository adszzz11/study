---
date: 2026-10-06
tags: [tech]
type: tech-tool-study
status: draft
---

# HyperLogLog 개요

## What

HyperLogLog(HLL)는 stream 안의 서로 다른 원소 수를 추정하는 probabilistic sketch다. 원소 자체를 보관하지 않으므로 membership이나 목록 조회는 할 수 없다.

## Why

정확한 `COUNT(DISTINCT)`는 cardinality에 비례하는 state와 분산 shuffle을 요구한다. HLL은 고정 수의 register만 유지해 일별 수십억 event나 다수 dimension 조합에서도 집계 state를 예측 가능하게 만든다.

## How It Works

1. 안정적이고 균등한 hash로 입력을 변환한다.
2. 앞 `p` bit로 bucket을 선택한다. register 수는 `m = 2^p`다.
3. 나머지 bit의 leading-zero run인 rank `ρ`를 구한다.
4. 선택된 register에 `max(기존값, ρ)`만 기록한다.
5. 모든 register를 harmonic mean 방식으로 결합해 estimate를 계산한다.

```text
element → uniform hash → bucket(p bits) + rank(leading-zero run)
                              │                 │
                              └──── register[bucket] = max(old, rank)
```

## 특징과 Trade-off

| 특성 | 의미 |
|---|---|
| Relative Standard Error | 대략 `1.04 / √m` |
| precision | 높일수록 register와 memory가 증가 |
| union | 동일 규약의 register별 `max`로 merge |
| low cardinality | HLL++/일부 구현은 bias correction·sparse representation 사용 |
| 전제 | hash 분포가 균등해야 오차 보장이 성립 |

Redis는 최대 12 KB와 표준 오차 0.81%를 제공한다. 단, HLL끼리라도 hash 함수·seed, precision, serialization 형식이 다르면 binary를 합쳐서는 안 된다.

## Limits

- 정확한 count, membership, 원소 열람, frequency를 제공하지 않는다.
- union은 강하지만 intersection/difference는 오차가 커질 수 있다.
- `NULL` 처리, 문자열 normalization, ID formatting을 입력 단계에서 명확히 해야 한다.

## Sources

- https://algo.inria.fr/flajolet/Publications/FlFuGaMe07.pdf
- https://datasketches.apache.org/docs/DistinctCountFeaturesMatrix.html
- https://github.com/citusdata/postgresql-hll
