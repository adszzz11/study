---
date: 2026-10-18
tags: [tech]
type: tech-tool-study
status: draft
---

# awwwards-mcp

> **한 줄 정의**: Awwwards 공개 디자인 레퍼런스를 AI coding agent가 검색·분석·캡처·비교하도록 제공하는 local `stdio` MCP server.

## Overview

`awwwards-mcp`는 추상적인 “Awwwards급” 요구를 실제 수상 사이트의 screenshot, palette, technology, element, award history, motion/structure 관찰값으로 바꾼다. 결과물은 스타일 복제가 아니라, 인용 가능한 reference와 구현 검증 기준을 담은 design brief여야 한다.

- [[01-overview|What / Why / 핵심 특징]]
- [[02-ecosystem|Ecosystem과 대안 비교]]
- [[03-references|공식 자료와 검증 출처]]
- [[05-projects|적용 프로젝트]] · [[cheatsheet|Cheatsheet]]

## Learning Path

- [ ] [[04-learning/01-getting-started|Getting Started]] — Node 확인, MCP 등록, 첫 reference 검색
- [ ] `search_sites`로 3개 안팎의 후보를 찾고 screenshot을 직접 확인한다.
- [ ] `get_site_details`, `get_site_elements`로 재사용할 cue와 복제하면 안 될 asset/copy를 분리한다.
- [ ] [[04-learning/02-deep-dive|Deep Dive]] — local index, capture, motion, verification loop
- [ ] `create_design_brief`로 구현 범위와 비재현 범위를 명시한다.

## When To Use

- Awwwards 기반의 디자인 방향을 근거와 함께 정해야 할 때
- landing page의 section, palette, CTA, motion을 reference와 비교 검증할 때
- local MCP host에서 API key 없이 제한적인 공개 레퍼런스 조사를 할 때

## When Not To Use

- 원본 asset, copy, layout을 그대로 재배포하거나 모방하려는 경우
- 대량 수집·지속 크롤링이 필요한 경우(권리, ToS, rate limit을 먼저 검토)
- Awwwards 외의 넓은 디자인 corpus만 필요한 경우

## Related Notes

- [[MOCs/Index]]
- [[MOCs/Scraping]]
- [[tech/ai/agent-garden|Agent Garden]]

## Sources

- https://github.com/INSANE0777/Awwwards-mcp
- https://github.com/INSANE0777/Awwwards-mcp/releases
- https://ts.sdk.modelcontextprotocol.io/v2/serving/stdio
- https://www.awwwards.com/
