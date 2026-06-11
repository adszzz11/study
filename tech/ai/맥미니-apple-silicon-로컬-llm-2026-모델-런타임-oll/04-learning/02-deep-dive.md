---
date: 2026-06-11
tags:
  - ai
  - local-llm
  - deep-dive
  - quantization
  - kv-cache
  - mlx
type: tech-tool-study
---

# 심화 실험

## 목표

- 같은 prompt를 여러 runtime에서 비교한다.
- model size, quantization, context length, KV cache가 체감에 미치는 영향을 분리해서 본다.
- Mac mini를 개인 AI node로 운영할 때의 한계를 기록한다.

## 1. 메모리 계산 감각

간단한 근사:

```text
model memory ~= parameter_count * quantization_bits / 8
runtime overhead + KV cache + prompt/image tokens + batch buffer 추가
```

주의:

- Q4 8B 모델이 대략 4GB라고 끝나지 않는다.
- context length를 4K에서 32K로 올리면 KV cache가 크게 증가한다.
- vision model은 image token 때문에 동일 parameter count의 text model보다 부담이 커질 수 있다.
- 2025 quantization profiling 연구처럼 낮은 bit precision이 모든 하드웨어에서 자동으로 빠르지는 않다.

## 2. Context length 실험

같은 모델로 context만 바꿔 테스트한다.

| 실험 | Context | Prompt | 볼 것 |
|---|---:|---|---|
| A | 4096 | 짧은 한국어 요약 | baseline latency |
| B | 8192 | 긴 문서 요약 | memory pressure |
| C | 16384+ | 코드베이스 일부 설명 | 응답 품질 저하, 속도 저하 |

예시 prompt:

```text
아래 문서를 한국어로 요약하고, 핵심 의사결정 5개와 리스크 5개를 표로 정리해줘.
```

## 3. Runtime별 실험 포인트

### Ollama

- 모델 pull/run이 쉬워 baseline에 적합
- coding agent, script, REST API에 붙이기 좋음
- 2026년 MLX preview와 GGUF 개선으로 Apple Silicon 경로가 계속 확장 중

```bash
ollama list
ollama show qwen3:8b
ollama run qwen3:8b
```

### LM Studio

- 같은 모델 계열에서 quantization variant를 눈으로 비교하기 좋음
- GUI chat과 Local Server를 모두 확인
- `lms` CLI로 headless 흐름도 점검

```bash
lms ps
lms server start
lms load --context-length=8192
```

### MLX-LM

- Apple Silicon native path와 Python 실험에 적합
- LoRA/full fine-tuning, quantization 실험 가능
- 제품형 API server는 직접 구성하는 관점으로 접근

```bash
mlx_lm.generate \
  --model mlx-community/Llama-3.2-3B-Instruct-4bit \
  --prompt "Compare GGUF and MLX for Apple Silicon"
```

### llama.cpp

- GGUF, Metal offload, `llama-server` option을 직접 다룬다.
- embedding/RAG server, template debugging, quantization 비교에 유리하다.

```bash
llama-server \
  -m ./models/model.gguf \
  -c 8192 \
  --host 127.0.0.1 \
  --port 8080
```

## 4. 성능 기록 표

| Runtime | Model | Quant | Context | Prompt tokens | Output tokens | Memory pressure | Notes |
|---|---|---|---:|---:|---:|---|---|
| Ollama |  |  |  |  |  |  |  |
| LM Studio |  |  |  |  |  |  |  |
| MLX-LM |  |  |  |  |  |  |  |
| llama.cpp |  |  |  |  |  |  |  |

## 5. 품질 평가 과제

| 과제 | 목적 | 판단 기준 |
|---|---|---|
| 한국어 긴 글 요약 | 한국어 품질 | 누락, 반복, 문체 |
| 코드 설명 | developer utility | hallucination, API 정확도 |
| JSON 출력 | structured output | schema 준수 |
| tool calling 흉내 | agent compatibility | 함수 인자 안정성 |
| RAG 답변 | context 사용 | 근거 기반 답변 |

## 6. 운영 기준

- 항상 켜둘 모델은 memory pressure가 낮은 3B~8B급을 우선한다.
- coding/agent 작업은 14B~32B급을 필요할 때만 load하는 방식이 현실적이다.
- `base_url`을 통일하면 [[litellm]] 또는 앱 설정만 바꿔 local/cloud 전환이 쉬워진다.
- [[codex]] 같은 coding agent에 붙일 때는 tool calling, streaming, context length를 별도로 검증한다.
