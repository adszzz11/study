---
date: 2026-11-28
tags: [tech]
type: tech-tool-study
status: draft
---

# P-FedSkill Ecosystem과 비교

## 비교 범위

제공 자료에는 구체적인 경쟁 framework 이름이 없다. 다음 표는 초록에 등장하는 접근과 이해를 위한 설계 대안을 비교하며, 실제 논문 baseline 목록을 의미하지 않는다.

| 접근 | 공유·활용 단위 | 선택 기준 | Task heterogeneity 대응 | 근거 범위 |
|---|---|---|---|---|
| Trajectory 직접 공유 | 원본 실행 기록 | 설명 없음 | 확인 불가 | 민감 정보로 공유가 어렵다는 배경 |
| Similarity 기반 기존 FSL | Compact skill representations | 주로 skill similarity | Client별 task 기여를 충분히 고려하지 않는다고 설명 | 저자들이 지적한 비교 대상 |
| P-FedSkill | Skill patches 중심의 공유·활용 | Client task 성과·적용 조건·현재 task 관련성 | PSS와 TASR 두 단계 | 이론적 보장·실험 효과는 저자 주장 |
| Local-only skill learning | Client 내부 경험과 skill | 로컬 기준으로 설계 가능 | 로컬 적합성은 높일 수 있으나 협업 제한 | 개념 설명용 대안; baseline 여부 미상 |

## 설계 판단

P-FedSkill의 차별점은 공유량 자체보다 **client별 유용성과 실행 시 적합성**을 함께 관리하는 구조다. 서로 다른 task 비중을 가진 client가 있다면 전체 평균만으로 효과를 판단하지 말고 client별 성과도 봐야 한다.

| 추가 확인할 비용 | 필요한 근거 |
|---|---|
| LSE 추출 비용 | 추출 호출 수·토큰·처리 시간 |
| PSS 평가 비용 | 평가 task 수·평가 주기·skill 후보 수 |
| TASR 실행 지연 | Task별 routing 시간·사용 토큰 |
| 공유·저장 비용 | Payload 크기·통신량·patch 수 |

위 항목은 후속 검토 제안이다. 자료에 비용 수치가 없어 성능 향상이 운영 비용을 상쇄하는지는 판단할 수 없다.

## Related Notes

- [[tech/ai/personalized-federated-skill-learning/README|학습 진입점]]

## Sources

- https://arxiv.org/abs/2611.33707 — 제공된 dossier의 서지 정보·초록 설명을 근거로 정리. 전문·코드·실험 수치는 확인하지 않음.
