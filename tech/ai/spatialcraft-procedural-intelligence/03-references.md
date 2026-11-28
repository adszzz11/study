---
date: 2026-11-26
tags: [tech]
type: tech-tool-study
status: draft
---

# References와 근거 범위

## 기본 자료

| 항목 | 내용 |
|---|---|
| 논문 | SpatialCraft: Evolving Procedural Intelligence from Experience and Skills for Spatial Reasoning Agents |
| arXiv ID | 2611.31475 |
| URL | https://arxiv.org/abs/2611.31475 |
| 작성 근거 | 사용자 제공 초록·서지 정보 dossier |

이 노트 작성 과정에서 논문 전문, 공식 repository, 저자 정보, 코드 공개 여부를 독립 검증하지 않았다. 설치 명령이나 API를 추정해 제공하지 않는다.

## 읽을 때 구분할 세 층

- **초록의 보고**: frozen model, Experience·Skill, Skill-anchored 제공, 무작위 withholding, positive utility 통합, 20개 설정 최고 accuracy.
- **설계 해석**: 전술 발견·제공 시점·기여 추정·절차 통합이 하나의 순환을 이룬다.
- **학습 제안**: 좌표계 예시, 로그 형식, 평가표, 프로젝트와 비용 측정. 논문의 공식 구현이나 검증된 적용 사례가 아니다.

## 전문 확인 시 질문

- [ ] benchmark·backbone·baseline의 정확한 이름과 평가 split은 무엇인가?
- [ ] accuracy 수치와 분산, 반복 실행 수, 비용은 어떻게 보고되는가?
- [ ] Experience 추출에 사용하는 rollout과 정답 판정 기준은 무엇인가?
- [ ] Utility Score의 수식, withholding 확률, 집계·선택 기준은 무엇인가?
- [ ] 여러 Experience의 상호작용과 추정 불확실성을 어떻게 다루는가?
- [ ] Skill의 표현·실행·중첩과 consolidation 이후 퇴행을 어떻게 처리하는가?
- [ ] 평가 task와 지식 생성 task는 어떻게 분리되는가?

답이 확보되기 전에는 미확인 항목을 확정 사실로 채우지 않는다.

## 연결

- [[tech/ai/spatialcraft-procedural-intelligence/README|학습 경로]]
- [[tech/ai/spatialcraft-procedural-intelligence/01-overview|주장과 한계]]

## Sources

- https://arxiv.org/abs/2611.31475 — SpatialCraft 논문. 이 노트는 제공된 초록·서지 정보 dossier에 근거하며, 전문이나 공식 코드를 검증한 결과가 아니다.
