---
date: 2026-11-28
tags: [tech]
type: tech-tool-study
status: draft
---

# P-FedSkill References

## 핵심 자료

| 항목 | 내용 |
|---|---|
| 논문명 | P-FedSkill: A Personalized Federated Skill Learning Framework under Task Heterogeneity |
| arXiv ID | 2611.33707 |
| URL | https://arxiv.org/abs/2611.33707 |
| 이번 노트의 근거 | 사용자가 제공한 서지 정보와 초록 기반 dossier |
| 확인하지 않은 자료 | 논문 전문, 부록, 공식 repository, 데이터셋, 실행 코드 |

## 주장과 근거 경계

| 항목 | 기록 가능한 내용 | 기록하면 안 되는 단정 |
|---|---|---|
| Framework | LSE·PSS·TASR의 역할과 기능 관계 | 정확한 통신 프로토콜·실행 위치 |
| Skill patch | Condition과 strategy로 구성 | Outcome이 patch 내부 필드라는 정의 |
| Theory | Personalized selection에 theoretical guarantee를 제시한다고 밝힘 | 최적성 증명, 특정 bound·가정 |
| Experiments | Extensive experiments로 효과를 검증했다고 주장 | 특정 benchmark·개선율·유의성 |
| Privacy | 원본 trajectory 공유의 어려움이 동기 | Skill 공유만으로 privacy 보장 |

## 전문 확보 후 확인할 질문

- [ ] PSS 목적함수, selection budget, 성과 추정 방식은 무엇인가?
- [ ] Theorem의 가정·대상·bound와 적용 범위는 무엇인가?
- [ ] TASR이 조건을 표현·매칭하는 방식은 무엇인가?
- [ ] Benchmark, baseline, client/task 분포, 반복 횟수와 분산은 무엇인가?
- [ ] 업로드 정보, 평가 데이터 접근 범위, 통신 순서는 무엇인가?
- [ ] Privacy 위협 모델과 실제 보호 기법이 명시되어 있는가?
- [ ] 공식 코드와 라이선스가 있는가? 미확인 상태에서는 설치 명령을 추정하지 않는다.

## Related Notes

- [[tech/ai/personalized-federated-skill-learning/README|학습 진입점]]

## Sources

- https://arxiv.org/abs/2611.33707 — 제공된 dossier의 서지 정보·초록 설명을 근거로 정리. 전문·코드·실험 수치는 확인하지 않음.
