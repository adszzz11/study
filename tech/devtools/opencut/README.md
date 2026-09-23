---
date: 2026-09-23
tags: [tech]
type: tech-tool-study
status: draft
---

# OpenCut

> **한 줄 정의**: OpenCut은 CapCut 대안을 표방하는 MIT-licensed 오픈소스 비선형 영상 편집기로, 현재 웹 기반 classic과 Rust core 기반 rewrite가 공존하는 전환기 프로젝트다.

## Overview

OpenCut은 paywall·cloud 의존성·제작물 데이터 통제 문제를 줄이는 **무료·오픈소스·local-first** 편집 경험을 목표로 한다. 지금 실제로 쓸 수 있는 것은 브라우저의 **classic**이며, 공식 저장소는 이를 이전 버전으로 안내한다. 새 **rewrite**는 Web·Desktop·Android·iOS와 automation surface가 하나의 Rust core를 공유하도록 재구성 중이다.

- **classic:** multi-track timeline, trim/ripple editing, captions, effects, masks, keyframe animation을 갖춘 browser-first editor
- **rewrite:** Editor API, plugin, MCP, headless mode, scripting을 목표로 하지만 아직 roadmap 단계
- **판단 기준:** 짧은 영상의 가벼운 편집은 classic을 시험할 수 있으나, production automation은 rewrite의 공개·안정화 전까지 전제로 두지 않는다.
- **상태 확인일:** 2026-09-23. `opencut.app`은 classic, `new.opencut.app`은 rewrite preview로 안내된다.

## Learning Path

- [ ] [[tech/devtools/opencut/01-overview|1. Overview]] — classic과 rewrite의 역할 및 전환 상태 구분하기
- [ ] [[tech/devtools/opencut/02-ecosystem|2. Ecosystem]] — browser editor와 desktop NLE 대안 비교하기
- [ ] [[tech/devtools/opencut/03-references|3. References]] — 공식 상태·release·개발 문서 확인 지점 익히기
- [ ] [[tech/devtools/opencut/04-learning/01-getting-started|4. Getting started]] — import부터 export까지 기본 편집 loop 실습하기
- [ ] [[tech/devtools/opencut/04-learning/02-deep-dive|5. Deep dive]] — keyframe, mask, ripple editing과 rewrite 설계 이해하기
- [ ] [[tech/devtools/opencut/05-projects|6. Projects]] — short-form template·local-first POC를 설계하기
- [ ] [[tech/devtools/opencut/cheatsheet|7. Cheatsheet]] — 기능 상태와 개발 명령을 빠르게 복습하기

## When To Use

- 설치 없이 빠르게 short-form video의 컷·자막·간단한 motion을 편집하고 싶을 때
- cloud upload 제약이 있는 환경에서 브라우저 기반 편집 workflow를 평가할 때
- Rust core, plugin-first editor, headless rendering 같은 차세대 편집기 구조를 연구할 때
- 초기 도구의 기능 변화와 project compatibility 위험을 감수할 수 있는 POC일 때

## When Not To Use

- 장편 영상, 복잡한 audio/video track, 안정적인 desktop NLE workflow가 핵심일 때
- MCP, Editor API, headless renderer를 지금 production integration의 전제로 삼아야 할 때
- 장기 보존해야 하는 프로젝트에 전환기 editor의 format·migration 정책을 검증하지 않았을 때
- 재인코딩 없는 빠른 cut/merge만 필요할 때는 LosslessCut 같은 전용 도구가 더 맞을 때

## Related Notes

- [[MOCs/Index]]
- [[MOCs/Devtools]]
- [[tech/devtools/remotion/README|Remotion]] — 코드와 데이터로 영상 생성·렌더링을 자동화하는 인접 주제

## Sources

- [OpenCut main repository / current status](https://github.com/OpenCut-app/OpenCut)
- [Rewrite tracking and architecture](https://github.com/OpenCut-app/OpenCut/issues/811)
- [OpenCut classic repository](https://github.com/OpenCut-app/opencut-classic)
- [Live classic editor](https://opencut.app/)
- [Rewrite preview](https://new.opencut.app/)
