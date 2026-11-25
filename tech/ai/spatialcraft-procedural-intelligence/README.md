---
date: 2026-11-26
tags: [tech]
type: tech-tool-study
status: draft
---

# SpatialCraft: Experience와 Skill로 진화하는 공간 추론 에이전트

> **한 줄 정의**: SpatialCraft는 모델 파라미터를 고정한 tool-using spatial reasoning agent가 실행 이력에서 Experience와 Skill을 축적·평가·통합하여 도구 orchestration을 개선하는 self-evolving framework다.

## Overview

공간 질문은 이미지의 픽셀만으로 풀기 어려울 수 있다. 3D reconstruction, segmentation, geometric computation 같은 도구를 쓰더라도 **무엇을 어떤 순서로 호출하고 출력을 어떻게 해석할지**는 별도의 문제다. SpatialCraft는 interaction history를 외부 procedural knowledge로 바꾸어 이 병목을 다룬다.

- **Experience**: 같은 task의 rollout을 대조해 얻은 condition-action tactic.
- **Skill**: activation condition과 termination condition을 갖춘 multi-step procedure.
- **평가와 통합**: Experience를 무작위 withholding하여 효용을 추정하고, 지속적으로 유용한 전술을 Skill에 통합한다.
- **근거의 범위**: 초록은 five spatial benchmarks × four backbones, 총 20개 설정 모두에서 최고 accuracy를 보고한다. 수치·개선 폭·비용·baseline 명칭은 제공되지 않았다.

Frozen은 모델 가중치가 고정된다는 뜻이다. 외부 Experience와 Skill은 바뀌므로 시스템의 행동까지 고정되는 것은 아니다.

## Learning Path

- [ ] [[tech/ai/spatialcraft-procedural-intelligence/01-overview|Overview]] — 문제와 핵심 개념 이해
- [ ] [[tech/ai/spatialcraft-procedural-intelligence/02-ecosystem|Ecosystem]] — 다른 접근과 역할 비교
- [ ] [[tech/ai/spatialcraft-procedural-intelligence/03-references|References]] — 출처와 확인 불가능한 정보 점검
- [ ] [[tech/ai/spatialcraft-procedural-intelligence/04-learning/01-getting-started|시작하기]] — rollout 기록과 오류 분류
- [ ] [[tech/ai/spatialcraft-procedural-intelligence/04-learning/02-deep-dive|Deep Dive]] — withholding과 consolidation 실습
- [ ] [[tech/ai/spatialcraft-procedural-intelligence/05-projects|Projects]] — 작은 평가 프로젝트 설계
- [ ] [[tech/ai/spatialcraft-procedural-intelligence/cheatsheet|Cheatsheet]] — 용어와 검증 체크리스트 복습

이 README가 학습 경로의 진입점이며, 각 하위 노트에서 돌아올 수 있다.

## When To Use

- 공간 도구를 이미 사용할 수 있지만 호출 선택·순서·해석에서 오류가 반복될 때.
- 모델 재학습 없이 실행 이력을 다음 task의 절차적 판단에 활용하려 할 때.
- 단순 memory 축적을 넘어 지식의 적용 시점과 유용성을 평가하고 싶을 때.

## When Not To Use

- segmentation이나 3D reconstruction 도구 자체의 정확도를 개선해야 할 때.
- 공식 설치법·API·재현 가능한 benchmark 수치가 즉시 필요할 때: 제공 자료만으로는 확인할 수 없다.
- 반복 rollout과 검증 비용 없이 즉각적인 성능 향상을 보장해야 할 때.

## Related Notes

- [[MOCs/Index]]
- [[MOCs/AI]]
- [[tech/ai/spatialcraft-procedural-intelligence/01-overview|SpatialCraft 개념과 orchestration]] — 관련 tech 개념 노트
- [[tech/ai/spatialcraft-procedural-intelligence/02-ecosystem|SpatialCraft와 대안 접근 비교]]

## Sources

- https://arxiv.org/abs/2611.31475 — SpatialCraft 논문. 이 노트는 제공된 초록·서지 정보 dossier에 근거하며, 전문이나 공식 코드를 검증한 결과가 아니다.
