---
date: 2026-09-20
tags: [tech]
type: tech-tool-study
status: draft
---

# Headroom Cheatsheet

## 핵심 모델

```text
Protect → Detect → Route → Compress → Cache original → Retrieve if needed
```

| Component | 역할 |
|---|---|
| Safety gates | system/user/recent context 보호 |
| CacheAligner | prefix-cache drift 관리 |
| ContentRouter | payload type 판별 |
| SmartCrusher | JSON/array/table 축약 |
| CodeAwareCompressor | tree-sitter AST 기반 code 처리 |
| Kompress-v2-base | ModernBERT/ONNX general text 처리 |
| CCR | local 원문 저장과 hash retrieval |

## 설치와 실행

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install headroom-ai

headroom --help
headroom proxy --port 8787
headroom wrap codex
```

> TypeScript `headroom-ai` package는 local proxy client이며 독립 CLI가 아니다.

## API 형태

```python
from headroom import compress

result = compress(messages, model="provider/model")
```

```ts
const result = await compress(messages, { model: "provider/model" });
```

정확한 import와 option은 설치한 version의 API 문서를 확인한다.

## MCP tools

| Tool | 용도 |
|---|---|
| `headroom_compress` | context 압축 |
| `headroom_retrieve` | CCR hash로 원문 조회 |
| `headroom_stats` | 압축 통계 확인 |

## Mode 구분

| Mode family | 값 | 의미 |
|---|---|---|
| SDK behavior | `audit` / `optimize` / `simulate` | 관찰·적용 동작 선택 |
| Proxy cache strategy | `cache` / `token` | prefix cache 안정성·token 최소화 선택 |

- 기본 `cache`: newest delta 중심 압축, 과거 prefix 유지
- `token`: 과거 turn도 재압축, cache hit 저하 가능

## CCR 기본값과 조건

- Store: local hash-keyed SQLite `ccr_store.db`
- TTL: 기본 30분
- Capacity: LRU-style eviction
- Alternative: in-memory 또는 custom backend
- 조건: model 감지 → tool 호출 → store에 원문 존재

> CCR은 storage-level reversible이다. final answer가 자동으로 lossless인 것은 아니다.

## Payload별 기대

| Payload | 기대 | 주의 |
|---|---|---|
| 반복 JSON | 높은 절감 가능 | anomaly와 schema 검증 |
| 반복 logs | 높은 절감 가능 | error/stack trace recall 검증 |
| Search/diff | relevant subset | line/order 의존성 확인 |
| Long docs | 높은 절감 가능 | required fact 누락 평가 |
| Source code | 낮거나 0% 가능 | passthrough가 정상일 수 있음 |

## 운영 체크

- [ ] baseline answer와 비용을 저장했는가?
- [ ] final answer accuracy를 비교했는가?
- [ ] retrieval failure를 시험했는가?
- [ ] provider cached input까지 계산했는가?
- [ ] passthrough/kill switch가 있는가?
- [ ] `HEADROOM_TELEMETRY`와 `HEADROOM_BEACON`을 검토했는가?

## 조사 기준 benchmark

v0.37.0 workload 절감률: code search 21%, SRE debugging 57%, codebase exploration 42%, GitHub issue triage 30%. workload와 hardware에 따라 달라진다.

## Sources

- https://docs.headroomlabs.ai/docs
- https://docs.headroomlabs.ai/docs/configuration
- https://docs.headroomlabs.ai/docs/ccr
- https://docs.headroomlabs.ai/docs/benchmarks
- https://github.com/headroomlabs-ai/headroom
