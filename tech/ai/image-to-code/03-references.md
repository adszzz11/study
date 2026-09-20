---
date: 2026-09-20
tags: [tech]
type: tech-tool-study
status: draft
---

# Image to Code — References

> [[02-ecosystem|이전: Ecosystem]] · [[README|목차로 돌아가기]] · [[04-learning/01-getting-started|다음: Getting Started]]

## 읽기 순서

| 순서 | 자료 | 핵심 질문 |
|---|---|---|
| 1 | Design2Code | 현재 MLLM이 어떤 visual element와 layout을 놓치는가? |
| 2 | screenshot-to-code | 실제 generation/render 확인 loop는 어떻게 구성되는가? |
| 3 | DesignBench | visual fidelity 외 code quality 문제는 무엇인가? |
| 4 | 1D-Bench·VisRefiner | multi-round refinement가 어떻게 평가되고 학습되는가? |
| 5 | Widget2Code | IR, component recognition, icon retrieval은 어떻게 결합되는가? |
| 6 | UI2App | screenshot에서 behavior까지 추론하려면 무엇을 평가해야 하는가? |
| 7 | WCAG 2.2 | 이미지로 보이지 않는 accessibility requirement는 무엇인가? |

## 논문과 Benchmark

### Design2Code — NAACL 2025

- URL: https://aclanthology.org/2025.naacl-long.199/
- 484개 real-world webpage를 평가한다.
- Visual element recall, layout accuracy, text·position·color 같은 세부 metric을 함께 본다.
- Human evaluation과 automated metric 사이의 차이를 이해하는 출발점이다.

### DesignBench

- URL: https://arxiv.org/abs/2506.06251
- Framework 기반 결과에서 component reuse와 markup duplication을 함께 살펴볼 때 유용하다.
- “보이는 결과”와 “유지보수 가능한 code”를 분리해 평가해야 함을 보여준다.

### 1D-Bench

- URL: https://arxiv.org/abs/2602.18548
- Multi-round component editing과 rendering success를 다룬다.
- 단발 score보다 iteration trajectory와 failure recovery를 기록하는 근거가 된다.

### VisRefiner

- URL: https://arxiv.org/abs/2602.05998
- Target과 rendered output의 visual difference를 code edit에 연결한다.
- Region/component 단위의 localized repair 설계에 참고한다.

### UI2App

- URL: https://arxiv.org/abs/2607.06306
- 327개 screenshot과 45개 multi-route app set에서 behavior 추론까지 평가한다.
- Navigation과 state transition을 별도 acceptance criterion으로 두는 근거다.

## 구현 Reference

### abi/screenshot-to-code

- URL: https://github.com/abi/screenshot-to-code
- Screenshot에서 asset을 추출하고 Chromium rendering으로 결과를 확인하는 workflow를 살펴본다.
- 특정 구현을 그대로 production에 쓰기보다 pipeline 구성과 실험 setup을 참고한다.

### Widget2Code

- URL: https://github.com/Djanghao/widget2code
- Layout detection, component recognition, icon retrieval, `WidgetDSL` 연결 방식을 확인한다.
- 직접 JSX를 생성하는 방식과 IR 기반 방식을 비교한다.

## Product와 표준

| 자료 | URL | 확인할 내용 |
|---|---|---|
| Google Stitch 소개 | https://developers.googleblog.com/stitch-a-new-way-to-design-uis/ | text/image 기반 UI generation과 refinement |
| Figma Make 안내 | https://help.figma.com/hc/en-us/articles/31304485164695-Create-a-Figma-Make-file | design context 활용, third-party content 사용권 주의 |
| W3C WCAG 2.2 | https://www.w3.org/TR/WCAG22/ | text alternative, keyboard, focus, name/role/value |

## Source 평가 메모

- 논문 수치는 해당 benchmark의 dataset·task·시점에 한정해서 해석한다.
- Product 기능은 바뀔 수 있으므로 사용 직전에 공식 문서를 다시 확인한다.
- Repository example은 license, dependency, model/API cost, data handling을 별도로 확인한다.
- Screenshot이나 design asset의 입력·재사용·게시 권한은 기술적 가능성과 별개의 조건이다.

## Sources

- https://aclanthology.org/2025.naacl-long.199/
- https://arxiv.org/abs/2506.06251
- https://arxiv.org/abs/2602.18548
- https://arxiv.org/abs/2602.05998
- https://arxiv.org/abs/2607.06306
- https://github.com/abi/screenshot-to-code
- https://github.com/Djanghao/widget2code
- https://developers.googleblog.com/stitch-a-new-way-to-design-uis/
- https://help.figma.com/hc/en-us/articles/31304485164695-Create-a-Figma-Make-file
- https://www.w3.org/TR/WCAG22/
