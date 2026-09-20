---
date: 2026-09-20
tags: [tech]
type: tech-tool-study
status: draft
---

# inspoAI MCP — Cheatsheet

> [[README|목차로 돌아가기]]

## 핵심 요약

| 항목 | 기억할 문장 |
|---|---|
| 목적 | agent가 UI 구현 전에 reference와 design context를 조사하게 한다 |
| 정체 | hosted design-intelligence MCP integration으로 소개된다 |
| 공개 연동 | Claude, Cursor, Replit, Lovable, Codex를 표방한다 |
| 미확인 정보 | endpoint, tool schema, auth, rate limit, GitHub source는 공개 검증 자료가 부족하다 |
| 안전 원칙 | read-only PoC → scope 검증 → source review → human approval |

## 도입 전 질문

- [ ] 사용 중인 MCP Client와 현재 연결 방법이 공식적으로 지원되는가?
- [ ] `tools/list` 또는 client inventory에서 실제 tool과 input schema를 확인했는가?
- [ ] 검색, 저장, upload, brand scan 등 side effect를 구분했는가?
- [ ] query, URL, 내부 design asset이 vendor에 어떻게 저장·처리되는지 확인했는가?
- [ ] 결과마다 source URL, 라이선스·상표 검토 상태를 남기는가?
- [ ] token, WCAG, keyboard navigation을 구현 constraint로 주는가?

## Prompt recipe

```text
[제품 맥락]의 [사용자 작업]에 맞는 [platform] UI references를 찾아라.
각 reference의 source URL과, 재사용 가능한 UX pattern만 요약하라.
copy, logo, illustration, screenshot layout은 복제하지 마라.
우리 제약: [design tokens] / [WCAG level] / [framework].
구현 전 선택한 pattern과 rationale을 표로 제시하라.
```

## 대안 선택

| 필요 | 우선 검토 |
|---|---|
| 실제 UI/UX 사례 탐색 | Inspo AI 또는 Mobbin MCP |
| 내부 Figma 자산과 구현 정합성 | Figma MCP |
| 설치 가능한 UI component | 21st MCP |
| OSS, self-hosting, source audit | Nutlope Inspo |

## 이름 주의

`inspoai.io`의 **Inspo AI MCP**와 `inspomcp.dev` / `Nutlope/inspo`의 **Inspo**는 별도 제품이다. endpoint, publisher, license를 각각 확인한다.

## Sources

- https://www.inspoai.io/mcp
- https://mobbin.com/mcp
- https://developers.figma.com/docs/figma-mcp-server/
- https://21st.dev/mcp
- https://inspomcp.dev/about
