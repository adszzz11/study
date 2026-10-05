---
date: 2026-10-06
tags: [tech]
type: tech-tool-study
status: draft
---

# HyperLogLog Cheatsheet

## 핵심 공식

```text
m = 2^p
RSE ≈ 1.04 / √m
merge(registers) = register별 max
```

## Redis

```redis
PFADD hll:daily:2026-10-06 user:1 user:2
PFCOUNT hll:daily:2026-10-06
PFMERGE hll:weekly hll:daily:2026-10-06 hll:daily:2026-10-07
```

## BigQuery

```sql
HLL_COUNT.INIT(user_id, 15)
HLL_COUNT.MERGE(user_hll)
HLL_COUNT.EXTRACT(user_hll)
```

## Trino

```sql
approx_set(user_id)
cardinality(merge(user_hll))
```

## Do / Don't

| Do | Don't |
|---|---|
| daily sketch를 merge해 기간 unique 계산 | daily unique estimate를 합산 |
| hash·precision·encoding 호환성 검증 | 서로 다른 engine binary를 임의 merge |
| sample exact count로 error 추적 | billing·권한의 유일한 근거로 사용 |
| set expression이면 Theta Sketch 평가 | HLL로 정확한 intersection을 기대 |

## Sources

- https://redis.io/docs/latest/develop/data-types/probabilistic/hyperloglogs/
- https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/hll_functions
- https://trino.io/docs/current/functions/hyperloglog.html
