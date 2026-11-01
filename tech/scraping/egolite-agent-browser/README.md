---
date: 2026-11-01
tags: [tech]
type: tech-tool-study
status: draft
---

# ego(lite) — AI agent용 공유 Chromium 브라우저

> **한 줄 정의**: ego(lite)는 실제 로그인 상태를 유지한 Chromium 안에서 AI agent가 독립된 `Space`로 웹 작업을 수행하는 local-first browser automation 플랫폼이다.

## Overview

ego(lite)는 별도 headless/CDP browser를 띄우는 대신, 사람과 agent가 하나의 desktop Chromium을 공유하면서 서로의 작업을 분리하려는 제품이다. agent는 `ego-browser` CLI 또는 Node.js SDK로 Task Space를 열고, accessibility tree 기반 `Snapshot`의 ref를 이용해 UI를 조작한다.

핵심 가치는 기존 Chrome profile의 로그인 상태를 활용하면서도, agent 작업 탭을 남겨 사람이 검토·takeover할 수 있게 하는 데 있다. 다만 authenticated page content에 접근할 수 있으므로, Space를 보안 sandbox로 오해해서는 안 된다.

## Learning Path

- [ ] [[tech/scraping/egolite-agent-browser/01-overview|Overview]] — 문제와 핵심 특징을 이해한다.
- [ ] [[tech/scraping/egolite-agent-browser/02-ecosystem|Ecosystem]] — Playwright·Browser Use·Browserbase와 경계를 비교한다.
- [ ] [[tech/scraping/egolite-agent-browser/04-learning/01-getting-started|시작하기]] — 설치, profile import, 첫 Task Space를 실습한다.
- [ ] [[tech/scraping/egolite-agent-browser/04-learning/02-deep-dive|심화]] — Snapshot, runtime, 권한 경계를 익힌다.
- [ ] [[tech/scraping/egolite-agent-browser/05-projects|Projects]] — 적용 과제를 선택해 구현한다.
- [ ] [[tech/scraping/egolite-agent-browser/cheatsheet|Cheatsheet]] — 명령과 작업 규칙을 빠르게 확인한다.
- [ ] [[tech/scraping/egolite-agent-browser/03-references|References]] — 공식 문서와 source code를 추적한다.

## When To Use

- 개인 또는 팀 workstation에서 이미 로그인된 SaaS, GitHub, CRM, analytics를 자동화할 때
- 사람이 언제든 browser control을 넘겨받아야 하는 조사·QA·back-office workflow일 때
- 동일 browser 안에서 여러 read-only task를 Space별로 병렬화하고 결과 탭을 audit할 때

## When Not To Use

- deterministic E2E test와 CI가 목적이면 Playwright가 더 적합하다.
- 서버에서 대규모 browser concurrency와 운영 observability가 필요하면 Browserbase 같은 hosted infrastructure를 검토한다.
- CAPTCHA, SMS/QR login, hardware key, OAuth authorization, 결제·publish·delete처럼 사람의 확인이 필요한 경계에서는 agent가 멈춰야 한다.

## Related Notes

- [[MOCs/Index]]
- [[MOCs/Scraping]]
- [[tech/scraping/browserless/README|Browserless]]

## Sources

- https://www.egolite.app/document/en/docs/product-introduce
- https://www.egolite.app/document/en/docs/space
- https://github.com/citrolabs/ego-lite

