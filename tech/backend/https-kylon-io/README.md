---
date: 2026-10-22
tags: [tech]
type: tech-tool-study
status: draft
---

# Kylon

> **한 줄 정의**: Kylon은 사람·AI agent·회사 데이터·업무 도구를 공유 `Room`에서 연결해 대화, workflow, 내부 App 운영을 함께 수행하는 AI-native company harness다.

## Overview

Kylon은 개인용 AI chat을 넘어서 팀이 **공유 맥락과 실행 이력**을 갖고 일하도록 설계된 workspace다. 사람과 여러 agent가 Room에서 작업하고, SaaS Connection·record·workflow·App을 같은 업무 맥락에 둔다.

```text
Workspace
  └─ Room (사람, thread, 공유 맥락)
       └─ Agent (질문 가능 범위, tool 사용)
            └─ Connection (Gmail / CRM / Drive 등 계정 권한)
                 └─ App · record · workflow · run history
```

- 핵심은 답변 생성이 아니라 반복 업무의 handoff, 실행, 검토, 승인을 연결하는 것이다.
- outbound message와 권한 확대 등 영향이 큰 행위는 human-in-the-loop approval을 전제로 설계한다.
- SOC 2 Type II 및 ISO/IEC 27001:2022는 공식 안내상 진행 중이므로, 인증 완료로 가정하면 안 된다.

## Learning Path

- [ ] [[01-overview|Overview]] — 제품의 문제 정의, Room-first 구조, 핵심 기능 이해
- [ ] [[02-ecosystem|Ecosystem]] — chat, iPaaS, internal-tool builder와의 선택 기준 비교
- [ ] [[03-references|References]] — 공식 제품·보안·운영 문서 원문 확인
- [ ] [[04-learning/01-getting-started|Getting started]] — 최소 권한으로 첫 Room과 workflow 설계
- [ ] [[04-learning/02-deep-dive|Deep dive]] — permission, approval, App, run history 심화
- [ ] [[05-projects|Projects]] — AR, sales, 현장 운영 등 적용 과제 실습
- [ ] [[cheatsheet|Cheatsheet]] — 핵심 용어와 운영 checklist 복습

## When To Use

- 여러 담당자와 agent가 같은 업무 맥락을 이어받아야 할 때
- CRM 갱신, research, invoice follow-up처럼 검토 가능한 반복 업무를 자동화할 때
- SaaS 계정 접근을 Connection별로 제한하고 approval 흐름을 남기고 싶을 때
- 대화에서 출발한 tracker, form, 내부 App과 workflow를 한 workspace에서 운영할 때
- Codex 또는 Claude Code의 결과를 비개발 팀이 Room에서 이어서 검토·승인해야 할 때

## When Not To Use

- 개인의 단발성 질문·문서 작성만 필요할 때
- 엄격하고 결정론적인 규칙 기반 automation만 필요할 때는 n8n, Zapier, Make가 더 단순할 수 있다.
- 복잡한 software lifecycle, 세밀한 코드 제어, 대규모 custom backend가 핵심일 때
- credential, data residency, 감사 요구가 hosted workspace의 보안·보존 정책과 맞지 않을 때
- prompt injection 위험을 승인 검토와 최소 권한으로 통제할 운영 역량이 없을 때

## Related Notes

- [[MOCs/Index]]
- [[MOCs/Backend]]
- [[tech/ai/agent-orchestration/README|AI 에이전트 오케스트레이션 플랫폼]]
- [[tech/ai/composio/README|Composio]]

## Sources

- https://kylon.io/
- https://kylon.io/help
- https://kylon.io/blog/how-kylon-connects-agents-and-tools
- https://kylon.io/blog/how-permissions-work-in-kylon
- https://kylon.io/help/approve-agent-actions
- https://kylon.io/help/prompt-injection-protection
