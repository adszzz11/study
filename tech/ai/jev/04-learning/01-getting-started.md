---
date: 2026-09-20
tags: [tech]
type: tech-tool-study
status: draft
---

# Jev Getting Started

> [[../README|목차로 돌아가기]] · [[02-deep-dive|다음: Deep Dive]]

## 학습 목표

- support ticket 하나에 `is_urgent`, `department`, `frustration`을 함께 평가한다.
- Choice의 `other`와 confidence 기반 review policy를 이해한다.
- API key를 server-side environment에서만 취급한다.

## 1. SDK 설치와 credential

```bash
# Python
pip install typesafe-sdk

# JavaScript / TypeScript
npm install @typesafe-ai/sdk
```

`TYPESAFE_API_KEY`는 server-side environment 또는 secret manager에만 둔다. browser bundle, repository, 이 노트의 code block에 실제 key를 넣지 않는다.

## 2. Playground에서 먼저 관찰

support ticket을 `state`로 넣고 다음 질문을 한 request에서 실행한다.

| question | primitive | 설정 예 |
|---|---|---|
| `is_urgent` | Noul | “이 ticket은 즉시 대응이 필요한가?” |
| `department` | Choice | billing, technical, account, other |
| `frustration` | Score | low, medium, high |

같은 state의 question들은 독립적으로 병렬 평가된다. 결과 값뿐 아니라 distribution과 confidence를 기록해 사람이 납득하는지 확인한다.

## 3. REST request 형태

직접 endpoint는 `POST https://api.typesafe.ai/v1/systemone`이다. 최신 동작을 따를 때는 `jev-latest` alias를, 재현 가능한 production rollout에는 pin한 model version을 사용한다. 정확한 request schema는 설치한 SDK version의 Quick Start를 기준으로 확인한다.

```bash
curl https://api.typesafe.ai/v1/systemone \
  -H "Authorization: Bearer $TYPESAFE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "jev-latest",
    "state": "Customer: I was charged twice and nobody has replied for 3 days.",
    "questions": [
      {"name": "is_urgent", "type": "noul", "question": "Does this require immediate attention?"},
      {"name": "department", "type": "choice", "options": ["billing", "technical", "account", "other"]},
      {"name": "frustration", "type": "score", "levels": ["low", "medium", "high"]}
    ]
  }'
```

> [!NOTE]
> 위 payload는 primitive 역할을 설명하는 학습용 skeleton이다. field 이름과 nested schema는 SDK/공식 Quick Start의 현재 version과 대조한 뒤 실행한다.

## 4. 첫 policy

```python
if department.confidence >= 0.90 and is_urgent.probability < 0.20:
    enqueue(department.value)
elif department.confidence >= 0.70:
    request_confirmation()
else:
    send_to_human_review()
```

이 예시는 threshold 출발점일 뿐이다. `0.90`이 안전하다는 뜻은 아니며, labeled historical tickets에서 auto-route의 error rate와 review volume을 함께 측정한다.

## Sources

- https://docs.typesafe.ai/introduction/quickstart
- https://github.com/typesafe-ai/typesafe-sdk-python
- https://github.com/typesafe-ai/typesafe-sdk-js
