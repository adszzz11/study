---
date: 2026-09-23
tags: [tech]
type: tech-tool-study
status: draft
---

> **한 줄 정의**: HyperFrames는 AI agent가 만든 HTML/CSS/JavaScript composition을 프레임별로 seek하여 deterministic MP4/WebM으로 렌더링하는 HeyGen의 Apache-2.0 오픈소스 video-rendering framework다.

## Overview

HyperFrames는 웹 기술로 만든 motion graphic을 편집 가능한 프로젝트 폴더로 유지하면서, live playback이 아닌 **정확한 timestamp별 capture**로 영상 파일을 만든다. 느린 장비나 animation clock의 흔들림 때문에 frame이 누락될 위험을 줄이는 것이 핵심이다.

- Authoring: 일반 HTML/CSS/JavaScript와 agent workflow
- Timeline: `data-start`, `data-duration`, `data-track-index` 등의 data attribute
- Rendering: headless Chrome capture + FFmpeg encoding
- Tooling: CLI, Studio, Player, Core, Engine, Producer 패키지
- 확인 기준: 현재 확인한 최신 안정 릴리스는 `v0.8.60` (2026-09-22)이다.

세부 개념은 [[01-overview|개요]], 대안 선택은 [[02-ecosystem|에코시스템]], 명령어는 [[cheatsheet|치트시트]]에서 확인한다.

## Learning Path

- [ ] [[04-learning/01-getting-started|환경 준비와 첫 렌더]]: Node.js 22+, FFmpeg, sample project, preview
- [ ] [[04-learning/01-getting-started#timeline-바꾸기|Timeline 바꾸기]]: stage/clip의 duration·track을 조정
- [ ] [[04-learning/02-deep-dive|Deterministic rendering 심화]]: seek contract와 runtime 제약 이해
- [ ] [[04-learning/02-deep-dive#gsap과-frame-adapter|GSAP과 Frame Adapter]]: seekable animation을 구현·검증
- [ ] [[05-projects|실전 프로젝트]]: template, render API, queue 설계로 확장

## When To Use

- HTML/CSS 기반 브랜드 motion graphic, product demo, social video를 자동화할 때
- CMS/JSON data만 바꿔 9:16·16:9 등 영상 variant를 대량 생성할 때
- AI agent가 생성·수정할 수 있는 웹 source artifact와 영상 export를 함께 관리할 때
- live browser recording보다 frame-accurate output과 regression 검증이 중요할 때

## When Not To Use

- 이미 React/JSX composition과 managed rendering 인프라가 확립되어 있어 [[tech/devtools/remotion/README|Remotion]]이 자연스러울 때
- LaTeX, 기하학, 수학 교육 animation이 주력이라 Manim의 Python scene graph가 더 맞을 때
- Canvas-centric vector animation editor workflow가 요구될 때
- 단순한 일회성 screen recording처럼 deterministic render의 비용과 설정이 정당화되지 않을 때

## Related Notes

- [[MOCs/Index]]
- [[MOCs/Devtools]]
- [[tech/devtools/remotion/README|Remotion]]
- [[tech/scraping/playwright/README|Playwright]]

## Sources

- https://hyperframes.heygen.com/introduction
- https://github.com/heygen-com/hyperframes
- https://github.com/heygen-com/hyperframes/releases
- https://hyperframes.heygen.com/packages/cli
- https://hyperframes.heygen.com/packages/engine
