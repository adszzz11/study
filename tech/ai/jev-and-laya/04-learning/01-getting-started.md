---
date: 2026-09-25
tags: [tech]
type: tech-tool-study
status: draft
---

# Jev와 laya Getting Started

> [[../README|목차로 돌아가기]] · [[02-deep-dive|다음: Deep Dive]]

## 학습 목표

- 하나의 support ticket에 `Choice`, `Score`, `Noul` 질문을 만든다.
- Jev HTTP API와 laya `Router` 호출 형태를 비교한다.
- 결과를 즉시 실행하지 않고 offline evaluation 대상으로 저장한다.

## 1. Atomic question부터 설계

“이 고객의 가치가 높은가?”처럼 여러 의미가 섞인 질문 대신 한 질문에 한 판단만 둔다.

| 좋지 않은 질문 | 분해한 질문 |
|---|---|
| 고객이 위험하고 급한가? | `urgency`, `billing_issue`, `churn_risk` |
| 바로 환불할까? | `is_refund_request`, `refund_policy_eligible`, 최종 rule |

```python
ticket = "3일째 결제가 두 번 청구됐습니다. 오늘 환불하지 않으면 해지하겠습니다."

questions = {
    "department": {
        "type": "choice",
        "instructions": "Which department should handle this?",
        "criteria": {
            "billing": "payments, invoices, refunds",
            "technical": "bugs and service errors",
            "sales": "pricing and account questions",
        },
    },
    "frustration": {
        "type": "score",
        "instructions": "How frustrated is the customer?",
        "criteria": ["calm", "frustrated", "very angry"],
    },
    "refund_request": {
        "type": "noul",
        "instructions": "Does the customer ask for a refund?",
    },
}
```

## 2. Jev: HTTP API로 첫 호출

`TYPESAFE_API_KEY`는 dashboard에서 발급하고 secret manager 또는 환경 변수로만 주입한다. 노트·source control에 넣지 않는다.

```bash
curl -X POST https://api.typesafe.ai/v1/systemone \
  -H "Authorization: Bearer $TYPESAFE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "state": "3일째 결제가 두 번 청구됐습니다. 오늘 환불하지 않으면 해지하겠습니다.",
    "model": "jev-latest",
    "questions": {
      "department": {
        "type": "choice",
        "instructions": "Which department should handle this?",
        "criteria": {"billing": "payments and refunds", "technical": "bugs"}
      },
      "refund_request": {
        "type": "noul",
        "instructions": "Does the customer ask for a refund?"
      }
    }
  }'
```

Python SDK 형태는 다음과 같다.

```python
from typesafe_sdk import Choice, Noul, Score, TypeSafeClient

client = TypeSafeClient()  # TYPESAFE_API_KEY 사용
response = client.system_one(
    state=ticket,
    questions={
        "department": Choice(**{k: v for k, v in questions["department"].items() if k != "type"}),
        "frustration": Score(**{k: v for k, v in questions["frustration"].items() if k != "type"}),
        "refund_request": Noul(instructions=questions["refund_request"]["instructions"]),
    },
)
print(response.answers["department"].choice)
```

## 3. laya: local Router로 첫 호출

```bash
python -m pip install laya
```

```python
from laya import Router

router = Router(preload=True)  # 세 checkpoint를 미리 load; 초기 download/메모리를 고려한다.
result = router.predict(ticket, questions)

print(result["answers"]["department"]["choice"])
print(result["answers"]["refund_request"]["noul"])
print(result["routing"]["model"])
```

- HTTP self-host: `python -m pip install "laya[serve]" && laya-serve`
- MCP server: `python -m pip install "laya[mcp]"`
- multilingual·긴 입력은 Router가 고른 checkpoint와 `max_len` 설정을 로그로 남긴다.

## 4. 첫 결과를 검증 데이터로 다루기

최초 호출은 demo이지 automation 승인이 아니다. 과거 ticket을 sample로 삼아 prediction, ground truth, reviewer decision, latency를 기록한다.

| 확인 | 최소 질문 |
|---|---|
| 정확도 | department가 실제 담당 팀과 일치하는가? |
| coverage | 어떤 비율을 자동 처리 후보로 둘 수 있는가? |
| 비용 | false positive가 잘못된 환불/전달로 이어지는가? |
| calibration | 같은 0.85가 실제로 비슷한 정답률을 뜻하는가? |

## 완료 체크리스트

- [ ] atomic question 3개를 만들었다.
- [ ] Choice, Score, Noul을 모두 호출했다.
- [ ] Jev 또는 laya 한 경로에서 결과 schema를 확인했다.
- [ ] secret을 code와 note에 기록하지 않았다.
- [ ] 과거 사례를 이용한 offline eval dataset을 만들었다.

## Sources

- https://docs.typesafe.ai/introduction/quickstart
- https://github.com/NandhaKishorM/laya
- https://pypi.org/project/laya/
