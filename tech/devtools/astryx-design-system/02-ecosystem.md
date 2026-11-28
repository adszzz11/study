---
date: 2026-11-13
tags: [tech]
type: tech-tool-study
status: draft
---

# Astryx — Ecosystem

> [[tech/devtools/astryx-design-system/README|목차로 돌아가기]] · [[tech/devtools/astryx-design-system/04-learning/01-getting-started|다음: 시작하기]]

## 선택지 비교

| 선택지 | 성격 | styling / 소유권 | Astryx보다 적합한 경우 |
|---|---|---|---|
| **Astryx** | component system + theme compiler + agent CLI | token theme, CSS override, 필요 시 source swizzle | — |
| shadcn/ui | registry/CLI 중심 open-code distribution | component를 project로 가져와 직접 수정·소유 | Tailwind 중심이고 component별 local ownership/registry가 더 중요할 때 |
| MUI | Material Design 기반 종합 React library | production-ready component와 customization | Material 언어와 성숙한 enterprise ecosystem을 수용할 때 |
| Radix Primitives | low-level unstyled accessible primitive | behavior만 제공, presentation은 팀이 구현 | 자체 Design System의 style layer를 처음부터 완전 통제할 때 |

## 판단 기준

Astryx는 Radix처럼 headless-only가 아니고, MUI처럼 특정 visual language를 중심에 두지도 않으며, shadcn/ui처럼 일회성 file copy 모델에만 머물지도 않는다. **updatable package theme + source-level escape hatch + agent-readable CLI**의 조합이 차별점이다.

| 질문 | Astryx의 답 |
|---|---|
| “브랜드를 바꿀 수 있는가?” | token과 `defineTheme()` extension으로 바꾼다. |
| “upstream 변경을 받을 수 있는가?” | theme `extends`로 package lineage를 유지한다. |
| “예외 component는?” | `swizzle`로 source를 eject해 project가 소유한다. |
| “agent hallucination은?” | `component`, `search`, `docs` CLI로 설치 버전의 API를 조회하게 한다. |

## Theme 생태계

first-party theme은 Neutral, Butter, Chocolate, Gothic, Matcha, Stone, Y2K의 일곱 가지다. 이는 제품의 최종 brand를 강제하는 preset이 아니라, 확장 가능한 token 출발점으로 보는 편이 좋다. multi-brand에서는 각 brand가 base theme을 `extends`하고 accent·typography·radius처럼 차이가 필요한 token만 덮어쓴다.

## Sources

- https://ui.shadcn.com/docs/official
- https://mui.com/material-ui/getting-started/
- https://www.radix-ui.com/primitives/docs/overview/introduction
- https://astryx.atmeta.com/docs/theme
