---
date: 2026-06-11
tags:
  - ai
  - local-llm
  - projects
  - rag
  - agent
type: tech-tool-study
---

# 실전 프로젝트

## 프로젝트 1. 개인 로컬 LLM API 서버

### 목표

- Mac mini를 `localhost` 또는 LAN 내부 local LLM endpoint로 사용한다.
- 기본 모델은 Ollama, 비교/수동 테스트는 LM Studio로 분리한다.

### 구성

```text
Laptop / Editor / Agent
        |
        v
http://mac-mini.local:11434 or :1234/v1
        |
        v
Ollama / LM Studio
        |
        v
Qwen / Gemma / DeepSeek / coding model
```

### 체크리스트

- [ ] 고정 hostname 또는 local network alias 설정
- [ ] 기본 model 1개 선정
- [ ] API health check script 작성
- [ ] memory pressure가 높으면 context length 낮추기
- [ ] 외부 network 노출 금지 또는 방화벽 설정

## 프로젝트 2. 로컬 우선 coding assistant

### 목표

- 작은 수정, 설명, 테스트 생성은 local model로 처리한다.
- 복잡한 architecture reasoning은 cloud model로 fallback한다.

### 추천 조합

| 역할 | 모델/runtime |
|---|---|
| 빠른 코드 설명 | Ollama + 8B/14B |
| 코드 생성 실험 | Qwen Coder 계열 |
| OpenAI-compatible routing | [[litellm]] |
| agent tool context | [[model-context-protocol-mcp]] |

### Python smoke test

```python
from openai import OpenAI

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")

response = client.chat.completions.create(
    model="qwen3:8b",
    messages=[
        {"role": "system", "content": "You are a concise coding assistant."},
        {"role": "user", "content": "Explain how to refactor this function safely."},
    ],
)
print(response.choices[0].message.content)
```

## 프로젝트 3. 개인 문서 RAG

### 목표

- 개인 노트, PDF, markdown을 local embedding/RAG pipeline으로 검색한다.
- 답변 생성은 Mac mini local model을 우선 사용한다.

### 구성 요소

| Layer | 선택지 |
|---|---|
| 문서 파싱 | markdown loader, PDF parser, [[docling]] |
| Embedding | Ollama embedding model, llama.cpp embedding server |
| Vector store | SQLite/Chroma/Qdrant |
| Generation | Ollama 또는 LM Studio Local Server |
| Gateway | [[litellm]] |

## 프로젝트 4. MLX-LM fine-tuning 실험

### 목표

- Apple Silicon에서 LoRA 또는 quantization 실험을 해본다.
- 제품 운영이 아니라 learning/profiling 프로젝트로 둔다.

### 실험 항목

- [ ] 작은 instruction dataset 준비
- [ ] MLX-LM chat model baseline 기록
- [ ] LoRA fine-tuning 수행
- [ ] 원본/튜닝 모델 같은 prompt 비교
- [ ] memory, time, 품질 변화 기록

## Best Practices

| 원칙 | 설명 |
|---|---|
| 작은 모델부터 시작 | 3B~8B로 endpoint와 workflow를 먼저 안정화 |
| context를 욕심내지 않기 | long context는 KV cache 비용이 커짐 |
| runtime별 역할 분리 | Ollama는 automation, LM Studio는 GUI 비교, MLX-LM은 실험 |
| model card 기록 | license, context, quantization, template를 같이 기록 |
| cloud fallback 유지 | local model은 비용·프라이버시 장점, cloud model은 품질·복잡도 장점 |

## 완료 기준

- [ ] `curl` 또는 OpenAI client로 local endpoint 호출 가능
- [ ] 모델 3개 이상 비교 기록
- [ ] Mac mini memory 구성별 추천 모델 표 작성
- [ ] agent/RAG 중 하나에 실제 연결
- [ ] [[ai-ecosystem]] 안에서 local/cloud 역할 정리
