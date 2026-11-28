---
date: 2026-11-28
tags: [tech]
type: tech-tool-study
status: draft
---

# P-FedSkill Overview

## What

**Federated Skill Learning(FSL)**은 trajectory를 compact skill representation으로 증류하고 central server에 업로드해 공유하는 접근이다. 협업 단위를 원본 실행 기록에서 skill로 바꾼다. P-FedSkill은 여기에 client task 성과와 적용 조건을 고려하는 개인화를 도입한다.

## Why

Client마다 task가 다르면 같은 skill도 기여도가 다르다. 초록은 기존 FSL이 주로 skill similarity로 공유 대상을 정하면 해당 client에게 도움이 적은 skill이 전달되어 agent 성능이 저하될 수 있다고 설명한다.

- **Client 수준 질문:** 이 client의 task들에 유용한 skill은 무엇인가? → PSS
- **실행 수준 질문:** 현재 task에 적용할 skill은 무엇인가? → TASR

## 기능 흐름

```text
Client agent trajectories
  → LSE: skill patches + task execution outcomes
  → PSS: client별 personalized skill set
  → TASR: 현재 task에 관련된 patch subset
  → Agent execution 지원
```

이는 기능 관계를 요약한 그림이다. 정확한 연산 위치, 업로드 payload, server/client 통신 순서를 나타내지 않는다.

## LSE: 조건·전략·결과 분리

| 추출 정보 | 역할 | Patch 내부 여부 |
|---|---|---|
| Task applicability condition | 언제 적용할지 판단 | 포함 |
| Execution strategy | 어떻게 수행할지 안내 | 포함 |
| Task execution outcome | 해당 skill의 유용성 평가 근거 | 별도 추출; 내부 구성요소로 정의되지 않음 |

**Skill patch = applicability condition + execution strategy**다. Condition의 표현 형식, strategy 길이·구조, outcome 평가 척도는 미확인이다.

## PSS와 TASR

| 구분 | Personalized Skill Selection(PSS) | Task-Aware Skill Routing(TASR) |
|---|---|---|
| 판단 단위 | Client의 task들 | 현재 실행 task |
| 판단 근거 | Execution outcomes와 applicability conditions | Applicability conditions |
| 결과 | Client별 personalized skill set | Task-relevant patch subset |

PSS는 skill 간 유사성만이 아니라 skill과 client task 사이의 관계를 고려한다. TASR은 보유 후보 중 이번 실행에 필요한 부분을 고른다. Client에게 유용한 전체 skill과 개별 task에 필요한 skill이 다를 수 있다는 해석이 가능하다.

## 기여와 한계

초록에서 확인되는 기여는 LSE·PSS·TASR을 결합한 framework, personalized selection에 대한 theoretical guarantee 제시, extensive experiments를 통한 효과 검증 주장이다.

- 보장이 optimality·approximation·convergence·generalization 중 무엇을 대상으로 하는지, 가정과 bound가 무엇인지는 미확인이다.
- Benchmark, baseline, client 수, task 분포, 지표, 개선 폭, 통계적 변동은 확인되지 않는다.
- Trajectory를 직접 공유하지 않아도 condition·strategy에 민감 정보가 남을 수 있다. Privacy attack 실험이나 Differential Privacy 적용이 확인된 것은 아니다.

## Related Notes

- [[tech/ai/personalized-federated-skill-learning/README|학습 진입점]]

## Sources

- https://arxiv.org/abs/2611.33707 — 제공된 dossier의 서지 정보·초록 설명을 근거로 정리. 전문·코드·실험 수치는 확인하지 않음.
