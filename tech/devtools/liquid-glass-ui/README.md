---
date: 2026-11-27
tags: [tech]
type: tech-tool-study
status: draft
---

# Liquid Glass — 반투명 음악 앱 인터페이스 분석

> **한 줄 정의**: Liquid Glass는 제공된 영상 설명에서 보라색·파란색 음악 앱 목업과 반투명 패널로 표현된 UI 디자인 스타일이다.

## Overview

이 tool-study는 특정 도구의 설치법이 아니라 **Visual Layer 분석과 비교 실습**을 다룬다. 직접적인 근거는 사용자 제공 dossier이며, 원본 영상은 확인하지 못했다.

| 구분 | 내용 |
|---|---|
| 확인된 단서 | 보라색·파란색, 반투명 패널, 음악 앱 목업 |
| 분석 질문 | 배경의 존재감을 유지하면서 콘텐츠와 조작 요소를 구분할 수 있는가? |
| 해석 | 패널은 콘텐츠를 묶으면서 배경과 시각적으로 연결되는 표면일 수 있음 |
| 확인 불가 | 제품명, Framework, Rendering Engine, API, Blur·Refraction·Animation, 성능·접근성 수준 |

위 분석 질문은 제작자가 밝힌 도입 목적이 아니다. 이름만으로 특정 기업의 Design System이나 물리 기반 효과를 추정하지 않는다.

## Learning Path

- [ ] [[tech/devtools/liquid-glass-ui/01-overview|Overview]]: 관찰과 해석, 핵심 특징을 구분한다.
- [ ] [[tech/devtools/liquid-glass-ui/02-ecosystem|비교]]: 영상 속 네 가지 스타일과 비교의 한계를 읽는다.
- [ ] [[tech/devtools/liquid-glass-ui/03-references|References]]: 자료의 범위와 미확인 정보를 확인한다.
- [ ] [[tech/devtools/liquid-glass-ui/04-learning/01-getting-started|시작하기]]: 같은 Layout에서 Transparency를 실험한다.
- [ ] [[tech/devtools/liquid-glass-ui/04-learning/02-deep-dive|심화 실습]]: Color·Surface·배경 변수를 분리한다.
- [ ] [[tech/devtools/liquid-glass-ui/05-projects|Projects]]: 음악 앱 시안과 Playground를 제작한다.
- [ ] [[tech/devtools/liquid-glass-ui/cheatsheet|Cheatsheet]]: 주장과 검증 항목을 빠르게 점검한다.

## When To Use

- 반투명 Surface와 배경의 관계를 분석할 때
- 음악 앱 시안의 Color, Visual Hierarchy, 가독성을 실험할 때
- 같은 콘텐츠를 유지한 스타일 비교의 설계 기준이 필요할 때

## When Not To Use

- 특정 플랫폼 API나 제품의 공식 구현 지침이 필요할 때
- Blur, Refraction, Animation의 실제 구현을 확인하려 할 때
- 검증된 사용성·접근성·성능 결과가 필요할 때

## Related Notes

- [[MOCs/Index]]
- [[MOCs/Devtools]]
- 관련 tech 학습 주제: CSS Transparency와 가독성 — 현재 작업 폴더에 기존 노트가 없어 링크 생략.
- [[tech/devtools/liquid-glass-ui/02-ecosystem|UI 스타일 비교]]

## Sources

- 사용자 제공 dossier: 네 가지 UI 스타일을 제시한 영상에 관한 설명. 원본 URL은 제공되지 않아 기재할 수 없음.
- 원본 영상·코드·사용자 평가·성능 측정 자료는 직접 확인하지 못함. 실습과 검증 기준은 이 노트의 제안임.
