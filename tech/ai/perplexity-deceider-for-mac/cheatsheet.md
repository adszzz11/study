---
date: 2026-10-27
tags: [tech]
type: tech-tool-study
status: draft
---

# Perplexity Decider for Mac cheatsheet

## Endpoint and requirements

```text
POST http://127.0.0.1:8080/v1/decisions
model: pplx-decider-flash-v1.2
```

- Apple silicon M1+, macOS 13+, RAM 16 GB, 여유 디스크 약 6 GB
- 첫 실행에서 약 5.8 GB model artifact를 download
- menu bar `Ready (text + images)` 후 호출
- Flash는 **one question per request**를 기본으로 한다.

## Request shape

```json
{
  "model": "pplx-decider-flash-v1.2",
  "state": {"ticket": "I was charged twice."},
  "questions": {
    "route": {
      "type": "choice",
      "instructions": "Which team should handle this ticket?",
      "criteria": {
        "billing": "Charges, refunds, plans, or invoices",
        "technical": "A malfunction or product issue",
        "other": "None of the above"
      }
    }
  }
}
```

## Decision types

| Type | `criteria` | 주요 결과 | 대표 policy |
|---|---|---|---|
| `noul` | 없음 | `P(true)` | `p >= threshold`이면 review/block |
| `choice` | option → 설명 object | choice, option별 probabilities, confidence | top probability가 낮으면 review |
| `score` | 낮음→높음 ordered array | level probabilities, expected score | score/확률로 우선순위 정렬 |

## Design rules

- `choice` option은 상호 배타적으로 쓰고 `other`를 둔다.
- `score` level은 순서와 관찰 조건을 구체적으로 쓴다.
- threshold는 예측값이 아니라 labeled validation의 precision/recall과 error cost로 정한다.
- probability가 높아도 고영향 decision은 human review를 남긴다.
- local Flash와 hosted model 사이에서 threshold를 재사용하지 말고 재검증한다.

## Migration to hosted

```text
local:  http://127.0.0.1:8080/v1/decisions
hosted: https://api.perplexity.ai/v1/decisions
header: Authorization: Bearer <PERPLEXITY_API_KEY>
```

schema는 같지만 data transfer, 비용, model/serving, calibration이 달라진다.

## Sources

- https://docs.perplexity.ai/docs/decisions/decider-for-mac
- https://docs.perplexity.ai/docs/decisions/quickstart
- https://docs.perplexity.ai/api-reference/decisions-post
