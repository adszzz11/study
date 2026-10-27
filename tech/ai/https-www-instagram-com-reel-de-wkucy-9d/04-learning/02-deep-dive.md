---
date: 2026-10-27
tags: [tech]
type: tech-tool-study
status: draft
---

# Deep dive: reliable agent system

## Reflection with bounded control

generator–critic loop은 최대 반복 횟수와 quality threshold 없이는 비용·latency를 키운다. critic은 자유 텍스트보다 명시적 rubric과 pass/fail reason을 반환하게 한다.

```text
draft → critic(rubric) → pass | revise (max 2) → escalate
```

## State and memory

- `state`: 현재 run의 계획, tool result, retry count처럼 수명과 schema가 명확한 정보
- `memory`: 사용자 선호·장기 context처럼 저장 근거, retention, 삭제 정책이 필요한 정보

둘을 분리하고, sensitive data를 무조건 memory에 넣지 않는다. state transition과 tool call은 traceable해야 한다.

## Human-in-the-Loop and guardrails

이메일 발송, 배포, 결제, DB write는 preview와 approval을 요구한다. approval에는 실행 대상, 변경 내용, 예상 영향, rollback 방법을 포함하고 승인 전에는 side effect를 내지 않는다.

Guardrail은 input/output filtering만이 아니다. 권한 제한, tool allowlist, budget/timeout, PII 처리, audit log를 함께 설계한다.

## Multi-agent expansion

single-agent 평가를 통과한 뒤 coordinator, specialist, evaluator를 분리한다. 각 agent에 역할, 허용 tool, input/output schema, timeout, handoff 기준을 정의한다. agent 수가 품질을 보장하지 않으므로 end-to-end evaluation으로 단순 구조와 비교한다.

## Sources

- https://docs.cloud.google.com/architecture/choose-design-pattern-agentic-ai-system
- https://modelcontextprotocol.io/docs/getting-started/intro
- https://a2a-protocol.org/latest/
