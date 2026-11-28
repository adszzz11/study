---
date: 2026-11-27
tags: [tech]
type: tech-tool-study
status: draft
---

# References — 근거와 보충 자료

## 1차 근거의 상태

사용자 제공 dossier는 네 가지 스타일을 소개하는 영상의 분석 요약이다. 원본 URL이 없어 영상의 상세 화면, 동작, 제작 의도를 재확인할 수 없다. URL을 추정하거나 다른 영상으로 대체하지 않는다.

| 주장 | 근거 상태 | 기록 방법 |
|---|---|---|
| 옅은 색의 기술 문서 예시 | dossier에 명시 | 관찰 요약 |
| 본문 집중에 도움이 될 가능성 | 분석적 해석 | 가설 |
| 탐색이 빠르거나 읽기 쉬움 | 측정 자료 없음 | 검증 필요 |
| 특정 framework 사용 | 구현 자료 없음 | 판단 불가 |

## 보충 자료의 용도

아래 공식 문서는 실습의 검증 기준으로만 사용한다. 원본 예시의 구현이나 접근성 상태에 관한 출처가 아니다.

| 자료 | 활용 |
|---|---|
| WCAG 2.2 | 성공 기준과 적용 범위 확인 |
| Contrast (Minimum) | 텍스트와 배경의 대비 점검 |
| Use of Color | 색만으로 정보를 전달하는지 점검 |
| Keyboard / Focus Visible | 키보드 조작과 focus 표시 점검 |
| Non-text Contrast | UI component·상태를 식별하는 시각 정보의 대비 점검 |

## 후속 수집 항목

- 원본 URL, 제작자, 게시일과 관찰 시점
- 실제 화면의 heading, navigation, typography, interaction 상태
- 적용한 성공 기준, 측정 도구, 환경, 결과와 남은 한계

## Related Notes

- [[tech/devtools/minimalism-documentation-ui/README|학습 진입점]]
- [[tech/devtools/minimalism-documentation-ui/cheatsheet|검토 체크리스트]]

## Sources

- 1차 근거: 사용자 제공 dossier(영상 분석 요약). 원본 영상의 URL·제목·제작자·게시일은 미제공이다. 원본 화면이나 실험 결과를 직접 확인한 자료가 아니다.
- 보충 검증 기준: [WCAG 2.2](https://www.w3.org/TR/WCAG22/). 아래 접근성 점검의 기준이며, 원본 예시의 준수 여부를 입증하지 않는다.

- https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html
- https://www.w3.org/WAI/WCAG22/Understanding/use-of-color.html
- https://www.w3.org/WAI/WCAG22/Understanding/keyboard.html
- https://www.w3.org/WAI/WCAG22/Understanding/focus-visible.html
- https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html
