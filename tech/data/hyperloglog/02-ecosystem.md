---
date: 2026-10-06
tags: [tech]
type: tech-tool-study
status: draft
---

# Ecosystem과 비교

## 선택지 비교

| 선택지 | 강점 | 제약 / 피할 시점 | 대표 구현 |
|---|---|---|---|
| Exact `COUNT(DISTINCT)` / Set | 정확, 원소 조회 가능 | 높은 cardinality의 memory·shuffle 비용 | SQL, Redis Set |
| HLL / HLL++ | 작고 빠른 update·union, 분산 rollup | 근사값, membership·정확한 set 연산 불가 | Redis, BigQuery, Trino, PostgreSQL HLL |
| CPC Sketch | 같은 공간에서 HLL보다 높은 정확도 가능 | serialization/deserialization이 HLL보다 느릴 수 있음 | Apache DataSketches |
| Theta Sketch | union·intersection·difference·Jaccard | cardinality-only에서는 HLL보다 공간 효율이 낮을 수 있음 | DataSketches, Druid 연계 |
| Bloom Filter | membership의 빠른 사전 검사 | distinct count 용도가 아님; false positive | RedisBloom |
| Count-Min Sketch | frequency·heavy hitter 추정 | distinct count 용도가 아님 | stream libraries |

## 플랫폼별 사용 관점

- **Redis**: `PFADD`, `PFCOUNT`, `PFMERGE`로 operational counter를 간단히 구현한다.
- **BigQuery**: `HLL_COUNT.INIT` 결과를 `BYTES`로 저장해 raw event 재스캔 없이 rollup한다. precision 범위는 10–24, 기본값은 15다.
- **Trino**: `approx_set()`의 `varbinary` sketch를 저장하고 `merge()` 후 `cardinality()`를 호출한다.
- **PostgreSQL HLL extension**: hash quality와 extension의 type/설정 호환성을 명시적으로 관리한다.
- **Apache DataSketches**: 새로운 설계에서는 HLL만 고정하지 말고 CPC와 Theta를 요구사항에 맞춰 비교한다.

## Decision Guide

```text
정확한 count 또는 원소 목록이 필요한가? ─ 예 → Exact Set / COUNT(DISTINCT)
                         │ 아니오
intersection/difference가 중요한가? ─── 예 → Theta Sketch
                         │ 아니오
DB/warehouse 호환성과 단순 rollup이 우선인가? → HLL/HLL++
                         │ 아니오
cardinality-only에서 저장 효율이 최우선인가? → CPC Sketch 평가
```

DataSketches는 CPC가 HLL보다 약 40% 적은 저장공간을 사용할 수 있다고 안내한다. 이는 구현·정확도 목표에 의존하므로 실제 distribution으로 benchmark한다.

## Sources

- https://datasketches.apache.org/docs/CPC/CpcSketches.html
- https://datasketches.apache.org/docs/Architecture/MajorSketchFamilies.html
- https://trino.io/docs/current/functions/hyperloglog.html
- https://hive.apache.org/docs/latest/language/datasketches-integration/
