---
date: 2026-10-11
tags: [tech]
type: tech-tool-study
status: draft
---

# DeerFlow — References

> [[README|목차로 돌아가기]]

## 공식 시작점

| 자료 | 확인 목적 |
|---|---|
| [GitHub repository / README](https://github.com/bytedance/deer-flow) | 설치, repository 구성, license, 현재 변경사항 |
| [Documentation](https://deerflow.tech/en/docs) | 문서의 전체 진입점 |
| [Core Concepts](https://deerflow.tech/en/docs/introduction/core-concepts) | Harness, App, agent runtime 용어 |
| [v2.0.0 release](https://github.com/bytedance/deer-flow/releases/tag/v2.0.0) | 1.x와 2.x의 전환 배경 |
| [v2.1.x releases](https://github.com/bytedance/deer-flow/releases) | durable batch delegation, memory, extension, auth 변화 |

## Harness와 운영

- [Harness](https://deerflow.tech/en/docs/harness) — package release 상태와 runtime 범위
- [Design Principles](https://deerflow.tech/en/docs/harness/design-principles) — middleware-first 설계
- [Subagents](https://deerflow.tech/en/docs/harness/subagents) — isolated context와 delegation
- [Tools](https://deerflow.tech/en/docs/harness/tools) — tool category와 설정
- [Skills](https://deerflow.tech/en/docs/harness/skills) — `SKILL.md` package와 loading
- [Sandbox](https://deerflow.tech/en/docs/harness/sandbox) — LocalSandbox/AIO/E2B 경계
- [Integration Guide](https://deerflow.tech/en/docs/harness/integration-guide) — LangGraph와 state persistence
- [Memory Tutorial](https://deerflow.tech/en/docs/tutorials/work-with-memory) — memory middleware와 tool mode

## Application과 정책

- [App Quick Start](https://deerflow.tech/en/docs/application/quick-start) — Python 3.12+, Node.js 22+, `uv`, `pnpm`, nginx, LLM API key 요구사항
- [MIT License](https://github.com/bytedance/deer-flow/blob/main/LICENSE) — 배포·수정 전 license 원문 확인

> release note와 online 문서는 빠르게 바뀐다. 설치 명령, provider 지원, package 배포 상태, security option은 실행 직전에 공식 원문으로 다시 확인한다.

## 추가 조사: Orchestration 운영·검증 자료

| 자료 | 확인 목적 |
|---|---|
| [DeerFlow v2.1.0 release](https://github.com/bytedance/deer-flow/releases/tag/v2.1.0) | verifiable execution, durable batch delegation, scheduling, trace ID의 release-level 변경 확인 |
| [DeerFlow Subagents](https://deerflow.tech/en/docs/harness/subagents) | delegation limit, timeout/turn/token budget, managed/custom subagent allowlist 확인 |
| [DeerFlow Configuration](https://deerflow.tech/en/docs/harness/configuration) | subagent, checkpointer, guardrail, sandbox 설정 surface 확인 |
| [LangGraph Persistence](https://langchain-ai.github.io/langgraph/concepts/durable_execution/) | checkpoint와 cross-thread store의 역할 분리, resume/fault tolerance 원리 확인 |
| [LangGraph Interrupts](https://langchain-ai.github.io/langgraph/concepts/breakpoints/) | human-in-the-loop pause/resume을 durable state transition으로 구현하는 방식 확인 |

> 버전 주의: `batch_task`, receipt, scheduling, custom/managed subagent 관련 설정은 빠르게 바뀔 수 있다. 설계를 채택하거나 config를 적용하기 전에 위 원문의 현재 버전과 release note를 함께 대조한다.
