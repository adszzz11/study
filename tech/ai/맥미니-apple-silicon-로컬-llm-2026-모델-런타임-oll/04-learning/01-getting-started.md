---
date: 2026-06-11
tags:
  - ai
  - local-llm
  - getting-started
  - ollama
  - lm-studio
  - mlx
type: tech-tool-study
---

# 초기 셋업

## 목표

- Mac mini에서 local LLM baseline을 만든다.
- Ollama, LM Studio, MLX-LM을 각각 한 번씩 실행한다.
- API client가 local endpoint를 호출할 수 있는지 확인한다.

## 0. 사전 확인

```bash
sw_vers
sysctl -n machdep.cpu.brand_string
system_profiler SPHardwareDataType | grep -E "Chip|Memory"
```

체크할 항목:

- Apple Silicon M-series인지 확인
- unified memory 용량 확인
- 여유 disk space 확인: model 여러 개를 받으면 수십 GB가 빠르게 찬다.

## 1. Ollama baseline

### 설치

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

### 첫 모델 실행

```bash
ollama run qwen3:8b
```

가벼운 비교용 모델:

```bash
ollama run llama3.2:3b
ollama run gemma3:4b
```

14B급 테스트:

```bash
ollama run deepseek-r1:14b
```

### REST API 호출

```bash
curl http://localhost:11434/api/chat -d '{
  "model": "qwen3:8b",
  "messages": [{"role": "user", "content": "한국어로 5줄 요약해줘"}],
  "stream": false
}'
```

### 확인 포인트

| 항목 | 기준 |
|---|---|
| first token latency | 처음 응답까지 걸리는 시간 |
| sustained throughput | 초당 token 생성 체감 |
| memory pressure | Activity Monitor에서 memory pressure 확인 |
| quality | 한국어 요약, 코드 설명, reasoning task로 확인 |

## 2. LM Studio로 모델 비교

### GUI 흐름

- LM Studio 설치
- Discover/Search에서 `Qwen`, `Gemma`, `DeepSeek`, `gpt-oss` 검색
- Apple Silicon friendly, GGUF/MLX, quantization variant 확인
- Chat 탭에서 같은 prompt로 모델 비교

### Local Server

OpenAI-compatible endpoint는 일반적으로 다음 형태다.

```text
http://localhost:1234/v1
```

Python client 예시:

```python
from openai import OpenAI

client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

response = client.chat.completions.create(
    model="local-model",
    messages=[{"role": "user", "content": "로컬 LLM 런타임을 비교해줘"}],
)

print(response.choices[0].message.content)
```

### `lms` CLI 흐름

```bash
lms ps
lms server start
lms load --context-length=4096
```

## 3. MLX-LM native 실험

### 설치

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install mlx-lm
```

### Generation

```bash
mlx_lm.generate --prompt "Explain Apple unified memory for LLM inference"
```

### Chat

```bash
mlx_lm.chat --model mlx-community/Llama-3.2-3B-Instruct-4bit
```

## 4. 결과 기록 템플릿

| Runtime | Model | Quant | Context | Memory pressure | 체감 속도 | 품질 메모 |
|---|---|---|---:|---|---|---|
| Ollama | `qwen3:8b` | default | 4096 | 낮음/중간/높음 |  |  |
| LM Studio |  |  |  |  |  |  |
| MLX-LM |  |  |  |  |  |  |

## 5. 다음 연결

- API gateway가 필요하면 [[litellm]]로 local/cloud routing을 구성한다.
- tool context가 필요하면 [[model-context-protocol-mcp]]와 local endpoint 연결을 실험한다.
- runtime 비교는 [[../02-ecosystem|에코시스템 비교]]로 돌아가서 정리한다.
