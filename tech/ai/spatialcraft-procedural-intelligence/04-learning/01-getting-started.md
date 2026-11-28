---
date: 2026-11-26
tags: [tech]
type: tech-tool-study
status: draft
---

# 시작하기: 도구 운용 오류 관찰

## 실습의 범위

초록의 아이디어를 이해하기 위한 소규모 실습이다. 공식 설치·재현 절차가 아니다. 실제 agent가 없다면 저장된 실행 기록을 수작업으로 비교해도 된다.

## 준비

- 정답 또는 검증 기준이 있는 작은 공간 질문 집합.
- 사용 가능한 공간 도구와 입력·출력 명세.
- 같은 task를 여러 번 실행한 rollout 기록.
- 실행마다 달라진 조건을 기록할 로그.

## 1. 실행을 기록한다

다음은 학습용 로그 형식이며 논문의 schema가 아니다.

```yaml
task_id: spatial-001
rollout_id: run-01
tool_calls:
  - tool: geometric_computation
    input_summary: 대상 A와 B의 좌표
    output_summary: 거리 측정값
    interpretation: 좌표계와 단위 확인 필요
final_answer: 미기록
correct: null
error_stage: null
call_count: 1
```

이미지·task·도구 버전·모델 설정도 고정하거나 변경 내역을 기록한다. 도구 출력 오류와 agent의 운용 오류를 혼동하지 않는다.

## 2. 오류를 분류한다

| 분류 | 관찰 질문 |
|---|---|
| 도구 선택 | 필요한 정보를 제공하는 도구를 골랐는가? |
| 호출 순서 | 선행 정보 없이 계산을 시작했는가? |
| 출력 해석 | 좌표계·단위·대상 대응을 올바르게 이해했는가? |
| 도구 자체 | 올바른 입력에도 출력이 잘못되었는가? |

## 3. 같은 task의 경로를 대조한다

서로 다른 질문의 성공률부터 비교하지 말고, 동일 질문의 rollout 차이를 본다. 성공·실패 경로의 조건과 행동을 표로 적고 후보 Experience를 만든다.

> 학습용 Experience: 두 측정값의 좌표계가 다르면 직접 비교하기 전에 좌표계를 맞춘다.

한 번의 성공은 일반화 근거가 아니다. 적용 조건과 반례를 함께 적는다.

## 4. Skill의 경계를 적는다

- **Activation**: 식별된 두 대상의 기하 관계를 계산해야 할 때.
- **Procedure**: 대상 식별 → 좌표계 확인 → 기하 계산 → 결과 해석.
- **Termination**: 관계를 해석해 답할 수 있거나, 필요한 정보가 없어 중단할 때.

위 조건과 절차는 개념 설명용 예시이며 논문에 수록된 실제 Skill이 아니다.

## 완료 기준과 다음 단계

- [ ] 동일 task의 복수 rollout과 오류 단계가 기록되어 있다.
- [ ] 후보 Experience가 조건과 행동으로 표현되어 있다.
- [ ] Skill의 시작·종료 조건이 명시되어 있다.

다음: [[tech/ai/spatialcraft-procedural-intelligence/04-learning/02-deep-dive|withholding과 consolidation]] · [[tech/ai/spatialcraft-procedural-intelligence/README|학습 경로]]

## Sources

- https://arxiv.org/abs/2611.31475 — SpatialCraft 논문. 이 노트는 제공된 초록·서지 정보 dossier에 근거하며, 전문이나 공식 코드를 검증한 결과가 아니다.
