---
date: 2026-09-20
tags: [tech]
type: tech-tool-study
status: draft
---

# Image to Code — Getting Started

> [[../03-references|이전: References]] · [[../README|목차로 돌아가기]] · [[02-deep-dive|다음: Deep Dive]]

## 목표

한 장의 UI screenshot을 유지보수 가능한 static page로 재구현하고, browser screenshot으로 차이를 확인한다. 첫 실습에서는 behavior를 추측하지 않고 **명시적으로 관찰 가능한 범위**만 구현한다.

## 1. 입력과 권한 준비

- [ ] 직접 만들었거나 재구현 권한이 있는 screenshot인가?
- [ ] Target viewport width/height를 아는가?
- [ ] 사용 가능한 logo, icon, image, font 원본이 있는가?
- [ ] Desktop 외 mobile screenshot 또는 다른 state가 있는가?
- [ ] 민감 정보가 screenshot에 포함되지 않았는가?

```yaml
input:
  reference: landing-desktop.png
  viewport: {width: 1440, height: 1024}
  states: [default]
  assets_dir: ./public/assets
  target: React + CSS Modules
  authorized: true
```

## 2. 화면을 구조로 분해

코드를 생성하기 전에 page region과 반복 component를 적는다.

```text
Page
├── Header
│   ├── Logo
│   ├── Navigation
│   └── PrimaryAction
├── Hero
│   ├── Copy
│   └── ProductImage
└── FeatureGrid
    └── FeatureCard × 3
```

함께 추출할 값:

- Content container의 최대 폭과 좌우 gutter
- Section 간 vertical spacing
- Font family, size, weight, line-height
- Color, border, radius, shadow
- Grid/Flex 정렬과 gap
- 반복 component와 variant

## 3. 생성 contract 작성

```text
Target: React + CSS Modules.
Use the repository's existing components and tokens first.
Implement semantic landmarks and native interactive elements.
Do not invent interactions that are not visible in the references.
Do not redraw supplied assets with CSS or generated SVG.
Match the 1440×1024 reference, then add a simple mobile reflow.
Avoid absolute positioning except for true overlays.
Return a short list of assumptions and unresolved details.
```

“똑같이 만들어 줘”보다 stack, 재사용 우선순위, 금지 사항, viewport, 완료 조건을 명시하는 편이 결과를 안정시킨다.

## 4. Baseline 구현

첫 pass의 우선순위는 다음과 같다.

1. Build와 browser render가 성공한다.
2. 큰 layout block의 위치와 크기를 맞춘다.
3. 실제 text와 asset을 넣는다.
4. Typography, color, border, shadow를 맞춘다.
5. Semantic HTML과 keyboard behavior를 보완한다.

```html
<header>...</header>
<main>
  <section aria-labelledby="hero-title">...</section>
  <section aria-labelledby="features-title">...</section>
</main>
```

Click 가능한 `div`보다 `button`과 `a` 같은 native element를 우선한다.

## 5. Render와 비교

Reference와 동일한 viewport, browser, device scale에서 screenshot을 만든다.

| 비교 순서 | 질문 |
|---|---|
| 1. Macro layout | section 높이, container 폭, column 비율이 맞는가? |
| 2. Element recall | 빠진 text, icon, card, divider가 있는가? |
| 3. Alignment | baseline, center, edge 정렬이 맞는가? |
| 4. Typography | font, size, weight, line-height, wrapping이 맞는가? |
| 5. Surface | color, radius, border, shadow가 맞는가? |

Mismatch를 한 번에 모두 고치지 말고 가장 큰 원인부터 patch한다.

```yaml
iteration: 2
region: hero
observed: "copy column is 56 px too wide; heading wraps one line later"
likely_cause: "grid template ratio and max-width"
patch_scope: "Hero.module.css"
result: "re-render required"
```

## 6. 완료 전 검사

- [ ] Fresh install/build와 browser runtime이 성공한다.
- [ ] Reference viewport에서 큰 누락이나 overflow가 없다.
- [ ] Mobile viewport에서 reflow가 깨지지 않는다.
- [ ] Heading/landmark 구조와 `alt`, `label`이 적절하다.
- [ ] Keyboard로 주요 control을 사용할 수 있고 focus가 보인다.
- [ ] Hardcoded coordinate와 중복 markup이 과도하지 않다.
- [ ] 추측한 behavior와 placeholder asset을 문서화했다.
- [ ] 사용한 asset과 UI에 대한 권한을 확인했다.

## Sources

- https://aclanthology.org/2025.naacl-long.199/
- https://github.com/abi/screenshot-to-code
- https://www.w3.org/TR/WCAG22/

