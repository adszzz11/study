---
date: 2026-11-26
tags: [tech]
type: tech-tool-study
status: draft
---

# SpatialCraft Overview

> 도구 접근 권한만으로는 안정적인 도구 운용 능력이 생기지 않는다.

## What

SpatialCraft는 frozen MLLM을 사용하는 공간 추론 agent의 self-evolving framework다. 외부 지식인 Experience와 Skill을 바꾸어 이후 실행을 개선한다. 여기서 학습은 parameter update보다 **procedural knowledge의 진화**를 뜻한다.

## Why

Stateless agent는 이전 실행에서 얻은 교훈을 유지하지 못해 같은 실수를 반복할 수 있다. 도구를 도입하면 병목은 다음으로 이동한다.

1. 질문에 맞는 도구 선택.
2. 선행 정보에 맞춘 호출 순서 결정.
3. 출력 해석과 다음 행동 연결.

연구 질문은 “모델을 다시 학습시키지 않고 interaction history로 도구 운용을 개선할 수 있는가?”다.

## 핵심 구조

| 요소 | 역할 | 확인되지 않은 세부사항 |
|---|---|---|
| Experience | 동일 task의 rollout 대조로 조건별 행동 전술 추출 | rollout 선택, 성공 판정, 저장 형식 |
| Skill | 시작·종료 조건이 명시된 다단계 절차 | 표현 언어, 실행 엔진, 중첩·충돌 처리 |
| Skill-anchored Experience | 연결된 Skill 활성 중에만 전술 제공 | 실제 context 비용 변화 |
| Contrastive Utility Score | 같은 task에서 무작위 withholding으로 기여 추정 | 수식, 제외 확률, 표본 수, 상호작용 처리 |
| Consolidation | 일관된 positive utility의 Experience를 Skill에 통합 | 퇴행 감지, 폐기·수정, negative utility 처리 |

Experience는 단순 로그가 아니라 **조건 → 행동** 지침이다. Skill은 여러 행동의 적용 구간을 정의한다. Skill-anchored Experience는 task 시작 시 한 번 제공하는 지침과 달리, 관련 절차가 활성화된 동안 제공된다.

```text
실행 이력 → 동일 task의 rollout 대조 → Experience 추출
        → Skill에 연결 → 무작위 withholding으로 효용 평가
        → 유용한 Experience를 Skill에 통합
```

이 흐름은 초록 구성요소를 연결한 개념도이며, 구현의 정확한 처리 순서를 보장하는 명세가 아니다.

## 결과를 읽는 범위

초록은 5개 benchmark와 4개 backbone의 20개 설정 모두에서 최고 accuracy를 보고한다. 그러나 이름, 수치, 비교 대상, 통계적 유의성은 제공 자료에서 확인되지 않는다. **일관된 우위가 보고되었다**고 말할 수 있지만 효과 크기나 비용 대비 효율은 판단할 수 없다.

무작위 withholding은 기여도 추정 장치다. 이를 엄밀한 개별 causal effect의 보장으로 확대하지 않는다. Context 사용량 감소나 지식 간섭 완화도 가능한 설계상 이점이며 측정 결과가 아니다.

## 다음 학습

- [[tech/ai/spatialcraft-procedural-intelligence/README|학습 경로]]
- [[tech/ai/spatialcraft-procedural-intelligence/04-learning/02-deep-dive|효용 평가와 통합 실습]]

## Sources

- https://arxiv.org/abs/2611.31475 — SpatialCraft 논문. 이 노트는 제공된 초록·서지 정보 dossier에 근거하며, 전문이나 공식 코드를 검증한 결과가 아니다.
