---
date: 2026-09-20
tags: [tech]
type: tech-tool-study
status: draft
---

# Image to Code — Cheatsheet

> [[README|목차로 돌아가기]]

## 핵심 Mental Model

```text
목표 ≠ 원본 source recovery
목표 = visually faithful + executable + maintainable reconstruction
```

```text
Image(s)
  → normalize
  → OCR + visual grounding
  → component/layout/token IR
  → stack-aware generation
  → build + render
  → compare + localized repair
  → multidimensional QA + human review
```

## 좋은 입력

- 정확한 viewport와 state label
- Desktop + mobile screenshot
- Default + hover/focus/modal/error state
- OCR text와 bounding box
- 원본 asset, font, design token
- Target stack와 browser support
- 기존 component library와 repository conventions

## Prompt Skeleton

```text
Reconstruct the attached UI in <target stack>.
Viewport/state: <width × height, state name>.
Reuse existing components, tokens, and supplied assets first.
Use semantic HTML and native interactive elements.
Do not invent behavior that is not visible or specified.
Avoid absolute positioning except for true overlays.
Render at the target viewport and patch the largest mismatch first.
List assumptions, placeholders, and unresolved behavior.
```

## Repair 우선순위

1. Build/runtime failure
2. Missing block·text·asset
3. Macro layout와 container size
4. Alignment와 spacing
5. Typography와 wrapping
6. Color·border·radius·shadow
7. Responsive와 interaction
8. Semantics·accessibility·code quality

## Metric Map

| 목적 | Metric/검사 |
|---|---|
| 실행 | install/build, runtime error, timeout |
| 전체 시각 | pixel diff, SSIM/LPIPS, CLIP/DINO |
| 요소 | block/text recall, position, size, color |
| 구조 | semantic HTML, reuse, lint, duplication |
| 반응형 | viewport snapshots, overflow, reflow |
| 상호작용 | click, form, modal, route, state transition |
| 접근성 | axe, keyboard, focus, contrast, ARIA |
| 보안 | dependency, secret, unsafe HTML/URL |

## 피해야 할 Pattern

- Screenshot 전체를 한 장의 background image로 처리
- 모든 요소를 absolute coordinate로 배치
- 실제 asset이 있는데 CSS/SVG로 임의 재작성
- Clickable `div`, 누락된 label/alt, 보이지 않는 focus
- Screenshot에 없는 API·auth·validation을 사실처럼 추측
- 기존 component 대신 hardcoded markup 반복
- Visual score 하나만으로 production ready 판정
- 타사 UI·asset을 권한 확인 없이 입력·게시

## Definition of Done

- [ ] Build와 browser render 성공
- [ ] 지정 viewport/state에서 주요 요소 누락 없음
- [ ] Desktop/mobile overflow와 reflow 확인
- [ ] Interaction test 통과
- [ ] Semantic HTML, keyboard, focus, ARIA 확인
- [ ] 기존 component/token 재사용 및 duplication review
- [ ] Dependency, external URL, secret 검사
- [ ] Asset/UI 권리 확인
- [ ] Assumption과 unresolved behavior 기록
- [ ] Human review 완료

## Sources

- Design2Code: https://aclanthology.org/2025.naacl-long.199/
- screenshot-to-code: https://github.com/abi/screenshot-to-code
- DesignBench: https://arxiv.org/abs/2506.06251
- 1D-Bench: https://arxiv.org/abs/2602.18548
- VisRefiner: https://arxiv.org/abs/2602.05998
- UI2App: https://arxiv.org/abs/2607.06306
- WCAG 2.2: https://www.w3.org/TR/WCAG22/
