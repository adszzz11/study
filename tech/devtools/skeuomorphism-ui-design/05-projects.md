---
date: 2026-11-27
tags: [tech]
type: tech-tool-study
status: draft
---

# Projects — 검증 가능한 적용

| 프로젝트 | 구현 범위 | 제출물 | 검증 포인트 |
|---|---|---|---|
| 오디오 제어 프로토타입 | 흰색 화면, 노브, 슬라이더, 가상 값 | 실행 화면·입력 규칙 | 입력과 값 변화 일치 |
| 동일 기능 스타일 비교 | Skeuomorphism·Minimalism 패널 | 동일 작업 설명·관찰 기록 | 스타일 외 조건 통제 |
| 접근성 보완 | 레이블·키보드·숫자 입력·초기화 | 키보드 점검 기록 | 외형 없이도 작업 가능 |

## 권장 진행

1. 가상 값 프로토타입에서 경계·초기화·동기화를 확인한다.
2. 같은 기능의 비교 패널을 만들고 시간·오입력·질문을 기록한다.
3. 접근성 보완 후 같은 작업을 다시 수행한다. 바꾼 조건을 명시한다.
4. 선택적으로 실제 오디오를 연결하고 적용 값과 UI 상태의 동기화를 별도 확인한다.

## 결과 기록 양식

```text
프로토타입 / 버전:
조작 규칙 / 범위 / step:
작업 / 기기 / 제시 순서:
목표 값 / 소요 시간 / 오입력:
사용자가 묻거나 막힌 점:
관찰 / 해석 / 다음 검증:
```

완료 기준은 사실적인 외형이 아니라 값 일치, 조작 규칙의 이해, 시각적 형태에 의존하지 않는 작업 수행이다. 결과는 실험 조건 안에서만 해석한다.

## Navigation

- [[tech/devtools/skeuomorphism-ui-design/README|학습 경로로 돌아가기]]

## Sources

- 제공 dossier: 영상 요약의 00:00 장면 설명. 원본 URL 미제공이며 실제 동작은 확인하지 못했다.
- 보충 실습 문서: MDN `input type="range"` — https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input/range
- 보충 접근성 문서: WAI-ARIA APG Slider Pattern — https://www.w3.org/WAI/ARIA/apg/patterns/slider/
- 위 URL은 실습 참고 자료이며 영상의 출처 또는 화면 구현의 증거가 아니다.
