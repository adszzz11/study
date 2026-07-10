---
date: 2026-06-23
tags:
  - tech
  - ai
  - fugu
  - sakana-ai
  - cheatsheet
type: tech-tool-study
parent: "[[README]]"
---

# Sakana Fugu 치트시트

> [[05-projects|이전: 프로젝트]] | [[README|목차로 돌아가기]]

---

## 핵심 요약

| 항목 | 내용 |
|------|------|
| 제품 유형 | managed multi-agent model API |
| API 형태 | OpenAI-compatible API |
| 핵심 가치 | model/agent orchestration을 사용자가 직접 설계하지 않아도 됨 |
| 대표 모델 | `fugu`, `fugu-ultra-20260615` |
| 적합 작업 | coding, code review, scientific reasoning, paper reproduction, patent research, long-running autonomous analysis |

---

## Fugu vs Fugu Ultra

| 모델 | 선택 기준 | 주의점 |
|------|-----------|--------|
| `fugu` | latency와 품질 균형, provider/model opt-out 필요 | Ultra보다 품질 상한은 낮을 수 있음 |
| `fugu-ultra-20260615` | 어려운 reasoning/research/coding task에서 품질 우선 | 더 많은 expert agents, full agent pool 고정, latency/cost 증가 가능 |

---

## 기본 호출 패턴

```python
from openai import OpenAI

client = OpenAI(
    api_key="...",
    base_url="https://api.example-fugu-compatible/v1",
)

response = client.chat.completions.create(
    model="fugu",
    messages=[
        {"role": "user", "content": "Analyze this bug report and propose a verified fix."}
    ],
)

print(response.choices[0].message.content)
print(response.usage)
```

---

## 평가 지표

| 지표 | 봐야 하는 이유 |
|------|----------------|
| `latency_seconds` | interactive workflow 가능 여부 |
| `input_tokens`, `output_tokens` | cost driver |
| `cost_per_success` | 단순 비용보다 중요한 조달 지표 |
| `pass_fail` | deterministic benchmark 성공 여부 |
| `critical_finding_recall` | code/security/research에서 중요한 issue를 놓치지 않는지 |
| `hallucination_rate` | citation, code, factual claim 검증 실패율 |
| `variance` | 같은 task 반복 시 안정성 |

```text
task_id, model, latency_seconds, input_tokens, output_tokens, cost, pass_fail, hallucination, notes
```

---

## 비교 대상

| 비교 대상 | 핵심 질문 |
|-----------|-----------|
| Single frontier model | orchestration 없이도 충분한가? |
| [[study/tech/ai/litellm]] / OpenRouter | routing/gateway만으로 충분한가? |
| RouteLLM | strong/weak routing으로 비용을 줄일 수 있는가? |
| Mixture-of-Agents | layered multi-agent composition이 필요한가? |
| MASRouter | role/collaboration routing 연구와 무엇이 다른가? |
| [[study/tech/ai/multi-agent-platforms/autogen]] / LangGraph | 직접 orchestration을 소유할 가치가 있는가? |

---

## 도입 패턴

### Primary model

```text
App -> Fugu -> evaluator -> human review
```

빠르게 시작할 수 있지만 내부 route 디버깅은 제한적이다.

### Hard-case escalator

```text
Single model -> failure/low confidence -> Fugu Ultra -> verifier
```

비용을 제어하면서 어려운 case에 품질 우선 orchestration을 쓴다.

### Independent reviewer

```text
Primary output -> Fugu review -> tests/static analyzer -> human approval
```

code review, security review, research claim checking에 유용하다.

---

## 운영 체크리스트

- [ ] 같은 prompt set으로 `fugu`, `fugu-ultra-20260615`, single model을 비교한다.
- [ ] token usage, latency, pass/fail, hallucination rate를 request별로 저장한다.
- [ ] 내부 route를 볼 수 없다는 점을 vendor risk로 기록한다.
- [ ] provider/model opt-out 조건에서 품질과 비용 변화를 측정한다.
- [ ] Ultra는 full agent pool 고정이라는 제약을 compliance 검토에 반영한다.
- [ ] benchmark claim은 자체 private task suite로 재검증한다.
- [ ] deterministic verifier(test, linter, citation checker)를 붙인다.

---

## 한 줄 판단

| 상황 | 판단 |
|------|------|
| 복잡한 multi-step task가 많고 agent pipeline을 직접 유지하기 어렵다 | Fugu 평가 가치 높음 |
| route 감사, provider별 사용 기록, 재현성이 최우선이다 | manual agents 또는 gateway 중심 접근 검토 |
| 단순 chat/completion이 대부분이다 | single frontier model이 더 단순 |
| 어려운 task에만 품질 상한이 필요하다 | Fugu Ultra를 escalator로 사용 |

---

## 관련 노트

- [[study/tech/ai/agent-orchestration/conductor]] - workflow orchestration 연구 맥락
- [[study/tech/ai/model-context-protocol-mcp]] - agent tool/context integration
- [[study/tech/ai/autoresearch-study]] - research automation 적용 사례
