---
date: 2026-06-23
tags:
  - tech
  - ai
  - fugu
  - sakana-ai
  - multi-agent
  - orchestration
status: learning
type: tech-tool-study
---

# Sakana Fugu 분석

> **한 줄 정의**: Sakana Fugu는 여러 frontier LLM/agent를 하나의 OpenAI-compatible API 뒤에서 동적으로 조율하는 "multi-agent system as a model" 제품이다.

## 개요

Fugu는 사용자가 직접 planner, worker, verifier, model router를 설계하지 않아도 복잡한 multi-step task에 여러 expert model을 동원하도록 만든 managed multi-agent API다. 겉으로는 OpenAI-compatible endpoint처럼 호출하지만, 내부에서는 task별 model selection, switching, coordination이 수행된다.

핵심 가설은 단일 frontier model을 계속 키우는 것만이 답이 아니라는 점이다. coding, reasoning, science, long-context, tool-use처럼 provider별 강점이 갈라진 상황에서는 runtime orchestration이 더 나은 cost-performance를 만들 수 있다.

---

## Quick Start

```bash
# Fugu는 OpenAI-compatible API를 표방하므로
# 기존 OpenAI client의 base_url, api_key, model만 바꾸는 방식으로 평가를 시작한다.

export FUGU_API_KEY="..."
export FUGU_BASE_URL="https://api.example-fugu-compatible/v1"

python eval_fugu.py --model fugu
python eval_fugu.py --model fugu-ultra-20260615
```

```python
from openai import OpenAI

client = OpenAI(
    api_key="...",
    base_url="https://api.example-fugu-compatible/v1",
)

response = client.chat.completions.create(
    model="fugu",
    messages=[
        {"role": "user", "content": "Review this PR diff and list blocking issues."}
    ],
)

print(response.choices[0].message.content)
```

> [!note]
> 실제 endpoint, API key, model availability는 Sakana Fugu 공식 페이지와 계정 설정을 확인한다. 학습에서는 동일 prompt set으로 latency, token usage, pass/fail, hallucination rate를 비교하는 것이 중요하다.

---

## 학습 경로

### 1단계: 문제의식 이해

- [ ] [[01-overview|개요]] 읽기 - Fugu가 해결하려는 model selection과 multi-agent orchestration 문제
- [ ] `single frontier model`, `model router`, `managed multi-agent API`의 차이 정리
- [ ] Fugu와 Fugu Ultra의 latency/quality trade-off 이해

### 2단계: 생태계 비교

- [ ] [[02-ecosystem|생태계]]에서 OpenRouter, RouteLLM, Mixture-of-Agents, MASRouter, AutoGen/LangGraph와 비교
- [ ] [[study/tech/ai/litellm]] 같은 gateway/router와 Fugu의 orchestration 차이 정리
- [ ] [[study/tech/ai/multi-agent-platforms/autogen]]이나 LangGraph로 직접 만든 agent pipeline과 비교 기준 작성

### 3단계: 근거 자료 확인

- [ ] [[03-references|참고자료]]에서 Sakana Fugu 공식 페이지와 technical report 확인
- [ ] TRINITY와 Conductor가 Fugu식 orchestration에 주는 연구적 배경 파악
- [ ] benchmark claim의 공개 범위와 한계 기록

### 4단계: 실습

- [ ] [[04-learning/01-getting-started|시작하기]] - OpenAI-compatible client로 `fugu`, `fugu-ultra-20260615` 호출 비교
- [ ] [[04-learning/02-deep-dive|심화]] - manual planner-worker-verifier pipeline과 Fugu 비교
- [ ] provider/model opt-out이 가능한 경우 compliance 조건별 품질/비용 변화 측정

### 5단계: 실전 적용

- [ ] [[05-projects|실전 프로젝트]]에서 code review gate, research reproduction, patent landscape benchmark 설계
- [ ] [[cheatsheet|치트시트]]로 평가 지표와 운영 체크리스트 빠르게 참조

---

## 파일 구조

```text
https-sakana-ai-fugu-분석/
├── README.md
├── 01-overview.md
├── 02-ecosystem.md
├── 03-references.md
├── 04-learning/
│   ├── 01-getting-started.md
│   └── 02-deep-dive.md
├── 05-projects.md
└── cheatsheet.md
```

## 바로가기

| 단계 | 파일 | 설명 |
|------|------|------|
| 개요 | [[01-overview]] | What/Why, 특징, 아키텍처 |
| 생태계 | [[02-ecosystem]] | 경쟁/대안 기술 비교 |
| 참고자료 | [[03-references]] | 공식 페이지, technical report, 관련 논문 |
| 시작하기 | [[04-learning/01-getting-started]] | 기본 호출과 평가 harness |
| 심화 | [[04-learning/02-deep-dive]] | orchestration 연구와 manual agents 비교 |
| 프로젝트 | [[05-projects]] | 실전 적용 아이디어 |
| 치트시트 | [[cheatsheet]] | 핵심 개념, 선택 기준, 평가 지표 |

---

## 관련 노트

- [[study/tech/ai/litellm]] - LLM provider gateway/router와 Fugu의 차이 비교
- [[study/tech/ai/agent-orchestration/conductor]] - agent orchestration 연구/도구 맥락
- [[study/tech/ai/multi-agent-platforms/autogen]] - 직접 multi-agent workflow를 설계하는 대안
- [[study/tech/ai/model-context-protocol-mcp]] - agent가 외부 tool/context를 쓰는 integration layer

---

**생성일**: 2026-06-23  
**상태**: 학습 중
