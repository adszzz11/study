---
date: 2026-10-27
tags: [tech]
type: tech-tool-study
status: draft
---

# Ecosystem: format과 runtime 비교

| 형식·방법 | 주 대상 | 생성물 구성 | 강점 | 주의점 |
|---|---|---|---|---|
| `.gguf` | llama.cpp, Local LLM, CPU/Metal | metadata + tokenizer 정보 + tensor의 single binary | portable, quantization, local deployment | architecture/version 지원 확인 필요 |
| `.safetensors` | Transformers, training/fine-tuning, vLLM 계열 | 안전한 tensor file; config/tokenizer는 대개 별도 | pickle보다 안전, 빠른 metadata parsing | 단독으로 runnable model spec이 아닐 수 있음 |
| `.pt` / `.pth` | PyTorch research/checkpoint | `state_dict` 또는 Python object | PyTorch workflow와 직접 연결 | pickle load는 untrusted file에 위험 |
| `.onnx` | cross-runtime serving, edge inference | graph + weights의 Protocol Buffers serialization | framework-neutral graph | 최신 LLM/quant export가 항상 매끄럽지는 않음 |
| GPTQ / AWQ | NVIDIA GPU weight-only quantization | 보통 safetensors checkpoint + quant config | GPU memory 절감·throughput 최적화 | container보다 quantization method에 가까움 |
| `.llm` | 공통 LLM runtime 없음 | 정의되지 않음 | 없음 | 확장자만으로 format 판단 불가 |

## 선택 기준

- **CPU 또는 Apple Silicon local inference**: target runtime이 지원한다면 GGUF를 우선 검토한다.
- **학습·adapter merge·Hub 배포**: `safetensors` + config/tokenizer 파일 묶음이 일반적이다.
- **framework 간 serving/edge**: export 가능성을 검증한 뒤 ONNX를 검토한다.
- **NVIDIA GPU memory 압박**: GPTQ/AWQ와 engine 호환성을 함께 평가한다.

## Container와 quantization을 구분하기

GGUF, safetensors, ONNX는 저장 구조 또는 실행 graph의 표현 방식이다. GPTQ/AWQ는 weight를 줄이는 quantization 방식이다. 따라서 “GPTQ 파일”도 실제로는 safetensors와 별도 quantization config일 수 있다.

## Sources

- https://huggingface.co/docs/hub/gguf
- https://huggingface.co/docs/safetensors/index
- https://docs.pytorch.org/docs/stable/notes/serialization
- https://onnx.ai/onnx/api/serialization.html
