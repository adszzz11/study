---
date: 2026-10-19
tags: [tech]
type: tech-tool-study
status: draft
---

# AI Engineering from Scratch — Cheatsheet

> [[README|목차로 돌아가기]]

## Core Loop

```text
Define success → Build a narrow workflow → Measure → Harden → Deploy → Monitor → Improve
```

## Design Rules

| Do | Avoid |
|---|---|
| deterministic code와 LLM judgment를 분리 | model에게 workflow control 전체 위임 |
| small, typed, validated tool schema | 범용 shell/database 권한 노출 |
| citation과 retrieval eval을 함께 설계 | “vector DB 연결”만으로 RAG 완료 선언 |
| trace에 version·documents·tools·cost 기록 | prompt만 저장하고 재현성 기대 |
| side effect에 approval gate | model output으로 publish/delete/payment 실행 |

## Minimum Metrics

```text
quality = task success + groundedness + tool success
operations = p50/p95 latency + token cost + error rate
safety = blocked unsafe actions + authorization failures + review findings
```

## Pre-deploy Checklist

- [ ] task success와 failure definition이 문서화되어 있는가?
- [ ] normal/edge/adversarial/tool-failure fixture가 있는가?
- [ ] model, prompt, corpus, tool schema version을 trace하는가?
- [ ] retry가 idempotent action에만 적용되는가?
- [ ] credential이 tool별 least privilege로 분리되었는가?
- [ ] destructive action에 user confirmation 또는 human approval이 있는가?
- [ ] PII redaction, retention, access policy가 정해졌는가?

## MCP Reminder

MCP는 context와 tools를 연결하는 protocol이지 trust를 부여하는 mechanism이 아니다. server discovery, tool description, tool output 모두 untrusted input으로 취급하고 permission boundary를 별도로 강제한다.

## Sources

- https://modelcontextprotocol.io/specification/2025-06-18
- https://opentelemetry.io/docs/specs/semconv/gen-ai/
- https://genai.owasp.org/llmrisk/
