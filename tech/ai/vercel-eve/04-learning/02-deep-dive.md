---
date: 2026-10-19
tags: [tech]
type: tech-tool-study
status: draft
---

# Vercel eve — Deep Dive

> [[../README|목차로 돌아가기]] | [[01-getting-started|이전: 시작하기]]

## Durable Execution

각 workflow step은 checkpoint된다. deployment, crash, timeout 뒤 이미 끝난 step을 다시 실행하지 않고 마지막 checkpoint부터 resume하는지 검증한다. 하지만 실행 중 끊긴 non-idempotent tool은 retry될 수 있다.

```text
read state → prepare action → approval → write action → record outcome
                    │             │
                    │             └─ park / human decision / resume
                    └─ checkpoint
```

write action에는 idempotency key를 전달하고, 재개 시 external state를 조회해 중복 실행을 막는다. payment, email, publish, delete, database mutation은 approval 대상 후보로 본다.

## Sandbox and Credentials

App runtime에는 model call, credentials, connection client, tool executor가 남는다. `bash`, file manipulation, code execution은 isolated session sandbox에서 실행된다. provider credential을 sandbox에 직접 주입하지 말고 app-side credential brokering과 scope가 좁은 connection을 사용한다.

## Skills vs Subagents

| 구분 | Skill | Subagent |
|---|---|---|
| 목적 | 현재 agent에 procedure/instruction 추가 | 전문 업무를 별도 agent에 위임 |
| Context | 현재 context 공유 | fresh context |
| Tools/Sandbox | parent 환경 | 독립 tool set·sandbox |
| 사용 예 | 문서 작성 규칙 | SQL 분석 specialist, security review specialist |

Subagent는 병렬화 수단이기도 하지만 권한 분리 수단이다. parent가 모든 credential을 넘기지 말고, child task에 필요한 tool만 제공한다.

## Evals and Deployment

1. 정상·경계·실패·prompt injection 사례를 포함한 representative prompt를 고른다.
2. 실제 session을 실행해 task success, citation quality, safety violation, latency, cost를 score한다.
3. pinned version에서 baseline을 저장한다.
4. upgrade와 deployment 전에 동일 eval을 돌리고, threshold 미달이면 staged rollout을 멈춘다.

운영 환경은 Vercel managed path 또는 self-hosted Postgres + Docker sandbox 중 선택한다. 전자는 OIDC와 managed integration 결합이 자연스럽고, 후자는 runtime 구성과 운영 책임이 더 크다.

## Sources

- https://github.com/vercel/eve/blob/main/docs/concepts/execution-model-and-durability.mdx
- https://vercel.com/kb/guide/how-to-use-eve-subagents
- https://github.com/vercel/eve/blob/main/docs/guides/deployment/vercel.mdx
- https://github.com/vercel/eve/blob/main/docs/guides/deployment/self-hosting.md
