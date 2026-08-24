---
date: 2026-08-24
tags: [tech]
type: tech-tool-study
status: draft
---

# Zapier — Deep Dive

> [[01-getting-started|이전: Getting Started]] · [[../README|목차로 돌아가기]] · [[../05-projects|다음: Projects]]

## 1. Delivery semantics를 보수적으로 설계하기

외부 API, timeout, retry가 섞인 workflow는 "정확히 한 번" 실행된다고 가정하지 않는다. **at-least-once 가능성**을 전제로 side effect를 idempotent하게 만든다.

| 기법 | 적용 예 |
|---|---|
| External event ID | source event의 고유 ID를 target record에 저장 |
| Idempotency key | API가 지원하면 create request에 전달 |
| Processed state | Table에 `event_id`, `status`, `processed_at` 기록 |
| Upsert | unique key 기준 create-or-update |
| Guard field | `automation_origin`, `processed_at`으로 self-trigger 차단 |

```text
receive event
 → lookup event_id in Table
 → if completed: stop
 → mark processing
 → perform external action with idempotency key
 → mark completed + result_id
```

`processing` 상태에서 멈춘 run을 어떻게 복구할지 timeout과 reconciliation rule도 정해야 한다.

## 2. Polling과 deduplication

Polling Trigger는 API에서 record를 조회하고 unique ID를 기준으로 새 항목을 판별한다. 다음 경우를 검토한다.

- API가 stable unique ID와 monotonically increasing timestamp를 제공하는가?
- 동일 timestamp record의 ordering이 안정적인가?
- 수정 event와 생성 event를 구분할 수 있는가?
- polling window보다 늦게 도착한 record를 놓치지 않는가?
- Free/Professional/Team·Enterprise interval이 요구 latency에 맞는가?

높은 정확도가 필요하면 source의 webhook, outbox, queue 또는 주기적 reconciliation job을 함께 고려한다.

## 3. Branch, loop, fan-out의 비용

Zapier는 성공한 작업 단위를 task로 센다. 2026-08-24 기준 대표 rule은 다음과 같다.

| 실행 요소 | Task |
|---|---:|
| 일반 app/action step | 대체로 1 |
| Formatter, Filter, Paths, Delay, Looping, Tables, Forms 등 일부 built-in | 0 |
| Zapier MCP tool call | 2 |
| AI step — standard / advanced / premium | 1 / 3 / 5 |
| Code step 기본 실행 | 1 |
| Code extended runtime | plan allowance 초과 30초당 추가 1 |

Looping 자체가 0 task여도 loop 내부 app action은 item마다 task를 소비한다.

```text
monthly tasks
= runs × Σ(branch probability × records × paid steps)
+ retries
+ MCP/AI tool calls
```

예: 월 2,000건, 평균 3개의 유료 app action, 10%가 4개 item으로 fan-out되어 action 1개를 추가 수행한다면 retry 전 약 `2,000 × 3 + 2,000 × 0.1 × 4 = 6,800 tasks`다.

## 4. AI를 deterministic workflow 안에 가두기

```text
untrusted input
 → AI Guardrails
 → constrained extraction/classification
 → schema validation
 → deterministic Paths
 → human approval for high-impact action
 → external write
 → activity/audit review
```

### 설계 원칙

- 자유문 생성보다 enum classification과 typed extraction을 우선한다.
- JSON schema validation 실패 시 자동 수정 loop보다 quarantine path를 둔다.
- 결제, 삭제, 외부 발송, 권한 변경에는 human approval을 둔다.
- Agent가 사용할 tool과 account scope를 최소화한다.
- prompt와 knowledge source 안의 instruction을 신뢰 경계별로 구분한다.
- 동일 input에서도 Agent 행동이 달라질 수 있으므로 Activity log를 검토한다.

## 5. MCP, SDK, CLI 선택

| 인터페이스 | 실행 위치 | 적합한 경우 | 주의 |
|---|---|---|---|
| MCP | Claude/ChatGPT/Cursor 등 AI client | assistant가 대화 중 action 수행 | tool allowlist, confirmation, 2 tasks/call |
| SDK | application code | 제품 기능에 Zapier action 내장 | open beta 변경 가능성, error contract |
| CLI | terminal/coding agent | 개발·운영 중 action 탐색/실행 | shell/credential scope와 audit |
| Zap | Zapier managed runtime | 반복 event-driven business process | step/task, runtime, replay 의미 |

이들은 모두 governed access layer를 쓰지만 caller와 lifecycle이 다르다. 반복 자동화는 Zap, interactive agent action은 MCP, 제품 코드 통합은 SDK가 기본 출발점이다.

## 6. Custom connector 경계

Webhooks/Code step이 여러 Zap에 복제되면 Developer Platform app으로 승격할 시점이다.

```javascript
module.exports = {
  triggers: {},
  searches: {},
  creates: {},
  resources: {},
  beforeRequest: [],
  afterResponse: []
};
```

- authentication과 token refresh를 중앙화한다.
- request/response normalization을 hook에 둔다.
- contract test와 sample payload를 유지한다.
- API version 변경을 connector release로 관리한다.

## 7. 운영 runbook

| 증상 | 먼저 볼 것 | 안전한 대응 |
|---|---|---|
| 중복 record | Trigger ID, retry, replay, self-loop | write 중단, key별 reconcile, guard 추가 |
| record 누락 | polling interval, filter, sample schema | source와 History 대조, 범위 제한 replay |
| task 급증 | loop item, branch, AI/tool call, retry | Zap pause 여부 판단, high-cardinality input 차단 |
| auth 실패 | token expiry, scope, account owner | 최소 권한으로 reconnect, 영향을 받는 Zap test |
| AI 오작동 | input, prompt, tool activity | tool revoke/disable, audit 후 constraint 강화 |

## Sources

- [How Zap triggers work](https://help.zapier.com/hc/en-us/articles/8496244568589-How-Zap-triggers-work)
- [Zapier task usage rates](https://zapier.com/pricing/rates)
- [Data safety with Zapier Agents](https://help.zapier.com/hc/en-us/articles/24687564925453-Data-safety-with-Zapier-Agents)
- [MCP vs SDK vs CLI](https://zapier.com/blog/zapier-mcp-vs-sdk/)
- [Developer Platform CLI tutorial](https://docs.zapier.com/integrations/quickstart/cli-tutorial)

