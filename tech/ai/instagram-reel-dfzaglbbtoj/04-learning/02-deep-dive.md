---
date: 2026-11-17
tags: [tech]
type: tech-tool-study
status: draft
---

# Deep Dive

## Reel claim 검증

식별된 도구가 생긴 뒤에는 영상의 인상과 제품의 실제 동작을 분리한다.

```text
claim → 원본 문구/화면 → 공식 문서 → 최소 재현 → 결과·제한 기록
```

## 체크 항목

- 버전과 model name이 영상 게시 시점과 현재 문서에서 같은가?
- 데모의 입력 데이터, prompt, 권한, 후편집이 공개되었는가?
- 결과 품질을 속도·비용·privacy trade-off와 함께 평가했는가?
- 실패 사례와 제약 조건도 같은 비중으로 기록했는가?

## 비교 결론 작성법

`더 좋다` 대신 특정 task와 조건을 쓴다. 예: “N개 PDF의 표 추출 task에서, 로컬 실행 요구와 정확도 기준을 충족한다.” 제품 미식별 상태에서는 이 결론을 작성하지 않는다. 비교 축은 [[tech/ai/instagram-reel-dfzaglbbtoj/02-ecosystem|Ecosystem]]에서 관리한다.

## Sources

- https://www.instagram.com/reel/DfzaglBBToj/?utm_source=ig_web_copy_link&xtok=NTc4MTIwNjQ2YQ==
