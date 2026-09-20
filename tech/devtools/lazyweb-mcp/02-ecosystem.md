---
date: 2026-09-20
tags: [tech]
type: tech-tool-study
status: draft
---

# Lazyweb MCP Ecosystem

## 비교

| 도구 | 주된 context | 강점 | Lazyweb 대비 선택 기준 |
|---|---|---|---|
| Lazyweb MCP | 실제 UI, flows, growth mechanics | 조사에서 audit·recommendation·backlog까지 잇는 workflow | conversion, pricing, onboarding 개선을 evidence와 함께 agent에 맡길 때 |
| Mobbin MCP | 대규모 mobile/web 제품 screen·flow 라이브러리 | 공식 페이지가 소개하는 방대한 shipped-screen catalog와 깊은 reference 탐색 | 순수 UI/UX reference의 폭과 flow 탐색이 최우선일 때; plan 조건 확인 필요 |
| 21st MCP | 구현 가능한 component, theme, template, code | catalog 검색 뒤 code/dependency 설치·생성·publish 가능 | 참조 분석보다 React/shadcn component를 바로 프로젝트에 들일 때 |
| Figma MCP | 조직의 Figma file, token, component, layout | design system을 source of truth로 쓰고 design/code 왕복 지원 | 외부 사례보다 사내 설계를 code/canvas로 동기화할 때 |

## 역할 분리

```text
외부 사례 조사       조직 설계 제약          구현
Lazyweb / Mobbin  →  Figma / design system →  21st 또는 자체 component
       └──────────── metric 실험으로 검증 ────────────┘
```

- **Lazyweb과 Mobbin**: 외부 제품에서 검증할 후보 패턴을 찾는다. 사례가 자사 성과를 보장하지는 않는다.
- **21st**: 가져와 조정할 수 있는 구현물을 중심으로 한다. dependency, license, bundle·accessibility 영향을 code review한다.
- **Figma**: 팀의 token, component, layout을 우선하는 내부 source of truth다. 외부 사례를 Figma 규칙에 맞게 번역한다.

## 선택 질문

1. 지금 필요한 것은 사례의 근거인가, 바로 쓸 component인가, 내부 design source인가?
2. target platform과 flow의 coverage가 실제로 있는가? 샘플이 아니라 해당 사례를 열어 확인한다.
3. research 결과를 누가 결정하고 어떤 metric으로 검증할 것인가?
4. account plan, access scope, data retention이 팀의 요구와 맞는가?

## Sources

- https://www.lazyweb.com/product
- https://mobbin.com/mcp
- https://docs.21st.dev/mcp
- https://developers.figma.com/docs/figma-mcp-server/
