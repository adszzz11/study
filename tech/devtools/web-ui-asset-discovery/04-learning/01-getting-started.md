---
date: 2026-11-26
tags: [tech]
type: tech-tool-study
status: draft
---

# 시작하기 · Reference에서 요구사항으로

## 목표와 준비

버튼 또는 책 형태 예시 하나를 골라 관찰 기록과 검증 계획을 만든다. 초기 단계는 실행 가능한 에셋 확보를 전제로 하지 않는다. 실제 코딩은 전달 형식과 사용 조건을 확인한 뒤 작은 실험 화면에서 진행한다.

## 1. 시각적 특징 기록

https://threeui.com/browse 를 탐색할 수 있다면 후보 하나를 선택한다. 아래 표는 작성용 양식이며 실제 관찰 결과가 아니다.

| 항목 | 기록할 내용 |
|---|---|
| 형태·색상 | 윤곽, 색상 조합, 질감 |
| 배치 | 크기, 여백, 정렬 |
| interaction | hover·click·focus 동작의 확인 여부 |
| animation | 움직임·속도·반복 여부의 확인 여부 |
| 미확인 | 정지 화면에서 알 수 없는 동작과 구현 방식 |

## 2. 전달 형식 확인

복사 기능을 실제로 사용할 수 있다면 내용이 code, prompt 또는 다른 형식인지 먼저 살펴본다. 현재 dossier만으로 이 단계를 재현할 수는 없다.

- code: 파일 구성, dependencies, 실행 조건을 확인한다.
- prompt: 요구사항과 제약이 충분한지 확인한다.
- 기타·불명확: 형식과 처리 방법을 확인하기 전 통합을 보류한다.

## 3. 작은 구현 검증

확보한 형식이 확인되면 버튼 한 개 또는 카드 한 개에 적용한다. 아래는 직접 작성한 요구사항 전달 예시이며 threeui의 복사 결과가 아니다.

```text
목표: 선택한 reference의 시각적 의도를 단일 카드로 구현한다.
프로젝트: [실제 framework·버전·스타일 방식]
관찰한 특징: [형태·색상·배치]
필요한 동작: [직접 정한 interaction]
미확인 사항: [확인하지 못한 animation 등]
수정 범위: [대상 파일·화면]
완료 기준: 외형·동작 검증, 실행 성공, console error 확인.
미확인 제품 기능이나 dependencies를 사실로 가정하지 말 것.
```

## 완료 체크리스트

- [ ] 관찰한 특징과 추가 확인할 동작을 나눴다.
- [ ] 전달 형식과 사용 조건을 확인했다. 확인 불가 시 사유를 기록했다.
- [ ] 구현 가능 시 외형·동작·오류·dependencies를 각각 점검했다.
- [ ] 구현하지 못한 항목을 성공으로 처리하지 않았다.

다음: [[tech/devtools/web-ui-asset-discovery/04-learning/02-deep-dive|심화 실습]]

## Related Notes

- [[tech/devtools/web-ui-asset-discovery/README|학습 경로로 돌아가기]]

## Sources

- https://threeui.com/browse — dossier에 제시된 탐색 화면 URL. 아래 내용은 제공된 영상 요약에 근거하며, 사이트의 현재 기능을 직접 검증한 결과는 아니다.
