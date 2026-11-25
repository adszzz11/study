---
date: 2026-11-26
tags: [tech]
type: tech-tool-study
status: draft
---

# Projects: 절차적 지식 실험

## 제안의 성격

다음은 원리를 학습하기 위한 프로젝트다. 논문이 검증한 적용 사례나 공식 구현이 아니다. 제공 dossier에서 마지막 프로젝트 행은 중간에 끊겨 있으며, 아래 적용 범위 비교의 구체 설계는 이 노트의 실습 제안이다.

| 프로젝트 | 구현 방향 | 핵심 검증 질문 |
|---|---|---|
| 공간 QA orchestration 실험기 | 도구 agent에 Experience 저장소와 Skill 실행 상태 추가 | Stateless 방식보다 동일 오류의 재발이 줄어드는가? |
| Experience 평가 harness | 동일 task 반복 실행에서 무작위 withholding과 결과 기록 | 유용해 보이는 규칙이 실제 성능에 기여하는가? |
| Skill 적용 범위 비교기 | task 시작 시 제공과 Skill 활성 중 제공 비교 | 제공 시점이 행동과 정확도에 어떤 차이를 만드는가? |
| Consolidation 검증기 | Skill 버전별 통합 전후 비교 | 통합 효과가 미사용 task에서도 유지되는가? |

## 권장 첫 프로젝트: 평가 harness

1. 작은 task 집합과 정답 기준을 정한다.
2. [[tech/ai/spatialcraft-procedural-intelligence/04-learning/01-getting-started|실행 로그]]로 stateless 기준 실행을 수집한다.
3. 동일 task의 경로를 대조해 후보 Experience를 만든다.
4. [[tech/ai/spatialcraft-procedural-intelligence/04-learning/02-deep-dive|withholding 실습]]으로 제공·제외 결과를 수집한다.
5. 지속적으로 유용한 전술만 Skill에 통합하고 별도 task에서 평가한다.

## 산출물

- task별 rollout과 도구 호출 로그.
- 조건·행동·근거 실행 ID를 가진 Experience 목록.
- activation·termination condition이 명시된 Skill 버전.
- task별 accuracy, 호출 수, 비용, 실패 유형 비교표.

## 완료 기준

- [ ] 기준 실행과 변경 실행의 조건이 기록되어 있다.
- [ ] 지식 추출에 쓴 task와 별도 평가 task가 구분되어 있다.
- [ ] 효과가 없거나 악화된 사례도 결과에 포함되어 있다.
- [ ] 실습 지표와 논문 결과를 혼용하지 않는다.

## 연결

- [[tech/ai/spatialcraft-procedural-intelligence/README|학습 경로]]
- [[tech/ai/spatialcraft-procedural-intelligence/02-ecosystem|접근 방식 비교]]

## Sources

- https://arxiv.org/abs/2611.31475 — SpatialCraft 논문. 이 노트는 제공된 초록·서지 정보 dossier에 근거하며, 전문이나 공식 코드를 검증한 결과가 아니다.
