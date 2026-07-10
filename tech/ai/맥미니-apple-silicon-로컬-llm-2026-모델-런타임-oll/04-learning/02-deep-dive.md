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

## 추가 조사: Hermes Agent 동시 실행 기준 실험

### 64GB memory budget 가정

Mac mini M4 Pro 64GB에서 실제 LLM에 전부를 쓸 수 있다고 보면 안 된다. macOS, browser, editor, Hermes Agent, terminal multiplexer, vector DB, embedding process, file watcher가 같이 memory를 쓴다.

실무 예산:

| 항목 | 보수적 예산 | 메모 |
|---|---:|---|
| macOS + 기본 앱 | 8~12GB | browser tab 수에 따라 크게 변동 |
| Hermes Agent / coding agent | 2~8GB | 작업공간 크기, tool call, 로그에 따라 변동 |
| RAG/embedding/vector store | 2~8GB | chunking, index build 중 peak가 큼 |
| 항상 켜둘 8B/14B model | 5~10GB+ | Ollama library 기준 `qwen3:8b` 5.2GB, `qwen3:14b` 9.3GB |
| 주력 30B/32B model | 19~25GB+ | weight 외 KV cache/runtime overhead 필요 |
| 여유 buffer | 8~16GB | memory pressure green/yellow 경계 유지용 |

### 추천 운영 패턴

1. **Default model:** `qwen3:8b` 또는 `qwen3:14b`
   - Hermes Agent의 빠른 요약, 분류, 초안, 간단한 코드 설명에 사용한다.
   - context는 처음에 8K~16K로 제한하고, long document는 chunk/RAG로 보낸다.

2. **Heavy research model:** `qwen3:30b` 또는 `qwen3:32b`
   - 논문/문서 비교, 코드베이스 분석, 긴 의사결정 문서 작성에 사용한다.
   - 동시에 여러 research를 돌릴 때는 같은 30B model에 요청을 몰아주고, 다른 30B+ model을 추가로 load하지 않는다.

3. **Verifier model:** `deepseek-r1:32b`
   - 최종 결론 검토, 수학/논리/반례 찾기에 사용한다.
   - thinking output이 길 수 있으므로 `max_tokens`와 task 범위를 좁힌다.

4. **Vision model:** `gemma3:12b` 또는 `gemma3:27b`
   - screenshot, chart, PDF page image 설명에만 별도 사용한다.
   - vision model은 image token 때문에 text-only 27B보다 memory가 더 빡빡하게 느껴질 수 있다.

### 실험 matrix

| Test | Loaded models | Context | Background jobs | Pass 기준 |
|---|---|---:|---|---|
| A | `qwen3:8b` | 8K | Hermes Agent 1개 | memory pressure green, 응답 지연 낮음 |
| B | `qwen3:14b` | 16K | Hermes Agent + browser research | memory pressure green/yellow, swap 증가 작음 |
| C | `qwen3:30b` | 16K | RAG query + file search | sustained throughput 체감 가능 |
| D | `qwen3:30b` + embedding | 32K | research 2개 | swap 급증 없고 실패 없이 완료 |
| E | `llama3.3:70b` | 4K~16K | heavy job 없음 | 단독 실험으로만 pass |

### 측정 명령

```bash
ollama ps
ollama list
vm_stat
memory_pressure
top -l 1 -o mem | head -n 30
```

간단한 smoke prompt:

```text
아래 연구 메모를 읽고, 결론/근거/리스크/다음 실험을 한국어 bullet로 분리해줘.
각 bullet은 근거 문장 번호를 포함해.
```

### LiteLLM routing 예시

```yaml
model_list:
  - model_name: local-fast
    litellm_params:
      model: ollama/qwen3:8b
      api_base: http://localhost:11434
  - model_name: local-research
    litellm_params:
      model: ollama/qwen3:30b
      api_base: http://localhost:11434
  - model_name: local-reasoning
    litellm_params:
      model: ollama/deepseek-r1:32b
      api_base: http://localhost:11434
```

운영 원칙:

- Hermes Agent의 기본값은 `local-fast`로 둔다.
- 긴 research synthesis만 `local-research`로 보낸다.
- 결론 검토와 반례 찾기는 `local-reasoning`으로 분리한다.
- cloud fallback은 architecture decision, high-stakes writing, local model disagreement 때만 사용한다.
