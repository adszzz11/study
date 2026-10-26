---
date: 2026-10-27
tags: [tech]
type: tech-tool-study
status: draft
---

# Getting started

## 1. 설치 전 확인

- Apple silicon M1 이상, macOS 13 이상, RAM 16 GB, 여유 디스크 약 6 GB를 준비한다.
- [공식 문서](https://docs.perplexity.ai/docs/decisions/decider-for-mac)에서 `Decider.dmg`를 내려받아 Applications로 옮긴다.
- 첫 실행 시 model download가 끝날 때까지 기다린다. menu bar에 `Ready (text + images)`가 표시되는지 확인한다.

model download에는 network가 필요하지만, 준비가 끝난 뒤 request의 `state`는 local endpoint에서 처리된다.

## 2. 첫 `choice` request

질문 하나만 넣어 support ticket의 담당 팀을 선택하게 한다.

```bash
curl -sS http://127.0.0.1:8080/v1/decisions \
  -H 'Content-Type: application/json' \
  -d '{
    "model": "pplx-decider-flash-v1.2",
    "state": "I was charged twice for my order last week.",
    "questions": {
      "route": {
        "type": "choice",
        "instructions": "Which team should handle this message?",
        "criteria": {
          "billing": "Charges, refunds, plans, or invoices",
          "shipping": "Delivery, tracking, or damaged shipment",
          "technical": "A product or service malfunction",
          "other": "None of the above"
        }
      }
    }
  }'
```

응답의 `answers.route`에서 최고 `choice`, option별 `probabilities`, `confidence`를 확인한다. application code는 label 문자열만 믿지 말고 confidence/probability policy도 함께 기록한다.

## 3. `noul`로 review queue 만들기

민감 정보 여부처럼 false negative 비용이 큰 문제는 보수적으로 시작한다.

```json
{
  "type": "noul",
  "instructions": "Does this text contain a password, API token, or other secret?"
}
```

예를 들어 `P(true) >= 0.2`이면 block 또는 human review queue로 보낼 수 있다. `0.2`는 예시일 뿐이며, labeled sample의 precision, recall, false-negative cost로 정해야 한다. 이것은 CI secret scanner를 대체하는 장치가 아니라 보조 방어선이다.

## 4. 다음 실험

1. `score`로 urgency level을 세 단계 이상 정의한다.
2. 각 label의 예시와 반례를 포함한 작은 labeled set을 만든다.
3. probability와 실제 label을 비교해 threshold를 고정한다.
4. 질문을 여러 개 묶지 말고 Flash에서는 request당 한 question을 기본으로 한다.

## Sources

- https://docs.perplexity.ai/docs/decisions/decider-for-mac
- https://docs.perplexity.ai/docs/decisions/quickstart
