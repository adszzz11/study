---
date: 2026-11-26
tags: [tech]
type: tech-tool-study
status: draft
---

# Ecosystem: 도구 운용을 개선하는 접근

## 비교의 기준

아래는 접근 방식별 **개념 비교**다. 구체적인 경쟁 framework나 논문의 실제 실험 baseline 목록은 제공되지 않았다.

| 접근 | 개선·활용 대상 | SpatialCraft와의 차이 | 판단 가능한 범위 |
|---|---|---|---|
| 픽셀 중심 MLLM 추론 | 시각 입력의 모델 추론 | 외부 공간 도구 운용을 개선 | 픽셀만으로 어려운 질문이 연구 배경 |
| Stateless tool-using agent | 현재 task의 호출과 해석 | interaction history를 축적 | 반복 실수가 문제로 제시됨 |
| 고정 multi-step procedure | 미리 정의한 절차 | Skill이 Experience를 통합하며 진화 | 해당 baseline의 실험 여부 불명 |
| Task당 한 번 Experience 제공 | 작업 단위 지침 | Skill 활성 구간에 지침 제공 | 제공 방식의 차이는 초록에 명시 |
| Parameter update 기반 개선 | 내부 모델 가중치 | frozen model과 외부 지식 사용 | 학습 비용·성능 직접 비교 없음 |
| SpatialCraft | Experience·Skill 기반 orchestration | 적용 시점·효용 추정·통합 결합 | 20개 설정 최고 accuracy 보고 |

## 생태계에서의 위치

3D reconstruction, segmentation, geometric computation은 공간 정보를 얻거나 계산하는 도구다. SpatialCraft의 대상은 그 알고리즘 자체가 아니라 **도구를 운용하는 agent의 절차적 판단**이다.

- 출력 자체가 틀렸다면 도구의 품질부터 점검한다.
- 올바른 출력을 얻고도 좌표계나 순서를 잘못 다뤘다면 orchestration 개선을 검토한다.
- 도입 판단에는 accuracy 외에 반복 실행 비용과 지식 관리 부담도 별도로 측정한다. 이는 실습 권고이며 논문의 측정 결과가 아니다.

## 연결

- [[tech/ai/spatialcraft-procedural-intelligence/README|학습 경로]]
- [[tech/ai/spatialcraft-procedural-intelligence/05-projects|비교 실험 프로젝트]]

## Sources

- https://arxiv.org/abs/2611.31475 — SpatialCraft 논문. 이 노트는 제공된 초록·서지 정보 dossier에 근거하며, 전문이나 공식 코드를 검증한 결과가 아니다.
