---
date: 2026-10-22
tags: [tech]
type: tech-tool-study
status: draft
---

# Kylon Overview

## What

Kylon은 회사 업무를 위한 AI-native workspace 또는 **company harness**다. 사람, 여러 AI agent, 회사 데이터, 외부 업무 도구를 Workspace와 Room 중심으로 묶어 작업의 대화·결정·실행 결과를 공유한다.

개인 AI chat의 결과가 각자 탭에 흩어지는 문제 대신, 팀이 같은 Room에서 thread와 업무 맥락을 보고 다음 담당자 또는 agent가 이어받도록 한다.

## Why

반복 업무에는 단순한 생성 모델보다 다음 요소가 함께 필요하다.

| 필요한 운영 요소 | Kylon에서의 대응 |
| --- | --- |
| 공유 맥락과 handoff | Room, thread, persistent memory |
| 실제 업무 시스템 접근 | Connection과 계정별 권한 |
| 데이터 입력·조회 화면 | App과 shared record |
| 반복 실행 | schedule, webhook, record change 기반 workflow |
| 위험한 실행 통제 | approval card와 draft-first 흐름 |
| 사후 확인 | tool trace, thread receipt, run history |

예를 들어 agent가 billing mailbox를 조사하고 tracker record를 갱신한 뒤, follow-up email은 draft로만 남긴다. 담당자는 Room에서 근거와 초안을 검토하고 Send 여부를 결정한다.

## Core Concepts

### Workspace, Room, Agent

- **Workspace**: 멤버, 데이터, Connection, 운영 범위를 묶는 최상위 경계다.
- **Room**: 사람과 agent가 함께 일하는 공유 대화·맥락 단위다. Room membership과 agent에게 질문할 수 있는 access list는 구분해서 이해한다.
- **Agent**: Room 문맥, 허용된 knowledge와 Connection을 바탕으로 tool을 쓰고 결과를 남긴다. Kylon agent 외에 Claude Code, Codex, Devin 등의 외부 agent도 연결할 수 있다.

### Connection과 permissions

Kylon은 Gmail, Outlook, Slack, Notion, GitHub, Salesforce 등을 포함해 3,000+ integration을 표방한다. 권한을 대략 다음 네 층으로 나눈다.

1. **Agent** — 무엇을 알고 어떤 tool을 사용할 수 있는가
2. **Room** — 누가 대화와 결과를 보는가
3. **App / Workflow** — 어떤 automation이 record나 외부 데이터를 바꾸는가
4. **Connection** — 어느 계정으로 실제 action을 실행하는가

Connection은 편리한 전역 권한이 아니라 업무별 최소 권한으로 부여한다.

### App, records, workflow

대화에서 CRM, tracker, 외부 입력 form 같은 App을 만들고 record를 공유할 수 있다. 공식 설명 기준 App은 Neon serverless Postgres, Git 기반 draft/version 관리, Vercel deployment를 사용한다. workflow는 schedule, webhook, record change를 trigger로 agent 작업을 실행한다.

## Safety and Operations

- email, message, X post 같은 outbound 행위는 draft 후 사람이 Send하는 흐름을 우선한다.
- App publish, 공개 범위 확대, Connection 접근, 멤버 초대 등은 approval card 대상이다.
- prompt injection을 완전히 차단하는 제품이라고 간주하지 말고, 신뢰하지 않는 입력을 검토하고 최소 권한·승인을 유지한다.
- tool reply trace와 automation run history에서 outcome, duration, output, credit 사용량을 점검한다. 이는 별도 export audit log라고 단정하기보다 업무 맥락의 실행 기록으로 이해한다.

## Platform and Compliance Notes

공식 Help Center는 웹, macOS desktop, iOS/Android를 안내한다. Privacy Policy는 데이터가 주로 미국 GCP에 저장된다고 설명한다. GDPR compliant라는 제품 주장은 확인할 수 있으나, SOC 2 Type II와 ISO/IEC 27001:2022는 진행 중이다. procurement 전에는 최신 security 문서와 계약 조건을 재확인한다.

## Further Reading

- [[README|학습 경로로 돌아가기]]
- [[02-ecosystem|Ecosystem 비교]]
- [[04-learning/01-getting-started|최소 권한으로 시작하기]]
