---
date: 2026-09-20
tags: [tech]
type: tech-tool-study
status: draft
---

# Agent Browser

> **한 줄 정의**: Agent browser는 LLM/VLM이 screenshot·DOM·accessibility tree·WebMCP tool로 웹 상태를 인식하고, planning–action–verification loop를 반복해 사람 대신 웹 작업을 수행하는 browser automation system이다.

## Overview

Agent browser는 자연어로 주어진 목표를 browser action으로 바꾸고, 실행 결과를 다시 관찰해 다음 행동을 결정한다. 미리 작성한 selector와 고정 workflow가 중심인 전통적 browser automation과 달리, 처음 보는 page나 변경된 UI에도 재탐색과 replanning으로 대응하는 것이 핵심이다.

```text
User goal → Planner → Observe → Act → Verify
                         ↑          │
                         └─ re-plan ┘
```

관찰에는 screenshot, DOM, accessibility tree, WebMCP tool을 사용할 수 있고 실행에는 click, type, scroll, navigation, extraction, file transfer, API call이 포함된다. 실무에서는 안정된 selector/API를 먼저 쓰고 불확실한 부분만 model에 맡기는 **deterministic-first, agentic-fallback**이 기본 패턴이다.

> [!important]
> Model의 “완료” 발언은 성공 증거가 아니다. URL, DOM state, API response, 생성된 record, 다운로드 파일처럼 외부 상태를 별도로 검증해야 한다.

## Learning Path

- [ ] [[01-overview|Overview]] — What/Why, 핵심 구성요소와 특징
- [ ] [[02-ecosystem|Ecosystem]] — Playwright, Playwright MCP, Stagehand, Browser Use, Computer Use, WebMCP 비교
- [ ] [[03-references|References]] — 공식 문서와 읽는 순서
- [ ] [[04-learning/01-getting-started|Getting Started]] — 안전한 local sandbox에서 첫 agent loop 설계
- [ ] [[04-learning/02-deep-dive|Deep Dive]] — hybrid perception, verifier, session, security, evaluation
- [ ] [[05-projects|Projects]] — 난이도별 실전 프로젝트와 완료 기준
- [ ] [[cheatsheet|Cheatsheet]] — 선택 기준, loop, guardrail 빠른 참조

## When To Use

- API가 없거나 API로 노출되지 않은 legacy/internal web application을 다룰 때
- 로그인 이후 dashboard, 복잡한 form, multi-page workflow를 자동화할 때
- UI 변화가 잦아 selector 유지보수 비용이 큰 탐색적 workflow를 처리할 때
- 새로운 site를 zero/few-shot으로 탐색하고 필요한 정보를 추출할 때
- CAPTCHA/MFA나 고위험 action에서 human takeover를 포함한 반자동 workflow가 필요할 때

## When Not To Use

- 안정된 API나 deterministic script로 같은 목표를 더 빠르고 신뢰성 있게 달성할 수 있을 때
- 단순 web search, crawling, 정적 scraping만 필요한 경우
- 결제·전송·게시·삭제를 사용자 승인 없이 완전 자율로 수행해야 하는 경우
- prompt injection, credential 노출, cross-origin data transfer를 통제할 수 없는 환경
- 성공 여부를 외부 상태로 검증하거나 action trace를 감사할 수 없는 업무
- CAPTCHA 우회나 site policy 위반이 전제되는 자동화

## Related Notes

- [[MOCs/Index]]
- [[MOCs/AI]]
- [[tech/ai/model-context-protocol-mcp/README|Model Context Protocol (MCP)]] — WebMCP 및 tool interface와 비교할 protocol 배경
- [[tech/ai/agent-garden|Agent Garden]] — agent system을 설계하고 운영하는 더 넓은 맥락

## Sources

- [OpenAI — Computer-Using Agent](https://openai.com/index/computer-using-agent/)
- [OpenAI — Introducing ChatGPT agent](https://openai.com/index/introducing-chatgpt-agent/)
- [Microsoft — Playwright MCP](https://github.com/microsoft/playwright-mcp)
- [Browserbase — Stagehand](https://github.com/browserbase/stagehand)
- [Browser Use](https://github.com/browser-use/browser-use)
- [Chrome for Developers — WebMCP early preview](https://developer.chrome.com/blog/webmcp-epp)
- [Chrome for Developers — Agent security considerations for WebMCP](https://developer.chrome.com/docs/agents/security)
- [Anthropic — Mitigating prompt injections in browser use](https://www.anthropic.com/news/prompt-injection-defenses)

