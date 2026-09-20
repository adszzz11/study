---
date: 2026-09-20
tags: [tech]
type: tech-tool-study
status: draft
---

# 05. Headroom Projects

## Project 1. Compression audit harness

### 목표

실제 사용 예정 payload에서 절감률과 correctness를 함께 측정한다.

### Dataset

- code search result
- structured JSON/API response
- CI/test logs
- documentation/RAG chunks
- source code

### 산출물

```text
cases/
├── json/
├── logs/
├── search/
├── docs/
└── code/
results/
├── baseline.jsonl
└── headroom.jsonl
```

각 case에 expected error, required fact, forbidden omission을 적고 baseline과 compressed run을 같은 model 조건으로 비교한다.

### Metrics

| Metric | 목적 |
|---|---|
| token reduction | 실제 context 감소량 |
| task accuracy | 최종 답변 동등성 |
| anomaly recall | error/outlier 보존 |
| compression p50/p95 | local overhead |
| retrieval success | CCR 복구 신뢰성 |
| cost per completed task | cache까지 포함한 경제성 |

## Project 2. CCR chaos test

### 목표

“원문을 되찾을 수 있다”는 가정을 장애 상황에서 검증한다.

- [ ] retrieval-required question을 만든다.
- [ ] 정상 hash로 원문 복구를 확인한다.
- [ ] TTL 이후 같은 call을 반복한다.
- [ ] capacity를 채워 eviction을 유도한다.
- [ ] proxy restart 후 persistence를 확인한다.
- [ ] multi-worker가 같은 SQLite store를 사용할 때 contention을 관찰한다.
- [ ] retrieval tool을 차단하고 answer degradation을 기록한다.

완료 조건은 모든 request 성공이 아니라 failure가 **관찰 가능하고 정의된 fallback**으로 끝나는 것이다.

## Project 3. Prefix cache 경제성 비교

### 목표

긴 coding session에서 `cache`와 `token` mode 중 어느 쪽이 총비용을 줄이는지 확인한다.

| Run | Mode | 기록할 값 |
|---|---|---|
| A | uncompressed | input, cached input, latency, accuracy |
| B | `cache` | delta compression, cache hit, total cost |
| C | `token` | total compression, cache drift, total cost |

최소 20-turn scripted task를 여러 번 반복하고 warm/cold cache를 분리한다. 단일-turn microbenchmark로 multi-turn 결론을 내리지 않는다.

## Project 4. Safe proxy rollout

### 단계

1. secret-free replay traffic에서 `audit/simulate` 성격의 관찰을 수행한다.
2. low-risk workload 일부에 opt-in한다.
3. compression skip reason과 retrieval failure를 dashboard에 추가한다.
4. quality regression threshold와 passthrough kill switch를 정의한다.
5. Beacon/telemetry 정책과 CCR retention을 문서화한다.
6. canary 결과가 baseline을 만족할 때만 범위를 넓힌다.

### Rollback

- provider base URL을 기존 endpoint로 되돌린다.
- wrapper 없이 agent를 실행한다.
- application-level compression hook을 disable한다.
- CCR store 삭제는 retention policy와 incident 조사 필요성을 확인한 뒤 별도로 수행한다.

## Project 완료 기준

- [ ] representative workload와 baseline이 version control에 있다.
- [ ] token 절감과 task correctness가 함께 보고된다.
- [ ] CCR expiry/eviction/tool failure가 검증됐다.
- [ ] `cache`/`token` 선택 근거가 실제 billing metric에 기반한다.
- [ ] privacy setting과 operational metadata 경계가 기록됐다.
- [ ] disable/rollback 절차가 rehearsal됐다.

## Sources

- https://docs.headroomlabs.ai/docs/benchmarks
- https://docs.headroomlabs.ai/docs/ccr
- https://docs.headroomlabs.ai/docs/configuration
- https://docs.headroomlabs.ai/docs/limitations
- https://github.com/headroomlabs-ai/headroom#proof
