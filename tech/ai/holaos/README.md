---
date: 2026-08-17
tags: [tech]
type: tech-tool-study
status: draft
---

# holaOS

> **한 줄 정의**: holaOS는 AI agent가 장기간 작업할 수 있도록 Desktop UI, workspace contract, durable memory, Apps/MCP, Skills, Automations와 교체 가능한 Agent Harness를 결합한 local-first agent workspace다.

## Overview

holaOS는 Claude Code나 Codex 같은 개별 agent를 대체하는 단일 model이 아니라, agent가 여러 session에 걸쳐 일할 수 있게 **실행 환경을 지속시키는 workspace layer**다. 프로젝트는 이 접근을 **Environment Engineering**이라고 부른다.

핵심은 다음 항목을 chat history 밖의 명시적인 contract와 runtime state로 분리하는 데 있다.

- `workspace.yaml`: model, Apps, Skills, Commands, MCP registry
- `AGENTS.md`: 항상 적용되는 standing instructions와 policy
- Runtime: session, queue, binding, memory proposal, capability projection
- Harness: Runtime이 compile한 실행 package를 받아 실제 agent loop 수행
- Apps/MCP: Gmail, GitHub, browser 같은 외부 capability 연결
- Automations: cron 또는 event trigger로 workspace task 실행

```text
Desktop → Workspace Contract → Runtime Services → Harness Host → Model + Tools
```

> [!warning] 조사 기준
> 이 노트는 **2026-08-17** 기준이다. Desktop manifest가 아직 `0.1.0`인 초기 프로젝트이므로 설치 방법, 지원 platform, provider와 harness 구현 범위는 도입 직전에 공식 문서와 repository에서 다시 확인한다.

## Learning Path

- [ ] [[01-overview|Overview]] — What/Why, architecture, 특징과 한계 이해
- [ ] [[02-ecosystem|Ecosystem]] — agent harness, framework, MCP host와 역할 비교
- [ ] [[03-references|References]] — 공식 문서와 license 원문 확인
- [ ] [[04-learning/01-getting-started|Getting Started]] — workspace contract 초안과 안전한 검증 순서
- [ ] [[04-learning/02-deep-dive|Deep Dive]] — run compilation, memory, capability projection 분석
- [ ] [[05-projects|Projects]] — 장기 research workspace부터 단계별 구현
- [ ] [[cheatsheet|Cheatsheet]] — 파일, 상태 계층, 보안 질문 빠른 참조

## When To Use

- research, content, inbox, 운영 업무가 여러 날과 여러 session에 걸쳐 이어질 때
- Claude Code, Codex, 내장 agent 사이에서 policy, Skills, Apps를 공유하고 싶을 때
- local workspace를 중심으로 MCP와 외부 SaaS를 함께 운영할 때
- facts, user preference, 최근 진행 상태와 authored policy를 서로 다른 수명으로 관리해야 할 때
- 재사용 가능한 agent 환경을 Template 또는 App으로 배포하려 할 때

## When Not To Use

- 한 번의 prompt나 짧은 coding session이면 충분할 때
- mature한 enterprise support, 객관적 benchmark, 장기 안정성이 필수일 때
- signed Desktop이 필요한데 macOS Apple Silicon 외 platform의 설치 완성도를 직접 검증할 여유가 없을 때
- cloud provider로 context가 전송되면 안 되지만 Ollama 기반 local inference를 구성할 수 없을 때
- 제3자 대상 SaaS나 상용 제품에 embedded하려는데 Modified Apache 2.0의 commercial 조건을 검토하지 않았을 때

## Related Notes

- [[MOCs/Index]]
- [[MOCs/AI]]
- [[tech/ai/model-context-protocol-mcp/README|Model Context Protocol (MCP)]] — Apps와 외부 tool을 연결하는 protocol layer
- [[tech/ai/litellm/README|LiteLLM]] — model/provider routing을 별도 gateway로 둘 때 비교할 노트
- [[tech/ai/agent-garden|Agent Garden]] — 재사용 가능한 agent 환경과 workflow를 함께 살펴볼 노트

## Sources

- [holaOS 공식 개요](https://www.holaos.ai/docs/getting-started)
- [Concepts: Environment Engineering](https://www.holaos.ai/docs/concepts/concepts)
- [Quick Start](https://www.holaos.ai/docs/getting-started/quick-start)
- [GitHub repository](https://github.com/holaboss-ai/holaOS)
- [INSTALL.md](https://github.com/holaboss-ai/holaOS/blob/main/INSTALL.md)
- [Workspace Model](https://www.holaos.ai/docs/concepts/workspace-model)
- [Memory and Continuity](https://www.holaos.ai/docs/concepts/memory-and-continuity)
- [Run Compilation](https://www.holaos.ai/docs/contribute/runtime/run-compilation)
- [Runtime Tools](https://www.holaos.ai/docs/concepts/agent-harness/runtime-tools)
- [App Anatomy](https://www.holaos.ai/docs/build/apps/app-anatomy)

