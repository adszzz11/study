---
date: 2026-09-20
tags: [tech]
type: tech-tool-study
status: draft
---

# UI UX Pro Max — Ecosystem

[[tech/devtools/ui-ux-promax/README|학습 진입점]] · 이전: [[tech/devtools/ui-ux-promax/01-overview|Overview]]

## 역할 비교

| 선택지 | 주 역할 | UI UX Pro Max 대비 |
|---|---|---|
| UI UX Pro Max | AI agent용 design-intelligence retrieval | 제품·스타일·UX rule을 검색해 결정 생성 |
| shadcn/ui | React component source/primitives | 구현 재료에 강함; 디자인 방향은 별도 필요 |
| Tailwind CSS | utility-first styling | 빠른 구현 도구; design reasoning/UX DB는 제공하지 않음 |
| Figma | 협업 design/prototyping | 사람 중심 workflow·handoff에 강함 |
| Storybook | component 문서화·visual QA | 구현 후 검증에 강함 |
| 자체 `SKILL.md` + tokens | 조직 맞춤 지식 | 브랜드 적합성은 높지만 curation·검색 유지비가 큼 |

## 권장 조합

```text
UI UX Pro Max: product intent → design decision / MASTER.md
        ↓
Tailwind + shadcn/ui: component implementation
        ↓
Storybook + a11y checks: rendered component QA
        ↓
Figma: team review, prototype, handoff
```

UI UX Pro Max의 output을 그대로 brand rule로 확정하지 않는다. 기존 design token과 product requirement를 우선하고, retrieval 결과는 선택 근거와 QA checklist로 사용한다.

## 선택 기준

- **새 제품/새 surface**: UI UX Pro Max로 방향을 만들고 component library를 결합한다.
- **성숙한 design system**: 조직 tokens를 retrieval data 또는 prompt constraint로 우선한다.
- **component regression**: Storybook과 visual test를 중심에 둔다.
- **협업 승인과 prototype**: Figma를 source of collaboration으로 유지한다.

## Sources

- https://github.com/nextlevelbuilder/ui-ux-pro-max-skill
- https://ui.shadcn.com/
- https://tailwindcss.com/
- https://www.figma.com/
- https://storybook.js.org/
