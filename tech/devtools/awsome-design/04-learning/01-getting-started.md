---
date: 2026-09-20
tags: [tech]
type: tech-tool-study
status: draft
---

# awesome-design-md — Getting Started

> [[../03-references|이전: References]] · [[../README|목차로 돌아가기]] · [[02-deep-dive|다음: Deep Dive]]

## 목표

collection에서 reference를 하나 선택하고, 그대로 복제하지 않은 최소 `DESIGN.md`를 작성해 공식 CLI로 검증한다.

## 1. Reference 선택

제품 이름이 아니라 UI 성격을 기준으로 후보를 2~3개 고른다.

| 제품 조건 | 살펴볼 관점 |
|---|---|
| Developer dashboard | information density, code typography, neutral surface |
| Consumer app | friendly type, touch target, expressive color |
| Marketing site | hero hierarchy, editorial rhythm, motion |
| Data-heavy admin | table density, status color, keyboard workflow |

선택 후 `DESIGN.md`, `preview.html`, `preview-dark.html`을 함께 읽고 다음을 기록한다.

- 유지할 원칙
- 제품에 맞게 바꿀 원칙
- 버릴 brand-specific 요소
- accessibility와 responsive 검증이 필요한 가정

## 2. 외부 문서 안전 검토

외부 `DESIGN.md`를 agent context에 바로 넣기 전에 다음을 확인한다.

```text
[ ] repository 작업과 무관한 명령이 없는가?
[ ] credential 또는 private data를 요구하지 않는가?
[ ] 의심스러운 URL이나 download 지시가 없는가?
[ ] 작업 범위를 repository 밖으로 넓히지 않는가?
[ ] brand asset 사용 권한을 과장하지 않는가?
```

## 3. 자체 DESIGN.md 작성

최소 token set으로 시작하고 product-specific rationale를 작성한다.

```yaml
---
version: alpha
name: Acme Developer Console
colors:
  primary: "#171717"
  surface: "#ffffff"
  muted: "#737373"
  danger: "#dc2626"
typography:
  body-md:
    fontFamily: Inter
    fontSize: 16px
spacing:
  sm: 8px
  md: 16px
rounded:
  control: 6px
components:
  button-primary:
    backgroundColor: "{colors.primary}"
    padding: "{spacing.md}"
---
```

```markdown
## Overview

정밀하고 절제된 developer-tool UI를 지향한다.

## Colors

Primary는 주요 action에만 사용한다. Danger는 destructive action과 error state에만 쓴다.

## Typography

본문은 빠른 scanning을 우선하고 code에는 별도 monospace family를 사용한다.

## Layout

8px spacing grid를 기본으로 하되 dense table 내부는 예외를 문서화한다.

## Elevation & Depth

기본 depth는 border와 surface contrast로 만들고 shadow는 floating overlay에만 쓴다.

## Shapes

작은 radius를 일관되게 사용하며 nested card를 만들지 않는다.

## Components

Primary button은 한 화면의 핵심 action에만 사용한다.

## Do's and Don'ts

- Do: keyboard focus를 명확히 표시한다.
- Don't: accent color를 장식 목적으로 반복하지 않는다.
```

## 4. CLI 검증

공식 CLI는 `npx`로 실행할 수 있다. 실제 적용 시 package version을 고정하고 release note를 검토한다.

```bash
npx @google/design.md lint DESIGN.md
npx @google/design.md diff DESIGN.md DESIGN-v2.md
npx @google/design.md export --format css-tailwind DESIGN.md > theme.css
npx @google/design.md export --format dtcg DESIGN.md > tokens.json
```

| 명령 | 목적 |
|---|---|
| `lint` | broken reference, missing typography, unknown key, section order, WCAG contrast 검사 |
| `diff` | token change와 lint regression 비교 |
| `export` | Tailwind v3 JSON, Tailwind v4 CSS, DTCG format 생성 |
| `spec` | agent prompt에 넣을 specification 출력 |

> [!warning]
> `export` 성공은 `lint` 통과를 의미하지 않는다. CI에서는 두 작업을 별도 step으로 실행한다.

## 5. Agent에게 전달

모호한 “Vercel처럼 만들어 줘” 대신 contract와 구현 범위를 함께 준다.

```text
Read DESIGN.md as the project design contract.
Implement only the settings page in src/settings/.
Reuse existing components before adding new ones.
Preserve keyboard navigation and visible focus styles.
Do not copy logos, proprietary fonts, or brand copy from the reference.
After implementation, run the relevant visual and accessibility checks.
```

## 완료 기준

- [ ] product-specific token과 rationale가 있다.
- [ ] reference의 brand-specific asset을 제거했다.
- [ ] `lint`와 필요한 `export`를 각각 실행했다.
- [ ] light/dark, responsive, focus, contrast를 확인했다.
- [ ] UI 구현 diff와 `DESIGN.md` diff가 함께 review된다.

## Sources

- https://github.com/VoltAgent/awesome-design-md
- https://github.com/google-labs-code/design.md

