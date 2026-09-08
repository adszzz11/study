---
date: 2026-09-08
tags: [tech]
type: tech-tool-study
status: draft
---

# Ruflo

> **한 줄 정의**: Ruflo는 Claude Code·Codex 같은 coding agent에 multi-agent swarm, persistent memory, MCP tools, hooks, policy/security layer를 더하는 오픈소스 **agent meta-harness / orchestration platform**이다.

## Overview

Ruflo는 새로운 foundation model이나 범용 application framework가 아니다. 기존 coding agent 주위에 execution layer를 두고 작업 분해, agent routing, 공유 memory, lifecycle hook, tool policy와 audit를 조율한다.

```text
User
  ↓
Ruflo CLI / MCP
  ↓
Hooks · Router · Workflow
  ↓
Swarm Coordinator
  ↓
Specialized Agents
  ↓
AgentDB / RuVector Memory
  ↓
Claude · OpenAI · Gemini · Local LLM
  ↑
Learning / Routing Feedback Loop
```

> [!warning] Version snapshot
> 조사 기준일은 **2026-09-08**이며 npm `latest`는 **3.38.23**이다. 저장소 일부 문서에는 `3.31.0` 또는 `3.5.0`이 남아 있으므로 설치 전 `npm view ruflo version`으로 재확인한다. agent·command·plugin·MCP tool 개수도 릴리스마다 달라질 수 있다.

## Learning Path

- [ ] [[01-overview|1. What/Why와 핵심 아키텍처]]
- [ ] [[02-ecosystem|2. 대안 도구와 선택 기준]]
- [ ] [[03-references|3. 공식 자료와 검증 순서]]
- [ ] [[04-learning/01-getting-started|4. 안전한 sandbox에서 시작하기]]
- [ ] [[04-learning/02-deep-dive|5. swarm·memory·hooks·guidance 심화]]
- [ ] [[05-projects|6. 작은 프로젝트로 검증하기]]
- [ ] [[cheatsheet|7. 명령·개념 치트시트]]

## When To Use

- 하나의 coding task를 research, implementation, test, review 역할로 분해하고 병렬 조율할 때
- Claude Code·Codex 등 기존 coding agent를 교체하지 않고 swarm과 persistent memory를 덧붙일 때
- MCP, hooks, workflow를 통해 여러 client의 실행 방식을 한 곳에서 관리할 때
- 반복되는 project pattern과 작업 trajectory를 session 사이에서 재사용할 때
- destructive operation, secret, budget, audit에 공통 policy gate가 필요할 때

## When Not To Use

- 단일 agent와 짧은 context로 충분한 작은 수정: orchestration overhead가 더 클 수 있다.
- state transition을 코드로 엄밀하게 정의하는 production application runtime이 필요한 경우: LangGraph 같은 graph runtime이 더 직접적이다.
- 최소 SDK로 handoff와 tracing만 구현하려는 경우: OpenAI Agents SDK 같은 작은 abstraction이 적합할 수 있다.
- subsystem maturity, dependency provenance, secret handling을 별도로 검증할 여력이 없는 production 환경
- 많은 MCP tools를 모두 노출해도 된다고 가정하는 환경: context 비용과 attack surface가 커진다.

## Related Notes

- [[MOCs/Index]]
- [[MOCs/AI]]
- [[tech/ai/model-context-protocol-mcp/README|Model Context Protocol (MCP)]]
- [[tech/ai/agent-orchestration/cli-agents|CLI Agents]]
- [[tech/ai/litellm/README|LiteLLM]]

## Sources

- [Ruflo official README](https://github.com/ruvnet/ruflo/blob/main/README.md)
- [Ruflo npm package and versions](https://www.npmjs.com/package/ruflo?activeTab=versions)
- [Ruflo changelog](https://github.com/ruvnet/ruflo/blob/main/CHANGELOG.md)
- [Ruflo configuration](https://github.com/ruvnet/ruflo/blob/main/v3/implementation/init/CONFIGURATION.md)
- [Ruflo core plugin](https://github.com/ruvnet/ruflo/blob/main/plugins/ruflo-core/README.md)
- [AgentDB plugin](https://github.com/ruvnet/ruflo/blob/main/plugins/ruflo-agentdb/README.md)
- [Guidance architecture overview](https://github.com/ruvnet/ruflo/blob/main/v3/%40claude-flow/guidance/docs/guides/architecture-overview.md)

