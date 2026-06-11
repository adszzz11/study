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
