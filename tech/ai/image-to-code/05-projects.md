---
date: 2026-09-20
tags: [tech]
type: tech-tool-study
status: draft
---

# Image to Code — Projects

> [[04-learning/02-deep-dive|이전: Deep Dive]] · [[README|목차로 돌아가기]] · [[cheatsheet|다음: Cheatsheet]]

## Project 1. Single-page Reconstruction

권한이 있는 landing page screenshot 한 장을 semantic HTML/CSS 또는 React로 재구현한다.

| 항목 | 내용 |
|---|---|
| 난이도 | Beginner |
| 입력 | Desktop screenshot, viewport, asset 원본 |
| 산출물 | 실행 가능한 page, assumption log, before/after screenshot |
| 핵심 학습 | layout decomposition, token 추출, baseline render |

완료 조건:

- Build와 browser render 성공
- 주요 block/text 누락 없음
- Heading/landmark와 native control 사용
- Reference viewport visual review 통과
- Placeholder와 추측 사항 문서화

## Project 2. Responsive Multi-state Page

Desktop/mobile 및 modal open/closed screenshot을 함께 사용해 responsive page를 만든다.

| 항목 | 내용 |
|---|---|
| 난이도 | Intermediate |
| 입력 | 2개 이상 viewport, 2개 이상 UI state |
| 산출물 | Responsive components, interaction test, visual snapshots |
| 핵심 학습 | breakpoint 추론, state modeling, content reflow |

```yaml
references:
  - file: desktop-default.png
    viewport: [1440, 1024]
    state: default
  - file: mobile-default.png
    viewport: [390, 844]
    state: default
  - file: mobile-menu-open.png
    viewport: [390, 844]
    state: navigation-open
```

완료 조건:

- Viewport별 overflow와 reflow 검사
- Menu의 focus management와 Escape 동작
- Screenshot에 없는 state는 requirement로 명시
- 각 state의 visual regression snapshot 유지

## Project 3. Component-aware Migration

기존 repository의 design system을 이용해 legacy screenshot을 재구현한다.

| 항목 | 내용 |
|---|---|
| 난이도 | Advanced |
| 입력 | Screenshot, component catalog, token, repository conventions |
| 산출물 | 기존 component를 재사용한 page와 mapping report |
| 핵심 학습 | repo-aware generation, component reuse, code quality 평가 |

```yaml
mapping:
  primary_cta: Button/primary/lg
  feature_item: Card/outlined
  heading: Typography/display-lg
  horizontal_gap: spacing/12
unresolved:
  - "Hero illustration source asset is unavailable"
```

완료 조건:

- 새 primitive보다 기존 component·token 우선
- 반복 markup을 reusable component로 추출
- Lint, typecheck, unit/interaction test 통과
- Visual fidelity 저하가 design system constraint 때문이면 기록

## Project 4. Visual Repair Agent

Browser screenshot과 DOM metadata를 이용해 mismatch를 localized patch로 고치는 loop를 구현한다.

```text
reference + current render
  → diff regions
  → DOM/component mapping
  → patch proposal
  → build/render/test
  → accept or revert
```

기록할 metric:

- Rendering success rate
- Block/text recall
- Region-level visual score
- Round별 score 변화와 token/time cost
- Regression 발생 횟수
- Human acceptance

Guardrail:

- Patch 범위 제한
- Maximum round와 no-improvement stop
- Build 실패 시 마지막 성공 상태 유지
- Dependency 추가와 외부 URL 사용은 별도 review
- 최종 accessibility와 human review 필수

## 공통 실험 기록 Template

```yaml
experiment:
  date: 2026-09-20
  input_rights_checked: true
  target_stack: React + CSS Modules
  reference_viewports: [[1440, 1024], [390, 844]]
  model_or_tool: "record exact version"
  rounds: 4
  build: pass
  visual_findings: []
  interaction_findings: []
  accessibility_findings: []
  assumptions: []
  unresolved: []
```

## Sources

- https://github.com/abi/screenshot-to-code
- https://github.com/Djanghao/widget2code
- https://arxiv.org/abs/2602.18548
- https://arxiv.org/abs/2602.05998
- https://arxiv.org/abs/2607.06306

