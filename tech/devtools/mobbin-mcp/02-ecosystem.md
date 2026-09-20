---
date: 2026-09-20
tags: [tech]
type: tech-tool-study
status: draft
---

# Mobbin MCP — Ecosystem

## 역할 비교

| 도구 | 주 데이터 원천 | 핵심 역할 | 읽기/쓰기 | Mobbin 대비 적합한 경우 |
|---|---|---|---|---|
| **Mobbin MCP** | 타사 실제 제품의 UI/UX screen·flow·section | market/design research, pattern synthesis | Read-only | 경쟁 사례 기반의 설계 근거가 필요할 때 |
| **Figma MCP** | 조직의 Figma file·design system | selected frame의 code/context 추출, canvas 수정 | Read + Write | 이미 확정된 내부 디자인을 구현하거나 Figma를 갱신할 때 |
| **Refero MCP** | Refero의 실제 제품 UI 레퍼런스 | 레퍼런스 조사 | 주로 research | Mobbin과 다른 corpus에서 탐색 범위를 넓힐 때 |
| **21st MCP** | reusable UI component/template/code catalog | component 검색·설치·생성·publish | Read + Write 성격 | 즉시 쓸 React/shadcn 계열 구현물이 필요할 때 |

## 선택 기준

Figma MCP는 경쟁 제품을 찾는 서비스가 아니라 **자사 source of truth를 code와 연결하는 도구**다. Mobbin MCP는 외부 제품에서 검증된 pattern을 찾는 데 집중한다. 21st MCP는 reference보다 재사용 가능한 구현물과 component workflow에 가깝다. Refero MCP는 같은 research 문제에 대해 다른 UI corpus를 제공하는 대안이다.

따라서 “무엇을 만들어야 하는가”가 불명확하면 Mobbin MCP부터, “우리 시스템에서 어떻게 만들어야 하는가”가 핵심이면 Figma MCP를 우선한다. “무엇을 바로 가져와 구현할 수 있는가”는 21st MCP의 영역이다.

## 보완 workflow

```text
PRD / feature intent
  → Mobbin MCP: external patterns 조사·비교
  → UX decision: 공통 패턴, 예외, 제품 제약 기록
  → Figma MCP: internal tokens·components·frame context 확인
  → 구현 agent: 프로젝트 component로 코드화
  → review: reference 링크와 구현 영향 함께 검토
```

이 순서는 도구 결과를 정답으로 취급하지 않는다. 외부 사례는 hypothesis를 만들고, 내부 design system·accessibility·규제·기술 제약이 최종 판단을 제한한다.

## Sources

- [Figma MCP server documentation](https://developers.figma.com/docs/figma-mcp-server/)
- [Refero MCP](https://refero.design/mcp)
- [21st MCP](https://21st.dev/mcp)
- [Mobbin MCP](https://mobbin.com/mcp)
