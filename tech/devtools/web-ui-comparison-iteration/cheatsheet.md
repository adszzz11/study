---
date: 2026-11-27
tags: [tech]
type: tech-tool-study
status: draft
---

# Cheatsheet: 비교 → 수정 → 재관찰

## 반복 전

- [ ] baseline과 비교할 결과를 지정한다.
- [ ] viewport·배율·데이터·초기 state·스크롤을 맞춘다.
- [ ] 폰트 로딩과 Motion 관련 환경 설정을 확인한다.
- [ ] Layout / 시각 표현 / Motion / 상호작용 중 검토 축을 고른다.
- [ ] Motion은 공통 시작 이벤트와 녹화 구간을 정한다.

## 요청 템플릿

```text
대상:
관찰한 차이:
원하는 변화:
이번 수정 범위:
동일 조건 재확인 방법:
기존 동작의 회귀 확인 항목:
```

## 반복 후

- [ ] 변경 실행과 실제 개선을 따로 확인한다.
- [ ] 동일 조건으로 결과를 다시 수집한다.
- [ ] 정적 화면과 시간에 따른 동작을 각각 판정한다.
- [ ] 변경 전후 근거와 판정 사유를 남긴다.
- [ ] 미해결 차이·회귀·보류를 기록한다.

## 흔한 오판

| 오판 | 교정 |
|---|---|
| “더 비슷하게”만 요청 | 대상·관찰·범위·확인 방법 명시 |
| 조건이 다른 화면 비교 | 구현 차이와 조건 차이 분리 |
| 스크린샷이 같으니 Motion도 같음 | 같은 시작점의 녹화로 검증 |
| 변경 완료 응답을 품질 통과로 처리 | 실제 화면과 기존 상호작용 재확인 |
| `417 / 417`을 일치율로 해석 | 지표 정의가 없으므로 의미 미확인 |
| `/reanimate`를 공식 기능으로 소개 | 일부 보이는 명령 단서이며 정체 미확인 |

## 연결

[[tech/devtools/web-ui-comparison-iteration/04-learning/01-getting-started|반복 기록 양식]] · [[tech/devtools/web-ui-comparison-iteration/README|학습 경로]]

## Sources

- 제공 dossier: 원본 영상·게시물 URL 미제공. 영상의 직접 재검증은 수행하지 않았으며, 관찰 서술은 dossier에 근거한다.
- 보충 학습: [Playwright — Visual comparisons](https://playwright.dev/docs/test-snapshots). 실습 설계를 위한 공식 문서이며 영상에서 사용한 도구라는 뜻은 아니다.
