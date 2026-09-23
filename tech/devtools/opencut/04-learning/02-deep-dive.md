---
date: 2026-09-23
tags: [tech]
type: tech-tool-study
status: draft
---

# OpenCut — Deep Dive

[[tech/devtools/opencut/README|학습 진입점]] · 이전: [[tech/devtools/opencut/04-learning/01-getting-started|Getting started]]

## 1. Keyframe과 graph editor

keyframe은 특정 시간의 property 값을 저장한다. 예를 들어 scale을 `100% → 110%`, opacity를 `0 → 100%`로 두면 clip에 zoom-in과 fade-in을 만들 수 있다. graph editor의 bezier handle은 두 keyframe 사이 변화의 acceleration을 조절한다.

실습은 position, scale, opacity를 한 clip에 각각 적용하고 다음을 비교하는 것이다.

| 설정 | 관찰할 결과 |
|---|---|
| linear | 일정한 속도로 변화 |
| ease-out | 시작은 빠르고 끝은 부드러움 |
| overshoot 없이 짧은 duration | short-form에서 과한 motion을 줄인 강조 |

## 2. Mask, blur, canvas background

mask는 layer의 일부를 hide/reveal한다. blur와 canvas background를 조합하면 세로 video에 가로 source를 넣을 때 빈 공간을 덜 산만하게 처리할 수 있다.

1. 세로 canvas에 가로 clip을 배치한다.
2. canvas background에 blur 또는 solid/gradient를 적용한다.
3. foreground clip에 rectangle/ellipse mask를 적용하고 feather를 바꾼다.
4. mobile에서 가장자리와 text contrast를 확인한다.

효과를 추가할 때는 장식보다 message hierarchy를 우선한다. mask가 내용 이해를 어렵게 하거나 blur가 caption contrast를 낮추면 제거한다.

## 3. Ripple editing

일반 trim은 clip 길이만 줄여 뒤에 빈 공간을 남길 수 있다. **ripple editing**은 한 clip을 줄이거나 삭제할 때 뒤 clip들의 time position을 보정해 gap을 닫는 작업 방식이다.

```text
Before: [A 0–5s][B 5–10s][C 10–15s]
Trim A: [A 0–3s][gap 3–5s][B 5–10s][C 10–15s]
Ripple: [A 0–3s][B 3–8s][C 8–13s]
```

release note는 ripple editing을 diff-based interval calculation으로 분리한 변화를 언급한다. 실습에서 clip A의 중간을 자른 뒤 B와 C가 어떻게 이동하는지, overlay·audio track이 의도치 않게 어긋나지 않는지 확인한다.

## 4. Rewrite와 automation 경계

rewrite의 shared Rust core는 Web·Desktop·Mobile UI와 MCP·Headless·Scripting이 동일 engine을 이용하도록 하는 방향이다. 장기적으로는 project model과 renderer를 automation에서도 재사용할 여지가 있지만, roadmap list는 stable API 계약이 아니다.

| 지금 할 수 있는 일 | 아직 전제로 두지 말아야 할 일 |
|---|---|
| classic으로 편집 UX와 template workflow 평가 | MCP로 production agent를 연결 |
| source·architecture·progress tracking 관찰 | headless batch renderer의 SLA 가정 |
| `proto use`와 Moon task로 개발 surface를 탐색 | classic 내부 API에 대한 장기 integration |

## 개발 surface 실행

공식 repository root에서 toolchain을 고정하고 각 surface를 분리 실행한다.

```sh
proto use
moon run web:dev
moon run api:dev
moon run desktop:dev
```

desktop은 공식 README 기준으로 매우 초기 단계다. local build 성공은 product readiness를 뜻하지 않으므로, 기능 확인은 status·issue·release와 함께 판단한다.

## Sources

- [v0.3.0 release](https://github.com/OpenCut-app/OpenCut/releases/tag/v0.3.0)
- [OpenCut rewrite tracking](https://github.com/OpenCut-app/OpenCut/issues/811)
- [OpenCut development commands](https://github.com/OpenCut-app/OpenCut)
- [Desktop README](https://github.com/OpenCut-app/OpenCut/blob/main/apps/desktop/README.md)
