---
date: 2026-10-06
tags: [tech]
type: tech-tool-study
status: draft
---

# Projects

## 1. DAU / WAU / MAU Service

날짜·제품·국가별 HLL을 생성하고, WAU/MAU는 daily sketch를 merge한다. raw event 재스캔을 줄이되, 매일 표본 exact baseline으로 drift를 관찰한다.

## 2. API Abuse / Telemetry Dashboard

endpoint별 unique client 또는 API key를 HLL gauge로 표시한다. 갑작스러운 cardinality 변화는 탐지 신호로 쓰되, 자동 차단은 원시 로그와 rate limit 규칙으로 재검증한다.

## 3. 광고·콘텐츠 Reach

campaign·creative·publisher별 sketch를 집계해 union reach를 계산한다. audience overlap이 의사결정의 핵심이면 HLL inclusion-exclusion 대신 Theta Sketch를 검토한다.

## 4. ETL Quality Monitor

source별 unique customer ID를 매일 추정하여 baseline 대비 급감·급증을 경보로 만든다. upstream schema 변경, `NULL` 증가, canonicalization 실패를 함께 진단한다.

## Delivery Checklist

- [ ] grain과 retention을 정의했다.
- [ ] hash input의 type·normalization·seed를 문서화했다.
- [ ] precision과 예상 RSE를 SLO에 맞췄다.
- [ ] merge compatibility fixture를 CI 또는 integration test에 넣었다.
- [ ] exact sample 비교와 anomaly alert를 마련했다.

## Sources

- https://redis.io/docs/latest/develop/data-types/probabilistic/hyperloglogs/
- https://datasketches.apache.org/docs/Architecture/MajorSketchFamilies.html
