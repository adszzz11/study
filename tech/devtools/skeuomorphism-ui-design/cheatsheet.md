---
date: 2026-11-27
tags: [tech]
type: tech-tool-study
status: draft
---

# Cheatsheet — 설계·리뷰 요약

| 질문 | 확인할 내용 |
|---|---|
| 무엇이 관찰되었나? | 흰색 오디오 화면, 노브, 슬라이더 |
| 무엇이 해석인가? | 물리적 장치 형태를 통한 값 조절 표현 |
| 무엇이 미확인인가? | 입력·기능·접근성·성능·구현·우열 |
| 구현의 중심은? | 시각적 표현 ↔ 입력 ↔ 공유 상태 ↔ 기능 |
| 비교의 전제는? | 같은 기능·데이터·작업, 표현만 변경 |

## 구현 체크리스트

- [ ] 조절 대상의 레이블과 현재 값이 있다.
- [ ] 범위·step·초기값을 명시했다.
- [ ] 노브의 조작 방향과 입력 규칙을 안내했다.
- [ ] 노브·슬라이더·숫자가 단일 상태를 공유한다.
- [ ] 경계·초기화·입력 취소를 확인했다.
- [ ] 키보드·focus·숫자 직접 입력을 확인했다.
- [ ] 외형만으로 접근성과 사용성을 단정하지 않았다.
- [ ] 실제 기능 연결 시 적용 결과도 확인했다.

```text
관찰: 화면에서 확인한 사실
해석: 그 형태가 뜻한다고 보는 설계 의도
검증: 실제 입력·작업으로 확인할 가설
```

**주의:** 이 자료로 질감·그림자 기법, 스타일의 역사·보급, 제품 생태계나 다른 스타일 대비 우수성을 확정하지 않는다.

## Navigation

- [[tech/devtools/skeuomorphism-ui-design/README|학습 경로로 돌아가기]]

## Sources

- 제공 dossier: 영상 요약의 00:00 장면 설명. 원본 URL 미제공이며 실제 동작은 확인하지 못했다.
- 보충 실습 문서: MDN `input type="range"` — https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input/range
- 보충 접근성 문서: WAI-ARIA APG Slider Pattern — https://www.w3.org/WAI/ARIA/apg/patterns/slider/
- 위 URL은 실습 참고 자료이며 영상의 출처 또는 화면 구현의 증거가 아니다.
