---
date: 2026-09-23
tags: [tech]
type: tech-tool-study
status: draft
---

# Getting Started: 첫 composition과 render

## 목표

sample project를 만들고, HTML을 고친 뒤 preview·lint·MP4 render까지 한 번 통과한다.

## 1. 환경 확인

HyperFrames CLI는 Node.js 22 계열, FFmpeg/FFprobe, Chrome 환경을 점검할 수 있다. 먼저 설치 상태를 확인한다.

```bash
node --version
ffmpeg -version
npx hyperframes doctor
```

CI나 Linux container에서는 Chrome, Docker, `/dev/shm`, frame cache 여유 공간도 `doctor` 결과에서 확인한다.

## 2. 프로젝트 생성과 preview

```bash
npx hyperframes init my-video
cd my-video
npx hyperframes preview
```

agent/CI처럼 prompt를 피해야 하는 경우에는 `--non-interactive`를 사용한다.

```bash
npx hyperframes init my-video --non-interactive
```

`index.html`을 열어 text, color, layout을 바꾸고 Studio 또는 browser preview에서 hot reload가 되는지 확인한다. preview가 정상이어도 최종 영상의 correctness를 뜻하지는 않는다. 반드시 lint와 render까지 진행한다.

## Timeline 바꾸기

stage의 해상도와 duration, clip의 시작 시간·길이·track을 변경해 time model을 익힌다. 예시는 개념을 보여 주는 간단한 markup이다.

```html
<div class="stage" data-duration="6">
  <section data-start="0" data-duration="2" data-track-index="0">
    <h1>Launch</h1>
  </section>
  <section data-start="2" data-duration="4" data-track-index="1">
    <p>HTML to deterministic video</p>
  </section>
</div>
```

- 첫 clip의 `data-duration`을 2초에서 3초로 바꾼다.
- 둘째 clip의 `data-start`도 3초로 옮겨 gap/overlap을 의도적으로 만든다.
- track index를 바꿔 layer 순서가 기대와 맞는지 preview로 본다.

정확한 schema와 지원 attribute는 설치된 CLI와 공식 HTML schema reference를 우선한다.

## 3. 검사와 render

```bash
npx hyperframes lint
npx hyperframes render --output output.mp4
```

render 후에는 영상의 시작·전환·마지막 frame을 확인한다. layout만 볼 경우 snapshot/keyframe 비교를 병행하고, motion도 검증할 경우 CLI의 `check`, `compare` 계열을 검토한다.

## 완료 기준

- [ ] `doctor`가 필수 render dependency를 통과한다.
- [ ] preview에서 HTML 변경이 보인다.
- [ ] lint 오류가 없다.
- [ ] `output.mp4`가 생성되고 clip 전환이 의도한 timestamp에 있다.
- [ ] 동일 입력으로 다시 render했을 때 주요 frame 차이가 없는지 확인했다.

## Sources

- https://hyperframes.heygen.com/packages/cli
- https://hyperframes.heygen.com/introduction
