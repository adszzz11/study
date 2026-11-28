---
date: 2026-11-27
tags: [tech]
type: tech-tool-study
status: draft
---

# 심화 — 절제 과정의 손실과 Accessibility

## 제거 실험

같은 콘텐츠와 기능을 유지하고 구분선, 배경, 아이콘 등을 한 번에 하나씩 변경한다. 여러 요소를 동시에 바꾸면 원인을 분리하기 어렵다. 각 단계의 화면과 판단 기록을 남긴다.

| 단계 | 변경 | 기대 효과 | 확인할 손실 |
|---|---|---|---|
| A | 기준 화면 유지 | 비교 기준 확보 | 기존 혼동 기록 |
| B | 장식적 구분선 제거 | 시각적 밀도 감소 | 절 경계 식별 약화 여부 |
| C | 보조 배경 제거 | 본문 집중 | 보조 설명과 본문 혼동 여부 |
| D | 중복 아이콘 제거 | 반복 감소 | 링크·버튼 식별 단서 손실 여부 |

이 표는 실험 제안이며 결과가 아니다. 변경 전후에 동일한 정보 찾기 과제를 수행하고, 손실이 관찰되면 해당 단서를 복원하거나 다른 방식으로 표현한다.

## Accessibility 점검

- **Text contrast**: WCAG 2.2 AA의 일반 텍스트는 최소 4.5:1, 큰 텍스트는 3:1을 기준으로 점검한다. 큰 텍스트의 정의·예외는 공식 기준을 확인한다.
- **Use of Color**: 링크나 상태를 색만으로 전달하는지 확인한다. 밑줄 등 추가 단서를 검토한다.
- **Keyboard navigation**: 키보드로 필요한 기능에 접근·조작할 수 있는지, focus 이동 순서가 의미에 맞는지 확인한다.
- **Focus visibility**: Tab 이동 중 현재 위치를 식별할 수 있는지 확인한다.
- **Non-text contrast**: 조작 요소와 상태를 식별하는 데 필요한 시각 정보는 관련 성공 기준의 3:1 요구와 예외를 확인한다.

이 점검만으로 WCAG 전체 준수를 선언할 수 없다. 옅은 화면이라는 인상도 contrast 측정을 대신하지 못한다. 원본 예시의 충족 여부는 미확인이다.

## 결과 해석

찾는 시간, 탐색 오류, 혼동한 지점을 기록하고 미적 선호는 별도 질문으로 남긴다. 작은 실습 결과는 해당 문서·참여자·환경에 한정한다. 표본, 제시 순서, 콘텐츠 친숙도 등 결과에 영향을 주는 조건을 함께 적는다.

성능 개선은 여기서 추론하지 않는다. 필요하면 별도의 구현과 측정 계획을 세운다.

## Related Notes

- [[tech/devtools/minimalism-documentation-ui/README|학습 진입점]]
- [[tech/devtools/minimalism-documentation-ui/cheatsheet|검토 체크리스트]]

## Sources

- 1차 근거: 사용자 제공 dossier(영상 분석 요약). 원본 영상의 URL·제목·제작자·게시일은 미제공이다. 원본 화면이나 실험 결과를 직접 확인한 자료가 아니다.
- 보충 검증 기준: [WCAG 2.2](https://www.w3.org/TR/WCAG22/). 아래 접근성 점검의 기준이며, 원본 예시의 준수 여부를 입증하지 않는다.

- https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html
- https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html
- https://www.w3.org/WAI/WCAG22/Understanding/focus-visible.html
