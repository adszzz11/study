---
date: 2026-11-03
tags: [tech]
type: tech-tool-study
status: draft
---

# AI Agent·MCP·콘텐츠 자동화 시스템: Overview

[[tech/ai/ai-agent-automation-systems/README|README]]로 돌아가기 · [[tech/ai/ai-agent-automation-systems/02-ecosystem|Ecosystem 비교]]

## What

AI automation system은 LLM의 판단 능력에 업무 context와 tool을 연결하고, 정해진 단계는 workflow로 고정하며, 실행 전후에 승인·로그·평가를 두는 운영 구조다. 좋은 결과는 긴 prompt 하나보다 역할, 입력 형식, 참고 사례, 금지 범위, 완료 조건을 선명하게 주는 데서 나온다.

## Why

- 모델은 조직 문서, 현재 정보, 업무 규칙을 기본적으로 알지 못한다.
- 권한을 과하게 주면 잘못된 메일, 데이터 유출, 비용 폭주, 오작동이 생길 수 있다.
- 모든 단계를 Agent에게 맡기면 재현성과 감사 가능성이 낮아진다.

## Architecture

```text
Trigger / User request
        ↓
Context layer ─ project rules · memory · knowledge base · reference assets
        ↓
LLM Agent ─ planning · reasoning · tool selection
        ↓
Tools ─ MCP · search · code · DB · email · calendar · media generation
        ↓
Deterministic workflow ─ validation · approval · retries · logging
        ↓
Human approval / publish / action
        ↓
Evaluation + trace + durable memory
```

## 핵심 특징

| 요소 | 역할 | 설계 기준 |
|---|---|---|
| Context | 업무에 필요한 규칙·자료 제공 | 필요한 문서만 retrieval한다 |
| MCP / Skills | tool·data와 재사용 가능한 업무 절차 연결 | 공급망과 permission을 검증한다 |
| Agent | 모호한 입력의 계획·판단 | 출력 schema와 완료 기준을 둔다 |
| Workflow | 정해진 실행 순서 | retry, validation, idempotency를 둔다 |
| Human-in-the-loop | 고위험 action 통제 | publish 전 approval을 강제한다 |
| Observability | 개선·복구의 근거 | input/output, tool call, cost, failure를 기록한다 |

## Memory의 분리

대화 전체를 매번 넣지 않는다. project brief, decision log, style guide, retrieval 문서를 분리하고 run에 필요한 항목만 주입한다. 이 방식은 context 비용과 오래된 지시가 현재 판단을 오염시키는 일을 줄인다.

## Sources

- https://lazyowen.com/guides
- https://docs.anthropic.com/en/docs/mcp
- https://docs.n8n.io/advanced-ai/ai-agents/

