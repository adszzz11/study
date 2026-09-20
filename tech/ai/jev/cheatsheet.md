---
date: 2026-09-20
tags: [tech]
type: tech-tool-study
status: draft
---

# Jev Cheatsheet

> [[README|목차로 돌아가기]]

## Core

| 항목 | 값 / 원칙 |
|---|---|
| API endpoint | `POST https://api.typesafe.ai/v1/systemone` |
| Model | `jev-latest`(최신) 또는 pin한 version(재현성) |
| Input | `state` (text/JSON) + `questions` |
| Execution | 같은 state에 대한 questions는 독립 병렬 평가 |
| Choice | 비순서 option, probabilities, confidence |
| Score | 순서 rubric, distribution, confidence |
| Noul | yes/no probability `0..1`; 별도 confidence 없음 |

## Question checklist

- [ ] question은 atomic인가?
- [ ] Choice에 `other`/`none`이 있는가?
- [ ] option과 rubric이 domain language로 명확한가?
- [ ] output이 action을 직접 실행하지 않고 policy code를 거치는가?
- [ ] model/version·question schema·result를 observability data로 남기는가?

## Policy pattern

```text
high confidence + low impact  → auto-act
medium confidence             → confirm / review
low confidence or high impact → stop / fallback / human approval
```

## Security

- API key는 server-side environment 또는 secret manager에만 저장한다.
- allowlist, authorization, idempotency는 model 결과와 독립적으로 재검증한다.
- timeout/error에는 safe fallback을 정한다.
- latency·price·quality는 vendor claim이 아니라 own workload에서 측정한다.

## Sources

- https://docs.typesafe.ai/introduction/quickstart
- https://docs.typesafe.ai/primitives
- https://docs.typesafe.ai/confidence
