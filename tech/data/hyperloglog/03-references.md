---
date: 2026-10-06
tags: [tech]
type: tech-tool-study
status: draft
---

# References

## Foundational Papers

1. Flajolet et al., [HyperLogLog: the analysis of a near-optimal cardinality estimation algorithm](https://algo.inria.fr/flajolet/Publications/FlFuGaMe07.pdf)
2. Google Research, [HyperLogLog in Practice (HLL++)](https://research.google.com/pubs/archive/40671.pdf)

## Official Documentation

1. Redis, [HyperLogLog / PFADD / PFCOUNT / PFMERGE](https://redis.io/docs/latest/develop/data-types/probabilistic/hyperloglogs/)
2. Google Cloud BigQuery, [HLL_COUNT functions](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/hll_functions)
3. Trino, [HyperLogLog functions](https://trino.io/docs/current/functions/hyperloglog.html)
4. Apache DataSketches, [HLL Sketches](https://datasketches.apache.org/docs/HLL/HllSketches.html)
5. Apache DataSketches, [Distinct-count feature matrix](https://datasketches.apache.org/docs/DistinctCountFeaturesMatrix.html)
6. CitusData, [postgresql-hll extension](https://github.com/citusdata/postgresql-hll)
7. Apache Hive, [DataSketches integration](https://hive.apache.org/docs/latest/language/datasketches-integration/)

## Reading Order

원리부터 이해하려면 원 논문 → HLL++ → 사용하는 engine의 공식 문서 순서로 읽는다. 제품 선택은 DataSketches feature matrix와 CPC/Theta 문서를 함께 비교한다.
