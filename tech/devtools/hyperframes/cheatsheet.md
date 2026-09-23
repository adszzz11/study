---
date: 2026-09-23
tags: [tech]
type: tech-tool-study
status: draft
---

# HyperFrames Cheatsheet

## 가장 짧은 workflow

```bash
# 환경 진단
npx hyperframes doctor

# 새 project
npx hyperframes init my-video
cd my-video

# 반복 authoring
npx hyperframes preview

# 구조 검사와 파일 출력
npx hyperframes lint
npx hyperframes render --output output.mp4
```

## CLI 명령어

| 목적 | 명령 | 메모 |
| --- | --- | --- |
| project 생성 | `npx hyperframes init my-video` | agent/CI는 `--non-interactive` 고려 |
| preview | `npx hyperframes preview` | HTML 변경을 빠르게 확인 |
| lint | `npx hyperframes lint` | composition 구조 오류 사전 확인 |
| render | `npx hyperframes render --output output.mp4` | 최종 MP4 생성 |
| 투명 video | `npx hyperframes render --format webm --output overlay.webm` | VP9 alpha WebM 출력 |
| 환경 진단 | `npx hyperframes doctor` | Node, FFmpeg, Chrome, Docker 등 확인 |
| 설치된 CLI 기준 확인 | `npx hyperframes <command> --help` | 문서보다 현재 설치본을 우선 |

## Timeline attribute 개념

```html
<section
  data-start="1.5"
  data-duration="2.0"
  data-track-index="1"
>
  Scene content
</section>
```

| attribute | 뜻 |
| --- | --- |
| `data-start` | composition 시작 후 clip을 시작할 시간 |
| `data-duration` | clip이 점유하는 시간 |
| `data-track-index` | track/layer 순서 표현 |

프로젝트/CLI 버전에 따라 정확한 schema가 달라질 수 있으므로 공식 HTML schema reference와 `--help`를 확인한다.

## Determinism checklist

- [ ] timestamp `T`만으로 animation state를 복원할 수 있다.
- [ ] `Date.now()`나 live network response를 visual state에 쓰지 않는다.
- [ ] font, image, video, JSON data의 version을 고정했다.
- [ ] render 전에 asset loading 완료를 보장한다.
- [ ] custom Frame Adapter는 package version을 pin하고 keyframe regression test를 둔다.
- [ ] CI render environment의 Chrome/FFmpeg/font를 Docker로 고정한다.

## Sources

- https://hyperframes.heygen.com/packages/cli
- https://hyperframes.heygen.com/concepts/frame-adapters
- https://hyperframes.heygen.com/packages/engine
