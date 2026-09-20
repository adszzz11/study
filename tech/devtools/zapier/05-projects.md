---
date: 2026-08-24
tags: [tech]
type: tech-tool-study
status: draft
---

# Zapier — Projects

> [[04-learning/02-deep-dive|이전: Deep Dive]] · [[README|목차로 돌아가기]] · [[cheatsheet|다음: Cheatsheet]]

## Project 1. Idempotent lead routing

### 목표

Form으로 받은 lead를 검증하고 CRM에 upsert한 뒤 담당자에게 알린다.

```text
Forms
 → validate consent/email
 → lookup event_id in Tables
 → enrich company
 → CRM upsert
 → assign owner with Paths
 → Slack notify
 → mark completed
```

### 완료 조건

- [ ] 동일 submission을 세 번 보내도 CRM record는 하나다.
- [ ] enrichment 실패 시 raw lead를 잃지 않는다.
- [ ] 담당자 결정 rule과 fallback owner가 문서화돼 있다.
- [ ] Slack 알림에는 민감 정보가 최소화돼 있다.
- [ ] 월간 task 예상치와 실제치를 비교한다.

## Project 2. Human-approved outbound message

### 목표

AI가 support ticket을 요약하고 답변 초안을 만들되, 사람이 승인·수정한 경우에만 발송한다.

```text
New ticket
 → Guardrails
 → classify + extract typed fields
 → draft response
 → Human-in-the-Loop
    ├─ approve/edit → send reply
    └─ reject       → escalate
 → write audit result
```

### 평가 항목

| 항목 | 측정 |
|---|---|
| Schema validity | required field 성공률 |
| Human correction | 수정된 초안 비율 |
| Safety | approval 없이 전송된 건수 = 0 |
| Cost | ticket당 AI step + tool call task |
| Audit | input, decision, final output 추적 가능 여부 |

## Project 3. MCP action sandbox

### 목표

AI client에 낮은 위험도의 Zapier action만 제공하고 tool-use boundary를 검증한다.

허용 예:

- calendar free/busy 조회
- draft 생성
- test channel 메시지 전송

초기 제외 예:

- 고객에게 직접 이메일 발송
- record delete
- billing 또는 permission 변경

### 실험 절차

1. test account와 test workspace를 만든다.
2. 최소 action과 account만 MCP에 연결한다.
3. ambiguous instruction과 prompt injection sample을 테스트한다.
4. destructive/high-impact action에 사용자 confirmation을 요구한다.
5. activity/audit log와 task usage를 검토한다.

## Project 4. Private connector spike

### 목표

공식 connector에 없는 내부 API를 Developer Platform CLI app으로 노출한다.

```text
Authentication: API key or OAuth2
Resource: Customer
Trigger: New Customer
Search: Find Customer
Create: Create Customer
Hooks: request headers + response normalization
```

### 산출물

- authentication과 secret handling 문서
- trigger deduplication key 정의
- happy/error/rate-limit contract test
- versioning과 rollback plan
- Webhooks/Code step을 계속 쓸 때와의 비용 비교

## 공통 회고 질문

- Zapier가 제거한 운영 부담은 무엇인가?
- Zapier abstraction 때문에 통제하기 어려워진 것은 무엇인가?
- duplicate, partial failure, replay를 실제로 시험했는가?
- 같은 workload를 Make/n8n/Pipedream으로 만들면 billing unit이 어떻게 달라지는가?
- production 전환에 필요한 security·governance gap은 무엇인가?

## Sources

- [Create forms in Zapier Forms](https://help.zapier.com/hc/en-us/articles/15927500577037-Create-forms-in-Zapier-Forms)
- [Human in the Loop](https://help.zapier.com/hc/en-us/articles/38737614362005-Add-a-human-review-step-to-your-Zap-with-Human-in-the-Loop)
- [Zapier MCP guide](https://zapier.com/blog/zapier-mcp-guide/)
- [Developer Platform CLI tutorial](https://docs.zapier.com/integrations/quickstart/cli-tutorial)
- [Data safety with Zapier Agents](https://help.zapier.com/hc/en-us/articles/24687564925453-Data-safety-with-Zapier-Agents)

