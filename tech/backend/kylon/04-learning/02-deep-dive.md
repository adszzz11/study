---
date: 2026-10-22
tags: [tech]
type: tech-tool-study
status: draft
---

# Kylon Deep Dive

## Permission Design

Kylon의 권한은 한 토글이 아니라 Agent, Room, App/Workflow, Connection의 조합으로 검토한다.

| 층 | 검토 질문 | 안전한 기본값 |
| --- | --- | --- |
| Agent | 무엇을 알고 어떤 tool을 쓸 수 있는가? | 업무별 agent와 좁은 tool scope |
| Room | 누가 맥락과 결과를 볼 수 있는가? | 전용 Room, 필요한 멤버만 초대 |
| App / Workflow | 어떤 변경을 자동 실행하는가? | preview·draft, 작은 trigger 범위 |
| Connection | 어느 계정으로 무엇을 실행하는가? | 최소 권한, 업무별 계정 또는 scope |

Room에 agent가 있다고 해서 모든 멤버가 그 agent에게 같은 질문을 할 수 있거나 모든 data에 접근하는 것은 아니다. access와 membership을 따로 확인한다.

## Approval and Prompt Injection

승인은 permission을 대체하지 않는다. 최소 권한으로 agent가 할 수 있는 범위를 먼저 줄이고, 그 안에서도 부작용이 큰 action은 사람이 보게 한다.

| Action | 권장 통제 |
| --- | --- |
| 외부 email/message/post | draft 생성 후 사람이 Send |
| App publish 또는 공개 범위 확대 | approval card와 대상 범위 검토 |
| Connection 접근·권한 확대 | 요청 이유, 계정, scope를 승인 |
| 멤버 초대 | workspace/Room 접근 범위 승인 |

외부 문서, email, web page에는 agent를 조종하려는 instruction이 섞일 수 있다. prompt injection을 완벽하게 막을 수 있다고 전제하지 말고, 신뢰하지 않는 텍스트를 tool instruction으로 취급하지 않도록 brief를 작성한다. 송신·삭제·권한 변경은 별도 확인을 유지한다.

## App and Workflow Lifecycle

공식 설명에 따르면 App은 Neon serverless Postgres, Git 기반 draft/version 관리, Vercel deployment를 사용한다. 이를 사용자가 직접 운영한다고 가정하기보다, 다음 제품 lifecycle을 검토한다.

1. App을 draft 또는 preview에서 field·mobile UI·data update 경로로 검토한다.
2. publish 전 public/private 범위와 연결된 record를 확인한다.
3. workflow trigger(schedule, webhook, record change)를 작은 범위로 시작한다.
4. outcome과 실패 사례를 반영해 schema·prompt·approval을 조정한다.

## Observability and Cost

tool 사용 reply의 trace, thread receipt, automation run history를 운영 evidence로 사용한다. run마다 outcome, duration, output, credit 단위를 확인해 실패와 과다 사용을 찾는다.

```text
Trigger → agent tool calls → record/draft → approval → outcome
             └──────── trace / receipt / run history ────────┘
```

이 기록은 별도 export 가능한 compliance audit log라고 단정하지 않는다. 보존 기간, export, 접근 제어, 계약상 감사 요건은 도입 전에 공식 문서 및 담당자에게 확인한다.

## CLI Agent Handoff

Codex 또는 Claude Code를 쓰는 팀은 Kylon CLI로 IDE/terminal agent의 결과를 Room에 남기는 흐름을 실험할 수 있다. workspace별로 취소 가능한 credential을 사용하고, 코드·secret·고객 데이터가 Room에 노출되는 범위를 사전에 정한다.

## Related Notes

- [[01-getting-started|Getting started]]
- [[../cheatsheet|Cheatsheet]]
- [[../03-references|공식 보안·운영 문서]]
