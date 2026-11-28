---
date: 2026-11-27
tags: [tech]
type: tech-tool-study
status: draft
---

# Cheatsheet — Minimalism 문서 UI 점검

## 근거 수준 빠르게 구분하기

| 구분 | 기록할 내용 |
|---|---|
| 관찰 | 옅은 색의 기술 문서 웹페이지라는 dossier 설명 |
| 해석 | 본문과 정보 구조에 집중하도록 도울 가능성 |
| 검증 필요 | 가독성, 탐색 속도, 만족도, accessibility |
| 판단 불가 | 원본 framework, component library, rendering 방식, 성능 |

## 설계 순서

```text
의미 관계 정리 → typography·spacing·color로 구분
→ interaction·상태 표시 → 같은 과제로 검증 → 필요한 단서 복원
```

## 제거 전 체크리스트

- [ ] 제거할 요소의 역할을 설명할 수 있는가?
- [ ] 제목·본문·보조 설명이 계속 구분되는가?
- [ ] 링크와 일반 텍스트, 버튼과 비조작 요소가 식별되는가?
- [ ] 현재 위치와 keyboard focus를 확인할 수 있는가?
- [ ] 색만으로 정보를 전달하지 않는가?
- [ ] 실제 text contrast와 관련 UI contrast를 점검했는가?
- [ ] 같은 과제의 시간·오류·혼동을 변경 전후에 기록했는가?
- [ ] 보기 좋은 인상과 과제 수행 결과를 분리했는가?

## 피할 결론

- “옅은 색이면 Minimalism이다”: 해당 예시의 단서를 정의로 확대하지 않는다.
- “단순하면 읽기 쉽다”: 정보 이해는 별도 검증한다.
- “장식이 줄면 성능이 좋아진다”: 구현과 측정 자료가 없다.
- “영상의 다른 스타일보다 낫다”: 콘텐츠와 과업이 함께 달라 직접 비교하기 어렵다.

기준을 자세히 확인할 때는 [[tech/devtools/minimalism-documentation-ui/03-references|References]]를 읽는다.

## Related Notes

- [[tech/devtools/minimalism-documentation-ui/README|학습 진입점]]
- [[tech/devtools/minimalism-documentation-ui/cheatsheet|검토 체크리스트]]

## Sources

- 1차 근거: 사용자 제공 dossier(영상 분석 요약). 원본 영상의 URL·제목·제작자·게시일은 미제공이다. 원본 화면이나 실험 결과를 직접 확인한 자료가 아니다.
- 보충 검증 기준: [WCAG 2.2](https://www.w3.org/TR/WCAG22/). 아래 접근성 점검의 기준이며, 원본 예시의 준수 여부를 입증하지 않는다.
