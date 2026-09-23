---
date: 2026-09-23
tags: [tech]
type: tech-tool-study
status: draft
---

# OpenCut — Cheatsheet

[[tech/devtools/opencut/README|학습 진입점]]

## 상태 한눈에 보기

| 항목 | 기억할 내용 |
|---|---|
| 현재 editor | `opencut.app`의 **classic** |
| rewrite preview | `new.opencut.app` |
| license | MIT |
| rewrite 중심 | 하나의 Rust core engine을 여러 UI/automation surface가 공유 |
| roadmap | Editor API, plugin, MCP, headless, scripting, desktop/mobile |
| 안전한 해석 | roadmap은 제공 완료 기능이 아니다. |

## Classic 작업 순서

```text
import → timeline 배치 → trim/split → text/caption
       → preview 검수 → export → target device 재생 확인
```

## 편집 용어

| 용어 | 뜻 |
|---|---|
| **trim** | clip의 시작 또는 끝 구간을 줄임 |
| **split** | 한 clip을 playhead 지점에서 둘로 나눔 |
| **ripple editing** | 편집 후 뒤 clip을 이동해 timeline의 gap을 닫음 |
| **keyframe** | 특정 시간의 property 값 |
| **graph editor** | keyframe 사이의 easing curve 편집기 |
| **mask** | layer의 보이는 영역을 제한하는 shape/region |
| **canvas background** | source 바깥의 video canvas 배경 |

## v0.3.0에서 확인할 기능

- masks: split, rectangle, ellipse, star 등과 position·feather·stroke 조절
- keyframe curves를 위한 graph editor
- audio/video volume·speed control 및 maintain pitch option
- preview zoom/pan, custom canvas size, canvas backgrounds
- transcript file import 기반 caption 생성

## 개발 명령

```sh
proto use
moon run web:dev       # localhost:5173
moon run api:dev       # localhost:8787
moon run desktop:dev   # apps/desktop/README.md 참고
```

## 도입 전 질문

- 필요한 기능이 classic에 오늘 실제로 있는가?
- browser workflow의 media 저장·처리·export가 조직 정책에 맞는가?
- automation requirement가 stable public API를 요구하는가?
- 장편·다층 editing에는 Kdenlive/Shotcut이 더 맞지 않는가?

## Sources

- [OpenCut current status and development](https://github.com/OpenCut-app/OpenCut)
- [Rewrite tracking](https://github.com/OpenCut-app/OpenCut/issues/811)
- [v0.3.0 release](https://github.com/OpenCut-app/OpenCut/releases/tag/v0.3.0)
- [OpenCut classic editor](https://opencut.app/)
