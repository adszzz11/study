---
date: 2026-10-06
tags: [tech]
type: tech-tool-study
status: draft
---

# HyperLogLog

> **한 줄 정의**: HyperLogLog(HLL)는 대규모 stream의 고유 원소 수(cardinality)를 작은 고정 메모리와 확률적 오차로 추정하고 merge할 수 있는 sketch이다.

## Overview

`COUNT(DISTINCT user_id)`는 본 모든 ID를 기억해야 한다. HLL은 hash의 희귀한 bit pattern을 register에 압축하여, 입력 크기와 무관한 공간으로 distinct count를 추정한다.

- [[01-overview|What, Why, 핵심 동작]]
- [[02-ecosystem|엔진·sketch 대안 비교]]
- [[cheatsheet|빠른 참조]]

## Learning Path

- [ ] [[04-learning/01-getting-started|Redis로 PFADD · PFCOUNT · PFMERGE]]를 실행한다.
- [ ] 같은 sample에서 exact count와 estimate의 상대오차를 비교한다.
- [ ] [[04-learning/02-deep-dive|precision, hash canonicalization, merge 호환성]]을 이해한다.
- [ ] BigQuery 또는 Trino에서 일별 sketch를 저장하고 기간 sketch를 merge한다.
- [ ] [[05-projects|실전 프로젝트]] 하나에 품질 검증과 운영 경계를 적용한다.

## When To Use

- DAU/WAU/MAU, unique visitor·query·device·IP 같은 large-scale cardinality.
- shard, 날짜, dimension별 집계를 나중에 union하여 rollup할 때.
- telemetry, 광고 reach, ETL 데이터 품질 지표처럼 작은 상대오차가 허용될 때.

## When Not To Use

- 청구, 권한, 재고처럼 정확한 수가 업무 결과를 바꾸는 경우.
- 원소 목록, membership, 빈도 조회가 필요한 경우.
- intersection/difference의 신뢰도가 핵심인 경우 — Theta Sketch를 우선 검토한다.

## Related Notes

- [[MOCs/Index]]
- [[MOCs/Data]]
- [[tech/data/dolt/README|Dolt]]
- [[01-overview]]

## Sources

- https://algo.inria.fr/flajolet/Publications/FlFuGaMe07.pdf
- https://research.google.com/pubs/archive/40671.pdf
- https://redis.io/docs/latest/develop/data-types/probabilistic/hyperloglogs/
- https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/hll_functions
- https://trino.io/docs/current/functions/hyperloglog.html
