---
date: 2026-09-20
tags: [tech]
type: tech-tool-study
status: draft
---

# 01. Headroom Overview

## What

Headroom은 application과 LLM provider 사이에 놓이는 **local context optimization layer**다. 전체 prompt를 일괄 요약하는 대신, context에서 크고 반복적인 tool-generated payload를 찾아 구조에 맞게 줄인다.

```text
Agent / Application
        │ messages, tool results, logs, files
        ▼
Safety gates / protected recent context
        ▼
CacheAligner ── prefix-cache drift 감지
        ▼
ContentRouter ── content type 판별
        ├─ SmartCrusher: JSON, arrays, tables
        ├─ Log / Search / Diff / HTML / Config compressors
        ├─ CodeAwareCompressor: tree-sitter AST
        └─ Kompress-v2-base: general text
        ▼
CCR store ── hash-keyed local SQLite
        ▼
Compressed context + headroom_retrieve
        ▼
LLM provider
```

## Why

Agentic workflow에서는 다음 데이터가 매 turn의 input context를 빠르게 키운다.

- `grep` 또는 code search 결과 수백 건
- CI, build, test, production logs
- MCP tool response와 API JSON
- DB rows와 RAG retrieval documents
- files와 장시간 conversation history

그 결과 input token 비용과 prefill latency가 늘고, context window가 일찍 소진된다. 반복 로그 속에 error가 묻히기도 하며, 이전 turn을 다시 압축하면 provider prefix cache가 깨질 수 있다. 반대로 단순 truncation은 JSON 구조, code syntax, tool-call ordering을 손상할 수 있다.

Headroom의 핵심 선택은 **모든 문장을 균등하게 줄이지 않는 것**이다. system prompt, user instruction, recent context를 보호하고 압축 이익이 큰 machine-generated content를 우선 처리한다.

## 핵심 특징

### Content-aware compression

`ContentRouter`는 Magika와 deterministic pattern matching으로 payload type을 판별한다.

| Content | 처리 방식 | 보존하려는 정보 |
|---|---|---|
| JSON / arrays | SmartCrusher, Adaptive K | schema, 처음·마지막 항목, error, warning, outlier |
| Logs | repetition 제거 | error, anomaly, stack trace |
| Search / diff | relevant subset 추출 | match와 changed hunk |
| HTML | boilerplate 제거 | 본문 content |
| Code | tree-sitter AST | import, signature, type |
| General text | ModernBERT/ONNX `Kompress-v2-base` | relevant passage |

`Adaptive K`는 Kneedle coverage curve, SimHash near-duplicate detection, zlib diversity validation을 사용해 남길 항목 수를 정한다. 다만 최근 code나 review/debug 대상 code는 기본 보호되어 code payload가 자주 passthrough될 수 있다.

### CCR: Compress–Cache–Retrieve

압축 전 원문은 hash-keyed local SQLite `ccr_store.db`에 저장된다. 압축 결과의 retrieval marker를 본 모델이 부족한 정보로 판단하면 `headroom_retrieve(hash)`로 원문을 요청할 수 있다.

- SQLite persistence와 multi-worker 공유
- 기본 TTL 30분
- capacity 도달 시 LRU-style eviction
- optional in-memory backend
- setuptools entry point 기반 custom backend
- Anthropic/OpenAI proxy path의 transparent retrieval handling

CCR은 **storage-level reversibility**를 제공하지만 downstream answer가 항상 lossless라는 뜻은 아니다. 모델이 retrieval 필요성을 감지하고, tool이 올바르게 실행되며, TTL/eviction 전에 원문이 남아 있어야 한다.

### Provider cache와의 공존

| Proxy mode | 최적화 목표 | Trade-off |
|---|---|---|
| `cache` (기본) | 이전 turn을 byte-faithful하게 유지하고 newest delta만 압축 | token 절감보다 prefix cache hit 안정성을 우선 |
| `token` | 이전 turn까지 재압축 | 더 큰 절감 가능, prefix cache drift 가능 |

SDK의 `audit / optimize / simulate` mode는 위 proxy mode와 다른 축이다. 전자는 압축 동작 방식, 후자는 multi-turn cache 전략을 고른다.

## 적용 표면

- Transparent proxy: `headroom proxy --port 8787`
- Agent wrapper: `headroom wrap claude|codex|copilot|aider|opencode|...`
- Python API: `compress(messages, model=...)`
- TypeScript SDK: `await compress(messages, { model })`
- MCP: `headroom_compress`, `headroom_retrieve`, `headroom_stats`
- Adapter: LangChain, LangGraph, Agno, Strands, LiteLLM, Vercel AI SDK

TypeScript package는 독립 CLI가 아니라 local Headroom proxy를 호출하는 SDK다. CLI는 Python/PyPI package에만 포함된다.

## Evidence를 읽는 법

공식 v0.37.0 재현 benchmark에서 workload 절감률은 code search 21%, SRE debugging 57%, codebase exploration 42%, GitHub issue triage 30%였다. 따라서 headline 수치보다 자신의 traffic distribution이 중요하다.

| Local payload | Token 절감 | Compression overhead p50 |
|---|---:|---:|
| JSON search results 100개 | 48% | 0.20 ms |
| JSON search results 500개 | 49% | 0.77 ms |
| Structured logs 500개 | 54% | 0.51 ms |
| Documentation text 약 20K tokens | 92% | 1.4 ms |
| Python source 약 200줄 | 0% | 1.3 ms |

이 수치는 Apple M-series local benchmark이며 LLM latency를 포함하지 않는다. 공개 평가는 최종 answer equivalence 전반을 강하게 입증하지 않으며 일부 sample은 `N=100`, 일부 metric에는 uncompressed baseline이 없다.

## Sources

- https://docs.headroomlabs.ai/docs/architecture
- https://docs.headroomlabs.ai/docs/how-compression-works
- https://docs.headroomlabs.ai/docs/code-compression
- https://docs.headroomlabs.ai/docs/ccr
- https://docs.headroomlabs.ai/docs/benchmarks
- https://docs.headroomlabs.ai/docs/limitations
