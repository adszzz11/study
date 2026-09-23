---
date: 2026-09-23
tags: [tech]
type: tech-tool-study
status: draft
---

# Ecosystem과 대안 비교

## 비교표

| 도구 | 주 authoring model | 강점 | HyperFrames를 택할 때 / 피할 때 |
| --- | --- | --- | --- |
| **HyperFrames** | HTML/CSS/JS + agent skill | 웹 자산 재사용, seek 기반 deterministic capture, Apache-2.0 | agent-driven HTML motion graphic·브랜드 영상에 적합. 대규모 managed distributed rendering은 운영 계층을 따로 설계한다. |
| [Remotion](https://www.remotion.dev/) | React/JSX | 성숙한 React 생태계, serverless rendering 선택지 | 이미 React composition 체계라면 강력한 대안. 조직·사용 형태에 따라 Company License 필요 여부를 확인한다. |
| [Motion Canvas](https://motioncanvas.io/docs/) | TypeScript generator + Canvas | 설명형 vector animation, editor/FFmpeg exporter | Canvas-centric 정밀 animation에 적합. HTML/CSS passthrough와 agent-first workflow는 HyperFrames가 자연스럽다. |
| [Manim Community](https://docs.manim.community/en/stable/) | Python scene graph | 수학·과학 시각화, LaTeX 중심 scene | 수식·기하·교육용 animation은 Manim이 우세하다. 웹 UI·product demo는 HyperFrames가 더 직접적이다. |
| browser capture / Playwright 녹화 | live page | 빠른 prototype | timing risk가 허용되는 일회성 capture에 한정한다. frame-accurate output에는 HyperFrames가 낫다. |

## 선택 기준

1. **source of truth**가 무엇인가? HTML/DOM이면 HyperFrames, React component면 Remotion, Python scene이면 Manim을 먼저 검토한다.
2. **재현성**이 중요한가? timestamp별 state를 보장해야 하면 live capture보다 deterministic render를 택한다.
3. **운영 모델**은 무엇인가? multi-tenant batch render라면 framework 선택과 별개로 queue, idempotency, storage, observability가 필요하다.
4. **라이선스**는 맞는가? Remotion을 상용 조직에서 쓰기 전에는 현재 license 조건을 공식 문서에서 재확인한다.

## HyperFrames 패키지 지형

| 계층 | 대표 package / 기능 | 역할 |
| --- | --- | --- |
| Authoring | CLI, Studio, Core | project 생성, 편집, 구조 검사 |
| Preview | Player, `<hyperframes-player>` | browser에서 composition 미리보기 |
| Render | Engine, Producer | Chrome capture, audio mix, encode |
| Integration | SDK, deploy templates | embedded editing, render API 구성 |

## Sources

- https://hyperframes.heygen.com/introduction
- https://hyperframes.heygen.com/packages/cli
- https://www.remotion.dev/
- https://github.com/remotion-dev/remotion/blob/main/packages/core/LICENSE.md
- https://motioncanvas.io/docs/
- https://docs.manim.community/en/stable/
