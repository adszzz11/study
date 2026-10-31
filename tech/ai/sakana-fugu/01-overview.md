---
date: 2026-06-23
tags:
  - tech
  - ai
  - fugu
  - sakana-ai
  - multi-agent
  - overview
type: tech-tool-study
parent: "[[README]]"
---

# Sakana Fugu - 개요

> [[README|목차로 돌아가기]] | [[02-ecosystem|다음: 생태계]]

---

## 1. What - Fugu란?

> **한 줄 정의**: Sakana Fugu는 여러 frontier LLM/agent를 하나의 OpenAI-compatible API 뒤에서 동적으로 조율하는 "multi-agent system as a model" 제품이다.

Fugu는 단일 model endpoint처럼 보이지만 내부적으로는 여러 expert agents를 조합하는 orchestrator model 계열 제품이다. 사용자는 `fugu` 또는 `fugu-ultra-20260615` 같은 model name을 호출하고, Fugu는 task 성격에 맞춰 model selection, switching, coordination을 처리한다.

```text
User / App
  -> OpenAI-compatible API
      -> Fugu / Fugu Ultra
          -> Learned Orchestrator
              -> Expert LLMs / Agents
                  -> Combined Answer
```

Sakana의 technical report는 Fugu를 "orchestrator models" 제품군으로 설명하며, Fugu와 Fugu-Ultra 두 모델을 공개했다고 밝힌다.

---

## 2. Why - 왜 필요한가?

### 배경

LLM 성능은 provider별로 강점이 다르게 분화되고 있다.

| 작업 영역 | 흔한 차이 |
|-----------|----------|
| Coding | bug localization, patch generation, test repair 성능 차이 |
| Reasoning | long-chain reasoning, math, planning 안정성 차이 |
| Science | 논문 이해, 실험 설계, domain knowledge 차이 |
| Long-context | 긴 문서 검색, cross-reference, context retention 차이 |
| Tool-use | function calling, shell/tool execution, state tracking 차이 |

문제는 사용자가 매번 다음 결정을 직접 내려야 한다는 점이다.

- 어떤 model을 언제 호출할지 정해야 한다.
- planner, worker, verifier 같은 agent role을 직접 설계해야 한다.
- 비용(cost)과 지연(latency)을 어디까지 허용할지 정해야 한다.
- provider별 privacy/compliance 조건을 반영해야 한다.
- multi-step task의 실패 지점을 관찰하고 재시도 정책을 만들어야 한다.

### Fugu의 핵심 가설

Fugu의 가설은 **단일 거대 모델을 계속 키우는 대신, 여러 모델의 specialization을 runtime에서 조합하면 복잡한 multi-step task에서 더 좋은 cost-performance를 낼 수 있다**는 것이다.

이 관점에서 Fugu는 model router보다 넓고, agent framework보다 managed service에 가깝다.

| 구분 | 설명 |
|------|------|
| Model router | strong/weak model 선택이나 provider routing 중심 |
| Agent framework | 개발자가 graph, role, memory, tool use를 직접 설계 |
| Fugu | orchestration 자체를 API/model 상품으로 제공 |

---

## 3. 핵심 특징

### One API abstraction

Fugu는 OpenAI-compatible API를 제공해 기존 client, coding harness, evaluation script의 전환 비용을 낮춘다. 앱 입장에서는 model 이름과 endpoint만 바꾸고 같은 chat/completions 스타일로 시작할 수 있다.

```python
from openai import OpenAI

client = OpenAI(api_key="...", base_url="https://...")

response = client.chat.completions.create(
    model="fugu",
    messages=[{"role": "user", "content": "Solve and verify this bug."}],
)
```

### Fugu vs Fugu Ultra

| 모델 | 성격 | 적합한 작업 |
|------|------|-------------|
| Fugu | latency와 품질의 균형형 | 일반 coding, review, analysis, agentic task |
| Fugu Ultra | 더 많은 expert agents를 동원해 품질 우선 | 어려운 reasoning, research, coding, long-running analysis |

Fugu Ultra는 더 강한 결과를 목표로 하지만 full agent pool이 고정되어 있고, 일반 Fugu처럼 provider/model opt-out을 유연하게 쓰는 방식은 아니다.

### Controllable agent pool

일반 Fugu는 특정 provider/model opt-out을 지원해 privacy, compliance, procurement 요구를 맞출 수 있다. 예를 들어 특정 vendor 사용을 금지하거나, 특정 jurisdiction 정책에 맞춰 agent pool을 제한하는 평가가 가능하다.

