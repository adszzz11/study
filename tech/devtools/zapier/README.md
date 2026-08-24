---
date: 2026-08-24
tags: [tech]
type: tech-tool-study
status: draft
---

# Zapier

> **한 줄 정의**: Zapier는 SaaS 앱·API·데이터·AI agent를 Trigger–Action workflow로 연결하고, 인증·실행·재시도·거버넌스를 관리하는 managed automation/iPaaS 플랫폼이다.

## Overview

Zapier는 여러 SaaS에 흩어진 업무를 **Zap**이라는 event-driven workflow로 연결한다. 사용자는 connector 인증, webhook/polling, field mapping, branching, retry 같은 통합 기반을 직접 운영하는 대신 비즈니스 규칙에 집중한다.

```text
Trigger → transform / filter / branch → action(s) → history / alert / replay
```

2026년의 Zapier는 단순 no-code automation을 넘어 다음 계층을 함께 제공한다.

| 계층 | 제품·기능 | 역할 |
|---|---|---|
| Automation | Zaps | Trigger–Action workflow 실행 |
| Data/state | Tables | automation용 structured state 저장 |
| Human interface | Forms | 입력·검토 화면과 Zap 연결 |
| AI/action | Agents, MCP, SDK, CLI | AI client와 code에 SaaS action 제공 |

공식 설명 기준으로 9,000+ apps와 30,000+ actions를 제공한다. 자세한 구조는 [[01-overview]], 대안 비교는 [[02-ecosystem]]을 참고한다.

## Learning Path

- [ ] [[01-overview|Overview]] — What/Why, 실행 모델, 핵심 기능
- [ ] [[02-ecosystem|Ecosystem]] — Make, n8n, Pipedream, Workato와 비교
- [ ] [[03-references|References]] — 공식 문서 지도와 검증 포인트
- [ ] [[04-learning/01-getting-started|Getting Started]] — 첫 Zap 설계·테스트·운영
- [ ] [[04-learning/02-deep-dive|Deep Dive]] — deduplication, idempotency, AI safety, 비용
- [ ] [[05-projects|Projects]] — lead routing, approval, AI action layer 실습
- [ ] [[cheatsheet|Cheatsheet]] — 빠른 설계·운영 참조

## When To Use

- 개발팀 대기 없이 SaaS 간 업무를 빠르게 자동화할 때
- 여러 부서가 connector, 인증, 실행 기록, 권한 정책을 공통으로 써야 할 때
- 비교적 낮거나 중간 규모의 event-driven workflow를 신속히 검증할 때
- AI assistant/agent에 CRM 갱신, 메시지 전송, 일정 생성 같은 governed action을 제공할 때
- Form, Table, approval을 하나의 managed workflow에 결합할 때

## When Not To Use

- 초고빈도 event processing, 대용량 ETL, millisecond latency가 핵심일 때
- on-premise 또는 완전한 self-hosting이 필수일 때
- 정확한 transaction, ordering, idempotency, compensation semantics를 직접 통제해야 할 때
- 단계가 많은 workflow에서 per-task 비용이 자체 구현·다른 실행 모델보다 커질 때
- 장기 실행 compute나 복잡한 code 중심 integration이 대부분일 때

## Related Notes

- [[MOCs/Index]]
- [[MOCs/Devtools]]
- [[../ripgrep/README|ripgrep]] — automation code와 설정을 빠르게 탐색하는 CLI
- [[../../ai/codex/README|Codex]] — MCP/CLI action을 사용하는 coding agent 맥락
- [[../../ai/agent-orchestration/cli-agents|CLI agents]] — agent tool orchestration 패턴

## Sources

- [What is Zapier?](https://help.zapier.com/hc/en-us/articles/37518970271245-What-is-Zapier)
- [What is a Zap?](https://help.zapier.com/hc/en-us/articles/8496309697421-What-is-a-Zap)
- [Zapier App Directory](https://zapier.com/apps)
- [Zapier MCP guide](https://zapier.com/blog/zapier-mcp-guide/)
- [Zapier task usage rates](https://zapier.com/pricing/rates)

