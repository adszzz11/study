---
date: 2026-10-27
tags: [tech]
type: tech-tool-study
status: draft
---

# Cheatsheet: LLM model artifacts

## 빠른 판별

| 질문 | 답 |
|---|---|
| `.llm`이 Local LLM 표준인가? | 아니다. suffix만으로 format을 판단하지 않는다. |
| Local CPU/Metal 실행 파일은? | 보통 GGUF + llama.cpp 계열 runtime |
| HF training checkpoint의 안전한 tensor format은? | safetensors; config/tokenizer는 별도일 수 있음 |
| `.pt`를 바로 load해도 되는가? | 신뢰하지 않는 source라면 안 된다. pickle risk를 먼저 검토한다. |
| GPTQ/AWQ는 container인가? | 대개 quantization method다. |

## 변환 mental model

```text
checkpoint + config + tokenizer
→ converter가 tensor name/layout을 target schema로 mapping
→ metadata packaging
→ optional quantization
→ target runtime test
```

## GGUF 확인 항목

- magic/version과 runtime compatibility
- architecture metadata: layer, hidden size, head, RoPE, context
- tokenizer, special token, chat template
- tensor descriptor: name, shape, type, offset
- source precision 및 quantization type

## 안전 원칙

- untrusted pickle checkpoint는 load하지 않는다.
- `safetensors`여도 publisher, checksum, license와 동반 config를 확인한다.
- quantization variant는 같은 F16/F32 source에서 각각 만든다.
- output 품질은 짧은 prompt만이 아니라 실제 target workload로 검증한다.

## Sources

- https://github.com/ggml-org/ggml/blob/master/docs/gguf.md
- https://huggingface.co/docs/safetensors/index
- https://docs.pytorch.org/docs/stable/notes/serialization
