---
date: 2026-10-19
tags: [tech]
type: tech-tool-study
status: draft
---

# AI Engineering from Scratch — Projects

> [[README|목차로 돌아가기]]

## 1. Evidence-first Knowledge Assistant

공개 문서 50개를 대상으로 citation이 필수인 Q&A API를 만든다.

- Deliverables: ingestion pipeline, hybrid retrieval, answer schema, 30-question eval set
- Success: retrieval recall, citation correctness, faithfulness baseline 기록
- Guardrail: source ACL과 document freshness를 answer generation보다 먼저 검사

## 2. Approval-gated Publishing Workflow

“research → verify → draft → user approval → publish” graph를 구현한다.

- Deliverables: persistent state, resumable job, approval UI/API, audit log
- Success: tool failure 후 재개 가능, approval 없는 publish 0건
- Guardrail: publish tool은 idempotency key와 explicit confirmation을 요구

## 3. Evaluation and Observability Harness

기존 agent/RAG app에 offline regression과 production trace를 더한다.

- Deliverables: golden dataset, CI budget gate, OpenTelemetry-compatible spans, dashboard
- Success: model/prompt 변경 전후 task success·p95 latency·cost 비교
- Guardrail: PII redaction, retention policy, sampling rate 문서화

## 4. MCP Security Lab

read-only 및 side-effecting MCP server를 분리하고 malicious server/tool output을 시험한다.

- Deliverables: scoped OAuth/credential policy, allowlist, sandbox, adversarial fixtures
- Success: data exfiltration·unauthorized write·prompt injection scenario 차단
- Guardrail: trusted server 등록과 destructive action에 human approval 필수

## Sources

- https://modelcontextprotocol.io/specification/2025-06-18
- https://developers.openai.com/api/docs/guides/evals
- https://mlflow.org/docs/latest/genai/
