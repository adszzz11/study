---
date: 2026-08-24
tags: [tech]
type: tech-tool-study
status: draft
---

# Zapier — Overview

> [[README|목차로 돌아가기]] · [[02-ecosystem|다음: Ecosystem]]

## What

Zapier는 서로 다른 SaaS와 API를 **Trigger–Action workflow**로 연결하는 managed automation/iPaaS다. 하나의 Zap은 한 Trigger와 하나 이상의 Action으로 구성되며, 앞 단계의 output field를 다음 단계 input으로 매핑한다.

```text
New lead
  → validate and enrich
  → create/update CRM record
  → assign owner
  → notify Slack
```

### 핵심 용어

| 용어 | 의미 |
|---|---|
| Zap | 하나의 자동화 workflow |
| Trigger | Zap을 시작하는 event |
| Action | 외부 앱 또는 Zapier가 수행하는 작업 |
| Task | 성공적으로 완료된 과금 대상 작업 단위 |
| App/connector | 인증과 API operation을 Zapier step으로 노출하는 integration |
| Zap run | Trigger record 하나를 처리한 실행 |

## Why

SaaS를 직접 연결하면 다음 기반 작업을 API마다 반복해야 한다.

- OAuth/API key 인증, token refresh, secret 관리
- Webhook endpoint 또는 polling scheduler 운영
- schema 차이, pagination, rate limit 처리
- 데이터 변환, 분기, retry, 실패 알림
- API version과 connector 유지보수
- 사용자 권한, audit log, retention policy 구현

Zapier는 이 integration layer를 managed service로 제공해 사용자가 업무 규칙과 결과에 집중하게 한다. 다만 managed abstraction은 실행 의미와 비용에 대한 통제력이 줄어드는 trade-off를 가진다.

## 실행 모델

```text
Event source
   ├─ Instant trigger: webhook
   └─ Polling trigger: API polling + unique ID deduplication
   ↓
Trigger record
   ↓
Field mapping / Formatter / Code
   ├─ Filter / Paths / Looping
   ├─ Delay / Schedule
   └─ Human-in-the-Loop
   ↓
App action / AI step / Agent / Webhook
   ↓
History / alerts / replay / audit / usage
```

### Instant와 Polling

| 방식 | 동작 | 장점 | 주의 |
|---|---|---|---|
| Instant | 원본 앱이 webhook을 전송 | 낮은 latency, 불필요한 조회 감소 | 원본 앱과 connector가 webhook을 지원해야 함 |
| Polling | Zapier가 API를 주기적으로 조회 | webhook이 없는 앱도 연결 | plan별 interval과 deduplication에 의존 |

공식 기본 polling interval은 Free 15분, Professional 2분, Team·Enterprise 1분이다. 실제 Trigger 방식은 앱 API와 connector 구현이 결정한다.

## 핵심 특징

### Connector와 인증

- public app, Zapier built-in tool, 조직 내부 private app을 조합한다.
- Trigger, Search, Create/Update/Delete, Resource, Authentication primitive를 제공한다.
- 없는 기능은 Webhooks, API request, Code by Zapier로 보완한다.
- 반복 사용할 custom connector는 Node.js 기반 Developer Platform CLI로 만든다.

### Logic, state, human interaction

| 기능 | 용도 |
|---|---|
| Filters / Paths | 조건부 중단과 branching |
| Looping / Sub-Zaps | collection 반복과 reusable workflow |
| Formatter / Code | 데이터 변환과 custom logic |
| Delay / Schedule | 시간 기반 실행 |
| Tables | deduplication, mapping, workflow state |
| Forms | 사용자 입력, conditional field, Table/Zap 연결 |
| Canvas | Zap, Agent, Table, Form, 수동 단계를 시각화 |
| Human-in-the-Loop | 외부 write 전 승인·거절·수정 checkpoint |

과거 **Zapier Interfaces**는 2026년에 **Zapier Forms**로 이름이 바뀌었고 기존 project와 기능은 유지된다.

### AI action layer

- **AI by Zapier**: 분류, 추출, 요약, 생성, tool calling step
- **Agents**: instruction, knowledge source, tools를 가진 autonomous worker
- **MCP**: Claude, ChatGPT, Cursor 같은 MCP client가 action을 tool call
- **SDK**: application code나 coding agent에서 programmatic action 실행; 2026-08-24 기준 open beta
- **CLI**: terminal에서 action 탐색·실행
- **AI Guardrails**: PII redaction, prompt injection/jailbreak, toxicity 검사

## 대표 위험

| 위험 | 완화책 |
|---|---|
| workflow가 자신을 다시 trigger | `processed_at`, external event ID, idempotency key 사용 |
| Search 후 Create 사이 race | upsert 또는 unique key와 재조회 사용 |
| AI의 비결정적 output | schema validation, deterministic Paths, approval 적용 |
| rate limit / partial failure | retry 정책, replay 전 중복 방지, 실패 queue 설계 |
| task 비용 급증 | record 수 × 유료 step 수 × retry율로 사전 추정 |

## Sources

- [What is a Zap?](https://help.zapier.com/hc/en-us/articles/8496309697421-What-is-a-Zap)
- [How Zap triggers work](https://help.zapier.com/hc/en-us/articles/8496244568589-How-Zap-triggers-work)
- [Introduction to apps on Zapier](https://help.zapier.com/hc/en-us/articles/21996626006541-Introduction-to-apps-on-Zapier)
- [Create forms in Zapier Forms](https://help.zapier.com/hc/en-us/articles/15927500577037-Create-forms-in-Zapier-Forms)
- [Zapier SDK](https://docs.zapier.com/sdk)

