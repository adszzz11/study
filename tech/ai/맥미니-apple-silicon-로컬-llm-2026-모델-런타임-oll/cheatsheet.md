---
date: 2026-06-11
tags:
  - ai
  - local-llm
  - cheatsheet
  - apple-silicon
type: tech-tool-study
---

# 치트시트

## Runtime 선택

| 목적 | 선택 |
|---|---|
| 가장 빠른 시작 | Ollama |
| GUI로 모델 찾기 | LM Studio |
| OpenAI-compatible local server | LM Studio, Ollama, llama.cpp |
| Apple Silicon native 실험 | MLX-LM |
| GGUF 저수준 튜닝 | llama.cpp |
| local/cloud 라우팅 | [[litellm]] |

## Mac mini 모델 감각

| Memory | 추천 범위 |
|---|---|
| 16GB | 3B~8B, Q4/Q5, context 보수적으로 |
| 24GB | 8B~14B 안정, 20B급은 조절 |
| 24/48GB M4 Pro | 20B~32B, 일부 35B/MoE |
| 48GB+ | 30B+ coding/agent, long context 실험 |

## Ollama

```bash
curl -fsSL https://ollama.com/install.sh | sh
ollama run qwen3:8b
ollama run llama3.2:3b
ollama run deepseek-r1:14b
ollama list
ollama show qwen3:8b
```

```bash
curl http://localhost:11434/api/chat -d '{
  "model": "qwen3:8b",
  "messages": [{"role": "user", "content": "한국어로 요약해줘"}],
  "stream": false
}'
```

## LM Studio

```bash
lms ps
lms server start
lms load --context-length=4096
```

```python
from openai import OpenAI

client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")
```

## MLX-LM

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install mlx-lm
```

```bash
mlx_lm.generate --prompt "Explain Apple unified memory for LLM inference"
mlx_lm.chat --model mlx-community/Llama-3.2-3B-Instruct-4bit
```

## llama.cpp

```bash
llama-server \
  -m ./models/model.gguf \
  -c 8192 \
  --host 127.0.0.1 \
  --port 8080
```

## API endpoints

| Runtime | Endpoint |
|---|---|
| Ollama native | `http://localhost:11434/api/chat` |
| Ollama OpenAI-compatible | `http://localhost:11434/v1` |
| LM Studio | `http://localhost:1234/v1` |
| llama.cpp | `http://localhost:8080/v1` |

## 핵심 개념

| 용어 | 의미 |
|---|---|
| Unified memory | CPU/GPU가 같은 memory pool을 공유하는 Apple Silicon 구조 |
| Metal | Apple GPU acceleration API |
| MLX | Apple Silicon용 array framework |
| GGUF | llama.cpp 중심의 local LLM model format |
| Quantization | weight precision을 낮춰 memory 사용량을 줄이는 기법 |
| KV cache | long context generation에서 attention key/value를 저장하는 memory |
| Context length | 모델이 한 번에 참조할 수 있는 token window |

## 실수 방지

- 모델 크기만 보지 말고 quantization, context, KV cache를 같이 본다.
- 16GB Mac mini에서 14B+ 모델은 context를 낮춰 테스트한다.
- vision model은 text model보다 memory 여유를 더 잡는다.
- agent에 붙이기 전 streaming, JSON output, tool calling compatibility를 확인한다.
- local endpoint를 외부 network에 노출하지 않는다.

## 관련 노트

- [[ai-ecosystem]]
- [[litellm]]
- [[model-context-protocol-mcp]]
- [[codex]]
