---
date: 2026-11-27
tags: [tech]
type: tech-tool-study
status: draft
---

# Skeuomorphism — 물리적 조작감을 표현하는 UI 스타일

> **한 줄 정의**: Skeuomorphism은 제공 사례의 노브·슬라이더처럼 물리적 조작 장치의 형태를 화면의 제어 요소에 반영하는 UI 디자인 스타일로 해석할 수 있다.

## Overview

이 학습은 노브와 슬라이더가 있는 흰색 오디오 제어 화면을 출발점으로 삼는다. 핵심은 기능을 어떤 조작 형태로 표현하고, 그 형태를 입력·상태·피드백과 어떻게 연결하는가다.

- **확인된 것:** 흰색 화면, 노브, 슬라이더, 네 가지 스타일 중 하나로 소개된 사실.
- **확인되지 않은 것:** 실제 조작, 오디오 값의 종류, 구현 기술, 성능, 접근성, 역사 및 보급 정도.
- 아래 실습과 사용 조건은 관찰된 형태를 바탕으로 한 설계 제안이다. 영상에서 검증된 효과를 뜻하지 않는다.

## Learning Path

- [ ] [[tech/devtools/skeuomorphism-ui-design/01-overview|Overview]] — 관찰과 해석, 설계 층 이해
- [ ] [[tech/devtools/skeuomorphism-ui-design/02-ecosystem|Ecosystem]] — 네 스타일의 예시와 비교 한계
- [ ] [[tech/devtools/skeuomorphism-ui-design/03-references|References]] — 자료 범위와 보충 문서 확인
- [ ] [[tech/devtools/skeuomorphism-ui-design/04-learning/01-getting-started|시작하기]] — 하나의 값을 두 제어 요소에 연결
- [ ] [[tech/devtools/skeuomorphism-ui-design/04-learning/02-deep-dive|심화 학습]] — 입력 규칙·접근성·비교 실험
- [ ] [[tech/devtools/skeuomorphism-ui-design/05-projects|Projects]] — 검증 가능한 프로토타입 만들기
- [ ] [[tech/devtools/skeuomorphism-ui-design/cheatsheet|Cheatsheet]] — 구현·리뷰 체크리스트

## When To Use

- 오디오 패널 등 물리적 제어 장치의 형태를 활용하는 프로토타입을 탐색할 때.
- 노브의 인지와 실제 조작 이해를 분리해 검증할 때.
- 같은 기능에서 표현 방식의 영향을 비교하려 할 때.

## When Not To Use

- 외형만으로 사용성·접근성·성능의 우수성을 보장하려 할 때.
- 정확한 값 입력이나 키보드 조작이 필요한데 보완 수단을 제공하지 못할 때.
- 이 단일 자료로 라이브러리 선택, 역사 또는 시장 보급을 판단하려 할 때.

## Related Notes

- [[MOCs/Index]]
- [[MOCs/Devtools]]
- [[tech/devtools/web-design-guidelines/README|Web Design Guidelines]] — UI 검토 관점을 확장할 때 참고.

## Sources

- 제공 dossier: 영상 요약의 00:00 장면 설명. 원본 URL 미제공이며 실제 동작은 확인하지 못했다.
- 보충 실습 문서: MDN `input type="range"` — https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input/range
- 보충 접근성 문서: WAI-ARIA APG Slider Pattern — https://www.w3.org/WAI/ARIA/apg/patterns/slider/
- 위 URL은 실습 참고 자료이며 영상의 출처 또는 화면 구현의 증거가 아니다.
