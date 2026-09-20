---
date: 2026-09-20
tags: [tech]
type: tech-tool-study
status: draft
---

# Claude-Mem

> **한 줄 정의**: Claude-Mem은 coding agent의 tool usage와 session 결과를 자동 수집·AI compression한 뒤 SQLite/Chroma에 보존하고, 다음 session에 관련 context를 다시 주입하는 open-source persistent memory plugin이다.

## Overview

LLM coding agent는 `/clear`, 재접속, context compaction을 거치면 이전 session의 조사 결과와 실패한 접근, architecture decision, 변경 파일을 잃기 쉽다. Claude-Mem은 hook으로 실제 작업을 capture하고 structured observation과 session summary로 압축해 장기 보존한다.

```text
작업 수행
  → tool event 자동 capture
  → AI observation/summary compression
  → SQLite + optional Chroma 저장
  → 다음 session에 관련 context injection
  → MCP search로 과거 기록 탐색
```

핵심은 사용자가 memory 문서를 매번 관리하는 대신 agent의 실제 작업 흔적을 자동 축적하는 것이다. Anthropic 공식 기능이 아니라 Alex Newman이 관리하는 community project이며, Claude Code built-in auto memory를 대체한다기보다 더 촘촘한 activity timeline과 검색 계층을 보강한다.

> [!NOTE]
> 조사 기준일은 2026-09-20이다. `main`의 manifest는 v13.25.2지만 GitHub Releases 화면의 최근 release는 v13.24.23으로, 배포 채널 사이에 시차가 있다. Grok Bot용 제품명은 “Grok Mem”으로 확장됐지만 npm package와 repository 이름은 `claude-mem`이다.

## Learning Path

- [ ] [[01-overview|Overview]] — 문제, 핵심 기능, architecture와 security boundary 이해
- [ ] [[02-ecosystem|Ecosystem]] — Claude Code auto memory 및 수동 memory 방식과 비교
- [ ] [[03-references|References]] — 공식 문서와 source code의 읽기 순서 확인
- [ ] [[04-learning/01-getting-started|Getting Started]] — 설치 전 검토, 설치, capture와 retrieval 검증
- [ ] [[04-learning/02-deep-dive|Deep Dive]] — hook, worker, storage, progressive disclosure 분석
- [ ] [[05-projects|Projects]] — 작은 pilot부터 운영 가능한 workflow로 확장
- [ ] [[cheatsheet|Cheatsheet]] — 경로, port, event, 검색 순서를 빠르게 참조

## When To Use

- 여러 session에 걸친 bugfix, migration, refactor의 조사 맥락을 이어갈 때
- 실패한 접근과 architecture decision까지 자동으로 남기고 싶을 때
- 과거 작업을 keyword/semantic search와 timeline으로 탐색해야 할 때
- Claude Code 외 Cursor, OpenCode, Codex CLI 등 여러 host에서 공통 memory worker를 검토할 때
- 수동 `MEMORY.md`만으로는 activity history의 granularity가 부족할 때

## When Not To Use

- source code, prompt, tool output을 외부 AI provider로 전송할 수 없는 환경
- credential redaction과 retention policy를 정의하지 못한 proprietary project
- 짧은 일회성 작업이라 persistent history의 가치가 설치·운영 비용보다 작을 때
- unauthenticated local worker를 loopback 밖에 노출해야 하는 환경
- 빠른 release cadence를 감당할 version pinning, backup, upgrade test가 없는 production rollout

## Related Notes

- [[MOCs/Index]]
- [[MOCs/Devtools]]
- [[tech/ai/model-context-protocol-mcp/README|Model Context Protocol (MCP)]] — 과거 observation을 단계적으로 조회하는 search interface
- [[tech/ai/agent-orchestration/cli-agents|CLI Agents]] — coding agent host와 tool integration 맥락
- [[tech/ai/llm-wiki-study/README|LLM Wiki Study]] — 장기 지식과 session memory의 차이

## Sources

- https://github.com/thedotmack/claude-mem
- https://github.com/thedotmack/claude-mem/blob/main/package.json
- https://github.com/thedotmack/claude-mem/releases
- https://github.com/thedotmack/claude-mem/blob/main/docs/public/installation.mdx
- https://github.com/thedotmack/claude-mem/blob/main/docs/public/configuration.mdx
- https://github.com/thedotmack/claude-mem/blob/main/SECURITY.md
- https://code.claude.com/docs/en/memory
