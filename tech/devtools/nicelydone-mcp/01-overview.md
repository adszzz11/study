---
date: 2026-09-20
tags: [tech]
type: tech-tool-study
status: draft
---

# Nicelydone MCP: Overview

## What

Nicelydone MCP는 AI client와 Nicelydone의 SaaS UI reference database 사이를 연결하는 remote MCP server다. Claude Code/Desktop, Cursor, Lovable, ChatGPT, Codex, Windsurf, VS Code, Zed 등의 MCP client 연결을 공식 페이지에서 안내한다. 실제 연결값은 로그인한 Pro 계정의 안내를 사용한다.

```text
AI client (Codex / Claude / Cursor)
  → Nicelydone MCP
  → search + structured metadata
  → screen / flow / component reference
  → original implementation
```

## Why

"작동하는 UI"와 "문제에 맞는 UI"는 다르다. agent가 table, empty state, invite flow의 실제 사례를 비교하면 상태 설계와 정보 우선순위의 후보를 더 구체적으로 논의할 수 있다. 이 도구의 목적은 screenshot을 복사하는 것이 아니라 설계 가설을 검증할 **근거 집합**을 만드는 데 있다.

## 특징

| 특징 | 학습 시 의미 |
| --- | --- |
| 12개 tool | screen·flow·component·app 검색, favorites/collections 조회, collection 생성·screen 저장을 지원한다고 공식 페이지가 설명한다. |
| Structured metadata 우선 | page type, UI element, layout pattern, description으로 먼저 좁혀 이미지 열람 전 비교할 수 있다. |
| SaaS reference 중심 | dashboard, settings, login, pricing page 및 onboarding, checkout, invite flow 같은 product UI 조사에 맞는다. |
| Collection | 재사용할 사례를 개인/team reference library로 축적할 수 있다. |
| Pro 결합 | MCP access는 Pro subscription에 포함되고 별도 API key 비용은 없다고 안내한다. 가격·권한은 도입 시 재확인한다. |

## 권리와 original work

reference screen은 각 권리자의 저작물이다. 다음처럼 분리한다.

- **채택:** 문제 구조, state coverage, label hierarchy, keyboard-friendly interaction 같은 일반화 가능한 pattern
- **재해석:** 자사 token, content model, component API, responsive breakpoint
- **배제:** 브랜드명·copy·logo·이미지 asset·고유한 화면 배치의 재현

결과물은 reference의 합성이 아니라 제품 제약에 맞춘 새 구현이어야 한다.

## Sources

- [Nicelydone MCP](https://nicelydone.club/mcp)
- [Nicelydone UI library](https://nicelydone.club/)
- [Nicelydone Help Center](https://vzero.nicelydone.club/help/)
