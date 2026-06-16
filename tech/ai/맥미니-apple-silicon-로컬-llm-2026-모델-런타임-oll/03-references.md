---
date: 2026-06-11
tags:
  - ai
  - local-llm
  - references
  - apple-silicon
type: tech-tool-study
---

# 참고 자료

## 공식 문서

| 자료 | 링크 | 메모 |
|---|---|---|
| Apple Mac mini Technical Specifications | https://www.apple.com/mac-mini/specs/ | M4/M4 Pro CPU/GPU, Neural Engine, memory bandwidth, Thunderbolt |
| Ollama GitHub | https://github.com/ollama/ollama | 설치, CLI, REST API, backend 정보 |
| Ollama model library | https://ollama.com/library | `qwen3`, `gemma3`, `deepseek-r1`, coding model 탐색 |
| LM Studio docs | https://lmstudio.ai/docs/app | App, model search/download, runtime 설정 |
| LM Studio OpenAI-compatible API | https://lmstudio.ai/docs/developer/openai-compat | `base_url=http://localhost:1234/v1` 연결 |
| LM Studio system requirements | https://lmstudio.ai/docs/app/system-requirements | OS, hardware, Apple Silicon 요구사항 |
| MLX GitHub | https://github.com/ml-explore/mlx | Apple ML Research의 array framework |
| MLX-LM GitHub | https://github.com/ml-explore/mlx-lm | generation, chat, quantization, LoRA/full fine-tuning |
| llama.cpp GitHub | https://github.com/ggml-org/llama.cpp | GGUF, Metal, `llama-server`, quantization |

## 릴리스·블로그

| 자료 | 날짜 | 메모 |
|---|---:|---|
| Ollama MLX on Apple Silicon preview | 2026-03-30 | MLX engine preview, Apple Silicon native path |
| https://ollama.com/blog/mlx |  |  |
| Ollama GGUF performance/model support | 2026-06-05 | GGUF compatibility와 performance 개선 |
| https://ollama.com/blog/improved-performance-and-model-support-with-gguf |  |  |

## 논문·비교 연구

| 자료 | 링크 | 핵심 포인트 |
|---|---|---|
| Apple Silicon runtime comparison paper | https://arxiv.org/abs/2511.05502 | MLX는 sustained generation throughput, llama.cpp는 lightweight single-stream, Ollama는 developer ergonomics 강점 |
| Apple Silicon quantization profiling paper | https://arxiv.org/abs/2508.08531 | 낮은 bit precision이 항상 빠른 것은 아니며 hardware/runtime/model별 profiling 필요 |

## 함께 볼 노트

- [[ai-ecosystem]] - local LLM이 전체 AI stack에서 맡는 위치
- [[litellm]] - OpenAI-compatible endpoint를 local/cloud gateway로 묶는 방법
- [[model-context-protocol-mcp]] - local model과 tool context 연결
- [[codex]] - coding agent가 local endpoint를 활용하는 방식 검토

## 검증 체크리스트

- [ ] 문서의 release date와 현재 runtime version이 맞는가?
- [ ] model card의 license가 개인/상업 사용 목적에 맞는가?
- [ ] GGUF 또는 MLX model의 quantization과 context length가 Mac mini memory에 맞는가?
- [ ] OpenAI-compatible API가 tool calling, structured output, streaming을 필요한 수준까지 지원하는가?

## 추가 조사: 64GB 추천 모델 출처

| 자료 | 링크 | 확인한 내용 |
|---|---|---|
| Ollama `qwen3` library | https://ollama.com/library/qwen3 | 8B 5.2GB, 14B 9.3GB, 30B 19GB, 32B 20GB, 30B/235B MoE, Hermes Agent launch 예시 |
| Ollama `deepseek-r1` library | https://ollama.com/library/deepseek-r1 | 32B 20GB, 70B 43GB, reasoning model, 0528 Qwen3-8B update |
| Ollama `gemma3` library | https://ollama.com/library/gemma3 | 12B 8.1GB, 27B 17GB, text+image, 128K context, QAT model |
| Ollama `llama3.3` library | https://ollama.com/library/llama3.3 | 70B 43GB, 128K context, multilingual/tool-use considerations |
| Qwen3-Coder-30B-A3B-Instruct model card | https://huggingface.co/Qwen/Qwen3-Coder-30B-A3B-Instruct | 30.5B total / 3.3B activated, native 256K context, agentic coding/tool calling |
| Qwen3-Coder-Next model card | https://huggingface.co/Qwen/Qwen3-Coder-Next | Apache-2.0 open-weight coding model, 실험 후보 |
| Qwen3-Coder-Next technical report | https://arxiv.org/abs/2603.00729 | 80B total / 3B active coding agent model, agent-centric benchmark 지향 |
| Qwen3.6-35B-A3B model card | https://huggingface.co/Qwen/Qwen3.6-35B-A3B | 35B-A3B급 long-context/tool-use 실험 후보, 262K default context는 OOM 주의 |

메모:

- model library의 file size는 weight size에 가깝고, 실제 사용량은 runtime overhead, KV cache, batch, image token, concurrent request 때문에 더 커진다.
- 64GB Mac mini에서는 30B/32B급을 주력으로 삼되, 70B급은 단독 실험으로 분리하는 것이 안정적이다.
- model card의 최대 context가 128K/256K/1M이어도 local Mac에서 그대로 쓰기보다 8K/16K/32K부터 측정한다.
