---
date: 2026-06-11
tags:
  - ai
  - local-llm
  - runtime
  - ollama
  - lm-studio
  - mlx
  - llamacpp
type: tech-tool-study
---

# 에코시스템 비교

## Runtime 선택지

| 선택지 | 적합한 사용자 | 강점 | 약점/주의 | Mac mini 추천 |
|---|---|---|---|---|
| **Ollama** | CLI/API로 빠르게 로컬 모델 붙일 개발자 | 설치·실행이 간단, REST API, OpenAI 호환, model library, agent/coding tool 연동 | 세부 튜닝 자유도는 llama.cpp/MLX보다 낮음. MLX engine은 2026년 기준 preview/확장 중 | 기본 추천. 서버·자동화·코딩 에이전트용 |
| **LM Studio** | GUI로 모델 탐색·채팅·API 테스트할 사용자 | Hugging Face 검색/다운로드, GUI, OpenAI-compatible endpoint, `lms` CLI, GGUF+MLX | headless 운영은 Ollama보다 무겁게 느껴질 수 있음 | 첫 로컬 LLM 입문, 모델 비교 실험용 |
| **MLX-LM** | Apple Silicon 성능·fine-tuning·Python 실험 | MLX native, quantization, LoRA/full fine-tuning, Hugging Face MLX models | 제품형 API 서버/GUI는 직접 구성 필요 | 연구·튜닝·성능 실험용 |
| **llama.cpp** | 저수준 제어와 portability 중시 | GGUF 표준, Metal 최적화, 다양한 quantization, `llama-server` | 모델별 template/serving 세팅을 직접 만질 일이 많음 | 고급 사용자, embedding/RAG/서버 튜닝 |
| **MLC-LLM / PyTorch MPS** | 특정 연구·배포 실험 | MLC는 compile/runtime 최적화, PyTorch MPS는 PyTorch 친화성 | 일반 사용 편의성은 낮고, PyTorch MPS는 대형/long-context에서 메모리 제약이 큼 | 일반 초기 셋업 우선순위는 낮음 |

## 모델·메모리 실무 감각

| Mac mini 구성 | 현실적인 모델 범위 | 추천 모델 예 |
|---|---|---|
| **M4 16GB** | 3B~8B, Q4/Q5, modest context | `qwen3:8b`, `gemma3:4b`, `llama3.2:3b` |
| **M4 24GB** | 8B~14B 안정, 20B급은 context 조절 | `qwen3:14b`, `phi4:14b`, `gemma3:12b`, `deepseek-r1:14b` |
| **M4 Pro 24/48GB** | 20B~32B, 일부 35B/MoE, 긴 context는 메모리 계산 필요 | `qwen3:30b`, `qwen3-coder`, `gpt-oss:20b`, `deepseek-r1:32b` |
| **48GB+ 권장 영역** | 30B+ coding/agent, multi-agent, long context | Ollama MLX preview의 35B급 coding model처럼 32GB 초과 unified memory 요구 사례 |

## Format 비교

| Format | 주 사용처 | 장점 | 주의 |
|---|---|---|---|
| GGUF | llama.cpp, Ollama, LM Studio | 배포가 쉽고 quantization variant가 많음 | model card의 chat template과 runtime option 확인 필요 |
| MLX | MLX-LM, LM Studio, Ollama preview | Apple Silicon native 실험과 fine-tuning에 유리 | GGUF만큼 범용 runtime 지원이 넓지는 않음 |
| HF checkpoint | 연구·변환·fine-tuning | 원본 model lineage 추적이 쉬움 | local serving 전 GGUF/MLX 변환이 필요할 수 있음 |

## 선택 흐름

```text
처음 로컬 LLM을 쓴다
  -> LM Studio로 모델을 눈으로 비교
  -> 괜찮은 모델을 Ollama로 고정
  -> 앱/agent에는 OpenAI-compatible endpoint 연결

성능과 fine-tuning을 실험한다
  -> MLX-LM으로 MLX model 실행
  -> quantization/context/token throughput 기록
  -> 필요하면 llama.cpp와 같은 prompt로 비교

서버 옵션을 직접 조정한다
  -> llama.cpp + GGUF
  -> llama-server, Metal offload, context, batch option 튜닝
```

## OpenAI-compatible API 관점

| Runtime | 기본 endpoint 예 | 용도 |
|---|---|---|
| Ollama | `http://localhost:11434` | native REST API, local automation |
| LM Studio | `http://localhost:1234/v1` | OpenAI client drop-in replacement |
| llama.cpp | `http://localhost:8080/v1` | lightweight local server |
| LiteLLM bridge | `http://localhost:4000/v1` | [[litellm]]로 local/cloud model 라우팅 |

```python
from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:1234/v1",
    api_key="local"
)

response = client.chat.completions.create(
    model="local-model",
    messages=[{"role": "user", "content": "Mac mini 로컬 LLM 장단점을 표로 정리해줘"}],
)
print(response.choices[0].message.content)
```

## 2026 트렌드

