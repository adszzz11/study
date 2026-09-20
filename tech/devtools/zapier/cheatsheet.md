---
date: 2026-08-24
tags: [tech]
type: tech-tool-study
status: draft
---

# Zapier — Cheatsheet

> [[05-projects|이전: Projects]] · [[README|목차로 돌아가기]]

## Workflow skeleton

```text
Trigger
 → validate / normalize
 → deduplicate
 → search / upsert
 → branch / loop
 → approval if high-impact
 → external action
 → record result / notify
```

## Trigger 선택

| 질문 | 선택 |
|---|---|
| source가 webhook 지원? | Instant Trigger 우선 |
| webhook 없음? | Polling Trigger + latency 확인 |
| stable unique ID 있음? | deduplication key로 사용 |
| workflow가 같은 resource 갱신? | origin/processed guard 추가 |

기본 polling interval:

- Free: 15분
- Professional: 2분
- Team·Enterprise: 1분

## Logic 빠른 선택

| 필요 | 기능 |
|---|---|
| 조건이 아니면 종료 | Filter |
| 여러 조건 경로 | Paths |
| collection 처리 | Looping |
| reusable workflow | Sub-Zaps |
| 문자열·날짜 변환 | Formatter |
| custom JS/Python | Code |
| 시간 지연 | Delay / Schedule |
| 작은 workflow state | Tables |
| 사람 입력 | Forms |
| 외부 write 전 검토 | Human-in-the-Loop |

## 중복 방지

```text
key = source_system + ':' + external_event_id

if Table[key].status == 'completed': stop
else:
  mark processing
  perform idempotent/upsert action
  mark completed with external_result_id
```

- target API의 idempotency key와 unique constraint를 우선한다.
- Search→Create만으로 동시 실행 race가 사라지지는 않는다.
- replay 전에 이미 발생한 side effect를 확인한다.

## AI safety

```text
Guardrails → constrained output → schema validation
→ deterministic Paths → human approval → external write
```

- enum과 typed JSON을 우선한다.
- tool/account scope를 최소화한다.
- delete, payment, send, permission change는 approval을 둔다.
- Agent output과 Activity log를 sample review한다.

## Task 계산

| 단위 | 2026-08-24 기준 |
|---|---:|
| 일반 app/action | 보통 1 task |
| 주요 built-in logic/Table/Form | 0 tasks |
| MCP tool call | 2 tasks |
| AI step standard/advanced/premium | 1/3/5 tasks |
| Code 기본 실행 | 1 task |

```text
monthly tasks
≈ events × paid steps × fan-out × (1 + retry rate)
  + AI/MCP tool calls
```

## 장애 triage

| 증상 | 확인 순서 |
|---|---|
| Zap이 안 시작됨 | app event → Trigger type → polling interval → auth → test data |
| field가 비어 있음 | source payload → sample → optional field → mapping |
| duplicate | Trigger ID → retry/replay → loop → Search/Create race |
| task 급증 | loop items → branching → AI tools → retry → unexpected volume |
| Agent 오작동 | input → prompt/knowledge → tool scope → activity → approval |

## Production checklist

- [ ] owner와 failure owner
- [ ] least-privilege credential
- [ ] unique key와 idempotency strategy
- [ ] schema validation과 null handling
- [ ] retry/replay 시 duplicate 검증
- [ ] PII 최소화와 retention 확인
- [ ] high-impact action approval
- [ ] task budget과 alert
- [ ] rollback 또는 manual reconciliation runbook

## Sources

- [How Zap triggers work](https://help.zapier.com/hc/en-us/articles/8496244568589-How-Zap-triggers-work)
- [Zapier task usage rates](https://zapier.com/pricing/rates)
- [Data safety with Zapier Agents](https://help.zapier.com/hc/en-us/articles/24687564925453-Data-safety-with-Zapier-Agents)
- [Zapier SDK](https://docs.zapier.com/sdk)
