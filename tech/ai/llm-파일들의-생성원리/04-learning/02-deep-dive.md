---
date: 2026-10-27
tags: [tech]
type: tech-tool-study
status: draft
---

# Deep Dive: binary layout, quantization, security

## GGUF의 개념적 layout

```text
magic / version
→ tensor 수 + metadata KV 수
→ typed metadata key/value pairs
→ tensor descriptors (name, shape, type, offset)
→ alignment padding
→ raw / quantized tensor blocks
```

GGUF writer는 Hugging Face config, tokenizer, tensor name/data를 읽어 metadata와 tensor descriptor를 만든다. alignment된 raw tensor 영역은 runtime이 `mmap`과 byte offset 기반 mapping에 활용하기 좋다. 정확한 field 크기와 version 규칙은 반드시 공식 spec을 기준으로 한다.

## safetensors의 layout

```text
8-byte little-endian header length
→ JSON header (tensor dtype, shape, byte offsets)
→ contiguous raw tensor byte buffer
```

JSON header와 raw bytes만으로 tensor를 표현하므로 Python pickle object 실행이 필요 없다. 다만 model architecture와 tokenizer는 보통 `config.json`, `tokenizer.json`, `generation_config.json`처럼 별도 배포된다.

## block quantization

quantization은 FP16 숫자를 단순 절단하는 과정이 아니다. 흔히 tensor를 block으로 나누고 각 block에 low-bit code와 scale(필요하면 offset)을 저장한다. inference kernel은 이를 근사 복원하거나 packed 표현을 직접 사용한다.

```text
FP16 weights → block 분할 → codebook/int code + scale 저장
                              ↓
                    packed quantized tensor
```

- 낮은 bit 수는 memory·bandwidth를 줄이지만 perplexity와 생성 품질에 영향을 줄 수 있다.
- 품질 평가는 파일 크기만이 아니라 target prompt, context length, runtime에서 수행한다.
- Q4_K, Q5_K, Q8_0은 GGML 계열 quantization type의 예이며 지원 여부는 build/version에 의존한다.

## 보안 경계

untrusted `.pt`/`.pth`는 함부로 `torch.load`하지 않는다. PyTorch serialization은 기본적으로 pickle을 사용하며 악성 payload가 code execution을 유발할 수 있다. 가능하면 신뢰할 수 있는 source에서 받은 `safetensors`를 사용하고, checksum·publisher·license를 확인한다.

## Sources

- https://github.com/ggml-org/ggml/blob/master/docs/gguf.md
- https://github.com/ggml-org/llama.cpp/blob/master/tools/quantize/quantize.cpp
- https://github.com/huggingface/safetensors/blob/main/SECURITY.md
- https://docs.pytorch.org/docs/stable/notes/serialization
