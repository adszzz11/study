---
date: 2026-11-25
tags: [tech]
type: tech-tool-study
status: draft
---

# Projects: Harness 정책 실험대

## 범위

Dossier의 프로젝트 1 설명은 중간에서 끝난다. 아래 구체 절차와 산출물, 프로젝트 2는 연구 질문을 바탕으로 작성한 **실습 제안**이다. 공식 MLEvolver 구현·설치법·재현 절차를 뜻하지 않는다.

## 프로젝트 1: Harness 정책 비교 실험대

반복 개선 가능한 작은 coding 또는 optimization task 하나를 고른다. 공통 실행기와 평가기를 두고 context·skill 정책만 교체할 수 있게 만든다.

| 구성 | 책임 | 산출물 |
|---|---|---|
| Runner | 동일 환경에서 후보 실행 | 실행 로그·artifact |
| Evaluator | 정확성·task score 평가 | 조건별 원시 결과 |
| Experiment store | 가설·변경·조건·결과 보존 | ID로 조회 가능한 기록 |
| Lesson store | 적용 조건·근거·사용 event 관리 | 정책별 lesson snapshot |
| Budget tracker | 추론과 관리 비용 계측 | 사용량·종료 사유 |

### 진행 순서

1. Task·model·budget·seed 목록·성공 기준을 고정한다.
2. Skill 정책을 고정하고 recency truncation / rolling summary / 개별 기록 접근을 비교한다.
3. Context 정책을 고정하고 유지 / 통합 / 상시 규칙화 / 미사용 삭제를 비교한다.
4. 반복별 score·실행 수·inference·조회량·lesson 사용 빈도를 정리한다.
5. 실패 사례에서 “근거를 못 봄”과 “잘못된 교훈 적용”을 분리해 분석한다.

### 완료 기준

- [ ] 정책 외 변경 사항과 예산 초과 여부를 추적할 수 있다.
- [ ] 모든 lesson에서 근거 실험으로 돌아갈 수 있다.
- [ ] 반복별 결과와 관리 비용을 포함한 비교표가 있다.
- [ ] 개별 기록 접근을 context folding 재현이라고 부르지 않는다.

## 프로젝트 2: Lesson 사용 이력 감사

목표는 삭제를 많이 하는 것이 아니라 미사용의 이유를 구별하는 것이다.

- 동일 lesson snapshot에 대해 관련 상황 발생·조회·적용·결과 event를 수집한다.
- 지속적 미사용 후보를 archive하고 삭제 이유와 복구 event를 남긴다.
- 희귀 조건 평가에서 필요한 lesson이 사라지는지 살펴본다.
- Threshold와 window를 바꿨을 때 후보 수·성과·복구 빈도를 비교한다.

완료 산출물은 event log, 후보 목록, 오삭제 의심 사례, 복구 기록이다. 사용 빈도만으로 lesson의 정확성을 판정하지 않았는지 검토한다.

## 결과 기록 양식

```text
Task / model / evaluator version:
Context policy / skill policy:
Inference budget / execution limit / seed:
Task score / runs / inference used:
Record lookups / lesson use events:
Management cost / wall-clock time:
Failure case / evidence IDs:
Limitations / next isolated experiment:
```

논문의 medal rate·`fast₁`과 자체 task score를 같은 지표처럼 비교하지 않는다.

## Navigation

- [[tech/ai/autoresearch-harness-design/README|학습 진입점]]

## Sources

- https://arxiv.org/abs/2611.28244
- https://doi.org/10.48550/arXiv.2611.28244
