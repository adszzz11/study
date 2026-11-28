---
date: 2026-11-27
tags: [tech]
type: tech-tool-study
status: draft
---

# 디자인 토큰과 스타일 비교를 통한 프로토타입의 디자인 시스템 적용

> **한 줄 정의**: 디자인 토큰과 스타일 비교는 프로토타입의 색상 코드·텍스트 스타일·디자인 변수를 대조해 디자인 시스템 적용에 필요한 차이를 검토하는 작업이다.

## Overview

AI가 완성한 디자인을 전달받은 뒤, 화면의 인상뿐 아니라 개별 속성과 기준의 연결을 검토하는 방법을 학습한다. 제공된 사례는 MeetBook 예약 캘린더이며, 특정 영역을 논의한 다음 디자인 시스템 적용과 전후 비교로 이어지는 흐름을 보여준다.

| 구분 | 자료가 뒷받침하는 범위 |
|---|---|
| 확인된 사실 | 비교 표, `/apply-ds-to-prototype`와 Figma URL 입력, 전후 디자인 탭 |
| 가능한 해석 | 시각적 속성을 디자인 시스템 기준에 맞추고 결과를 대조하려는 workflow |
| 미확인 | 자동 변경 범위, token matching, 컴포넌트 교체, 코드 생성, 정확도·시간 절감 |

이 노트 묶음은 특정 공개 도구의 사용 설명서가 아니다. 명령의 제공 환경과 실제 비교 값은 알려져 있지 않으며, 학습 절차와 프로젝트는 dossier를 바탕으로 한 실습 제안이다.

## Learning Path

- [ ] [[tech/devtools/design-token-style-comparison/01-overview|Overview]] — What/Why와 관찰 범위 이해
- [ ] [[tech/devtools/design-token-style-comparison/02-ecosystem|검토 방식 비교]] — 화면·속성·구성 단위별 접근 비교
- [ ] [[tech/devtools/design-token-style-comparison/03-references|References]] — 근거와 출처의 한계 확인
- [ ] [[tech/devtools/design-token-style-comparison/04-learning/01-getting-started|시작하기]] — 한 화면의 비교 기록 작성
- [ ] [[tech/devtools/design-token-style-comparison/04-learning/02-deep-dive|심화 학습]] — 값·참조·변경 수준 분리
- [ ] [[tech/devtools/design-token-style-comparison/05-projects|Projects]] — 검토 문서와 workflow 검증
- [ ] [[tech/devtools/design-token-style-comparison/cheatsheet|Cheatsheet]] — 반복 검토용 체크리스트 활용

## When To Use

- AI 디자인을 인수한 뒤 디자인 시스템 적용 범위를 정할 때
- 프로토타입의 특정 영역에서 색상·텍스트·변수 차이를 기록할 때
- 전후 화면과 변경 근거를 함께 전달할 때

## When Not To Use

- 기준 자료 없이 디자인 시스템 준수 여부를 확정하려 할 때
- 이 자료만으로 명령의 설치·실행 방법이나 자동화 성능을 보장하려 할 때
- 외형 비교만으로 토큰 연결, 접근성, 구현 품질 전체를 검증하려 할 때

## Related Notes

- [[MOCs/Index]]
- [[MOCs/Devtools]]
- [[tech/devtools/design-token-style-comparison/01-overview|프로토타입 검토와 디자인 시스템 적용 개념]]
- [[tech/devtools/design-token-style-comparison/04-learning/02-deep-dive|값과 변수 참조 비교]]

## Sources

- 사용자 제공 dossier: MeetBook 예약 캘린더 영상 요약 및 분석. 원본 출처 URL은 제공되지 않았다.
- 영상에 등장한 Figma 디자인 URL의 실제 주소도 제공되지 않았다. 출처와 참조 대상은 원본 확보 후 확인해야 한다.
