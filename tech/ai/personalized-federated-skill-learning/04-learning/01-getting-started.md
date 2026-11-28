---
date: 2026-11-28
tags: [tech]
type: tech-tool-study
status: draft
---

# 시작하기: Skill patch 직접 작성하기

## 목표와 준비

공식 구현 재현이 아니라 **초록의 아이디어를 이해하기 위한 제안 실습**이다. 민감 정보가 없는 합성 trajectory와 간단한 표만 있으면 시작할 수 있다. 공식 패키지나 설치 명령은 확인되지 않았다.

## 1. 합성 trajectory 만들기

예시 task는 “합성 CSV에서 누락값을 확인하고 합계를 계산하기”다.

```text
Task: amount 열의 합계 구하기
Observation: 일부 행에 빈 값이 있음
Action: 누락 행을 식별하고, 정해진 제외 규칙을 적용
Action: 유효한 숫자만 합산
Result: 기대한 합계와 일치
```

실제 고객 데이터·경로·인증정보를 넣지 않는다.

## 2. 조건과 전략 분리하기

다음 YAML은 학습용 스키마이며 논문의 공식 포맷이 아니다.

```yaml
skill_patch:
  id: sum_with_missing_values
  applicability_condition: "숫자 열 합산 task이며 누락값 제외 규칙이 주어짐"
  execution_strategy:
    - "대상 열과 누락값 규칙 확인"
    - "누락 행을 분리하고 유효 숫자만 합산"
    - "결과와 제외한 행 수 검증"
execution_outcome:
  task_id: synthetic_sum_01
  success: true
```

Outcome은 patch와 별도로 둔다. 이 예시의 success는 임의로 정한 학습용 지표다.

## 3. 적용 경계 확인하기

| Task | 적용 판단 예시 | 이유 |
|---|---|---|
| 누락값 제외 후 숫자 합계 | 적용 후보 | Condition과 일치 |
| 누락값을 평균으로 대체 후 합계 | 수정 필요 | 제외 규칙과 충돌 |
| 자유 형식 문서 요약 | 제외 후보 | Task 종류가 다름 |

이 표는 실제 PSS/TASR 알고리즘의 출력이 아니다. “좋은 전략인가”와 “이 task에 맞는가”를 분리하는 연습이다.

## 완료 기준

- [ ] 합성 trajectory 하나와 patch 두 개 이상을 작성했다.
- [ ] Condition·strategy·outcome을 구분했다.
- [ ] 각 patch의 적용·비적용 task를 하나씩 적었다.
- [ ] 실패 outcome도 기록해 선택 편향을 피했다.

다음은 [[tech/ai/personalized-federated-skill-learning/04-learning/02-deep-dive|client별 평가와 routing 실습]]이다.

## Related Notes

- [[tech/ai/personalized-federated-skill-learning/README|학습 진입점]]

## Sources

- https://arxiv.org/abs/2611.33707 — 제공된 dossier의 서지 정보·초록 설명을 근거로 정리. 전문·코드·실험 수치는 확인하지 않음.
