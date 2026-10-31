---
date: 2026-10-22
tags: [tech]
type: tech-tool-study
status: draft
---

# Kylon Cheatsheet

## Core Model

```text
Workspace → Room → Agent → Connection → App / Workflow → Run history
```

| 용어 | 짧은 설명 |
| --- | --- |
| Workspace | 멤버, data, Connection의 상위 경계 |
| Room | 사람과 agent가 맥락을 공유하는 업무 대화 공간 |
| Agent | Room 문맥과 허용된 tool로 작업하는 AI 주체 |
| Connection | 외부 SaaS 계정·권한 연결 |
| App | record와 UI를 가진 업무용 App |
| Workflow | schedule, webhook, record change로 실행되는 자동화 |
| Approval card | 사람이 검토해야 하는 영향 큰 action의 승인 UI |
| Run history | automation의 outcome, duration, output, credit 기록 |

## Default Guardrails

- **최소 권한**: 필요한 Connection, account, scope만 agent에 준다.
- **draft-first**: outbound email/message/post는 초안으로 만들고 사람이 Send한다.
- **small trigger**: workflow는 샘플 또는 좁은 schedule/record 조건으로 시작한다.
- **evidence**: source link, input, result, 예외를 Room 또는 record에 남긴다.
- **review**: trace, receipt, run history로 잘못된 tool 사용과 비용을 확인한다.
- **revoke**: 문제가 생기면 workflow를 멈추고 Connection/CLI credential을 취소할 수 있게 한다.

## Decision Rules

| 상황 | 우선 선택 |
| --- | --- |
| 개인 질문, 문서 초안 | ChatGPT Work / Claude 같은 개인 assistant |
| 규칙 기반의 결정론적 automation | n8n / Zapier / Make |
| 복잡한 custom software 개발 | Retool / Replit / Lovable 또는 개발 환경 |
| 공유 handoff, agent 실행, record·approval 운영 | Kylon |

## Before Publish or Send

- [ ] App의 public/private 범위와 mobile UI를 preview에서 확인했는가?
- [ ] record update가 의도치 않은 workflow를 trigger하지 않는가?
- [ ] sender account와 recipient가 정확한가?
- [ ] approval 대상 action을 자동 실행으로 우회하지 않았는가?
- [ ] untrusted input의 지시를 실행하지 않았는가?
- [ ] 실행 실패 시 중지·복구할 담당자가 정해져 있는가?

## Facts to Verify During Procurement

- 필요한 integration과 실제 permission scope
- data residency, retention, export, audit 요구 충족 여부
- security certification의 최신 상태 — SOC 2 Type II와 ISO/IEC 27001:2022는 dossier 기준 진행 중
- pricing, credit unit, concurrency, workflow 한도
- CLI credential 취소와 offboarding 절차

## Links

- [[README|Kylon README]]
- [[03-references|공식 출처]]
- [[04-learning/02-deep-dive|Deep dive]]
