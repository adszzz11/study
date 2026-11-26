---
date: 2026-11-27
tags: [tech]
type: tech-tool-study
status: draft
---

# Ecosystem: 작업 방식 비교

## 비교 범위

이 자료에서 이름이 확인되는 환경은 Claude뿐이다. 다른 제품과의 성능 비교 근거가 없으므로 작업 방식의 대안을 비교한다.

| 방식 | 비교 정보 | 활용 목적 | 한계·자료와의 관계 |
|---|---|---|---|
| 텍스트 기반 수정 | 자연어 요청 | 수정 의도 전달 | 요청은 관찰되지만 정확성 미확인 |
| 화면 병렬 비교 | 두 화면의 시각적 차이 | 전체 인상·차이 지점 확인 | 등장하지만 정량 일치를 증명하지 않음 |
| 녹화 기반 검토 | 시간에 따른 화면 변화 | Motion·상태 전환 확인 | 첨부·재녹화는 등장, 측정 방식 불명 |
| 자동 수정 루프 | 관찰에 따른 변경 | 반복 작업 자동화 | 언급만 확인, 범위·성공 여부 불명 |
| 정량적 visual regression | 고정 조건과 판정 기준 | 변경 전후 일관된 판정 | 실습 대안이며 영상의 사용 여부 미확인 |

## 선택 가이드

- 위치·간격 확인: 동일 viewport의 병렬 화면부터 시작한다.
- 속도·순서 확인: 시작 이벤트를 맞춘 녹화를 검토한다.
- 반복적인 정적 화면 회귀 감지: baseline과 허용 기준을 정의한 visual regression을 검토한다.
- 자동 수정: 결과 수집과 검증을 분리하고 미해결 차이를 남긴다.

화면 비교는 시각적 차이를 찾는 데 유용하지만 기능·접근성 검증을 대신하지 않는다. Claude의 우위나 완전 자율 수정의 작동 여부는 이 자료로 평가할 수 없다.

## 연결

[[tech/devtools/web-ui-comparison-iteration/04-learning/01-getting-started|조건을 고정하는 실습]] · [[tech/devtools/web-ui-comparison-iteration/README|학습 경로]]

## Sources

- 제공 dossier: 원본 영상·게시물 URL 미제공. 영상의 직접 재검증은 수행하지 않았으며, 관찰 서술은 dossier에 근거한다.
- 보충 학습: [Playwright — Visual comparisons](https://playwright.dev/docs/test-snapshots). 실습 설계를 위한 공식 문서이며 영상에서 사용한 도구라는 뜻은 아니다.
