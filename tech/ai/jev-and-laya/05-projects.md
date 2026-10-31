---
date: 2026-09-25
tags: [tech]
type: tech-tool-study
status: draft
---

# Jev와 laya Projects

> [[README|목차로 돌아가기]]

## 1. Support triage

**목표:** inbound email/ticket을 담당 부서, urgency, refund request, sentiment로 나눈 뒤 자동 라우팅 또는 human queue로 보낸다.

- Input: subject, body, customer tier, 기존 ticket summary
- Questions: `department` Choice, `urgency` Score, `refund_request` Noul
- Policy: high-confidence department만 auto-route; refund는 반드시 review
- 평가: routing accuracy, first-response time, misroute rate

## 2. Agent tool gate

**목표:** agent가 side effect를 일으키기 전에 user intent와 risk를 판정한다.

```text
agent proposal → intent Choice + risky Noul
  ├─ low-risk + policy pass → confirmation / execute
  └─ uncertain or risky → approval request
```

`delete`, `refund`, `send message`는 typed decision의 confidence가 높아도 authorization과 confirmation을 우회하지 않는다.

## 3. Security / observability triage

**목표:** alert/event JSON을 severity, owner, escalation 필요 여부로 판단한다.

- `severity`: Score 또는 Choice
- `owner`: Choice
- `needs_escalation`: Noul
- 검증: incident postmortem label과 비교하고, high-severity false negative를 별도 비용으로 보고한다.

## 4. RAG retrieval planner

**목표:** 검색 전 query intent, domain, freshness, tool-call necessity를 typed decision으로 선택한다.

낮은 confidence 또는 복합 query만 larger reasoning model에 넘긴다. retrieval planner가 answer quality를 자동 보장한다는 가정은 피하고, retrieval hit rate·citation correctness까지 평가한다.

## 5. Privacy-sensitive cascade

**목표:** PII가 든 ticket은 laya self-host로 먼저 판정하고, low-risk subset에만 생성형 LLM을 호출한다.

- data flow, retention, access control을 먼저 문서화한다.
- local model도 log·backup·crash report가 PII를 담을 수 있음을 점검한다.
- egress rule은 모델 선택이 아니라 network policy로 강제한다.

## 공통 완료 조건

- [ ] label definition과 reviewer guideline을 문서화했다.
- [ ] held-out data에서 threshold를 선택했다.
- [ ] auto-action과 human queue의 audit log를 남긴다.
- [ ] kill switch와 fallback 경로를 테스트했다.
- [ ] destructive action에 별도 authorization/confirmation을 둔다.

## Sources

- https://docs.typesafe.ai/confidence
- https://github.com/NandhaKishorM/laya
