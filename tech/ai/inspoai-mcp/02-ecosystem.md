---
date: 2026-09-20
tags: [tech]
type: tech-tool-study
status: draft
---

# inspoAI MCP — Ecosystem

> [[01-overview|이전: Overview]] · [[README|목차]] · [[03-references|다음: References]]

## 비교

| 제품 | 주된 context | MCP 연결/접근 | Inspo AI 대비 |
|---|---|---|---|
| **Inspo AI MCP** | UI inspiration, moodboard, brand intelligence, design audit | 공개 발표상 Claude/Cursor/Replit/Lovable/Codex 연동; 세부 endpoint 미공개 | 조사→방향 설정→생성까지의 design-intelligence workflow 지향 |
| [Mobbin MCP](https://mobbin.com/mcp) | 실제 mobile/web UI·UX 레퍼런스 | Remote MCP, OAuth; 유료 플랜 포함 | 가장 직접적인 상용 reference-library 대안이며 setup/auth 정보가 더 명확 |
| [Figma MCP](https://developers.figma.com/docs/figma-mcp-server/) | 조직의 Figma file, variables, components, layout | Remote/desktop server | 외부 영감보다 내부 design system과 구현 정합성에 적합 |
| [21st MCP](https://21st.dev/mcp) | UI component 검색·설치·생성·publish | terminal/MCP client, API key 선택 가능 | 레퍼런스 탐색보다 React/UI component delivery에 집중 |
| [Nutlope Inspo](https://inspomcp.dev/about) | 공개 production website capture, `DESIGN.md`, canonical component | hosted/free 및 self-host 가능한 OSS | 투명한 OSS·self-hosting이 필요할 때 적합; Inspo AI와 별도 서비스 |

## 조합 전략

| 목표 | 우선 도구 | 보완 도구 |
|---|---|---|
| 시장 UI pattern 조사 | Inspo AI 또는 Mobbin | Figma MCP로 내부 token 확인 |
| 기존 제품과 일관된 구현 | Figma MCP | 21st로 component delivery 보조 |
| self-hosting과 source audit | Nutlope Inspo | 별도 internal design-system source |
| 빠른 React prototype | 21st | 레퍼런스 조사 도구로 방향성 확보 |

선택은 “MCP를 쓰는가”보다 **어떤 context가 부족한가**에서 출발한다. 외부 사례, 내부 시스템, 배포 가능한 component는 서로 다른 종류의 context이며 한 도구가 모두 대체하지 않는다.

## Sources

- https://www.inspoai.io/mcp
- https://mobbin.com/mcp
- https://developers.figma.com/docs/figma-mcp-server/
- https://21st.dev/mcp
- https://inspomcp.dev/about
