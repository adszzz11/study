---
date: 2026-08-17
tags: [tech]
type: tech-tool-study
status: draft
---

# CodeBurn — Overview

> [[README|목차로 돌아가기]] · [[02-ecosystem|다음: Ecosystem]]

## What

CodeBurn은 AI coding tool이 디스크에 남긴 session transcript를 찾아 token, 추정 비용, tool usage, task 유형, delivery proxy로 변환하는 local-first observability 도구다. 분석을 위해 coding tool 앞에 proxy나 wrapper를 설치할 필요가 없다.

주요 입력은 다음과 같다.

| Provider 예시 | 대표 local data |
|---|---|
| Claude Code | `~/.claude/projects/.../*.jsonl` |
| Codex | `~/.codex/sessions/YYYY/MM/DD/rollout-*.jsonl` |
| Cursor | `state.vscdb` SQLite |
| OpenCode | `opencode*.db` SQLite |
| Gemini CLI | project별 session JSON |

## Why

AI coding 비용은 일반 API bill보다 원인을 추적하기 어렵다.

- 여러 agent와 IDE의 usage가 서로 다른 JSONL, JSON, SQLite에 흩어진다.
- bill은 총액을 보여도 어느 project, task, model, retry가 비용을 만들었는지 충분히 설명하지 않는다.
- input/output 외에 cache read/write, reasoning, web search, subscription-covered usage가 섞인다.
- 높은 token 사용량이 높은 생산성을 뜻하지 않는다. 반복 수정, 중복 read, 과도한 context와 쓰이지 않는 MCP도 비용을 만든다.

CodeBurn의 핵심 가치는 **기존 workflow를 바꾸지 않는 cross-tool 사후 분석**이다. task classification은 tool usage와 user-message keyword에 기반한 deterministic rule로 수행되며, 공식 문서상 classification을 위한 LLM call은 없다.

## 핵심 특징

### Cross-tool cost breakdown

- provider, model, project, task별 token과 cost
- input, output, cache read, cache write, web search 분리
- cache hit rate, cost per call, cost per edit
- subscription/proxy coverage와 API-rate 추정 비용 분리

### Deterministic analytics

13개 task category를 사용한다.

| 범주 | 대표 신호 |
|---|---|
| Coding | Edit, Write tool |
| Debugging | error/fix keyword와 tool usage |
| Feature Dev | add, create, implement keyword |
| Testing | pytest, vitest, jest command |
| Exploration | edit 없이 Read, Grep, WebSearch |
| Planning | planning 관련 tool |
| Delegation | agent spawn |
| Git Ops | commit, push, merge |

그 밖에 Refactoring, Build/Deploy, Brainstorming, Conversation, General이 포함된다.

### Efficiency와 delivery proxy

- **One-shot rate**: edit 이후 test와 재수정으로 이어지는 retry cycle을 포착한다.
- **Self-correction**: model이 같은 흐름에서 자신의 실수를 수정한 turn을 본다.
- **Yield**: session timestamp와 Git commit을 연결해 Productive, Reverted, Abandoned로 추정한다.
- **Optimize**: duplicate/junk read, low Read:Edit ratio, bloated `CLAUDE.md`, unused MCP, ghost agent/skill/command, cache/context bloat, low-worth session, outlier를 찾는다.

> [!warning] Metric 해석
> One-shot rate와 Yield는 operational proxy다. 실제 코드 품질, 요구사항 난이도, 사람의 검토 기여, business outcome을 직접 증명하지 않는다.

## 2026년 변화

| 시기 | 변화 |
|---|---|
| 2026-04 | Codex/provider plugin system, `optimize`, multi-provider 분석 |
| 2026-06 | MCP server, pricing gap-fill, proxy/subscription cost attribution |
| 2026-07 | `context`, `audit`, durable history/aggregation, UI 합계 통일 |
| `v0.9.19` | CLI·TUI·Desktop·Web·Menubar가 공통 aggregation path 사용 |

## 한계와 주의점

- local log schema 변화에 parser가 민감하며 token, 날짜 경계, provider discovery issue가 계속 생길 수 있다.
- 비용은 대체로 `local log × price table` 추정치이지 provider invoice가 아니다.
- Cursor Auto, Kiro, 일부 Copilot format처럼 model/token이 숨겨지면 대체 model이나 content length를 사용한다.
- local-first는 offline-only와 동의어가 아니다. 설치, update, pricing refresh, optional telemetry와 preview sync는 network를 쓸 수 있다.
- transcript와 cache 자체가 민감 정보일 수 있으므로 filesystem permission과 backup 범위를 점검해야 한다.

## Sources

- https://codeburn.app/docs
- https://codeburn.app/docs/models
- https://codeburn.app/docs/compare
- https://codeburn.app/docs/yield
- https://codeburn.app/docs/optimize
- https://github.com/getagentseal/codeburn/blob/main/CHANGELOG.md

