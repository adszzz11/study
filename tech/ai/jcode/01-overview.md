---
date: 2026-10-21
tags: [tech]
type: tech-tool-study
status: draft
---

# Jcode — 개요

> [[README|목차로 돌아가기]] | [[02-ecosystem|다음: 생태계]]

## What

Jcode는 Rust native TUI와 daemon/client 구조를 갖춘 AI coding-agent harness다. daemon은 session, provider request, tool 실행을 계속 보유하고 TUI는 Unix socket client로 붙는다. `jcode serve`를 실행한 원격 Linux host에 SSH socket forwarding으로 연결하는 운영도 가능하다.

## Why

동일한 LLM도 context 구성, tool loop, memory, 검증, session 지속 방식에 따라 작업 품질이 달라진다. Jcode는 한 agent의 응답을 기다리는 흐름 대신 독립 작업을 swarm으로 병렬화하고, 추가 session의 memory overhead를 낮추는 데 초점을 둔다.

## Key Features

| 영역 | 기능 | 실무상 의미 |
|---|---|---|
| Collaboration | swarm, DM, broadcast, sub-swarm, 파일 변경 알림 | task를 ownership별로 나눠 병렬 조사·구현 |
| Providers | Claude, OpenAI/Codex, Gemini, Copilot, Azure OpenAI, Ollama, LM Studio, OpenAI-compatible endpoint | model/provider를 작업 기준으로 비교 |
| Context | embedding 기반 semantic memory, `AGENTS.md`, `SKILL.md` | 긴 작업의 규칙·이력을 재활용 |
| Long-running work | background task persistence, unfinished todo의 `auto-poke` | build/test가 오래 걸려도 세션 유지 |
| Extensibility | project/global `mcp.json`, HTTP/SSE remote MCP, TypeScript SDK | tool 및 dashboard/CI 통합 |

## Architecture

```text
TUI client ── Unix socket ── Jcode daemon
                               ├─ sessions / swarm messages / memory
                               ├─ provider adapters
                               ├─ filesystem · shell · MCP tools
                               └─ background build/test tasks
```

daemon은 편리한 지속성을 제공하지만 sandbox가 아니다. SDK instance와 tool은 실행 사용자 권한으로 파일·shell에 접근할 수 있으므로, untrusted code/prompt에는 container 또는 VM 격리와 approval policy가 필요하다.

## Sources

- https://jcode.sh/docs
- https://jcode.sh/docs/commands
- https://jcode.sh/sdk
- https://github.com/1jehuang/jcode
