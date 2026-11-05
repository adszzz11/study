---
date: 2026-11-05
tags: [tech]
type: tech-tool-study
status: draft
---

# Cua Driver

> **한 줄 정의**: Cua Driver는 AI agent가 Accessibility tree, screenshot, native input, CDP를 통해 로컬 desktop application과 Chromium browser를 조작하게 하는 cross-platform computer-use tool layer이다.

## Overview

Cua Driver는 모델이나 agent loop가 아니라 Codex, Claude Code, Cursor 같은 agent harness가 호출하는 MCP/CLI/SDK runtime이다. UI 구조와 pixel 정보를 함께 관찰하고, 가능한 경우 named element action을 써서 API가 없는 GUI까지 자동화한다.

```text
Model → Agent harness → Cua Driver (MCP / CLI / SDK)
                       → OS Accessibility + native input + CDP
                       → desktop apps / Chromium browser
```

## Learning Path

- [ ] [[tech/ai/cua-driver/01-overview|Overview]] — 역할, 동작 loop, 핵심 특징을 이해한다.
- [ ] [[tech/ai/cua-driver/02-ecosystem|Ecosystem]] — Computer Use, Playwright 등과 선택 기준을 비교한다.
- [ ] [[tech/ai/cua-driver/04-learning/01-getting-started|시작하기]] — 환경 진단과 Calculator 안전 실습을 한다.
- [ ] [[tech/ai/cua-driver/04-learning/02-deep-dive|심화]] — browser binding, 권한, 검증 loop를 설계한다.
- [ ] [[tech/ai/cua-driver/05-projects|Projects]] — GUI gap에 맞는 적용 패턴을 검토한다.
- [ ] [[tech/ai/cua-driver/03-references|References]] — 공식 문서와 안전 가이드를 확인한다.
- [ ] [[tech/ai/cua-driver/cheatsheet|Cheatsheet]] — 명령과 production checklist를 빠르게 찾는다.

## When To Use

- legacy ERP/CRM, PDF viewer, spreadsheet, design tool처럼 API가 없거나 불완전한 desktop GUI를 agent가 다뤄야 할 때
- 사람이 login한 Chromium profile의 정해진 tab을 안전 경계 안에서 조작할 때
- API 또는 Playwright workflow의 마지막 GUI gap만 보완할 때

## When Not To Use

- 안정적인 API, MCP, database query가 이미 있는 작업: UI보다 구조화된 interface를 우선한다.
- 웹만 대상으로 한 deterministic regression test: locator와 test tooling이 강한 Playwright가 더 알맞다.
- irreversible submit, 결제, 민감 데이터 변경을 사람 승인·검증 없이 처리해야 하는 작업

## Related Notes

- [[MOCs/Index]]
- [[MOCs/AI]]
- [[tech/ai/model-context-protocol-mcp/README|Model Context Protocol (MCP)]]

## Sources

- https://cua.ai/docs/cua-driver
- https://cua.ai/docs/cua-driver/concepts/how-cua-driver-works
- https://cua.ai/docs/cua-driver/guides/permissions
- https://github.com/trycua/cua
