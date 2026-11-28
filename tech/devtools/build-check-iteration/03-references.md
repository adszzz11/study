---
date: 2026-11-26
tags: [tech]
type: tech-tool-study
status: draft
---

# References: 근거와 보조 자료

## 원자료의 범위

| 구분 | 확보된 정보 | 사용 원칙 |
|---|---|---|
| 사용자 dossier | 소개 영상의 단계·예시·조건 요약 | 영상 직접 시청이나 제품 검증으로 표현하지 않음 |
| 원본 URL | 미제공 | 추측한 제품·영상 링크를 만들지 않음 |
| 구현 세부 | 미공개 | 모델·언어·자동화 도구·평가법 단정 금지 |
| 실습 설계 | 이 노트에서 제안 | 자료의 사실과 구분해 표기 |

## 추가 확인 질문

- Browse는 어떤 정보를 수집하며 Check에는 무엇이 입력되는가?
- 유사도는 이미지·레이아웃·텍스트·상호작용 중 무엇을 측정하는가?
- 첫 Build·Check를 1라운드로 세는가? 재검사는 어떻게 집계하는가?
- 90%와 6라운드는 시연 설정인가, 기본값인가?
- 목표 충족과 한도 도달을 제품이 따로 보고하는가?
- 실제 라이선스 문서와 무료 제공 범위는 무엇인가?

## 보조 학습 URL

다음 문서는 일반적인 검사 구현을 위한 참고 자료다. dossier의 출처나 Craft Anything의 내부 구현 증거로 사용하지 않는다.

- [Playwright Assertions](https://playwright.dev/docs/test-assertions): 기대 결과를 assertion으로 표현하는 방법.
- [MDN KeyboardEvent](https://developer.mozilla.org/en-US/docs/Web/API/KeyboardEvent): 웹 게임의 키 입력 관찰 참고.

## 연결

[[tech/devtools/build-check-iteration/README|학습 지도]] · [[tech/devtools/build-check-iteration/04-learning/02-deep-dive|평가와 종료 조건 설계]]

## Sources

- 사용자 제공 dossier: Craft Anything 소개 영상의 수집 요약. 원본 URL은 제공되지 않아 기재할 수 없다. 제품 구현·성능·라이선스는 별도 확인이 필요하다.
- 보조 학습: [Playwright Assertions](https://playwright.dev/docs/test-assertions) — 검사 작성 참고이며 Craft Anything의 사용 도구라는 근거는 아니다.
