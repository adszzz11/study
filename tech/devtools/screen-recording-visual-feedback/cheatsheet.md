---
date: 2026-11-27
tags: [tech]
type: tech-tool-study
status: draft
---

# Cheatsheet

## 기본 루프

```text
조건 고정 → 녹화 → 차이 관찰 → 기대 동작 명시
         → 한 종류 수정 → 동일 조건 재녹화 → 품질 판정
```

## 빠른 체크

| 질문 | 확인 항목 |
|---|---|
| 무엇을 비교하나? | 기준·구현, 같은 동작 |
| 조건은 같은가? | viewport·초기 상태·시작 이벤트·재생 속도 |
| 공간 차이인가? | Spatial fidelity: 위치·크기·간격·정렬 |
| 시간 차이인가? | Temporal fidelity: 시작·지속·순서·전환 |
| 요청이 구체적인가? | 문제 구간 → 관찰 → 기대 → 확인 방법 |
| 끝났는가? | 적용 완료와 품질 통과를 별도 확인 |

## 요청 템플릿

```text
대상 / 문제 구간:
관찰된 동작:
기대 동작과 기준:
이번 수정 범위:
동일 조건 재검증 방법:
결과 / 남은 문제 / 부작용:
```

## 해석 금지와 대응

- `/reanimate`: 전체 문법과 제공 주체 미확인. 실행 가능한 공식 명령으로 안내하지 않는다.
- `417 / 417`: 단위·판정 기준 미확인. 품질 수치로 인용하지 않는다.
- 녹화 첨부: 전체 영상 분석·프레임 추출 방식은 미확인이다.
- 나란히 비교: 기준과 시작점이 불명확하면 결론을 보류한다.
- 개인정보·비밀값: 공유 전 가림 처리하고 필요한 범위만 녹화한다.

## 돌아가기

[[tech/devtools/screen-recording-visual-feedback/README|전체 학습 경로]] · [[tech/devtools/screen-recording-visual-feedback/03-references|근거의 한계]]

## Sources

- 제공 dossier: Claude 모션그래픽 수정 사례를 정리한 자료. 원본 URL·원본 영상·코드는 제공되지 않아 직접 검증하지 못했다.
- 실습 보조 문서: https://developer.mozilla.org/en-US/docs/Web/API/Screen_Capture_API — 화면 캡처 관련 개념을 더 살펴볼 출발점. 사례의 내부 구현을 입증하는 출처가 아니다.
