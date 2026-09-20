---
date: 2026-09-20
tags: [tech]
type: tech-tool-study
status: draft
---

# 04-2. Deep Dive

## 1. Safety gate부터 시작한다

Headroom은 모든 message를 압축 대상으로 보지 않는다. system prompt, user instruction, recent context, review/debug 대상 code처럼 의미 손실 비용이 큰 영역을 보호한다. 압축 효과가 0%인 것은 compressor failure가 아니라 의도적인 passthrough일 수 있다.

```text
incoming messages
  → protected? ── yes → passthrough
  → large enough? ── no → passthrough
  → content type detection
  → specialized compression
  → CCR save + marker
```

## 2. CacheAligner

Multi-turn agent에서 이전 turn 전체를 매번 다시 압축하면 serialized prefix byte가 바뀐다. provider가 이미 계산한 prefix cache를 재사용하지 못하면 token 수는 줄어도 전체 비용·latency가 나빠질 수 있다.

- `cache`: 과거 turn은 byte-faithful하게 유지하고 newest delta만 압축한다.
- `token`: 과거 turn도 다시 최적화해 input token을 더 줄인다.

평가는 `compressed token × input price`만으로 끝내지 말고 cached input price, cache hit rate, prefill latency를 함께 비교해야 한다.

## 3. ContentRouter와 specialized compressor

### JSON과 arrays

SmartCrusher는 schema와 representative item만 남기는 단순 sampling을 넘어 error, warning, outlier, 처음·마지막 항목을 우선 보존한다. Adaptive K가 coverage와 diversity를 보고 결과 크기를 정한다.

```json
{
  "schema": ["id", "status", "latency_ms"],
  "representative": ["first", "outlier", "error", "last"],
  "omitted": "repetitive normal rows",
  "retrieve": "hash marker"
}
```

이 예시는 개념도이며 실제 serialization format을 뜻하지 않는다.

### Logs, search, diff

- Logs: near-duplicate line을 줄이되 error와 stack trace를 우선한다.
- Search: relevant match와 주변 context를 남긴다.
- Diff: changed hunk를 중심으로 보존한다.

line number나 exact ordering이 downstream tool의 contract라면 compressed result만 쓰지 말고 원문 retrieval 또는 passthrough policy를 사용한다.

### Code와 general text

CodeAwareCompressor는 tree-sitter AST로 imports, signatures, types를 보존할 수 있다. 그러나 source code는 의미 밀도가 높아 실제로 보호 또는 passthrough되는 경우가 많다. dossier의 약 200-line Python benchmark도 0% 절감이었다.

General text는 과거 LLMLingua 경로가 아니라 ModernBERT/ONNX 기반 `Kompress-v2-base`를 사용한다.

## 4. CCR failure model

CCR의 성공에는 다음 연쇄가 모두 필요하다.

```text
원문 저장 성공
  → marker가 model context에 유지
  → model이 정보 부족을 감지
  → headroom_retrieve(hash) 호출
  → tool이 주입·실행
  → TTL/eviction 전 원문 존재
  → 원문을 사용해 답변 수정
```

따라서 다음 failure injection을 권장한다.

| 실험 | 기대 확인 |
|---|---|
| 잘못된 hash | 명확한 retrieval error와 안전한 fallback |
| TTL 만료 | stale marker 처리 방식 |
| capacity 초과 | LRU-style eviction 영향 |
| store lock/contention | multi-worker 안정성 |
| tool 호출 차단 | 모델이 불완전한 답을 확정하는지 |

## 5. Privacy와 운영 경계

Compression 자체가 local이라는 사실과 product가 어떤 operational metadata도 전송하지 않는다는 주장은 다르다. v0.37.0 dossier 기준:

- `HEADROOM_TELEMETRY`: 기본 off, local stats 전용
- `HEADROOM_BEACON`: 기본 on, token totals, ratios, skip reasons, provider/model ID, OS/architecture 같은 operational metadata 대상

민감 환경에서는 현재 version의 configuration과 privacy 문서를 확인하고 Beacon opt-out을 명시적으로 검증한다. prompt/code가 compression service로 전송되지 않더라도 provider로 보내는 원래 application traffic은 별개다.

## 6. Evaluation 설계

최소 evaluation unit은 payload compression ratio가 아니라 **task outcome**이다.

```text
같은 task + 같은 model + 같은 decoding 조건
├─ baseline: uncompressed
└─ candidate: Headroom
     ├─ answer correctness
     ├─ anomaly/error retention
     ├─ tool-call success
     ├─ retrieval frequency/success
     ├─ total billable tokens
     └─ end-to-end latency
```

workload를 JSON, logs, search, docs, source code로 stratify하고 평균뿐 아니라 worst-case regression을 본다. public benchmark가 QA accuracy 전체를 대신하지는 않는다.

## Sources

- https://docs.headroomlabs.ai/docs/architecture
- https://docs.headroomlabs.ai/docs/how-compression-works
- https://docs.headroomlabs.ai/docs/code-compression
- https://docs.headroomlabs.ai/docs/ccr
- https://docs.headroomlabs.ai/docs/benchmarks
- https://docs.headroomlabs.ai/docs/limitations
