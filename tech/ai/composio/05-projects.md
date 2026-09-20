---
date: 2026-07-19
tags: [tech]
type: tech-tool-study
status: draft
---

# Composio — Projects

> [[04-learning/02-deep-dive|이전: Deep Dive]] · [[README|목차]] · [[cheatsheet|다음: Cheatsheet]]

## Project 1. Read-only Personal Inbox Assistant

Gmail에서 최근 메일을 조회하고 local summary만 만드는 최소 project다.

| 항목 | 내용 |
|---|---|
| 목표 | Session, user auth, discovery 흐름 검증 |
| 허용 | message list/read |
| 금지 | send, delete, label change |
| 성공 기준 | 두 test user의 result/log/account가 완전히 분리됨 |

단계:

- [ ] immutable `user_id` mapping
- [ ] Gmail toolkit과 read-only tool allowlist
- [ ] Connect Link와 callback 검증
- [ ] Connected Account pin
- [ ] Session 저장/복구
- [ ] cross-tenant negative test

## Project 2. GitHub Issue Triage Agent

issue를 검색하고 label 제안을 만든 뒤 사람 승인 후 update한다.

```text
search issues -> fetch schema/data -> propose label/comment
  -> preview exact change -> human approval -> execute -> audit
```

핵심 실험:

- dynamic search와 fixed/preloaded tools의 tool-selection accuracy 비교
- public/private repository account pin 검증
- approval 전후 arguments hash 비교
- timeout 이후 duplicate comment 방지

평가표:

| Metric | 목표 |
|---|---|
| forbidden tool selection | 0 |
| wrong repository execution | 0 |
| duplicate write on retry | 0 |
| approval payload mismatch | 0 |

## Project 3. Gmail-to-Slack Digest

Trigger와 Sandbox를 함께 검증한다.

```text
Gmail trigger
  -> signed webhook 검증 + dedupe
      -> queue
          -> messages fetch
              -> Sandbox에서 grouping/summarization input 생성
                  -> Slack preview
                      -> approval/auto-post policy
```

고려할 점:

- webhook handler와 agent worker를 분리한다.
- email body의 sensitive data를 Slack으로 옮기기 전에 redaction한다.
- trigger replay와 Slack duplicate post를 idempotency key로 막는다.
- Sandbox가 필요 없으면 application code로 변환해 attack surface를 줄인다.

## Project 4. SDK vs Hosted MCP Policy Lab

같은 read/write workflow를 provider SDK와 hosted MCP 양쪽으로 연결해 차이를 기록한다.

| 실험 | Provider SDK | Hosted MCP |
|---|---|---|
| 기본 tool 실행 | 확인 | 확인 |
| `beforeExecute` 차단 | 적용 여부 기록 | 우회됨을 확인 |
| `afterExecute` audit enrich | 적용 여부 기록 | 우회됨을 확인 |
| local custom tool | 노출 확인 | 미노출 확인 |
| client portability | adapter 필요성 기록 | MCP clients 비교 |

결과물은 “어느 것이 더 좋다”가 아니라 어떤 policy를 어느 backend layer에서 강제해야 하는지 보여주는 architecture decision record다.

## Project 5. Connector Upgrade Harness

SDK/toolkit upgrade 전에 schema와 behavior drift를 자동 검증한다.

```text
fixtures/
├── discovery-cases.yaml
├── auth-cases.yaml
├── tool-inputs.yaml
└── expected-schemas/
```

Pipeline:

1. 현재 pinned version에서 schema snapshot 저장
2. candidate SDK/toolkit version 설치
3. input/output schema diff
4. sandbox account에서 read test
5. approval이 있는 write canary test
6. log/redaction/latency 비교
7. pass일 때만 lockfile update

## Production Readiness Checklist

### Identity and auth

- [ ] user/tenant/Session/Connected Account mapping이 server-side에서 검증된다.
- [ ] account를 추론하지 않고 명시적으로 pin한다.
- [ ] OAuth scope가 least privilege다.
- [ ] revoked/expired/reauth state의 UX가 있다.

### Actions

- [ ] write/destructive tool에 preview와 approval이 있다.
- [ ] retry는 idempotent하거나 remote state를 먼저 확인한다.
- [ ] allowlist/denylist가 test로 고정돼 있다.
- [ ] partial failure와 compensation 전략이 있다.

### Operations

- [ ] SDK와 toolkit version이 pin되어 있다.
- [ ] trigger signature/replay/deduplication을 검증한다.
- [ ] sensitive data가 log와 sandbox file에서 redacted된다.
- [ ] rate limit, latency, failure, tool selection을 관찰한다.
- [ ] vendor outage와 rollback/runbook이 있다.

## Sources

- https://docs.composio.dev/docs/configuring-sessions
- https://docs.composio.dev/docs/sessions-vs-direct-execution
- https://docs.composio.dev/docs/sessions-via-mcp
- https://docs.composio.dev/docs/extending-sessions/custom-tools-and-toolkits
- https://docs.composio.dev/reference/changelog

