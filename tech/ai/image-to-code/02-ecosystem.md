---
date: 2026-09-20
tags: [tech]
type: tech-tool-study
status: draft
---

# Image to Code — Ecosystem

> [[01-overview|이전: Overview]] · [[README|목차로 돌아가기]] · [[03-references|다음: References]]

## 접근 방식 비교

| 도구/접근 | 입력 → 출력 | 강점 | 적합한 경우 / 한계 |
|---|---|---|---|
| **Google Stitch** | text·image → UI design·frontend code | Gemini 기반 visual generation, chat refinement | 빠른 UI exploration에 적합. 기존 대형 codebase의 정밀 patch와는 목적이 다름 |
| **Figma Make** | Figma context·prompt → interactive prototype/code | design context와 대화형 iteration을 연결 | Figma 중심 workflow에 유리. Third-party content 권리와 publish 전 검토 필요 |
| **abi/screenshot-to-code** | screenshot → HTML/React/Vue 등 | 실제 asset 추출과 Chromium 기반 결과 확인 workflow | 공개 reference implementation과 local 실험에 유용. Production code 품질은 별도 review 필요 |
| **Widget2Code** | mobile UI image → WidgetDSL/code | layout detection, component recognition, icon retrieval 결합 | structured IR 연구에 유리. 일반 web app behavior 전체 복원과는 범위가 다름 |
| **General-purpose MLLM + coding agent** | image + repo context → code patch | 기존 codebase, test, browser tool을 함께 사용 가능 | model·prompt·tooling에 따라 편차가 크고 sandbox/guardrail 필요 |
| **수동 구현** | design spec → code | semantics, accessibility, architecture를 사람이 통제 | 시간이 더 들지만 고위험·복잡한 product UI에 여전히 필요 |
| **원본 design/code handoff** | Figma/source → implementation | token, component, behavior의 가장 정확한 근거 | 원본 접근이 가능하면 screenshot-only 방식보다 우선 |

## Research benchmark 비교

| 연구 | 평가 초점 | 이 노트에서의 의미 |
|---|---|---|
| **Design2Code** (2025) | 484개 real-world webpage, block/text/position/color와 human evaluation | pixel/CLIP 한 가지 지표로 충분하지 않음 |
| **DesignBench** (2025) | framework 기반 design-to-code 결과 | 시각적으로 맞아도 component reuse 대신 markup duplication이 생길 수 있음 |
| **1D-Bench** (2026) | multi-round component editing | 반복 editing이 rendering success와 visual similarity를 개선할 수 있음 |
| **VisRefiner** (2026) | visual difference를 code edit에 연결, self-refinement | diff를 localized repair action으로 바꾸는 구조가 중요 |
| **UI2App** (2026) | screenshot에서 multi-route app behavior 추론 | 정적 화면을 넘어 interaction 평가가 필요 |

## 선택 기준

| 질문 | 선택에 미치는 영향 |
|---|---|
| 원본 Figma/source가 있는가? | 있으면 structured metadata와 source를 우선한다. |
| 기존 repository를 수정하는가? | repo-aware coding agent와 localized patch가 적합하다. |
| 단순 prototype인가? | hosted generation tool로 빠르게 탐색할 수 있다. |
| pixel fidelity가 최우선인가? | asset reuse와 render–compare loop가 필수다. |
| production 배포인가? | semantic HTML, accessibility, security, interaction test를 추가한다. |
| 민감하거나 타사 소유 UI인가? | 입력·저장·게시 권한과 서비스 data policy를 먼저 확인한다. |

## 권장 조합

```text
원본 design metadata가 있음
  → Figma/design token/component library를 source of truth로 사용

screenshot만 있고 빠른 prototype이 목표
  → image-to-code tool → browser render → human refinement

기존 production repository에 통합
  → repo-aware agent → component mapping → localized patch
    → tests + visual regression + accessibility + review
```

## Sources

- https://developers.googleblog.com/stitch-a-new-way-to-design-uis/
- https://help.figma.com/hc/en-us/articles/31304485164695-Create-a-Figma-Make-file
- https://github.com/abi/screenshot-to-code
- https://github.com/Djanghao/widget2code
- https://aclanthology.org/2025.naacl-long.199/
- https://arxiv.org/abs/2506.06251
- https://arxiv.org/abs/2602.18548
- https://arxiv.org/abs/2602.05998
- https://arxiv.org/abs/2607.06306

