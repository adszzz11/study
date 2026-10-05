---
date: 2026-10-06
tags: [tech]
type: tech-tool-study
status: draft
---

# Getting Started: Redis HLL

## 목표

Redis의 HLL 명령으로 중복을 제거한 cardinality 추정과 기간 union을 체감한다.

```redis
PFADD hll:visitors:2026-10-06 user:1 user:2 user:2 user:3
PFCOUNT hll:visitors:2026-10-06

PFMERGE hll:visitors:week hll:visitors:2026-10-06 hll:visitors:2026-10-07
PFCOUNT hll:visitors:week
```

`user:2`를 두 번 넣어도 distinct cardinality에는 한 번만 반영된다. 결과는 추정치이므로 작은 표본에서 exact value와 완전히 같을 것을 기대하지 않는다.

## 실습: Exact Count와 비교

1. 같은 event sample을 exact `COUNT(DISTINCT)`와 HLL에 모두 적재한다.
2. `abs(estimate - exact) / exact`를 cardinality 구간별로 계산한다.
3. 아주 작은 cardinality, skewed key, `NULL`, 입력 문자열 normalization을 별도 case로 확인한다.

```sql
-- 평가용 exact baseline
SELECT COUNT(DISTINCT user_id) AS exact_users
FROM events
WHERE event_date = DATE '2026-10-06';
```

## 운영 규칙

- key naming에 grain을 담는다: `hll:visitors:{date}:{country}`.
- daily count를 합산하지 말고 daily sketch를 `PFMERGE`한다.
- 결과를 차단·청구 같은 irreversible decision의 유일한 근거로 사용하지 않는다.

## Sources

- https://redis.io/docs/latest/develop/data-types/probabilistic/hyperloglogs/
