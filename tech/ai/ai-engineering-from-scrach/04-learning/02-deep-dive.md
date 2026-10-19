---
date: 2026-10-19
tags: [tech]
type: tech-tool-study
status: draft
---

# AI Engineering from Scratch — Deep Dive

> [[README|목차로 돌아가기]]

## 1. Workflow as a State Machine

“검색 → 문서 검증 → 초안 생성 → 사용자 승인 → publish”를 graph로 모델링한다. 검색과 validation은 deterministic code로, ambiguity 해소와 draft 생성은 LLM으로 맡긴다. 각 state에 persistence, retry policy, maximum step, terminal failure를 둔다.

## 2. Evaluation-first Delivery

| Signal | 측정 질문 |
|---|---|
| Task success | 사용자가 목표를 달성했는가? |
| Groundedness | answer가 retrieved evidence로 지지되는가? |
| Tool success | 올바른 tool·parameter·순서였는가? |
| Safety | injection·권한 우회·unsafe action을 거부했는가? |
| Operations | latency와 token cost가 budget 안인가? |

golden dataset에는 정상 사례, edge case, adversarial prompt, tool failure fixture를 함께 둔다. LLM-as-a-judge는 scale에는 유용하지만 human-labeled sample과 calibration하지 않으면 단독 quality gate가 될 수 없다.

## 3. Production Hardening

- request ID와 trace context를 API, queue, tool call까지 전달한다.
- retry는 idempotent action에만 적용하고 exponential backoff·circuit breaker를 사용한다.
- rate limit, per-user authorization, secrets manager, audit event를 기본으로 둔다.
- prompt version, retrieved document ID, tool argument/result, token/cost, policy decision, user feedback을 trace한다.

## 4. Security Drill

malicious retrieved document와 malicious tool output을 fixture로 만들어 다음을 시험한다.

- system instruction 무시를 유도하는 indirect prompt injection
- user authorization 밖의 data exfiltration
- payment, deletion, publish 같은 destructive tool call
- tool output이 만든 unvalidated URL·SQL·shell argument

성공 조건은 “모델이 위험 문구를 알아챘다”가 아니라, policy layer가 data boundary·credential scope·approval gate로 실제 action을 막는 것이다.

## Sources

- https://docs.langchain.com/oss/python/langgraph/overview
- https://opentelemetry.io/docs/specs/semconv/gen-ai/
- https://genai.owasp.org/llmrisk/
