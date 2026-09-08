---
date: 2026-09-09
tags: [tech]
type: tech-tool-study
status: draft
---

# Remotion — Cheatsheet

[[tech/devtools/remotion/README|학습 진입점]] · 예제 전체: [[tech/devtools/remotion/04-learning/01-getting-started|Getting started]]

## 시간 계산

```text
frames = seconds × fps
seconds = durationInFrames / fps
lastFrame = durationInFrames - 1

30fps × 5초 = 150 frames (0..149)
Sequence from=60: 전체 frame 60 → 내부 frame 0
```

## 자주 쓰는 API

| API | 용도 | 주의 |
|---|---|---|
| `<Composition>` | component와 출력 설정 등록 | id와 entry 확인 |
| `useCurrentFrame()` | 현재 frame | Sequence 내부는 local frame |
| `useVideoConfig()` | fps·크기·길이 | 초와 frame 단위 혼동 금지 |
| `interpolate()` | 숫자 속성 보간 | 제한할 속성은 extrapolation clamp |
| `spring()` | spring motion | frame·fps 전달 |
| `<Sequence>` | 장면 시작·길이 | 자체적으로 transition 생성하지 않음 |
| `random(seed)` | seed 기반 랜덤 | seed를 매 render마다 바꾸지 않음 |
| `calculateMetadata()` | props·동적 영상 설정 해석 | Player에는 설정을 별도로 전달 |
| `selectComposition()` | 서버에서 composition 선택·metadata 해석 | render 단계와 같은 inputProps |
| `renderMedia()` / `renderStill()` | 영상 / 이미지 파일 출력 | Node.js renderer API |

## Motion 조각

component 내부에서 사용하는 코드다.

```tsx
import {interpolate, spring, useCurrentFrame, useVideoConfig} from 'remotion';

// Inside a React component:
const frame = useCurrentFrame();
const {fps} = useVideoConfig();
const opacity = interpolate(frame, [0, 20], [0, 1], {
  extrapolateLeft: 'clamp',
  extrapolateRight: 'clamp',
});
const scale = spring({frame, fps, config: {damping: 200}});
// Apply: style={{opacity, transform: `scale(${scale})`}}
```

## CLI

별도 실습 프로젝트의 루트에서 실행한다. 아래 `TitleCard`는 입문 예제의 Composition id다.

```bash
# Create a project using the wizard
npx create-video@latest

# Start Studio in a regular Remotion template
npm run dev

# Export the getting-started example
mkdir -p out
npx remotion render src/index.ts TitleCard out/title.mp4 --props=props.json --codec=h264

# Inspect one frame
npx remotion still src/index.ts TitleCard out/title.png --props=props.json --frame=20
```

심화 예제로 Root를 교체했다면 id를 `Report`로 바꾼다. 설치된 `remotion`과 모든 `@remotion/*`의 exact version을 일치시킨다. 조사 기준은 `4.0.522`이며 `@latest` 명령은 이후 다른 버전을 생성할 수 있다.

## Props와 export 경로

```text
Composition:
defaultProps → inputProps 병합 → calculateMetadata → 최종 props / metadata

Preview: Studio 또는 Player
Server export: Browser 프레임 캡처 → FFmpeg
Client export: Canvas 프레임 생성 → Mediabunny / WebCodecs
```

- Player를 설치하는 것만으로 파일 export가 완성되지는 않는다.
- client renderer는 `v4.0.491`부터 stable. 기본 경로의 CSS 지원은 브라우저 DOM 전체와 같지 않다.
- Media Parser는 phase-out 대상이다. 신규 미디어 처리는 Mediabunny 전환 안내를 확인한다.

## 문제 해결

| 증상 | 점검 순서 |
|---|---|
| 장면 타이밍 어긋남 | fps → 전체 frame → Sequence local frame |
| 길이만 바뀌고 내용은 이전 데이터 | metadata 선택 단계와 render 단계의 inputProps 일치 |
| font가 달라짐 | 고정 font asset → 한글 glyph → 로딩 완료 |
| 랜덤 효과가 매번 바뀜 | seed, `Math.random()`, 외부 데이터 변경 여부 |
| client export 스타일 차이 | limitations 문서 → 대표 CSS 단순화 → 실제 출력 재비교 |
| 서버 처리량 부족 | 대기 시간과 render 시간 분리 → asset I/O·동시성·메모리 측정 |
| 패키지 충돌 | 모든 Remotion package의 exact version과 lockfile 확인 |

## Sources

- [Fundamentals](https://www.remotion.dev/docs/the-fundamentals)
- [Animating properties](https://www.remotion.dev/docs/animating-properties)
- [spring](https://www.remotion.dev/docs/spring)
- [Sequence](https://www.remotion.dev/docs/sequence)
- [random](https://www.remotion.dev/docs/random)
- [calculateMetadata](https://www.remotion.dev/docs/calculate-metadata)
- [Renderer](https://www.remotion.dev/docs/renderer)
- [프로젝트 생성](https://www.remotion.dev/docs/)
- [CLI render](https://www.remotion.dev/docs/cli/render)
- [CLI still](https://www.remotion.dev/docs/cli/still)
- [Player](https://www.remotion.dev/docs/player)
- [Client-side rendering](https://www.remotion.dev/docs/client-side-rendering)
- [Client-side limitations](https://www.remotion.dev/docs/client-side-rendering/limitations)
- [Mediabunny 전환 공지](https://www.remotion.dev/blog/mediabunny)
