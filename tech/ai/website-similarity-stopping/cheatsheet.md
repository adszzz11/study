---
date: 2026-11-27
tags: [tech]
type: tech-tool-study
status: draft
---

# Cheatsheet

## 흐름과 종료

```text
Browse → Build ↔ Check → Complete
개념적 종료: similarity >= 0.90 OR completed_rounds >= 6
```

| 항목 | 기억할 점 |
|---|---|
| 90% | 품질 목표; metric과 타당성은 미확인 |
| 6라운드 | 횟수 한도; 시간·비용·품질 보장 아님 |
| target_reached | 실습용 목표 달성 종료 상태 |
| round_limit_reached | 실습용 목표 미달 한도 종료 상태 |
| 외형과 기능 | 별도로 검사·기록 |
| 마지막과 최고 | 다를 수 있으므로 반환 정책 명시 |
| 평가 실패 | 0점과 구분; 오류 처리 방침 필요 |

## 실행 전 체크

- [ ] Reference와 비교 항목을 정의했다.
- [ ] Viewport와 페이지 상태 등 평가 환경을 고정했다.
- [ ] 최초 Build 포함 여부와 라운드 단위를 정했다.
- [ ] 89·90·91% 및 5·6회 경계값을 확인했다.
- [ ] 동시 충족 우선순위와 평가 실패 처리를 정했다.
- [ ] 변경·점수·기능 검사·종료 이유와 최고 artifact를 기록한다.

90%·6회는 영상 요약에 제시된 수치다. 실제 구현·달성률·기능 평가 범위가 확인되었다는 뜻은 아니다. 위 상태 이름과 체크리스트는 적용 제안이다.

## 연결

[[tech/ai/website-similarity-stopping/04-learning/01-getting-started|시작하기]] · [[tech/ai/website-similarity-stopping/03-references|근거와 미확인 사항]] · [[tech/ai/website-similarity-stopping/README|학습 경로]]

## Sources

- 제공된 dossier: Craft Anything 소개 영상의 수집 요약. 원본 영상 URL과 공식 문서 URL은 제공되지 않았다. 따라서 기재할 수 있는 출처 URL이 없으며, 임의로 추정하지 않는다.
- 아래 정책 해석과 실습 제안은 제품 구현이나 성능을 검증한 자료가 아니다.
