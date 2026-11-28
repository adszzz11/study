---
date: 2026-11-27
tags: [tech]
type: tech-tool-study
status: draft
---

# Figma 링크를 활용한 프로토타입 디자인 시스템 적용 흐름

> **한 줄 정의**: Figma 디자인 URL과 `/apply-ds-to-prototype` 명령을 입력하고, 프로토타입의 색상·텍스트 스타일·디자인 변수를 비교하며 디자인 시스템 적용 결과를 검토하는 흐름이다.

## Overview

AI가 만든 화면을 전달받았다고 해서 디자인 시스템에 맞게 완성되었다고 판단할 수는 없다. 이 노트는 MeetBook 예약 캘린더 사례를 바탕으로 **대상 화면 → 명령·참조 링크 → 속성 비교 → 전후 검토**라는 작업 모델을 학습한다.

- 관찰된 요소: 특정 영역 강조, 명령과 Figma URL 입력, 속성 비교표, 디자인·컴포넌트·토큰 항목, 전후 디자인 탭.
- 학습 목표: 화면의 인상과 속성의 일치 여부를 구분하고 적용 성공 기준을 기록한다.
- 한계: 실행 제품, 설치법, 연동 방식, 자동 변경 범위는 미확인이다. 이 문서는 실행 가능한 제품 매뉴얼이 아니다.

## Learning Path

- [ ] [[tech/devtools/figma-design-system-application/01-overview|Overview: What / Why / 특징]]
- [ ] [[tech/devtools/figma-design-system-application/02-ecosystem|Ecosystem: 검토 방식 비교]]
- [ ] [[tech/devtools/figma-design-system-application/03-references|References: 근거와 확인 한계]]
- [ ] [[tech/devtools/figma-design-system-application/04-learning/01-getting-started|시작하기: 검토 범위와 기준]]
- [ ] [[tech/devtools/figma-design-system-application/04-learning/02-deep-dive|심화: 컴포넌트·토큰과 재현성]]
- [ ] [[tech/devtools/figma-design-system-application/05-projects|Projects: 실전 검토 과제]]
- [ ] [[tech/devtools/figma-design-system-application/cheatsheet|Cheatsheet: 빠른 점검]]

## When To Use

- AI가 생성한 프로토타입을 디자인 기준과 대조할 때.
- Figma 참조와 대상 화면 사이의 차이를 색상·텍스트·변수 단위로 설명할 때.
- 화면 변경과 컴포넌트·토큰 변경을 구분해 후속 검토 범위를 정할 때.

## When Not To Use

- 공식 Figma 명령이나 특정 제품의 설치·실행 방법을 찾을 때.
- 링크만으로 모든 속성이 자동 수정되었다는 보증이 필요할 때.
- 코드 생성, 배포, 접근성 적합성 또는 전체 화면으로의 변경 전파를 입증할 때.

## Related Notes

- [[MOCs/Index]]
- [[MOCs/Devtools]]
- [[tech/devtools/figma-design-system-application/01-overview|프로토타입 디자인 시스템 적용 개요]]

기존 vault 노트 목록은 제공되지 않아 다른 tech 노트의 경로는 추정하지 않았다. 위 MOC 링크는 vault 통합 시 사용하는 지정 경로다.

## Sources

- 사용자 제공 dossier: MeetBook 예약 캘린더 사례의 관찰·분석 요약. 원영상 제목과 URL은 제공되지 않았다. 따라서 원자료를 직접 재검증하지 못했다.
- Figma 공식 사이트(보조 링크): https://www.figma.com/ — 서비스 식별용이며, 사례의 명령이나 자동 적용 기능을 입증하는 출처가 아니다.
