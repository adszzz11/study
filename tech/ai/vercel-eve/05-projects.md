---
date: 2026-10-19
tags: [tech]
type: tech-tool-study
status: draft
---

# Vercel eve — Projects

> [[README|목차로 돌아가기]]

## 1. Customer Support Agent

Slack/Web Chat에서 ticket을 분류하고 승인된 knowledge base를 조회하는 agent를 만든다.

| 구성 | 설계 |
|---|---|
| Channels | Slack, Web Chat |
| Read tools | ticket 조회, knowledge search |
| Write tools | CRM update, refund, account change |
| Guardrail | write tool은 approval, idempotency key, audit record |
| Eval | 분류 정확도, citation fidelity, escalation 정확도, 중복 mutation 방지 |

**완료 기준**: refund·account change 요청은 승인 없이 실행되지 않고, 승인 대기 뒤에도 같은 session이 안전하게 resume한다.

## 2. Data Analyst Agent

자연어 질문을 분석 계획과 SQL 후보로 변환하고 sandbox에서 데이터를 분석한다. schema 설명과 sample data는 읽기 전용 connection으로 제공하며, 비용이 큰 query와 모든 write query는 approval 대상으로 둔다.

```text
question → plan → read-only SQL → sandbox analysis → cited result
                     │
                     └→ expensive/write query → approval → execute
```

**완료 기준**: SQL allowlist·row/scan limit·timeout을 적용하고, 결과가 query와 data source를 함께 제시하며, mutation은 human approval 없이는 실행되지 않는다.

## 3. Release Notes Triage Agent

eve release history와 팀의 pinned version을 비교해 upgrade 후보를 요약하는 scheduled agent를 만든다. 외부 release text는 data로 취급하고, breaking change가 의심되면 PR 생성 대신 review issue 초안을 준비한다.

**완료 기준**: 정해진 schedule에서 변경 근거 URL, 영향 범위, eval 실행 필요성을 남기고 배포 변경은 사람이 승인한다.

## Sources

- https://eve.dev/
- https://github.com/vercel/eve/releases
- https://github.com/vercel/eve/blob/main/docs/concepts/execution-model-and-durability.mdx
