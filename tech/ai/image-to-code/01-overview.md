---
date: 2026-09-20
tags: [tech]
type: tech-tool-study
status: draft
---

# Image to Code — Overview

> [[README|목차로 돌아가기]] · [[02-ecosystem|다음: Ecosystem]]

## What

Image to code는 UI 이미지를 분석해 실행 가능한 frontend code로 재구성하는 기술이다. 초기의 대표적 접근은 pix2code의 `CNN encoder → RNN decoder → DSL/code` 구조였지만, 최근에는 vision과 code generation을 함께 처리하는 **Multimodal LLM(MLLM)** 및 coding agent가 중심이다.

입력과 출력의 범위는 다음과 같다.

| 구분 | 예시 |
|---|---|
| 입력 | screenshot, wireframe, Figma frame, 여러 viewport/state 이미지 |
| 중간 표현 | bounding box tree, layout graph, semantic component tree, design token, DSL |
| 출력 | HTML/CSS, Tailwind, React/Next.js, Vue, Angular, Svelte |
| 검증 | browser render, visual diff, DOM/interaction test, accessibility audit |

## Why

- 반복적인 UI scaffold와 styling 작업을 줄인다.
- 초기 prototype을 빠르게 만들어 요구사항을 대화형으로 구체화한다.
- 디자인과 구현 사이의 간격을 browser rendering 결과로 확인한다.
- 기존 component library와 design token을 재사용해 handoff를 가속한다.

하지만 screenshot에는 다음 정보가 없다.

- hover·focus·validation·animation·routing 같은 behavior
- mobile/tablet breakpoint와 content reflow
- DOM semantics, ARIA, keyboard navigation
- 실제 asset 원본, font, design token
- API·state management·authentication·backend contract

따라서 결과물은 source recovery가 아니라 **관찰 가능한 화면을 바탕으로 한 가설적 재구현**이다. 누락된 behavior와 semantics는 명시적 요구사항, 추가 state 이미지, 기존 codebase에서 보완해야 한다.

## 핵심 특징

### 1. Input normalization

이미지를 resize·crop·color normalization한다. Desktop 한 장보다 desktop/mobile, modal open/closed, hover/focus처럼 여러 viewport와 state를 함께 주면 responsive layout과 behavior 추론이 쉬워진다.

### 2. Visual grounding

MLLM 또는 detector가 hierarchy, spacing, alignment, typography, color, border, icon, image region을 찾는다. 작은 글자와 비영어 text에는 OCR text와 bounding box를 별도로 제공하는 방식이 유리하다. Design2Code에서는 text-augmented prompting이 여러 모델의 element recall을 개선했다.

### 3. Asset pipeline

Logo, hero image, icon을 crop·retrieve·reuse하고, 대체할 수 없는 asset은 placeholder로 표시한다. Asset을 무조건 CSS나 SVG로 다시 그리면 visual fidelity와 권리 추적성이 모두 나빠질 수 있다.

### 4. Intermediate Representation(IR)

복잡한 pipeline은 이미지에서 JSX를 바로 생성하기보다 다음 구조를 거친다.

```yaml
page:
  tokens:
    color: {primary: "#...", surface: "#..."}
    spacing: [4, 8, 12, 16, 24, 32]
  components:
    - type: header
      layout: horizontal
      children: [logo, navigation, actions]
    - type: hero
      layout: two-column
      children: [copy, media]
```

Widget2Code는 layout detection, component recognition, 대규모 icon retrieval을 결합해 `WidgetDSL`을 생성한다.

### 5. Stack-aware generation

생성 전에 framework, styling 방식, component library, component 분리 기준, props/data model, breakpoint, browser support를 고정한다. 그렇지 않으면 겉보기에는 맞지만 hardcoded `div`와 반복 markup이 많은 결과가 나오기 쉽다.

### 6. Render–Compare–Repair

```text
generate → build → render → compare → locate mismatch → patch → repeat
```

2025–2026년의 핵심 변화는 단발 생성에서 **agentic visual refinement**로 이동한 것이다. 전체 파일을 매번 다시 만들기보다 차이가 큰 region과 관련 component를 찾아 localized patch를 적용한다.

### 7. 다차원 평가

| 평가축 | 대표 검사 |
|---|---|
| 실행 가능성 | install/build 성공, runtime error, timeout |
| Visual fidelity | pixel diff, SSIM/LPIPS, CLIP/DINO similarity |
| 세부 요소 | block recall, text, position, size, color |
| 구조·품질 | semantic HTML, component reuse, lint, duplication |
| Responsive | desktop/tablet/mobile, overflow, reflow |
| Interaction | click, form, modal, navigation, state transition |
| Accessibility | axe, keyboard, focus order, contrast, ARIA |
| Security | dependency, secret, unsafe HTML/URL 검사 |

## 현재 한계

Design2Code는 484개 real-world webpage 평가에서 visual element recall과 layout 정확도를 주요 약점으로 지적했다. Human evaluation에서 생성물이 원본을 대체할 수 있다고 평가된 비율은 49%였고, 복잡한 HARD set에서는 최신 모델도 block element의 30–40%를 놓쳤다. Demo 품질과 production readiness는 여전히 구분해야 한다.

## Sources

- https://aclanthology.org/2025.naacl-long.199/
- https://github.com/abi/screenshot-to-code
- https://github.com/Djanghao/widget2code
- https://arxiv.org/abs/2506.06251
- https://arxiv.org/abs/2602.18548
- https://arxiv.org/abs/2602.05998

