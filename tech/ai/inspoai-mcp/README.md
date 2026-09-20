---
date: 2026-09-20
tags: [tech]
type: tech-tool-study
status: draft
---

# inspoAI MCP

> **한 줄 정의**: Inspo AI MCP는 AI coding agent가 UI/UX 레퍼런스와 디자인 인텔리전스를 검색·활용하도록 연결하는 hosted design-intelligence MCP Server이다.

## Overview

AI agent는 코드를 만들 수 있어도 제품 맥락과 UX 관례가 없으면 작동하지만 개성 없는 UI를 만들기 쉽다. Inspo AI MCP는 자연어 디자인 검색, moodboard, brand intelligence를 agent workflow에 넣어 조사→방향 설정→구현 흐름을 지원하려는 제품이다.

공개 발표에서는 Claude, Cursor, Replit, Lovable, Codex 연동을 표방한다. 다만 2026-09-20 기준 공개 자료로는 MCP endpoint, tool schema, 인증 방식, rate limit, GitHub source를 독립적으로 확인하지 못했다. 실제 도입 전 설정 화면과 privacy/data policy에서 권한 및 data handling을 검증해야 한다.

```text
AI Host / Coding Agent
  -> MCP Client
    -> Inspo AI MCP Server
      -> design search · moodboard · brand/design analysis
        -> reference context for UI decisions
```

## Learning Path

- [ ] [[01-overview|Overview]] — 제품의 What/Why와 공개 정보의 경계 이해
- [ ] [[02-ecosystem|Ecosystem]] — Mobbin, Figma MCP, 21st, Nutlope Inspo와 비교
- [ ] [[03-references|References]] — 공식 문서와 검증 순서 확인
- [ ] [[04-learning/01-getting-started|Getting Started]] — read-only PoC와 tool inventory 점검
- [ ] [[04-learning/02-deep-dive|Deep Dive]] — context 품질, 안전성, human review 설계
- [ ] [[05-projects|Projects]] — 디자인 조사와 구현을 연결하는 실전 과제
- [ ] [[cheatsheet|Cheatsheet]] — 도입 판단과 운영 checklist 복습

## When To Use

- UI 구현 전에 product category, visual direction, UX convention을 빠르게 조사할 때
- Designer, PM, Engineer가 같은 reference set을 보며 구현 제약을 합의할 때
- 외부 레퍼런스와 내부 design token을 함께 사용해 agent의 UI 결과를 개선할 때
- screenshot을 복제하지 않고 pattern과 rationale을 요약·비교하는 workflow가 필요할 때

## When Not To Use

- source, endpoint, authentication, data retention을 확인할 수 없는 hosted integration을 허용할 수 없을 때
- 내부 Figma file·component·variable 정합성이 유일한 목표일 때 — Figma MCP가 더 직접적이다
- 바로 설치 가능한 React component가 필요할 때 — 21st 같은 component delivery 도구가 더 맞을 수 있다
- 라이선스·상표·screen capture 처리 기준 없이 외부 디자인을 production에 그대로 적용하려 할 때

## Related Notes

- [[MOCs/Index]]
- [[MOCs/AI]]
- [[tech/ai/model-context-protocol-mcp/README|Model Context Protocol (MCP)]] — protocol과 hosted server의 공통 기반

## Sources

- https://www.inspoai.io/mcp
- https://www.inspoai.io/
- https://www.linkedin.com/posts/mohamed-siraj-1a1910234_inspoai-mcp-aidesign-activity-7439314685394575360-vTWy
- https://modelcontextprotocol.io/specification/2025-03-26/architecture
- https://modelcontextprotocol.io/specification/2025-06-18/server
