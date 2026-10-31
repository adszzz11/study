---
date: 2026-09-25
tags: [tech]
type: tech-tool-study
status: draft
---

# Jev와 laya Cheatsheet

> [[README|목차로 돌아가기]]

## 핵심 구분

| 개념 | 의미 |
|---|---|
| state | 판단할 text 또는 context |
| atomic question | 한 개의 독립 판단 |
| Choice | 후보 중 하나 선택 |
| Score | ordered level 선택 |
| Noul | yes/no probability |
| confidence | Jev Choice/Score probability 분포의 집중도 요약 |

## Jev

```bash
curl -X POST https://api.typesafe.ai/v1/systemone \
  -H "Authorization: Bearer $TYPESAFE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"state":"ticket text","model":"jev-latest","questions":{}}'
```

```python
from typesafe_sdk import Choice, Noul, Score, TypeSafeClient

response = TypeSafeClient().system_one(state="ticket", questions={
    "owner": Choice(instructions="Choose owner", criteria={"billing": "payment"}),
    "urgent": Noul(instructions="Is this urgent?"),
})
```

- API key: `TYPESAFE_API_KEY`
- `Choice`/`Score`: answer + probabilities + `confidence`
- `Noul`: yes probability; confidence field로 가정하지 않는다.

## laya

```bash
python -m pip install laya
python -m pip install "laya[serve]"  # HTTP server
python -m pip install "laya[mcp]"    # MCP server
```

```python
from laya import Router

router = Router(preload=True)
result = router.predict("ticket", {
    "owner": {"type": "choice", "instructions": "Choose owner",
              "criteria": {"billing": "payment"}},
    "urgent": {"type": "noul", "instructions": "Is this urgent?"},
})
```

## Production gate

```text
1. offline held-out evaluation
2. calibration + risk-based threshold
3. low-risk auto-action only
4. review queue / human escalation
5. audit log + kill switch
```

## 반드시 확인

- [ ] 질문 하나에 판단 하나만 있는가?
- [ ] 50+ option, negation, language, long input을 별도 평가했는가?
- [ ] probability가 calibration된 실제 domain 수치인가?
- [ ] side effect에 authorization·confirmation·idempotency가 있는가?
- [ ] Jev API/SDK 또는 laya package version을 pin·기록했는가?

## Sources

- https://docs.typesafe.ai/introduction/quickstart
- https://docs.typesafe.ai/confidence
- https://github.com/NandhaKishorM/laya
