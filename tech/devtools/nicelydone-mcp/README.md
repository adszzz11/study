---
date: 2026-09-20
tags: [tech]
type: tech-tool-study
status: draft
---

# Nicelydone MCP

> **한 줄 정의**: Nicelydone MCP는 AI coding agent가 실제 SaaS UI screen·user flow·component library를 검색·참조해 original implementation의 설계 근거로 쓰게 하는 remote Model Context Protocol 서버다.

## Overview

LLM은 코드를 빠르게 만들지만, 특정 UX 문제에 맞는 information architecture·interaction pattern·visual hierarchy의 실전 맥락은 스스로 보유하지 않는다. Nicelydone은 출시된 SaaS 제품의 화면과 흐름을 retrieval context로 제공해 이 간극을 줄인다.

- **검색 단위:** screen, user flow, UI component, app
- **조사 순서:** metadata 검색 → 후보 비교 → pattern synthesis → original implementation
- **공식 규모:** 2026-09-20 기준 205,500+ screens, 12,900+ flows, 32,800+ components, 500+ SaaS apps를 표방한다.
- **중요한 경계:** reference는 UX insight를 위한 자료다. copy, branding, asset, 독창적 화면 구성을 복제하지 않는다.

## Learning Path

- [ ] [[tech/devtools/nicelydone-mcp/01-overview|1. Overview]] — What/Why, data layer, 권리 경계 이해하기
- [ ] [[tech/devtools/nicelydone-mcp/02-ecosystem|2. Ecosystem]] — design-reference MCP와 design system context 비교하기
- [ ] [[tech/devtools/nicelydone-mcp/03-references|3. References]] — 공식 자료와 재확인 지점 정리하기
- [ ] [[tech/devtools/nicelydone-mcp/04-learning/01-getting-started|4. Getting started]] — 계정 config로 research-only 요청 시작하기
- [ ] [[tech/devtools/nicelydone-mcp/04-learning/02-deep-dive|5. Deep dive]] — metadata 기반 synthesis와 검수 workflow 설계하기
- [ ] [[tech/devtools/nicelydone-mcp/05-projects|6. Projects]] — product UI 조사 프로젝트에 적용하기
- [ ] [[tech/devtools/nicelydone-mcp/cheatsheet|7. Cheatsheet]] — 요청 문구와 검수 항목 빠르게 복습하기

## When To Use

- B2B dashboard, settings, table, form, onboarding처럼 SaaS product UI의 검증된 pattern을 조사할 때
- 구현 전에 유사 flow를 비교해 상태·정보 밀도·interaction의 근거를 만들 때
- 외부 사례와 자사 design system을 함께 적용할 design brief가 필요할 때

## When Not To Use

- 자사 Figma file, token, component 규칙만 따라야 하는 작업이라 외부 사례 조사 가치가 작을 때
- 특정 live website의 typography·color·spacing을 정밀 검사하는 것이 주목적일 때
- reference의 visual identity를 재현하려는 목적일 때; 원본성·권리 경계를 지킬 수 없다면 사용하지 않는다.

## Related Notes

- [[MOCs/Index]]
- [[MOCs/Devtools]]
- [[tech/ai/model-context-protocol-mcp/README|Model Context Protocol (MCP)]]

## Sources

- [Nicelydone MCP](https://nicelydone.club/mcp)
- [Nicelydone UI library](https://nicelydone.club/)
- [Nicelydone Pricing](https://nicelydone.club/pricing)
- [Model Context Protocol introduction](https://modelcontextprotocol.io/docs/2026-07-28/getting-started/intro)
