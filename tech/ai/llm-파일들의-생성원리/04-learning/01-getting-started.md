---
date: 2026-10-27
tags: [tech]
type: tech-tool-study
status: draft
---

# Getting Started: checkpoint에서 GGUF까지

## 목표

Hugging Face 형식의 model directory를 llama.cpp가 읽을 수 있는 F16 GGUF로 변환하고, 필요하면 한 번만 quantize한다. 명령과 script 이름은 llama.cpp release에 따라 달라질 수 있으므로 실행 전 `docs/models.md`를 확인한다.

## 준비물

- 변환 대상의 architecture를 지원하는 llama.cpp
- 신뢰할 수 있는 Hugging Face model directory (`config.json`, tokenizer 관련 파일, safetensors 등)
- 대상 runtime에서 검증할 수 있는 충분한 disk space와 memory

## 흐름

```bash
# llama.cpp checkout에서: 모델을 F16 GGUF로 변환
python convert_hf_to_gguf.py /path/to/hf-model --outtype f16 --outfile model-f16.gguf

# F16 원본을 목표 quantization으로 한 번만 변환
./llama-quantize model-f16.gguf model-q4_k_m.gguf Q4_K_M

# runtime에서 metadata와 짧은 prompt를 확인
./llama-cli -m model-q4_k_m.gguf -p "Hello" -n 32
```

## 검증 checklist

- [ ] 모델 architecture와 converter 지원 여부를 확인했다.
- [ ] tokenizer, EOS token, chat template metadata가 유지됐는지 확인했다.
- [ ] F16/F32 source에서 quantize했다. 이미 저정밀인 GGUF를 재-quantize하지 않았다.
- [ ] file size, load 가능 여부, 짧은 generation을 비교했다.
- [ ] 원본 checkpoint의 license와 provenance를 기록했다.

## 흔한 실패

| 증상 | 우선 확인할 것 |
|---|---|
| converter가 tensor name을 찾지 못함 | architecture 지원과 checkpoint layout |
| 출력이 즉시 종료되거나 형식이 이상함 | tokenizer, special token, chat template |
| 품질이 급락함 | quantization level, 재-quantization 여부 |
| runtime이 load하지 못함 | GGUF version과 runtime build의 호환성 |

## Sources

- https://github.com/ggml-org/llama.cpp/blob/master/docs/models.md
- https://github.com/ggml-org/llama.cpp/blob/master/docs/development/HOWTO-add-model.md
