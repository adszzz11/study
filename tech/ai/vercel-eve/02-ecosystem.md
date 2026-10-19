---
date: 2026-10-19
tags: [tech]
type: tech-tool-study
status: draft
---

# Vercel eve — Ecosystem

> [[README|목차로 돌아가기]]

## Comparison

| 항목 | eve | LangGraph | CrewAI | Vercel AI SDK 단독 |
|---|---|---|---|---|
| 주 언어/모델 | TypeScript, filesystem-first agent app | Python/JS, graph orchestration | 주로 Python, role/crew 중심 | TypeScript, model/UI/tool primitives |
| Durable runtime | 기본 내장 | persistence·fault tolerance 제공 | 별도 운영 설계 비중 큼 | 별도 workflow/runtime 필요 |
| Sandbox·approval | framework 핵심 구성요소 | 직접 조합하는 경우가 많음 | 직접 조합 비중 큼 | 직접 통합 필요 |
| Multi-channel | Web/API/Slack 등 channel abstraction | 구현·통합 선택 | crew/flow 중심 통합 | UI·streaming 중심 |
| 배포 성격 | Vercel managed path 최적화, self-host 가능 | 다양한 deployment, 높은 제어력 | 빠른 multi-agent prototyping | agent framework가 아닌 toolkit |
| 적합한 경우 | TS/Vercel production agent | graph 기반 복합 workflow | 역할 기반 실험·업무 flow | 기존 app의 AI interaction |

## Selection Guide

- **eve**: channel, sandbox, approval, durable execution을 opinionated convention으로 묶고 싶을 때 적합하다.
- **LangGraph**: deterministic step과 agentic step의 graph를 명시적으로 조합하고, runtime 구조를 세밀하게 통제하려 할 때 적합하다.
- **CrewAI**: 역할과 delegation을 중심으로 multi-agent workflow를 빠르게 실험할 때 적합하다.
- **Vercel AI SDK**: streaming UI, model provider abstraction, tool calling을 기존 web application에 추가하되 agent runtime은 직접 선택할 때 적합하다.

## Adoption Caveat

eve는 public preview다. API와 integration behavior를 영구 전제로 두지 말고, version을 pin하고 release note를 검토하며 eval 및 staged deployment로 변경을 흡수한다.

## Sources

- https://eve.dev/
- https://www.langchain.com/oss-overview
- https://github.com/vercel/eve/releases
- https://vercel.com/platform
