---
date: 2026-09-08
tags: [tech]
type: tech-tool-study
status: draft
---

# Ruflo Ecosystem 비교

> [[01-overview|이전: 개요]] · [[README|목차]] · [[03-references|다음: 참고자료]]

## 비교의 기준

Ruflo는 **기존 coding agent를 강화하는 meta-harness**다. 아래 제품들은 일부 기능이 겹치지만 application runtime, SDK, research framework처럼 추상화 수준이 다르므로 feature count만 비교하면 안 된다.

| 제품 | 추상화/주 용도 | Ruflo 대비 강점 | Ruflo가 더 적합한 경우 |
|---|---|---|---|
| **LangGraph** | Python/JS low-level state graph, durable agent runtime | checkpoint, pause/resume, time travel, HITL, 명시적 graph control과 production runtime | Claude Code/Codex workspace에 swarm·memory·hooks를 빠르게 추가할 때 |
| **CrewAI** | Python high-level Crews + event-driven Flows | role·goal 기반 team을 application code로 설계하기 쉬움 | coding workspace, MCP, CLI, persistent developer memory가 중심일 때 |
| **Microsoft AutoGen** | message-driven agent framework/runtime | custom protocol과 multi-process/distributed runtime 연구 | 사전 구성된 coding role과 local project scaffolding이 필요할 때 |
| **OpenAI Agents SDK** | Agent, Runner, tools, handoffs, guardrails, tracing | 작고 명확한 SDK, OpenAI Responses와 tracing 통합 | 여러 coding-agent client와 local MCP ecosystem을 한 harness로 묶을 때 |

## 선택 질문

| 질문 | 선택 방향 |
|---|---|
| workflow state transition이 제품 logic의 핵심인가? | LangGraph |
| Python application 안에서 role-based team을 만들 것인가? | CrewAI |
| agent communication protocol/runtime를 직접 연구할 것인가? | AutoGen |
| OpenAI stack에서 작은 SDK와 handoff가 충분한가? | OpenAI Agents SDK |
| 이미 쓰는 coding agent와 repository workflow를 확장할 것인가? | Ruflo |

## Ruflo 내부 생태계

공식 README는 조사 시점에 35개 plugin을 열거한다.

| 영역 | 대표 plugin | 목적 |
|---|---|---|
| Core/orchestration | `ruflo-core`, `ruflo-swarm`, `ruflo-workflows` | CLI, coordination, workflow |
| Memory | `ruflo-agentdb`, `ruflo-rag-memory`, `ruflo-ruvector` | semantic memory, retrieval, vector engine |
| Security | `ruflo-security-audit`, `ruflo-aidefence` | audit, threat/security 검사 |
| Automation | `ruflo-autopilot`, `ruflo-loop-workers` | autonomous loop, background worker |
| Integration | `ruflo-browser`, `ruflo-federation` | browser와 분산/federated 기능 |
| Operations | `ruflo-cost-tracker`, `ruflo-metaharness` | cost 관찰, meta-harness 기능 |

Plugin은 command, skill, agent definition, 경우에 따라 자체 MCP server를 제공한다. **full CLI 설치 문서의 명령을 개별 plugin에 그대로 적용하지 말고**, 설치한 package의 help와 manifest를 확인한다.

## 함께 쓰는 방식

```text
Coding client (Claude Code / Codex)
  ├─ MCP → Ruflo orchestration and memory
  ├─ model calls → provider or LiteLLM gateway
  └─ repository → git, tests, CI

Ruflo workflow
  ├─ 필요하면 LangGraph service를 tool로 호출
  └─ external MCP servers를 제한된 namespace로 연결
```

- Ruflo와 MCP는 경쟁 관계가 아니다. MCP는 Ruflo가 capability를 노출하는 주요 surface다.
- LiteLLM은 provider routing/gateway, Ruflo는 agent/workflow orchestration에 초점이 있다.
- framework를 중첩할수록 tracing, retry, budget, ownership이 중복되므로 각 계층의 책임을 문서화한다.

## 평가 checklist

- [ ] 동일한 benchmark task를 single-agent baseline과 비교한다.
- [ ] 성공률뿐 아니라 token, latency, merge conflict, human review time을 기록한다.
- [ ] memory를 끈 run과 켠 run을 비교하고 stale retrieval을 검사한다.
- [ ] 필요한 MCP namespace만 allowlist한다.
- [ ] destructive tool과 secret 접근에 실제 denial test를 수행한다.
- [ ] 내부 alpha dependency와 upgrade/rollback 경로를 확인한다.

## Sources

- https://github.com/ruvnet/ruflo/blob/main/README.md
- https://github.com/ruvnet/ruflo/blob/main/plugins/ruflo-core/README.md
- https://github.com/ruvnet/ruflo/blob/main/package.json
- https://github.com/ruvnet/ruflo/blob/main/v3/implementation/init/CONFIGURATION.md

