---
date: 2026-10-27
tags: [tech]
type: tech-tool-study
status: draft
---

# References

## 권장 읽기 순서

1. GGUF spec으로 container의 header, metadata, tensor descriptor 순서를 잡는다.
2. llama.cpp의 모델 변환·quantization 문서에서 실제 toolchain을 본다.
3. safetensors format/security 문서로 tensor-only serialization의 경계를 이해한다.
4. PyTorch와 ONNX 문서로 checkpoint와 executable graph의 차이를 비교한다.

## 공식 문서와 소스

1. [GGUF format specification — ggml-org](https://github.com/ggml-org/ggml/blob/master/docs/gguf.md)
2. [GGUF on Hugging Face Hub](https://huggingface.co/docs/hub/gguf)
3. [llama.cpp: obtaining, converting and quantizing models](https://github.com/ggml-org/llama.cpp/blob/master/docs/models.md)
4. [llama.cpp model conversion guide](https://github.com/ggml-org/llama.cpp/blob/master/docs/development/HOWTO-add-model.md)
5. [llama.cpp gguf Python writer/reader tools](https://github.com/ggml-org/llama.cpp/tree/master/gguf-py)
6. [Safetensors format](https://github.com/huggingface/safetensors/blob/main/README.md)
7. [Safetensors security rationale](https://github.com/huggingface/safetensors/blob/main/SECURITY.md)
8. [PyTorch serialization semantics](https://docs.pytorch.org/docs/stable/notes/serialization)
9. [ONNX serialization](https://onnx.ai/onnx/api/serialization.html)
10. [FileInfo: `.llm` extension](https://fileinfo.com/extension/llm)

## 확인 질문

- 이 문서가 설명하는 것은 file container, quantization method, 또는 runtime 중 무엇인가?
- 지원 architecture와 tokenizer metadata의 범위는 어디까지인가?
- untrusted artifact를 load할 때 code execution surface는 있는가?
