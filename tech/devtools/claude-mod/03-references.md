---
date: 2026-10-04
tags: [tech]
type: tech-tool-study
status: draft
---

# Claude Mod References

## 공식 발표와 가이드

1. [Customize Claude Code with mods in TypeScript — Anthropic, 2026-10-01](https://claude.com/blog/claude-code-mods) — 개념, UI와 runtime extension의 범위, 보안 경고.
2. [Getting started with Claude Code mods — Claude.dev](https://claude.dev/blog/getting-started-with-claude-code-mods/) — Token Weather를 만드는 단계별 실습, validation과 test.
3. [Extend Claude Code — Features overview](https://code.claude.com/docs/en/features-overview) — Skills, Hooks, MCP, Plugins의 선택 기준.
4. [Claude Code plugins — Anthropic](https://claude.com/blog/claude-code-plugins) — plugin과 marketplace의 배경.
5. [Claude Marketplace](https://claude.com/marketplace/plugins) — 배포/발견 surface.

## Source Code와 API

1. [Mods README](https://github.com/anthropics/claude-code/blob/main/mods/README.md) — built-in Mod, plugin layout, test kit, composition contract.
2. [function-hooks TypeScript declarations](https://github.com/anthropics/claude-code/blob/main/mods/types/claude-code.d.ts) — event와 engine API type의 source reference.
3. [Built-in Mods directory](https://github.com/anthropics/claude-code/tree/main/mods) — `diff`, `telemetry`, `sec-default`, `agents-md` 구현 사례.
4. [Function hooks design/community update](https://github.com/anthropics/claude-code/issues/91870) — composition/order 관련 설계 논의.

## Community

- [awesome-claude-code-mods](https://github.com/karanb192/awesome-claude-code-mods) — 아이디어 탐색용 catalogue. 설치 전에는 반드시 code와 dependency를 독립 검토한다.

## 읽는 순서

공식 getting-started → built-in `diff` source → type declaration → feature overview → community 사례 순서가 좋다. API는 early access 성격으로 변경될 수 있으므로, 설치한 Claude Code가 생성한 `.claude-plugin/types/`를 최종 기준으로 삼는다.
