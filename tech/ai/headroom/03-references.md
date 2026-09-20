---
date: 2026-09-20
tags: [tech]
type: tech-tool-study
status: draft
---

# 03. Headroom References

## 공식 시작점

- [Documentation](https://docs.headroomlabs.ai/docs) — 제품 개념과 주요 integration
- [GitHub repository](https://github.com/headroomlabs-ai/headroom) — source, README, reproducible benchmark 명령
- [Releases](https://github.com/headroomlabs-ai/headroom/releases) — version history; 조사 기준 최신 정식 버전 v0.37.0
- [PyPI: headroom-ai](https://pypi.org/project/headroom-ai/) — Python package와 CLI
- [npm: headroom-ai](https://www.npmjs.com/package/headroom-ai) — local proxy를 호출하는 TypeScript SDK

## Architecture와 compression

- [Architecture](https://docs.headroomlabs.ai/docs/architecture) — proxy, CacheAligner, ContentRouter, compressor, CCR의 흐름
- [How Compression Works](https://docs.headroomlabs.ai/docs/how-compression-works) — content detection과 compressor routing
- [Code Compression](https://docs.headroomlabs.ai/docs/code-compression) — tree-sitter AST 기반 처리와 보호 정책
- [CCR](https://docs.headroomlabs.ai/docs/ccr) — Compress–Cache–Retrieve store, TTL, eviction, retrieval
- [Configuration](https://docs.headroomlabs.ai/docs/configuration) — mode와 runtime configuration
- [Limitations](https://docs.headroomlabs.ai/docs/limitations) — passthrough와 알려진 제약

## 성능 자료

- [Benchmarks](https://docs.headroomlabs.ai/docs/benchmarks) — local microbenchmark와 workload 결과
- [README proof section](https://github.com/headroomlabs-ai/headroom#proof) — 재현 명령과 headline claim의 범위

## 읽을 때 확인할 질문

- 절감률이 synthetic JSON인가, 실제 coding/SRE workload인가?
- token count만 비교했는가, final answer equivalence도 평가했는가?
- compression overhead에 provider latency가 포함됐는가?
- `cache` mode의 prefix cache 이득까지 비용 계산에 포함됐는가?
- retrieval이 필요했던 case에서 모델이 실제로 tool을 호출했는가?
- source code처럼 0% 절감이 정상인 payload를 실패로 오해하지 않았는가?

## 주장별 신뢰 범위

| 주장 | dossier가 뒷받침하는 범위 | 과도한 해석 |
|---|---|---|
| token을 절감한다 | workload별 21–57%, 반복 JSON/text에서 더 큼 | 모든 coding agent에서 60–95% |
| local compression이다 | compression service로 prompt/code를 보내지 않음 | 네트워크 traffic이 전혀 없음 |
| CCR로 복구 가능하다 | 원문을 local store에 저장하고 hash로 retrieve | 모든 answer가 자동으로 lossless |
| latency overhead가 낮다 | Apple M-series local compression p50 | end-to-end LLM latency가 항상 감소 |

## Vault 학습 순서

- 개념: [[headroom/01-overview]]
- 대안 비교: [[headroom/02-ecosystem]]
- 첫 실습: [[headroom/04-learning/01-getting-started]]
- 내부 원리: [[headroom/04-learning/02-deep-dive]]
- 평가 project: [[headroom/05-projects]]

## Sources

- https://docs.headroomlabs.ai/docs
- https://docs.headroomlabs.ai/docs/benchmarks
- https://docs.headroomlabs.ai/docs/limitations
- https://github.com/headroomlabs-ai/headroom
- https://github.com/headroomlabs-ai/headroom/releases
