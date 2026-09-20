---
date: 2026-09-20
tags: [tech]
type: tech-tool-study
status: draft
---

# Nicelydone MCP: Ecosystem

## 비교

| 도구 | 주 데이터 / 강점 | Nicelydone 대비 선택 기준 |
| --- | --- | --- |
| **Nicelydone MCP** | SaaS web UI, flow, component, personal collection | dashboard·settings·form·onboarding 같은 SaaS product UI 조사에 적합 |
| [Refero MCP](https://refero.design/mcp) | 142,000+ screens, 12,000+ flows, web+iOS, metadata 기반 research | mobile/iOS reference까지 넓게 필요하거나 Refero Skill methodology가 필요할 때 |
| [Mobbin MCP](https://mobbin.com/mcp) | 600,000+ real product screens, 넓은 mobile/web library | cross-platform 또는 consumer/mobile 사례가 핵심일 때 |
| [Fudge MCP](https://design.withfudge.com/) | live website capture와 URL 기반 typography·color·layout·contrast inspection | UX flow보다 특정 website의 visual implementation detail을 분석할 때 |
| Figma MCP / design system context | 내부 design file, token, component 규칙 | 외부 시장 reference가 아니라 자사 source of truth 준수가 목적일 때 |

표의 숫자와 제공 범위는 각 제품의 공개 페이지 기준이며 구독 전 다시 확인한다.

## 함께 쓰는 방식

이 도구들은 상호 배타적이지 않다. 예를 들어 Nicelydone으로 onboarding pattern을 찾고, Figma context로 자사 token·component 제약을 적용한다. 이어 browser test로 responsive state와 keyboard flow를 검증하는 구성이 자연스럽다.

```text
시장 reference (Nicelydone)
  → pattern hypothesis
  → 내부 source of truth (Figma / design system)
  → original code
  → accessibility + responsive QA
```

## 선택 질문

1. 필요한 것은 **외부 제품의 flow pattern**인가, 아니면 **자사 component의 정확한 사용법**인가?
2. web SaaS가 중심인가, mobile/iOS 사례가 중심인가?
3. 화면의 구조를 비교할 것인가, 특정 URL의 CSS-like visual detail을 검사할 것인가?
4. 검토할 시간에 original brief와 접근성 검수까지 포함했는가?

## Sources

- [Nicelydone MCP](https://nicelydone.club/mcp)
- [Refero MCP](https://refero.design/mcp)
- [Mobbin MCP](https://mobbin.com/mcp)
- [Fudge](https://design.withfudge.com/)
