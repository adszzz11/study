---
date: 2026-10-06
tags: [tech]
type: tech-tool-study
status: draft
---

# Deep Dive: Precision, Merge, Rollup

## Precision Budget

`m = 2^p` register일 때 HLL의 RSE는 대략 `1.04 / √m`이다. precision을 정할 때는 허용 relative error, 집계 key 수, 보관 기간, sparse-to-dense 전환을 함께 계산한다.

| register 수 `m` | 근사 RSE |
|---:|---:|
| 1,024 | 3.25% |
| 16,384 | 0.81% |
| 65,536 | 0.41% |

## Merge Contract

merge가 안전하려면 다음이 모두 같아야 한다.

- HLL family와 precision
- hash algorithm, seed, 입력 canonicalization
- register encoding과 serialization version
- `NULL` 및 type coercion 규칙

따라서 다른 engine의 `varbinary`/`BYTES`를 “둘 다 HLL”이라는 이유만으로 합치지 않는다. 생산 데이터 전에는 known-set fixture를 통한 compatibility test를 둔다.

## BigQuery Rollup

일별 sketch를 저장하고 월별에는 sketch만 merge한다.

```sql
-- 일별 상태 저장 예시
SELECT
  event_date,
  HLL_COUNT.INIT(user_id, 15) AS user_hll
FROM `project.dataset.events`
GROUP BY event_date;

-- 기간 cardinality: raw event가 아니라 daily sketch를 merge
SELECT HLL_COUNT.MERGE(user_hll) AS monthly_users
FROM `project.dataset.daily_user_hll`
WHERE event_date BETWEEN DATE '2026-10-01' AND DATE '2026-10-31';
```

## Trino Rollup

`approx_set(user_id)`의 결과를 `varbinary`로 저장하고 조회 시 `merge()` → `cardinality()` 순서로 사용한다. 일별 estimate의 산술 합은 cross-day duplicate를 과대계상한다.

```sql
SELECT cardinality(merge(user_hll)) AS period_users
FROM daily_user_hll
WHERE event_date BETWEEN DATE '2026-10-01' AND DATE '2026-10-31';
```

## Sources

- https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/hll_functions
- https://trino.io/docs/current/functions/hyperloglog.html
- https://datasketches.apache.org/docs/DistinctCountFeaturesMatrix.html
