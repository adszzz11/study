---
date: 2026-06-23
tags:
  - tech
  - ai
  - fugu
  - sakana-ai
  - learning
type: tech-tool-study
parent: "[[../README]]"
---

# Fugu 시작하기

> [[../03-references|이전: 참고자료]] | [[../README|목차로 돌아가기]] | [[02-deep-dive|다음: 심화]]

---

## 목표

Fugu를 처음 평가할 때의 목표는 "내부 routing을 맞히는 것"이 아니라, 같은 task suite에서 **결과 품질, latency, cost, hallucination rate**가 single model이나 manual agents보다 나은지 측정하는 것이다.

---

## 1. 준비물

| 항목 | 설명 |
|------|------|
| Fugu API key | Sakana 계정에서 발급 |
| OpenAI-compatible client | Python `openai` SDK, curl, existing coding harness |
| Prompt set | coding, reasoning, research 등 반복 가능한 task |
| Evaluator | unit test, rubric, human review, LLM-as-judge 보조 평가 |
| Logging | request id, model, latency, token usage, cost, pass/fail 저장 |

```bash
pip install openai pandas rich
```

```bash
export FUGU_API_KEY="..."
export FUGU_BASE_URL="https://api.example-fugu-compatible/v1"
```

> [!warning]
> `FUGU_BASE_URL`은 예시 placeholder다. 실제 base URL은 Sakana Fugu 공식 페이지 또는 계정 문서에서 확인한다.

---

## 2. 기본 호출

```python
import os
import time
from openai import OpenAI

client = OpenAI(
    api_key=os.environ["FUGU_API_KEY"],
    base_url=os.environ["FUGU_BASE_URL"],
)

messages = [
    {
        "role": "user",
        "content": "You are reviewing a pull request. Find correctness bugs and rank them by severity.",
    }
]

start = time.perf_counter()
response = client.chat.completions.create(
    model="fugu",
    messages=messages,
)
elapsed = time.perf_counter() - start

print(response.choices[0].message.content)
print({"latency_seconds": elapsed, "usage": response.usage})
```

비교할 때는 같은 prompt set으로 최소 세 조건을 실행한다.

| 조건 | 목적 |
|------|------|
| `fugu` | latency/quality 균형형 baseline |
| `fugu-ultra-20260615` | 품질 우선 agent pool |
| single frontier model | orchestration 없이 같은 task를 수행했을 때의 기준 |

---

## 3. 간단한 evaluation harness

```python
import csv
import os
import time
from openai import OpenAI

client = OpenAI(api_key=os.environ["FUGU_API_KEY"], base_url=os.environ["FUGU_BASE_URL"])

TASKS = [
    {
        "id": "review-001",
        "prompt": "Review this diff for logic bugs:\n\n<diff omitted>",
        "expected": "flags missing authorization check",
    },
    {
        "id": "science-001",
        "prompt": "Explain the likely failure mode in this experiment protocol:\n\n<protocol omitted>",
        "expected": "identifies confounding variable",
    },
]

MODELS = ["fugu", "fugu-ultra-20260615"]

with open("fugu_eval.csv", "w", newline="") as f:
    writer = csv.DictWriter(
        f,
        fieldnames=["task_id", "model", "latency_seconds", "tokens", "answer"],
    )
    writer.writeheader()

    for task in TASKS:
        for model in MODELS:
            start = time.perf_counter()
            response = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": task["prompt"]}],
            )
            elapsed = time.perf_counter() - start
            usage = response.usage
            tokens = getattr(usage, "total_tokens", None) if usage else None

            writer.writerow(
                {
                    "task_id": task["id"],
                    "model": model,
                    "latency_seconds": round(elapsed, 3),
                    "tokens": tokens,
                    "answer": response.choices[0].message.content,
                }
            )
```

---

## 4. agentic benchmark 설계

Fugu의 장점은 단순 Q&A보다 multi-step 검증 task에서 드러날 가능성이 크다.

| Benchmark 후보 | 입력 | 평가 |
|----------------|------|------|
| Code review | PR diff, failing test, static analyzer output | 실제 blocking bug 발견률, false positive |
| Paper reproduction | PDF, repo, dataset instruction | missing detail, reproduction gap, runnable checklist |
| Patent landscape | paper/patent 20개 이상 | claim map 정확도, novelty/overlap matrix |
| Security assessment | scope, app docs, logs | evidence quality, retest steps, unsafe recommendation 여부 |
| Long-context analysis | 긴 design doc, incident report | cross-reference recall, contradiction detection |

---

## 5. 결과 관찰 방식

Fugu는 내부 route를 공개하지 않으므로 route tracing 대신 output과 운영 지표를 본다.

| 지표 | 수집 방법 |
|------|-----------|
| Latency | client-side timer, server timing metadata |
| Token usage | API response `usage` field |
| Cost | provider dashboard, invoice export, request tags |
| Pass/fail | deterministic test, expected finding, human rubric |
| Hallucination | citation verification, code compile/test, factual claim check |
| Stability | 같은 task 반복 실행 후 variance 측정 |

```text
minimum useful log row:
task_id, model, timestamp, latency, input_tokens, output_tokens, cost, pass_fail, reviewer_notes
```

---

## 6. Compliance 실습

일반 Fugu는 특정 provider/model opt-out을 지원한다. 민감 데이터나 조달 정책이 있는 조직에서는 opt-out 조건별 품질과 비용 변화를 측정한다.

| 조건 | 측정할 것 |
|------|-----------|
| default pool | 최고 품질/기본 latency |
| provider opt-out | 품질 하락 여부, compliance 만족 여부 |
| restricted model set | cost 증가, hallucination 변화 |
| Fugu Ultra | full agent pool 고정 조건에서 품질 상한 |

---

## 관련 노트

- [[study/tech/ai/litellm]] - 같은 prompt set을 여러 provider/model에 흘리는 gateway 평가
- [[study/tech/ai/model-context-protocol-mcp]] - agentic task가 외부 tool/context를 필요로 할 때의 integration layer
- [[study/tech/ai/autoresearch-study]] - paper reproduction benchmark 설계 참고
