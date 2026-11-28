---
date: 2026-11-28
tags: [tech]
type: tech-tool-study
status: draft
---

# P-FedSkill 학습 프로젝트

아래 프로젝트는 공식 재현이 아니라 dossier의 기능 구분을 이해하고 평가 질문을 만드는 제안이다.

## Project 1: 합성 Skill patch catalog

- **목표:** “언제”와 “어떻게”를 함께 기술한다.
- **입력:** 표 계산·문서 요약 등 민감 정보 없는 합성 trajectory.
- **작업:** Patch ID, applicability condition, execution strategy를 정리하고 outcome 표를 따로 만든다.
- **산출물:** Patch catalog와 task별 성공·실패 기록.
- **완료 기준:** 각 patch에 적용 사례와 반례가 있고 outcome을 patch 정의와 구분한다.

## Project 2: Client별 선택 실험

- **목표:** 같은 skill의 client별 유용성이 달라지는지 관찰한다.
- **입력:** 동일 후보군과 서로 다른 task 비중을 가진 가상 client 두 개 이상.
- **작업:** 고정된 budget에서 공통 선택과 client별 선택을 비교한다. 선택 규칙은 직접 정한 proxy임을 표시한다.
- **산출물:** Client별 성과표, 전체 평균, 평가 비용 기록.
- **완료 기준:** 학습용 평가와 최종 평가를 분리하고, 평균에 가려진 client별 차이를 설명한다.

## Project 3: Routing ablation

- **목표:** 후보군 구성과 실행 시 subset 선택의 기여를 분리한다.
- **작업:** Selection 유무 × routing 유무의 네 구성을 동일 budget으로 비교한다.
- **산출물:** 성공률·토큰·지연 표와 condition 오판 사례.
- **완료 기준:** 두 단계 조합이 항상 우수하다고 전제하지 않고 관찰 결과와 한계를 적는다.

## 결과 기록 틀

```text
자료: 합성 데이터 / 논문 재현 아님
Agent 모델·설정:
Client별 task 비중:
후보 patch 수 / 선택·routing budget:
선택 규칙 / condition 매칭 규칙:
평가 분리 방식 / 반복 횟수:
전체·client별 성과 / 변동:
평가 비용 / 실행 지연 / 토큰:
실패 사례 / 해석 한계:
```

공개 산출물에는 합성 데이터만 사용한다. 실제 trajectory를 사용하려면 추출된 patch에도 민감 내용이 남는지 별도 검토해야 한다.

## Related Notes

- [[tech/ai/personalized-federated-skill-learning/README|학습 진입점]]

## Sources

- https://arxiv.org/abs/2611.33707 — 제공된 dossier의 서지 정보·초록 설명을 근거로 정리. 전문·코드·실험 수치는 확인하지 않음.
