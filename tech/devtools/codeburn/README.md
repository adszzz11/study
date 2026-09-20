---
date: 2026-08-17
tags: [tech]
type: tech-tool-study
status: draft
---

# CodeBurn

> **한 줄 정의**: CodeBurn은 Claude Code, Codex, Cursor 등 AI coding tool의 로컬 session log를 읽어 token 사용량·추정 비용·작업 유형·model 효율·delivery 성과를 분석하는 local-first AI coding observability 도구다.

## Overview

- 이 노트의 **CodeBurn**은 legacy modernization 업체가 아니라 AgentSeal의 open-source 프로젝트 [`getagentseal/codeburn`](https://github.com/getagentseal/codeburn)을 뜻한다.
- API proxy나 wrapper를 끼우지 않고 JSONL, JSON, SQLite로 남은 기존 session transcript를 사후 분석한다.
- provider별 데이터를 session/call/tool 단위로 정규화한 뒤 pricing, deterministic task classification, daily aggregation을 적용한다.
- TUI, CLI, Web, Desktop, macOS Menubar, GNOME, JSON/CSV, MCP surface를 제공한다.
- 조사 기준일은 **2026-08-17**이다. npm stable `v0.9.19`는 36 integrations로 표시하지만 `main`과 공식 문서는 40 integrations를 표기하므로, 설치 버전의 `--version`과 `--help`를 우선한다.

```text
local logs → provider adapters → normalized data → pricing/classification
           → durable cache → TUI/CLI/Web/Desktop/Export/MCP
```

## Learning Path

- [ ] [[01-overview|Overview]] — What/Why, 핵심 기능과 한계
- [ ] [[02-ecosystem|Ecosystem]] — ccusage, Tokscale, provider dashboard 등과 비교
- [ ] [[03-references|References]] — 공식 문서와 검증 포인트
- [ ] [[04-learning/01-getting-started|Getting Started]] — 안전한 설치와 첫 baseline
- [ ] [[04-learning/02-deep-dive|Deep Dive]] — adapter, deduplication, pricing, heuristic 해석
- [ ] [[05-projects|Projects]] — 개인·팀 단위 관찰 프로젝트
- [ ] [[cheatsheet|Cheatsheet]] — 자주 쓰는 명령과 판단 규칙

## When To Use

- Claude Code, Codex, Cursor처럼 여러 AI coding tool의 비용을 한곳에서 비교할 때
- provider bill의 총액을 project, model, task, retry loop 수준으로 분해하고 싶을 때
- wrapper 도입 없이 이미 존재하는 local logs로 빠르게 baseline을 만들 때
- cache hit, one-shot rate, cost per edit, expensive session을 운영 지표로 추적할 때
- `optimize`로 duplicate read, context bloat, unused MCP 같은 낭비 후보를 찾을 때
- Git history가 있는 repository에서 session spend와 delivery 사이의 상관을 탐색할 때

## When Not To Use

- provider invoice와 1센트까지 일치하는 회계·청구 근거가 필요할 때
- 실제 코드 품질, business value, 개인 성과를 하나의 heuristic 점수로 판정하려 할 때
- session transcript와 cache를 보관할 로컬 환경의 접근 통제가 충분하지 않을 때
- provider schema가 바뀐 직후처럼 parser 정확성을 검증하지 못한 상태일 때
- 완전한 offline-only 실행이 필수인데 pricing refresh, update, optional telemetry/sync의 network 동작을 통제하지 못할 때

## Related Notes

- [[MOCs/Index]]
- [[MOCs/Devtools]]
- [[../../ai/codex/README|Codex]] — CodeBurn이 분석하는 대표 AI coding agent
- [[../ripgrep/README|ripgrep]] — local-first CLI workflow와 구조화된 출력의 비교 사례

## Sources

- https://codeburn.app/docs
- https://github.com/getagentseal/codeburn
- https://www.npmjs.com/package/codeburn
- https://github.com/getagentseal/codeburn/blob/main/CHANGELOG.md
- https://github.com/getagentseal/codeburn/blob/main/package.json

