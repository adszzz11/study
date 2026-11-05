---
date: 2026-11-05
tags: [tech]
type: tech-tool-study
status: draft
---

# Cua Driver: Ecosystem

[[tech/ai/cua-driver/README|Cua Driver 목차]] · [[tech/ai/cua-driver/01-overview|Overview]] · [[tech/ai/cua-driver/03-references|References]]

## 비교

| 도구 | 주 범위 | 강점 | 선택 기준 |
|---|---|---|---|
| Cua Driver | 로컬 desktop + Chromium | background control, Accessibility+pixel, agent-neutral MCP | 실제 사용 중인 desktop app을 Codex/Claude Code가 조작할 때 |
| OpenAI Computer Use | hosted/local browser·desktop runtime | OpenAI API/agent stack 통합, hosted browser | OpenAI-managed environment 또는 자체 execution loop가 필요할 때 |
| Anthropic Computer Use | app이 소유한 실행 환경 | Claude tool protocol, client-controlled runtime | Claude 중심 custom agent runtime일 때 |
| Playwright | browser automation | deterministic locator, test tooling, cross-browser | 대상이 웹뿐이고 scriptable workflow일 때 |
| browser-use | LLM browser agent | agentic web navigation, hosted browser ecosystem | desktop app 없이 web task 중심일 때 |

## 선택 원칙

Cua Driver는 특정 모델이 제공하는 computer tool이 아니라 model-neutral runtime이다. GUI 범위는 Playwright보다 넓지만, 반복 가능한 웹 test의 결정성은 Playwright가 낫다. OpenAI의 안전 가이드처럼 UI 대신 API나 MCP가 있으면 그것을 먼저 사용하고, Cua Driver는 GUI가 유일한 경계일 때 배치한다.

## 함께 쓰는 구성

```text
API / MCP ── 구조화된 읽기·쓰기 (우선)
Playwright ─ 웹의 deterministic 단계
Cua Driver ─ desktop 또는 남은 GUI gap
Human       ─ login, submit, 비용·권한 승인
```

## Sources

- https://developers.openai.com/api/docs/guides/tools-computer-use
- https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool
- https://playwright.dev/docs/browsers
- https://cua.ai/docs/cua-driver
