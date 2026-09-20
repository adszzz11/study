---
date: 2026-09-20
tags: [tech]
type: tech-tool-study
status: draft
---

# awesome-design-md — Overview

> [[README|목차로 돌아가기]] · [[02-ecosystem|다음: Ecosystem]]

## What

`awesome-design-md`는 Claude, Vercel, Linear, Figma, Supabase 등 실제 서비스의 공개 UI를 관찰해 AI coding agent가 읽을 수 있는 `DESIGN.md`로 정리한 reference collection이다. 공식 브랜드 design system의 복제본이 아니라 공개된 시각 언어를 해석한 **brand-inspired analysis**다.

각 reference는 원칙적으로 다음 자산을 포함한다.

| 자산 | 역할 |
|---|---|
| `DESIGN.md` | machine-readable tokens와 human-readable rationale를 결합한 design contract |
| `preview.html` | light surface에서 token과 component의 시각적 결과 확인 |
| `preview-dark.html` | dark surface에서 contrast와 시각적 결과 확인 |

## Why

AI가 생성한 UI는 기능적으로 완성되어도 rounded card, pastel gradient, 과도한 hero, 비슷한 spacing으로 수렴하는 “AI look”이 나타나기 쉽다. 자연어 prompt나 screenshot만으로는 다음 문제가 남는다.

- 화면마다 visual direction과 spacing이 흔들린다.
- `primary`, `surface`, `muted`, `danger` 같은 색상의 semantic role이 빠진다.
- responsive behavior와 접근성 guardrail이 전달되지 않는다.
- shadow 대신 border를 쓰는 이유, accent를 제한하는 이유 같은 judgment가 소실된다.
- 새 session마다 같은 디자인 설명을 반복해야 한다.

`DESIGN.md`는 이를 repository에 저장되는 agent-readable design contract로 바꾼다.

| 계약 요소 | 담는 내용 | 예시 |
|---|---|---|
| Exact value | color, type scale, spacing, radius | `spacing.md: 16px` |
| Semantic role | token을 어디에 쓰는가 | `primary`는 핵심 action에만 사용 |
| Rationale | 왜 이 규칙을 택했는가 | depth는 shadow보다 border로 표현 |
| Guardrail | Do/Don't, responsive, accessibility | decorative accent 남용 금지 |
| Persistent context | 여러 agent/session이 공유할 기준 | repository의 `DESIGN.md` |

## 문서 구조

공식 `DESIGN.md` format은 두 계층으로 구성된다.

### 1. YAML front matter

도구가 읽는 normative token 영역이다.

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
components:
  button-primary:
    backgroundColor: "{colors.primary}"
    padding: "{spacing.md}"
---
```

공식 schema는 `colors`, `typography`, `rounded`, `spacing`, `components`와 `{colors.primary}` 형식의 token reference를 정의한다.

### 2. Markdown body

사람과 agent가 함께 읽는 rationale와 적용 규칙 영역이다. 권장 section 순서는 다음과 같다.

1. `Overview`
2. `Colors`
3. `Typography`
4. `Layout`
5. `Elevation & Depth`
6. `Shapes`
7. `Components`
8. `Do's and Don'ts`

```markdown
## Overview
정밀하고 절제된 developer-tool UI를 지향한다.

## Colors
Primary는 중요한 action에만 사용하고 장식용으로 사용하지 않는다.
```

## 핵심 특징

- **Git-native**: Markdown이므로 diff, code review, branch, rollback이 쉽다.
- **Agent-readable**: 특정 vendor API 없이 여러 coding agent가 context로 사용할 수 있다.
- **Judgment 포함**: token 값뿐 아니라 적용 의도와 금지 규칙을 기록한다.
- **Reference-first**: 익숙한 visual direction에서 시작해 자체 design language로 빠르게 변형할 수 있다.
- **Toolchain 연결**: Google CLI로 lint, diff, Tailwind/DTCG export가 가능하다.

## 역사적 맥락

| 날짜 | 변화 | 의미 |
|---|---|---|
| 2025-10-28 | W3C Design Tokens Community Group이 Design Tokens Specification 2025.10 첫 stable version 발표 | aliases, theming, modern color spaces와 cross-platform interoperability의 공통 기반 제공 |
| 2026-04-21 | Google Labs가 Stitch의 `DESIGN.md` draft specification 공개 | token과 rationale을 결합한 agent-readable format 및 CLI 공개 |

> [!warning] Alpha status
> Google의 공식 `DESIGN.md` spec은 여전히 `alpha`이며 변경 가능성이 있다. schema와 CLI version을 고정하고 migration을 code change처럼 검토한다.

## 한계와 위험

- `DESIGN.md`만 repository에 추가해도 기존 UI가 자동으로 바뀌지는 않는다.
- product design, user research, information architecture, interaction quality를 대신하지 않는다.
- collection의 분석은 각 브랜드가 보증한 공식 design system이 아니다.
- repository의 MIT license가 상표, proprietary font, 사진, 실제 brand identity의 권리를 부여하지 않는다.
- contrast lint는 keyboard, focus, semantics, reduced motion을 검증하지 않는다.
- 외부 `DESIGN.md`는 untrusted input으로 보고 무관한 명령, 의심스러운 URL, repository 밖 변경 지시를 review해야 한다.

## Sources

- https://github.com/VoltAgent/awesome-design-md
- https://github.com/google-labs-code/design.md
- https://blog.google/innovation-and-ai/models-and-research/google-labs/stitch-design-md/
- https://www.w3.org/community/design-tokens/

