---
date: 2026-11-27
tags: [tech]
type: tech-tool-study
status: draft
---

# 프로토타입 기반 디자인 논의와 디자인 시스템 적용

> **한 줄 정의**: 프로토타입을 공통 검토 대상으로 삼아 화면의 구체적인 영역을 논의하고, 디자인 시스템의 스타일·컴포넌트·토큰 적용 결과를 비교하는 디자인 협업 방식.

## Overview

AI가 완성한 디자인을 전달받았을 때, 무엇을 기준으로 검토할 수 있을까? 제공된 자료는 MeetBook 예약 캘린더의 특정 영역을 강조하고, 스타일·변수 비교와 적용 전후 화면을 함께 살피는 흐름을 보여준다.

- **화면 수준:** 어느 위치의 구성과 표현을 바꿀지 정한다.
- **시스템 수준:** 색상 코드, 텍스트 스타일, 디자인 변수가 참조 기준에 맞는지 확인한다.
- **증거의 한계:** 짧은 영상 요약으로, 시간 절감·적용 정확도·UX 개선은 확인되지 않았다.

이 노트는 특정 제품의 설치 매뉴얼이 아니다. `/apply-ds-to-prototype`은 자료에 등장한 명령 문자열이며, 실행 환경과 공개 사용 가능 여부는 미상이다.

## Learning Path

- [ ] [[tech/devtools/prototype-based-design-discussion/01-overview|Overview]] — What/Why와 관찰 범위 이해
- [ ] [[tech/devtools/prototype-based-design-discussion/02-ecosystem|Ecosystem 비교]] — 검토 방식의 역할과 한계 비교
- [ ] [[tech/devtools/prototype-based-design-discussion/03-references|References]] — 출처 공백과 추가 확인 항목 점검
- [ ] [[tech/devtools/prototype-based-design-discussion/04-learning/01-getting-started|시작하기]] — 한 영역의 검토 기록 작성
- [ ] [[tech/devtools/prototype-based-design-discussion/04-learning/02-deep-dive|심화 학습]] — 디자인·컴포넌트·토큰 대응 검토
- [ ] [[tech/devtools/prototype-based-design-discussion/05-projects|Projects]] — 추적 가능한 실전 산출물 만들기
- [ ] [[tech/devtools/prototype-based-design-discussion/cheatsheet|Cheatsheet]] — 검토 시 빠르게 참조

## When To Use

- AI 생성 화면을 구체적인 위치와 변경 의도로 검토할 때
- 시각적 선호와 디자인 시스템 정합성을 구분해야 할 때
- 변경 전후 화면과 속성값을 함께 남겨야 할 때

## When Not To Use

- 정적 화면만으로 interaction·접근성·사용성을 확정하려는 경우
- 실행 환경이 없는 명령을 즉시 설치·재현하려는 경우
- 디자인 시스템 참조가 없는데 자동 적용의 정확성을 판정하려는 경우

## Related Notes

- [[MOCs/Index]]
- [[MOCs/Devtools]]
- 관련 tech 주제: Design tokens, UI component, Figma variables. 현재 작업 폴더에 기존 tech 노트가 없어 실제 노트 링크는 연결하지 않았다.

## Sources

- 사용자 제공 dossier: 짧은 영상의 수집 요약. 원본 영상 URL과 화면에 입력된 Figma URL은 제공되지 않았다. 원본을 직접 검증한 기록이 아니다.
- 보충 자료 URL: https://help.figma.com/ — Figma 공식 도움말 진입점. 개념을 추가 조사하기 위한 자료이며, 사례의 명령·연동 방식·정확성을 입증하는 출처는 아니다.
