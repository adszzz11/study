---
date: 2026-10-27
tags: [tech]
type: tech-tool-study
status: draft
---

# What and Why: LLM 모델 파일

## What

LLM 모델 파일은 Transformer가 학습한 parameter tensor와 모델을 복원·실행하는 정보를 직렬화한 artifact다. “`.llm` 파일”이라는 범용 표준은 없다. 이름을 `.llm`으로 바꾸어도 loader가 tensor layout, dtype, metadata를 알 수 없으므로 모델이 되지 않는다.

## Why

학습이 끝난 weight는 대개 FP32/FP16이라 크다. 배포 단계는 이를 저장·전송·추론 환경에 맞게 바꾼다.

```text
Training corpus
  → tokenizer 학습 / 선택
  → Transformer pretraining
  → fine-tuning / alignment / LoRA merge
  → 원본 checkpoint (safetensors 또는 .pt)
  → format conversion + metadata packaging
  → quantization (선택)
  → .gguf / .onnx / GPU checkpoint
```

## 모델 artifact에 들어가는 것

| 구성 | 역할 |
|---|---|
| Weight tensors | embedding, attention Q/K/V/O, MLP, normalization, output head의 숫자 배열 |
| Tensor descriptor | 이름, shape, dtype, byte offset으로 loader의 mapping을 결정 |
| Architecture metadata | layer 수, hidden size, attention head, RoPE, context length, MoE 구성 |
| Tokenizer·special token·chat template | 입력 encoding, EOS 처리, 대화 형식을 일관되게 유지 |
| Quantization data | block별 code와 scale/offset으로 저정밀 weight를 표현 |

## 핵심 특징

- **Serialization**: 메모리의 tensor/graph를 파일 byte stream으로 옮긴다.
- **Compatibility**: 같은 weight라도 runtime, architecture, tokenizer가 맞아야 한다.
- **Quantization**: 4-bit 같은 낮은 정밀도로 memory와 bandwidth를 줄이는 대신 정확도 손실 가능성이 있다.
- **Security**: tensor-only format은 임의 Python object를 역직렬화하는 pickle보다 안전한 배포 경로다.

## `.llm`의 혼동

`.llm`은 Local LLM 공통 format이 아니다. FileInfo는 이를 Second Life의 Linden Lab Mesh 확장자로 소개한다. 파일을 판별할 때는 suffix가 아니라 format magic, metadata, 생성 도구와 runtime 문서를 확인한다.

## Sources

- https://fileinfo.com/extension/llm
- https://github.com/ggml-org/ggml/blob/master/docs/gguf.md
- https://huggingface.co/docs/safetensors/index
