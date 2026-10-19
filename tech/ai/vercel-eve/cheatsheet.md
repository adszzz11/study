---
date: 2026-10-19
tags: [tech]
type: tech-tool-study
status: draft
---

# Vercel eve — Cheatsheet

> [[README|목차로 돌아가기]]

## Snapshot

| 항목 | 내용 |
|---|---|
| Provider | Vercel |
| Status | public preview |
| Language | TypeScript |
| Authoring model | filesystem-first: agent = directory |
| Runtime | durable workflow with checkpoints and resume |
| Isolation | app runtime credentials + session sandbox execution |
| Deployment | Vercel managed path 또는 self-hosted Postgres + Docker sandbox |

## Directory Vocabulary

```text
agent/
├── instructions.md  # identity, policy, response rules
├── tools/           # TypeScript tool behavior
├── skills/          # current agent procedure/instructions
├── connections/     # MCP/OpenAPI 등 external integration
├── channels/        # Web, API, Slack 등 entry point
├── subagents/       # fresh context·별도 권한의 child agent
├── schedules/       # scheduled job
└── evals/           # session-based regression evaluation
```

## Safety Rules

- `write`, `delete`, `send`, `refund`, `publish`는 approval 후보로 분류한다.
- non-idempotent external action에는 idempotency key와 resume 시 상태 조회를 둔다.
- provider key와 privileged credential을 sandbox에 직접 주입하지 않는다.
- tool input/output과 web content는 untrusted data로 다루고 schema·allowlist를 적용한다.
- subagent에는 parent의 모든 권한 대신 task별 최소 tool set을 준다.
- upgrade 전후에는 pinned version과 동일 eval set의 결과를 비교한다.

## Decision Rule

```text
Production readiness = task success + evidence quality + safety
                     + latency/cost + human-review efficiency
```

## Sources

- https://vercel.com/blog/introducing-eve
- https://eve.dev/
- https://github.com/vercel/eve/blob/main/docs/concepts/execution-model-and-durability.mdx
