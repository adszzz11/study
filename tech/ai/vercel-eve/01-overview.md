---
date: 2026-10-19
tags: [tech]
type: tech-tool-study
status: draft
---

# Vercel eve — Overview

> [[README|목차로 돌아가기]]

## What

Vercel eve는 directory 하나를 agent로 취급하는 open-source TypeScript framework다. 최소 구성은 `agent/instructions.md`이며, 필요에 따라 `tools/`, `skills/`, `connections/`, `channels/`, `subagents/`, `schedules/`, `evals/`를 추가한다. Markdown은 identity와 policy를, TypeScript file은 동작을 표현하므로 Git diff와 code review에 잘 맞는다.

## Why

Production agent에는 model call 외에도 retry/resume, 안전한 tool execution, credential 보호, 사람의 승인, channel integration, 관찰성과 regression eval이 필요하다. 이를 application마다 조립하면 policy와 운영 방식이 흩어진다. eve는 이 plumbing을 framework runtime에 넣어 개발자가 agent의 역할·도구·권한에 집중하도록 한다.

## Key Characteristics

| 특징 | 의미 | 설계 시 주의점 |
|---|---|---|
| Filesystem-first | agent 정의를 directory와 source file로 관리 | instruction도 code처럼 review한다 |
| Durable execution | step checkpoint 후 crash·timeout·deployment 뒤 resume | non-idempotent tool은 retry될 수 있다 |
| Isolated Sandbox | shell/file/code execution을 session별로 격리 | sandbox에 provider key를 직접 넣지 않는다 |
| Human approval | 위험한 tool 직전 session을 park하고 승인 후 재개 | refund, delete, publish, DB write에 적용한다 |
| Skills / subagents | procedure 추가와 별도 child agent를 구분 | subagent에는 least privilege를 적용한다 |
| Channels / evals | Web·API·Slack 등 channel과 session 기반 평가 지원 | release gate는 representative eval로 만든다 |

## Execution Boundary

```text
User / Channel
      │
      ▼
App runtime ── model call · credential · connection client · tool executor
      │
      ├── durable workflow checkpoint / park / resume
      │
      ▼
Session sandbox ── bash · files · code execution
```

`approval`, OAuth, user input을 기다리는 workflow는 compute를 점유하지 않고 park된다. 반대로 중간에 끊긴 side-effect tool은 재시도될 가능성이 있으므로 API idempotency key, 상태 조회, approval gate를 조합해야 한다.

## Sources

- https://vercel.com/blog/introducing-eve
- https://github.com/vercel/eve/blob/main/docs/concepts/execution-model-and-durability.mdx
- https://vercel.com/kb/guide/how-to-use-eve-subagents
