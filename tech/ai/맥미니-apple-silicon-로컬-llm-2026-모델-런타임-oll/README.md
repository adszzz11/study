---
date: 2026-06-11
tags:
  - ai
  - local-llm
  - apple-silicon
  - ollama
  - lm-studio
  - mlx
type: tech-tool-study
---

# 맥미니 Apple Silicon 로컬 LLM 2026 학습 가이드

> Mac mini Apple Silicon의 unified memory와 Metal/MLX 가속을 활용해 Ollama, LM Studio, MLX/MLX-LM 같은 local LLM runtime으로 open-weight 모델을 로컬 실행하는 개발·개인 AI 셋업.

## 목차

1. [[01-overview|개요]] - What/Why, 핵심 특징, 아키텍처
2. [[02-ecosystem|에코시스템]] - runtime, 모델, 메모리 기준 비교
3. [[03-references|참고 자료]] - 공식 문서, 논문, 릴리스 자료
4. 학습 자료
   - [[04-learning/01-getting-started|초기 셋업]]
   - [[04-learning/02-deep-dive|심화 실험]]
5. [[05-projects|실전 프로젝트]] - 개인 AI 노드, 코딩 에이전트, RAG
6. [[cheatsheet|치트시트]] - 빠른 명령과 선택 기준

---

## Quick Start

### 1. 기본 runtime은 Ollama로 시작

```bash
curl -fsSL https://ollama.com/install.sh | sh
ollama run qwen3:8b
```

### 2. 로컬 REST API 확인

```bash
curl http://localhost:11434/api/chat -d '{
  "model": "qwen3:8b",
  "messages": [{"role": "user", "content": "한국어로 요약해줘"}],
  "stream": false
}'
```

### 3. GUI 비교는 LM Studio

```bash
lms server start
lms ps
```

OpenAI-compatible client에서는 `base_url`만 바꾼다.

```python
from openai import OpenAI

client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")
```

---

## 학습 경로

### 1단계: baseline 만들기

- [ ] Mac mini 사양 확인: unified memory, memory bandwidth, 저장공간
- [ ] Ollama 설치 및 `qwen3:8b` 실행
- [ ] REST API와 OpenAI-compatible endpoint 차이 이해
- [ ] [[litellm]] 또는 [[model-context-protocol-mcp]] 같은 상위 도구와 연결 가능성 확인

### 2단계: runtime 비교

- [ ] LM Studio로 GGUF 모델 탐색과 Local Server 실행
- [ ] MLX-LM으로 Apple Silicon native generation 테스트
- [ ] llama.cpp의 `llama-server`와 GGUF serving 옵션 확인
- [ ] 모델 크기, quantization, context length, KV cache 관계 정리

### 3단계: 개인 AI 노드 구성

- [ ] coding/agent용 모델 1개, 한국어 요약용 모델 1개 선정
- [ ] API server 자동 시작 방식 선택
- [ ] prompt, system template, context length 기준 기록
- [ ] [[ai-ecosystem]] 흐름 안에서 cloud LLM과 local LLM 역할 분리

---

## 선택 기준 요약

| 목적 | 우선 선택 | 이유 |
|---|---|---|
| 빠른 개발/자동화 | Ollama | CLI, REST API, model library, OpenAI 호환 |
| GUI 모델 비교 | LM Studio | 검색, 다운로드, 채팅, Local Server가 쉬움 |
| Apple Silicon native 실험 | MLX-LM | MLX format, quantization, LoRA/full fine-tuning |
| 저수준 튜닝 | llama.cpp | GGUF, Metal, 다양한 quantization, `llama-server` |

---

## 관련 노트

- [[ai-ecosystem]]
- [[litellm]]
- [[model-context-protocol-mcp]]
- [[codex]]

## Q&A
**Q:** 주식 리서치, 연구, 투자자동화에서 Codex SDK와 local LLM을 어떻게 나눠 쓰는 게 좋은가?
**A:** 이 용도에는 local LLM만으로 전부 처리하기보다, 노트의 권장처럼 cloud/tool agent와 local endpoint의 역할을 분리하는 구성이 좋다. 공개 자료 수집, 리포트 크롤링, 데이터 파이프라인 코드 작성, backtest script 생성, broker API wrapper 구현은 `Codex SDK` 같은 coding/research agent에 맡기고, 계좌 내역, 보유 종목, 개인 투자 규칙, 매매 후보 검토처럼 민감하거나 반복적인 판단 보조는 Mac mini의 local LLM에 맡기는 방식이다.

권장 구조는 `Codex SDK -> research/code automation`, `local LLM -> private portfolio analyst/verifier`, `deterministic rule engine -> order decision/execution`이다. local LLM은 계좌 데이터와 투자 메모를 외부 API로 보내지 않는 장점이 있으므로, 포트폴리오 요약, 리스크 설명, 종목별 thesis 정리, 매매 전 체크리스트, strategy log 해석에 적합하다. 반대로 실제 주문 실행은 LLM이 직접 결정하게 두지 말고, position sizing, max loss, exposure limit, cooldown, 승인 단계 같은 규칙 기반 guardrail을 통과한 경우에만 broker API가 실행하도록 분리하는 편이 안전하다.

Mac mini 64GB급이라면 상시 모델은 `qwen3:8b` 또는 `qwen3:14b`, 깊은 리서치/비교는 `qwen3:30b`/`qwen3:32b`, 최종 논리 검토는 `deepseek-r1:32b`처럼 역할을 나눈다. `Ollama`를 기본 automation endpoint로 두고, `LiteLLM`으로 `local-fast`, `local-research`, `local-reasoning`, cloud fallback을 라우팅하면 Codex SDK와 local LLM을 같은 OpenAI-compatible 흐름에서 다루기 쉽다. 긴 리포트와 시계열 데이터는 long context에 그대로 넣기보다 RAG/vector store와 chunk 요약으로 처리하고, 모델 비교 때는 model, quantization, context length, prompt template, memory pressure를 함께 기록한다.

투자자동화의 핵심은 "LLM이 매수/매도를 마음대로 한다"가 아니라 "LLM이 리서치와 판단 근거를 구조화하고, 사람이 정한 deterministic policy가 실행을 제한한다"에 가깝다. 따라서 초기 MVP는 1) Codex SDK로 데이터 수집/backtest/리포트 생성 자동화, 2) local LLM으로 계좌/종목 메모 요약과 trade rationale 생성, 3) 주문은 paper trading 또는 human approval부터 시작, 4) 충분한 로그와 재현 가능한 backtest가 쌓인 뒤 제한된 자동 실행으로 확장하는 순서가 적합하다.
