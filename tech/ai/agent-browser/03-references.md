---
date: 2026-09-20
tags: [tech]
type: tech-tool-study
status: draft
---

# Agent Browser — References

> [[02-ecosystem|이전: Ecosystem]] · [[README|목차로 돌아가기]] · [[04-learning/01-getting-started|다음: Getting Started]]

> 조사 기준일: 2026-09-20. 제품 API와 preview 표준은 변경될 수 있으므로 실제 도입 전 공식 문서를 다시 확인한다.

## 먼저 읽을 자료

| 순서 | 자료 | 읽을 포인트 |
|---|---|---|
| 1 | [OpenAI — Computer-Using Agent](https://openai.com/index/computer-using-agent/) | visual control의 작동 방식, benchmark와 한계 |
| 2 | [Playwright MCP](https://github.com/microsoft/playwright-mcp) | accessibility snapshot, tool interface, runtime mode, security 경고 |
| 3 | [Stagehand](https://github.com/browserbase/stagehand) | deterministic code와 AI primitive의 조합 |
| 4 | [Browser Use](https://github.com/browser-use/browser-use) | Python agent loop와 optional vision |
| 5 | [WebMCP early preview](https://developer.chrome.com/blog/webmcp-epp) | declarative/imperative semantic tool 방향 |
| 6 | [WebMCP security](https://developer.chrome.com/docs/agents/security) | malicious manifest, contaminated output, origin restriction, confirmation |
| 7 | [Anthropic prompt-injection defenses](https://www.anthropic.com/news/prompt-injection-defenses) | browser-use 공격과 defense-in-depth 필요성 |

## Foundation: deterministic automation

- [Playwright Documentation](https://playwright.dev/docs/intro) — locator, auto-wait, browser context, trace, assertion의 기준선
- [Playwright Locators](https://playwright.dev/docs/locators) — role·label·text 기반 locator의 우선순위
- [Playwright Authentication](https://playwright.dev/docs/auth) — storage state 재사용과 민감 정보 취급
- [Selenium Documentation](https://www.selenium.dev/documentation/) — WebDriver 기반 browser automation 생태계
- [W3C WebDriver](https://www.w3.org/TR/webdriver2/) — browser remote control 표준

## Agent framework와 interface

- [Microsoft — Playwright MCP](https://github.com/microsoft/playwright-mcp) — MCP 기반 structured browser automation
- [Browserbase — Stagehand](https://github.com/browserbase/stagehand) — `act`, `extract`, `observe`와 Playwright-style API
- [Browser Use](https://github.com/browser-use/browser-use) — open-source browser agent framework
- [Anthropic — Computer Use](https://docs.anthropic.com/en/docs/agents-and-tools/tool-use/computer-use-tool) — computer tool의 loop와 보안 고려사항
- [OpenAI — Introducing ChatGPT agent](https://openai.com/index/introducing-chatgpt-agent/) — visual browser, text browser, terminal, connectors의 hybrid product architecture

## WebMCP

- [Chrome for Developers — WebMCP early preview](https://developer.chrome.com/blog/webmcp-epp) — 2026-02-10 공개된 early preview 개요
- [WebMCP GitHub organization](https://github.com/webmachinelearning/webmcp) — proposal과 공개 artifact 추적
- [Chrome for Developers — Agent security considerations](https://developer.chrome.com/docs/agents/security) — agent developer용 defense-in-depth 지침

## Security와 evaluation

- [Anthropic — Mitigating prompt injections in browser use](https://www.anthropic.com/news/prompt-injection-defenses) — 공격 성공률을 0으로 가정할 수 없는 이유
- [OWASP — Top 10 for LLM Applications](https://genai.owasp.org/llm-top-10/) — prompt injection, excessive agency, sensitive information disclosure 배경
- [WebArena](https://webarena.dev/) — realistic web task benchmark
- [BrowserGym](https://github.com/ServiceNow/BrowserGym) — browser agent 연구·평가 환경
- [BrowserBench](https://browserbench.org/) — browser 성능 benchmark이며 agent task 성공률과는 다른 지표임에 주의

## 자료를 읽을 때 확인할 질문

- Observation은 screenshot, DOM, accessibility tree, tool 중 무엇인가?
- Action reference가 coordinate, selector, role, stable element id 중 무엇인가?
- 성공은 model self-report가 아니라 무엇으로 검증하는가?
- Browser session, cookie, download, secret은 어디에 저장되는가?
- Cross-origin navigation과 data transfer를 어떻게 제한하는가?
- Purchase, send, publish, delete 직전 approval gate가 있는가?
- Trace, screenshot, network event를 재현 가능한 형태로 남기는가?
- Benchmark가 실제 target site와 auth 조건을 대표하는가?

## 인용 메모

- OpenAI CUA의 WebArena 58.1%와 인간 기준 78.2% 수치는 2025년 공개 자료의 초기 지표다.
- WebMCP는 2026년 2월 Chrome early preview로 공개됐으며 declarative와 imperative API를 제안한다.
- 구조화된 tool은 selector ambiguity를 줄이지만 tool description/output 자체가 untrusted content가 될 수 있다.
- Playwright MCP는 security boundary가 아니므로 origin, credential, process, profile 권한을 별도 통제해야 한다.