- **Ollama:** 2026년 3월 MLX preview, 2026년 6월 GGUF 호환성·성능 개선 발표.
- **LM Studio:** GUI 중심에서 `lms` CLI, headless server, GGUF+MLX runtime 지원으로 확장.
- **MLX-LM:** Apple Silicon native generation, chat, quantization, LoRA/full fine-tuning 실험의 중심.
- **llama.cpp:** GGUF와 Metal 최적화의 사실상 기반 layer 역할.
- **상위 orchestration:** [[model-context-protocol-mcp]], [[codex]], [[litellm]] 같은 도구가 local endpoint를 tool/model backend로 사용.

## 결론

- 첫 셋업은 **Ollama + LM Studio** 조합이 가장 실용적이다.
- 성능 실험과 fine-tuning은 **MLX-LM**을 별도 트랙으로 둔다.
- 저수준 server control과 embedding/RAG는 **llama.cpp**를 배운다.

## 추가 조사: Mac mini M4 Pro 64GB/2TB 모델 추천

기준 사양:

- **Mac mini M4 Pro**
- **Unified memory:** 64GB
- **SSD:** 2TB
- **운영 목표:** Hermes Agent + local LLM + 여러 research job 동시 실행

### 결론

64GB unified memory는 30B/32B급 quantized model을 실사용하기 좋은 구간이다. 다만 Hermes Agent, browser/research process, embedding/RAG, 여러 local server를 같이 띄울 계획이라면 70B급을 상시 모델로 두기보다 **항상 켜둘 8B/14B + 주력 30B/32B + 특수 목적 vision/reasoning model**로 나누는 편이 안정적이다.

| 역할 | 1순위 추천 | 대안 | 이유 |
|---|---|---|---|
| 항상 켜둘 기본 assistant | `qwen3:8b` 또는 `qwen3:14b` | `gemma3:12b` | 빠른 응답, 낮은 memory pressure, 한국어/요약/일반 research에 충분 |
| 주력 research/coding agent | `qwen3:30b` 또는 `qwen3:32b` | `Qwen3-Coder-30B-A3B-Instruct` GGUF/MLX quant | 64GB에서 품질과 속도의 균형이 좋고, 30B MoE는 활성 parameter가 작아 agent loop에 유리 |
| reasoning 전용 | `deepseek-r1:32b` | `deepseek-r1:14b` | 수학/논리/검토용. 답변이 길고 느릴 수 있어 필요할 때만 load |
| vision/document screenshot | `gemma3:27b` | `gemma3:12b` | text+image 입력, 문서 스크린샷/도표 질의에 유용 |
| 실험용 대형 모델 | `llama3.3:70b` | Qwen3-Coder-Next quant | 43GB급 weight는 64GB에 들어갈 수 있지만 Hermes/research 동시 실행과 long context에서는 여유가 작음 |

### Ollama 기준 빠른 설치 세트

```bash
# 항상 켜둘 모델
ollama pull qwen3:8b
ollama pull qwen3:14b

# 주력 research/coding
ollama pull qwen3:30b
ollama pull qwen3:32b

# reasoning / vision
ollama pull deepseek-r1:32b
ollama pull gemma3:27b
```

### 동시 실행 관점의 권장 조합

| 시나리오 | 권장 load | 설명 |
|---|---|---|
| 평상시 daemon | `qwen3:8b` 또는 `qwen3:14b` 1개 | Hermes Agent가 자주 호출하는 기본 local endpoint |
| research batch | `qwen3:30b` 1개 + embedding/RAG | 긴 문서 요약, 후보안 생성, 코드 탐색 |
| 검토 단계 | `qwen3:30b` 결과를 `deepseek-r1:32b`로 cross-check | reasoning model은 verifier처럼 짧게 사용 |
| vision 필요 | `gemma3:12b`/`27b`를 별도 session으로 load | image token 때문에 text model보다 memory 여유를 더 잡음 |
| 대형 실험 | `llama3.3:70b` 단독, context 4K~16K부터 | 다른 heavy job을 내리고 단일 실험으로 취급 |

### 피해야 할 기본값

- `70B`를 항상 켜두고 Hermes Agent와 여러 research job을 동시에 돌리는 구성
- model card의 최대 context를 그대로 쓰는 구성: 128K/256K는 가능 여부보다 **KV cache 비용**이 먼저 문제다.
- vision model과 30B+ text model을 동시에 오래 유지하는 구성
- quantization, context, prompt template를 기록하지 않고 모델만 바꿔 비교하는 방식

### 2TB SSD 운영 감각

- 2TB면 8B/14B/30B/32B/vision/reasoning 모델을 여러 variant로 보관해도 여유가 있다.
- 다만 GGUF/MLX quantization variant를 많이 받으면 200~500GB는 빠르게 사용한다.
- `Ollama`, `LM Studio`, `HF cache`, benchmark output, RAG index 위치를 분리해서 관리한다.

```bash
ollama list
du -sh ~/.ollama ~/.cache/huggingface 2>/dev/null
```

### 최신 확인 포인트

- Ollama의 `qwen3` library는 8B 5.2GB, 14B 9.3GB, 30B 19GB, 32B 20GB variant를 제공한다.
- Ollama의 `deepseek-r1` library는 32B 20GB, 70B 43GB variant를 제공한다.
- Ollama의 `gemma3` library는 12B 8.1GB, 27B 17GB, text+image, 128K context variant를 제공한다.
- Qwen3-Coder-30B-A3B-Instruct model card는 30.5B total / 3.3B activated parameter, native 256K context, agentic coding/tool calling을 강조한다.
