---
date: 2026-09-20
tags: [tech]
type: tech-tool-study
status: draft
---

# awesome-design-md — Cheatsheet

> [[05-projects|이전: Projects]] · [[README|목차로 돌아가기]]

## 핵심 구분

| 이름 | 정체 |
|---|---|
| `awesome-design-md` | brand-inspired `DESIGN.md` reference collection |
| Google `DESIGN.md` | schema, format, CLI를 제공하는 `alpha` specification |
| W3C DTCG | vendor-neutral design token interchange specification |
| `DESIGN.md` | YAML token + Markdown rationale로 구성된 project design contract |

## 최소 구조

```yaml
---
version: alpha
name: Product Design System
colors:
  primary: "#171717"
  surface: "#ffffff"
typography:
  body-md:
    fontFamily: Inter
    fontSize: 16px
spacing:
  md: 16px
rounded:
  control: 6px
components:
  button-primary:
    backgroundColor: "{colors.primary}"
    padding: "{spacing.md}"
---
```

## Markdown section 순서

```text
## Overview
## Colors
## Typography
## Layout
## Elevation & Depth
## Shapes
## Components
## Do's and Don'ts
```

## CLI

```bash
# schema/reference/section/contrast 검사
npx @google/design.md lint DESIGN.md

# token과 lint regression 비교
npx @google/design.md diff DESIGN.md DESIGN-v2.md

# Tailwind용 export
npx @google/design.md export --format css-tailwind DESIGN.md > theme.css

# DTCG format export
npx @google/design.md export --format dtcg DESIGN.md > tokens.json

# agent prompt용 specification 출력
npx @google/design.md spec
```

> `export` 성공 ≠ `lint` 성공. CI에서 각각 실행한다.

## Token 설계

```text
primitive: gray-950, space-4
    ↓
semantic: text-primary, action-primary
    ↓
component: button-primary-bg
```

- component가 가능한 한 semantic token을 참조하게 한다.
- token name에는 값보다 역할을 담는다.
- YAML 값과 Markdown rationale를 같은 PR에서 변경한다.
- dark mode, localization, responsive behavior와 state를 함께 검토한다.

## Reference 선택 질문

- UI density가 제품과 맞는가?
- content, dashboard, code 중 어떤 typography를 우선하는가?
- accent color가 action과 decoration 중 어디에 쓰이는가?
- border, shadow, surface로 depth를 어떻게 만드는가?
- responsive와 accessibility rule이 충분히 설명되는가?

## Agent 전달 prompt

```text
Read DESIGN.md as the project design contract.
Reuse existing components before adding new ones.
Implement only the requested screen and preserve current behavior.
Do not copy logos, proprietary fonts, photos, or brand copy.
Verify responsive layout, keyboard navigation, visible focus,
semantics, contrast, and reduced motion after implementation.
```

## Do / Don't

| Do | Don't |
|---|---|
| reference를 product-specific rule로 변형 | brand identity를 그대로 복제 |
| CLI와 schema version pinning | `alpha` format을 안정된 표준으로 가정 |
| 외부 문서를 untrusted input으로 review | 외부 명령과 URL을 agent에 그대로 전달 |
| lint + visual + accessibility test 병행 | contrast lint만으로 접근성 완료 주장 |
| provenance와 retrieval date 기록 | collection을 브랜드 공식 design system으로 표현 |

## 빠른 Review Checklist

- [ ] YAML reference가 모두 해석되는가?
- [ ] required section 순서가 맞는가?
- [ ] prose와 token이 충돌하지 않는가?
- [ ] light/dark contrast를 확인했는가?
- [ ] hover/focus/disabled/error state가 있는가?
- [ ] keyboard, semantics, reduced motion을 검증했는가?
- [ ] 상표·font·photo·logo 권리를 별도로 확인했는가?
- [ ] 구현 diff와 contract diff를 함께 review했는가?

## Sources

- https://github.com/VoltAgent/awesome-design-md
- https://github.com/google-labs-code/design.md
- https://www.w3.org/community/design-tokens/