```text
Evaluation condition A: full default Fugu pool
Evaluation condition B: provider X opt-out
Evaluation condition C: sensitive-data policy with restricted models
```

### 결과 중심 평가

Fugu는 내부 route와 model 사용 내역을 상세 공개하지 않는다. 따라서 운영자는 "어떤 model이 언제 불렸는가"보다 다음 지표를 중심으로 평가해야 한다.

| 지표 | 설명 |
|------|------|
| Latency | end-to-end 응답 시간, streaming 시작 시간 |
| Cost | request별 비용, token usage, subscription/pay-as-you-go 영향 |
| Pass/fail | benchmark 또는 사내 task suite 성공률 |
| Hallucination rate | citation, code, claim의 검증 실패율 |
| Repair rate | review 지적 후 실제 patch/test 통과 비율 |
| Compliance impact | opt-out 조건별 품질/비용 변화 |

---

## 4. 기반 연구

### TRINITY

TRINITY는 compact coordinator가 여러 LLM에 Thinker, Worker, Verifier 역할을 배정하는 연구다.

| 요소 | 설명 |
|------|------|
| Coordinator | 0.6B급 SLM hidden state 기반 compact coordinator |
| Learnable head | 20K 미만 learnable parameter head |
| Optimization | sep-CMA-ES로 coordination policy 최적화 |
| Role | Thinker, Worker, Verifier 역할 배정 |

Fugu를 이해할 때 TRINITY는 "작은 coordinator가 큰 expert model들을 어떻게 배정할 수 있는가"라는 관점을 준다.

### Conductor

Conductor는 7B model이 RL/GRPO로 natural-language workflow를 생성하고, worker model별 subtask, access list, communication topology를 설계하는 연구다.

| 요소 | 설명 |
|------|------|
| Conductor | 7B orchestration model |
| Training | RL/GRPO 기반 workflow optimization |
| Output | natural-language workflow, subtask assignment, access list |
| Topology | randomized agent pool, recursive topology, test-time scaling |

Conductor는 Fugu식 managed orchestration이 단순 routing을 넘어 workflow design 문제라는 점을 보여준다.

---

## 5. 벤치마크 주장과 해석

Sakana 공식 페이지는 Fugu/Fugu Ultra가 다음 benchmark에서 공개 frontier baselines와 경쟁한다고 제시한다.

| Benchmark | 성격 |
|-----------|------|
| SWE Bench Pro | software engineering, bug fix, patch 평가 |
| TerminalBench | terminal-based agent task |
| LiveCodeBench | coding problem 평가 |
| GPQA-D | graduate-level science reasoning |
| Humanity's Last Exam | broad hard reasoning benchmark |
| CharXiv Reasoning | chart/figure reasoning |

주의할 점은 일부 baseline이 provider-reported score이고, 내부 routing/model 사용 내역은 공개되지 않는다는 것이다. 따라서 benchmark claim은 방향성 근거로 보되, 실제 도입 전에는 자체 task suite로 재평가해야 한다.

---

## 6. 장점과 한계

| 장점 | 설명 |
|------|------|
| 낮은 전환 비용 | OpenAI-compatible API로 기존 client/harness 재사용 |
| 자동 orchestration | model selection, role coordination을 서비스가 담당 |
| multi-step task 적합성 | coding, research, verification task에서 강점 기대 |
| compliance 옵션 | 일반 Fugu의 provider/model opt-out 지원 |

| 한계 | 설명 |
|------|------|
| 내부 route 비공개 | 디버깅과 provider 사용 감사가 제한적 |
| vendor trust 필요 | orchestration 품질과 benchmark 해석을 provider에 의존 |
| 비용 예측 난이도 | agent pool과 test-time scaling 때문에 request별 비용 변동 가능 |
| latency trade-off | Ultra처럼 품질 우선 모델은 응답 시간이 길어질 수 있음 |

---

## 관련 노트

- [[study/tech/ai/litellm]] - provider gateway/router와 managed orchestration 비교
- [[study/tech/ai/agent-orchestration/conductor]] - orchestration model 연구 맥락
- [[study/tech/ai/multi-agent-platforms/autogen]] - 직접 agent role/workflow를 설계하는 대안

---

## References

- [Sakana Fugu 공식 페이지](https://sakana.ai/fugu/)
- [Sakana Fugu Technical Report](https://arxiv.org/abs/2606.21228)
- [TRINITY: An Evolved LLM Coordinator](https://ar5iv.labs.arxiv.org/html/2512.04695)
- [Learning to Orchestrate Agents in Natural Language with the Conductor](https://ar5iv.labs.arxiv.org/html/2512.04388)
