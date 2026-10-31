---
date: 2026-10-27
tags: [tech]
type: tech-tool-study
status: draft
---

# Projects

## 1. GGUF metadata inspector

**목표**: GGUF reader로 metadata KV, tensor name/shape/type/offset을 출력한다.

- input: 신뢰할 수 있는 GGUF sample
- output: architecture, context length, tokenizer 관련 metadata의 요약
- 확인: spec과 reader tool이 같은 tensor 수와 offset을 보고하는지 비교

## 2. Quantization trade-off benchmark

**목표**: 동일 F16 source에서 만든 Q4, Q5, Q8 artifact의 크기·속도·품질을 비교한다.

| 측정 | 방법 |
|---|---|
| disk size | `ls -lh`로 artifact별 기록 |
| load / generation speed | 같은 runtime, prompt, context, hardware에서 측정 |
| quality | 고정된 task set과 사람 검토 또는 정량 평가 사용 |

재-quantization은 비교 조건에서 제외한다. 각 variant는 같은 F16/F32 source에서 독립적으로 생성한다.

## 3. Safe checkpoint intake checklist

**목표**: 외부 model artifact를 받기 전 provenance와 load risk를 문서화한다.

- publisher, model card, license, checksum을 기록한다.
- format이 safetensors인지 pickle 기반 checkpoint인지 구분한다.
- architecture/config/tokenizer가 artifact와 함께 있는지 확인한다.
- 격리된 환경에서도 untrusted pickle load는 피한다.

## Sources

- https://github.com/ggml-org/llama.cpp/tree/master/gguf-py
- https://huggingface.co/docs/safetensors/index
- https://docs.pytorch.org/docs/stable/notes/serialization
