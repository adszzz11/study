---
date: 2026-11-27
tags: [tech]
type: tech-tool-study
status: draft
---

# 화면 녹화를 활용한 시각적 피드백과 반복 수정

> **한 줄 정의**: 화면 녹화를 활용한 시각적 피드백은 실행 화면의 변화 과정을 기록하고 비교하여, 구현 결과의 차이를 수정 요청과 재검증으로 연결하는 작업 방식이다.

## Overview

특정 제품이 아니라 **결과 화면을 다음 수정의 입력으로 재사용하는 피드백 루프**를 학습한다. 제공 사례에는 Claude에서 모션그래픽을 수정하는 채팅, 화면 녹화 첨부, 나란히 놓인 웹 화면과 자동 수정 언급이 등장한다.

- 기본 루프: 녹화 → 비교 → 수정 요청 → 변경 → 재녹화.
- Spatial fidelity: 위치·크기·간격·정렬을 검토한다.
- Temporal fidelity: 시작 시점·지속 시간·등장 순서·전환 흐름을 검토한다.
- 영상 처리 방식, 구현 스택, 자동 수정의 성공률은 확인되지 않는다. `/reanimate`와 `417 / 417`을 공식 기능이나 품질 보증으로 해석하지 않는다.

## Learning Path

- [ ] [[tech/devtools/screen-recording-visual-feedback/01-overview|Overview]]
- [ ] [[tech/devtools/screen-recording-visual-feedback/02-ecosystem|Ecosystem]]
- [ ] [[tech/devtools/screen-recording-visual-feedback/03-references|References]]
- [ ] [[tech/devtools/screen-recording-visual-feedback/04-learning/01-getting-started|시작하기]]
- [ ] [[tech/devtools/screen-recording-visual-feedback/04-learning/02-deep-dive|심화 학습]]
- [ ] [[tech/devtools/screen-recording-visual-feedback/05-projects|Projects]]
- [ ] [[tech/devtools/screen-recording-visual-feedback/cheatsheet|Cheatsheet]]

## When To Use

- 모션그래픽이나 UI 전환의 동작을 텍스트만으로 전달하기 어렵다.
- 기준과 구현의 차이를 구간별로 기록하고 반복 수정해야 한다.
- 수정 전후를 같은 조건에서 검토할 수 있다.

## When Not To Use

- 정적 정렬 하나만 확인하면 충분하다면 Screenshot부터 사용한다.
- 민감한 화면을 안전하게 가릴 수 없다면 녹화 공유를 보류한다.
- 자동 수정의 정확도·생산성을 입증할 성능 자료가 필요하다면 이 사례만으로 판단하지 않는다.

## Related Notes

- [[MOCs/Index]]
- [[MOCs/Devtools]]
- [[tech/devtools/remotion/README|Remotion]] — 코드로 만든 영상의 결과를 검토할 때 연결할 수 있는 학습 주제. 사례가 Remotion을 사용했다는 의미는 아니다.

## Sources

- 제공 dossier: Claude 모션그래픽 수정 사례를 정리한 자료. 원본 URL·원본 영상·코드는 제공되지 않아 직접 검증하지 못했다.
- 실습 보조 문서: https://developer.mozilla.org/en-US/docs/Web/API/Screen_Capture_API — 화면 캡처 관련 개념을 더 살펴볼 출발점. 사례의 내부 구현을 입증하는 출처가 아니다.
