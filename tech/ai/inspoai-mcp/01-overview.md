---
date: 2026-09-20
tags: [tech]
type: tech-tool-study
status: draft
---

# inspoAI MCP — Overview

> [[README|목차]] · [[02-ecosystem|다음: Ecosystem]]

## What

Inspo AI MCP는 AI coding agent에 UI/UX inspiration과 design context를 공급하려는 hosted MCP integration이다. 일반적인 MCP 관점에서는 Host가 MCP Client를 통해 Server의 `tools`, `resources`, `prompts` capability를 발견하고 사용한다.

공식 제품 메시지는 디자인 검색, collaborative moodboard, brand-guideline audit, 웹사이트의 색상·font·tech stack 추출, prompt 기반 UI generation을 하나의 design-intelligence workflow로 연결하는 데 있다.

## Why

UI 생성에서 코드 품질만으로는 충분하지 않다. 제품의 audience, 브랜드 톤, navigation, form, error state 같은 UX 관례를 먼저 조사해야 한다. 이 MCP의 목표는 agent가 구현 이전에 레퍼런스를 찾고 그 근거를 prompt context로 사용하게 만드는 것이다.

```text
모호한 구현 요청
  -> reference 조사
  -> pattern / 제약 / 선택 이유 요약
  -> design token·accessibility 제약 적용
  -> UI 구현
  -> human review
```

## 특징과 공개 정보의 한계

| 항목 | 공개적으로 알 수 있는 점 | 아직 검증할 점 |
|---|---|---|
| Design-context retrieval | UI/UX 레퍼런스와 스타일 맥락을 agent에 주는 포지션 | 실제 검색 범위, ranking, citation 형식 |
| Workflow | 검색, moodboard, brand intelligence, UI generation을 표방 | 각 기능이 MCP tool로 노출되는지 |
| Client | Claude, Cursor, Replit, Lovable, Codex 연동을 발표 | client별 transport와 authorization |
| 운영 | hosted service로 소개됨 | endpoint, rate limit, retention, source code |

> [!warning] 도입 전 검증
> 공개 API schema, tool 목록, 인증 방식, MCP endpoint, rate limit, GitHub source는 2026-09-20 기준 공개 자료에서 확인되지 않았다. account 연결 전에 실제 tool inventory, scope, privacy policy, data retention을 확인한다.

## 제품명 혼동 방지

**Inspo AI MCP**와 Together AI가 운영하는 오픈소스 **Inspo** (`inspomcp.dev`, `Nutlope/inspo`)는 서로 다른 제품이다. Nutlope Inspo는 공개 production website capture와 `DESIGN.md`를 제공하며 MIT source와 self-hosting 선택지가 있다. 비교하거나 설치할 때 URL과 publisher를 함께 확인한다.

## Sources

- https://www.inspoai.io/mcp
- https://www.launchrecord.com/products/inspoai
- https://modelcontextprotocol.io/specification/2025-03-26/architecture
- https://modelcontextprotocol.io/specification/2025-06-18/server
- https://inspomcp.dev/about
