---
date: 2026-09-23
tags: [tech]
type: tech-tool-study
status: draft
---

# HyperFrames: What, Why, 특징

## What

HyperFrames는 HTML을 video로 바꾸는 open-source framework다. AI agent가 HTML, CSS, JavaScript를 작성하면 결과물은 flatten된 video만 남는 대신 **수정 가능한 project folder**로 보존된다. 같은 파일을 agent, Studio, 로컬 도구가 함께 다룰 수 있다.

## Why

브라우저의 live animation을 screen recording하거나 실시간 재생으로 export하면 CPU 부하, animation clock, media timing에 따라 결과가 달라질 수 있다. HyperFrames는 renderer가 frame마다 정확한 시간을 composition에 요청하고 capture하므로, “frame N에서 어떤 pixel이 나와야 하는가”를 재현 가능한 계약으로 바꾼다.

React video tooling처럼 JSX/build step을 중심에 놓지 않고, AI agent가 다루기 쉬운 일반 HTML을 source artifact로 삼는 점도 선택 이유다.

## 핵심 특징

| 특징 | 의미 | 실무 효과 |
| --- | --- | --- |
| HTML-native composition | stage와 media layer를 HTML/data attribute로 선언 | 기존 CSS, web asset, DOM 지식을 재사용 |
| Deterministic rendering | timestamp별 seek 후 Chrome compositor 결과를 capture | live playback의 frame drop 위험 축소 |
| Seekable animation | GSAP, CSS, Lottie, Three.js 등을 Frame Adapter로 연결 | 특정 frame의 state를 계산·검증 가능 |
| Agent-first workflow | agent가 보통의 프로젝트 파일을 생성·편집 | prompt와 source file의 반복 작업이 자연스러움 |
| CLI·Studio loop | `init → preview → lint → render` | authoring부터 output까지 일관된 흐름 |

## 렌더링 모델

```text
HTML/CSS/JS composition
          │
          ├─ timeline metadata (start / duration / track)
          ▼
@hyperframes/engine: timestamp T로 seek
          ▼
headless Chrome compositor: frame pixel capture
          ▼
Producer: audio mix + FFmpeg encoding
          ▼
MP4 / WebM
```

`@hyperframes/engine`은 browser/capture orchestration을 맡고, Producer 계층은 audio mix와 FFmpeg encoding을 담당한다. 이 분리는 composition 작성자가 codec와 browser lifecycle을 직접 조율하지 않도록 한다.

## 제약과 운영상 주의점

- 렌더 비용은 대체로 frame 수 × 해상도 × scene 복잡도에 비례한다.
- 결과의 cross-machine 일관성에는 Docker, font, image/video asset, browser version을 함께 고정해야 한다.
- render 중 network fetch나 wall-clock API에 의존하면 deterministic contract가 깨질 수 있다.
- Frame Adapter API는 experimental v0이므로 version pinning과 render regression test를 둔다.
- 대규모 batch 운영에는 queue, retry, asset validation, object storage 같은 별도 운영 계층이 필요하다.

## Sources

- https://hyperframes.heygen.com/introduction
- https://hyperframes.heygen.com/packages/engine
- https://hyperframes.heygen.com/concepts/frame-adapters
- https://github.com/heygen-com/hyperframes
