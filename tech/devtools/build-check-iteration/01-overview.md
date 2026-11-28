---
date: 2026-11-26
tags: [tech]
type: tech-tool-study
status: draft
---

# Overview: Build·Check 반복 개발

## What

자료에 표시된 흐름은 다음과 같다. 화살표는 개념적 순서이며 실제 내부 구현을 뜻하지 않는다.

```text
Browse → Build → Check → Complete
           ↑       │
           └─ 수정 ┘
```

| 요소 | 자료에서 확인된 내용 | 확인되지 않은 부분 |
|---|---|---|
| Browse | 첫 단계로 표시 | 참고 탐색인지 요구사항 조사인지 |
| Build | 결과물 제작 | 생성 방식, 실행 환경, 모델 |
| Check | 제작 뒤 검사 | 자동·수동 여부, 검사 도구 |
| 반복 | Build·Check 반복 도식 | 피드백 전달·저장 형식 |
| Complete | 최종 단계 | 종료 사유를 구분하는 실제 UI |
| 종료 조건 | 웹사이트 유사도 90% 또는 최대 6라운드 | 평가법, 집계법, 공통 기본값 여부 |

## Why

요청과 실제 결과 사이에는 차이가 생길 수 있다. Snake의 화면 제작과 방향키 이동·먹이 섭취 후 성장·속도 증가의 검증은 별도 작업이다. 검사 가능한 acceptance criteria를 먼저 정하면 누락을 드러내고 수정 범위를 좁힐 수 있다.

## 핵심 특징과 설계 제안

1. **Acceptance criteria:** 입력·기대 결과·관찰 방법으로 요구사항을 분해한다.
2. **Feedback loop:** “성장 실패”보다 “먹이 섭취 뒤에도 길이가 유지됨”처럼 관찰 사실을 남긴다.
3. **Regression check:** 수정 후 이전에 통과한 기능도 재검사한다. 반복이 항상 개선을 보장하지는 않는다.
4. **Termination condition:** 목표 통과와 한도 소진을 별도 결과로 기록한다.

위 기록 방식과 상태 구분은 적용을 위한 제안이다. Craft Anything이 이를 구현한다는 사실은 확인되지 않았다. 별 수 그래픽, LICENSE 표기, 무료 자막만으로 사용 규모·성능·라이선스 종류·무료 범위를 확정할 수 없다.

## 다음 단계

[[tech/devtools/build-check-iteration/02-ecosystem|개발 절차 비교]] · [[tech/devtools/build-check-iteration/README|학습 지도]]

## Sources

- 사용자 제공 dossier: Craft Anything 소개 영상의 수집 요약. 원본 URL은 제공되지 않아 기재할 수 없다. 제품 구현·성능·라이선스는 별도 확인이 필요하다.
- 보조 학습: [Playwright Assertions](https://playwright.dev/docs/test-assertions) — 검사 작성 참고이며 Craft Anything의 사용 도구라는 근거는 아니다.
