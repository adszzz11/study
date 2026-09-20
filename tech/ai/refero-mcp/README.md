---
date: 2026-09-20
tags: [tech]
type: tech-tool-study
status: draft
---

# Refero MCP

> **한 줄 정의**: Refero MCP는 AI agent가 실제 제품 UI screen과 user flow를 검색·참조한 뒤 UI를 설계하도록 하는 Refero의 hosted, read-only Model Context Protocol server다.

## Overview

Refero MCP는 code 생성 이전에 검증된 제품 UI 사례를 찾고, 그 사례에서 design decision을 추출하게 하는 **design-research layer**다. LLM이 흔히 만드는 generic UI를 줄이기 위해 `Styles`, `Screens`, `Flows`라는 세 연구 레이어를 제공한다.

```text
Design brief → Refero research → reference lock → implementation → visual QA
```

공식 페이지와 GitHub는 corpus 수치를 각각 `142,000+ screens / 12,000+ flows`, `150,000+ screens / 6,000+ flows`로 표기한다. 집계 기준 또는 갱신 시점이 다를 수 있으므로, 구매·도입 전 현재 plan의 quota와 범위를 확인한다.

## Learning Path

- [ ] [[01-overview|Overview]] — 문제, research layer, hosted architecture 이해
- [ ] [[02-ecosystem|Ecosystem]] — Fudge, Figma MCP, gallery, community MCP와 비교
- [ ] [[03-references|References]] — 공식 문서와 제3자 source의 경계 확인
- [ ] [[04-learning/01-getting-started|Getting started]] — OAuth 연결과 첫 research brief 실습
- [ ] [[04-learning/02-deep-dive|Deep dive]] — reference synthesis, token, visual QA 심화
- [ ] [[05-projects|Projects]] — product workflow에 적용
- [ ] [[cheatsheet|Cheatsheet]] — 반복할 절차와 질문 복습

## When To Use

- 구현 전에 실제 제품의 UI pattern 또는 multi-step flow를 조사할 때
- empty state, onboarding, checkout, settings처럼 hierarchy 판단이 중요한 화면을 설계할 때
- 자연어 brief에서 여러 benchmark를 찾고 evidence와 제안을 분리한 report가 필요할 때
- AI coding agent의 UI 작업에 research-first guardrail을 넣을 때

## When Not To Use

- 자사 Figma frame과 design system을 정확히 재현하는 것이 유일한 목표일 때
- 특정 공개 웹 page 하나의 DOM, typography, spacing을 정밀하게 관찰해야 할 때
- corpus를 검색할 필요 없이 이미 승인된 reference와 요구사항이 충분할 때
- 외부 hosted service의 OAuth 및 유료 live access를 사용할 수 없을 때

## Related Notes

- [[MOCs/Index]]
- [[MOCs/AI]]
- [[tech/ai/model-context-protocol-mcp/README|Model Context Protocol (MCP)]]

## Sources

- https://refero.design/mcp
- https://github.com/referodesign/refero_skill
- https://github.com/referodesign/refero_skill/blob/master/.mcp.json
- https://github.com/referodesign/refero_skill/blob/master/skills/refero-design/SKILL.md
