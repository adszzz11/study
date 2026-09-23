---
date: 2026-09-23
tags: [tech]
type: tech-tool-study
status: draft
---

# Deep Dive: deterministic timeline과 Frame Adapter

## Deterministic rendering의 계약

일반 animation은 “지금부터 얼마나 시간이 흘렀는가”에 따라 움직인다. HyperFrames는 그 대신 renderer가 timestamp `T`를 지정하고 composition/runtime이 **T일 때의 state**를 복원하도록 요구한다.

```text
render frame 120 at 30 fps
  → T = 4.000s
  → runtime.seek(T)
  → DOM / Canvas / WebGL state settled
  → Chrome captures pixels
```

따라서 `Date.now()`, `performance.now()`, `requestAnimationFrame` 누적, render 도중의 network fetch처럼 실행 순간에 따라 달라지는 입력을 animation source로 삼지 않는다. asset과 data는 render 시작 전에 고정하거나 명시적으로 preload한다.

## GSAP과 Frame Adapter

GSAP timeline을 쓸 때는 timeline의 현재 위치가 render timestamp로부터 결정되게 한다. 중요한 것은 API 명칭보다 다음 불변식이다.

- 같은 input과 `T`는 같은 visual state를 낸다.
- seek가 frame 순서와 무관하게 동작한다. 즉 10초 frame 뒤에 2초 frame을 요청해도 맞아야 한다.
- media/font/asset loading이 capture 전에 완료된다.

Frame Adapter는 GSAP, CSS, Lottie, Three.js 등 custom runtime을 HyperFrames host에 연결하는 확장점이다. 공식 문서상 exported `FrameAdapter` interface는 **experimental v0 API**이므로 production integration에는 정확한 package version 고정과 rendering regression test가 필요하다.

## Regression test 전략

| 위험 | 검증 방법 |
| --- | --- |
| font fallback | container에 font를 포함하고 keyframe screenshot을 비교 |
| runtime seek 버그 | 0초, 전환 직전/직후, 마지막 frame을 비순차 seek해 비교 |
| asset 변경 | content hash 또는 manifest로 asset version을 고정 |
| adapter API 변경 | package pinning, sample composition render를 CI에 추가 |
| environment drift | Docker/browser/FFmpeg version을 image로 고정 |

## Cloud render 설계

공식 deploy guide의 template은 preview용 `<hyperframes-player>`와 render API를 출발점으로 제공한다. 서비스로 운영할 때는 Chromium·FFmpeg가 포함된 container/sandbox 위에 다음을 추가한다.

```text
authenticated /api/render
       │
       ▼
validate composition + assets
       │
       ▼
queue ── idempotency / deduplication ── retry policy
       │
       ▼
isolated render worker (Chrome + FFmpeg)
       │
       ▼
Blob / R2 object storage + signed result URL
```

tenant별 rate limit, storage retention, 실패 원인 관측, asset 크기·형식 검증을 application layer의 책임으로 둔다.

## Sources

- https://hyperframes.heygen.com/packages/engine
- https://hyperframes.heygen.com/concepts/frame-adapters
- https://hyperframes.heygen.com/guides/deploy
- https://hyperframes.heygen.com/packages/cli
