---
date: 2026-11-27
tags: [tech]
type: tech-tool-study
status: draft
---

# 시작하기 — 하나의 값, 두 가지 형태

## 1. 관찰과 추론 분리

- 관찰: 흰색 오디오 제어 화면에 노브와 슬라이더가 있다.
- 해석: 물리적 장치의 형태로 값 조절을 표현한다.
- 검증 과제: 사용자가 조작 방향과 현재 값을 이해하는지 확인한다.

## 2. 실습 계약 정하기

가상 `Level` 값을 사용한다. 범위 0–100, step 1, 초기값 50은 **실습에서 정한 값**이며 영상의 사양이 아니다. 실제 오디오 연결 없이 시작한다.

```text
pointer / keyboard / numeric input
                ↓
        normalize → shared value
                ↓
        knob / slider / value label
```

## 3. 구현 순서

1. 레이블을 연결한 기본 HTML range와 현재 값 표시를 만든다.
2. 단일 상태에 모든 입력을 연결한다. 범위 밖 값은 제한하고 step에 맞춘다.
3. 노브 표시와 입력을 추가한다. 예를 들어 수직 드래그를 선택했다면 위로 이동할수록 증가한다고 안내한다.
4. 숫자 입력·초기화를 추가하고 변경 시 두 표시를 함께 갱신한다.
5. 포인터와 키보드로 같은 범위를 조절한다. 노브의 드래그 감도는 별도로 조정한다.

## 완료 조건

- [ ] 어느 입력을 바꿔도 노브·슬라이더·숫자가 같은 값을 표시한다.
- [ ] 최솟값·최댓값에서 범위를 벗어나지 않는다.
- [ ] 초기화하면 모든 표시가 50이 된다.
- [ ] 키보드만으로 값 변경과 초기화가 가능하다.

노브의 외형 완성도보다 입력 → 상태 → 피드백의 일치를 우선한다.

## Navigation

- [[tech/devtools/skeuomorphism-ui-design/README|학습 경로로 돌아가기]]

## Sources

- 제공 dossier: 영상 요약의 00:00 장면 설명. 원본 URL 미제공이며 실제 동작은 확인하지 못했다.
- 보충 실습 문서: MDN `input type="range"` — https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input/range
- 보충 접근성 문서: WAI-ARIA APG Slider Pattern — https://www.w3.org/WAI/ARIA/apg/patterns/slider/
- 위 URL은 실습 참고 자료이며 영상의 출처 또는 화면 구현의 증거가 아니다.
