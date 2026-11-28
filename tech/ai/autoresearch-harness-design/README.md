---
date: 2026-11-25
tags: [tech]
type: tech-tool-study
status: draft
---

# Autoresearch Harness의 Context·Skill 관리와 MLEvolver 분석

> **한 줄 정의**: Autoresearch Harness는 실험을 자율적으로 설계·실행·개선하는 agent가 과거 시도와 재사용 가능한 교훈을 관리하도록 지원하는 실행 체계다.

## Overview

이 study는 *Demystifying the Autoresearch Harness: How Context and Skills Shape Self-Evolving Agents*를 바탕으로, **실험 이력의 보존**과 **재사용 lessons의 선별**을 구분해 학습한다. MLEvolver는 context folding과 skill deletion을 결합한다.

- **Context management:** 과거 시도에서 무엇을 유지할지 결정한다.
- **Skill management:** 시도에서 얻은 교훈을 어떻게 저장하고 재사용할지 결정한다.
- 핵심 관점: 개별 실험 기록은 다시 접근할 수 있도록 보존하고, lessons는 사용 이력에 따라 선별한다.

| Abstract 보고 결과 | 읽을 때의 범위 |
|---|---|
| Context folding이 2 benchmark × 3 model의 여섯 setting에서 최상위 | baseline 대비 최대 19.2%; 평균이나 차이의 단위는 확정 불가 |
| 미사용 lesson의 선택적 삭제가 통합·상시 규칙 승격보다 평균적으로 우세 | 모든 skill을 줄이거나 무조건 삭제하라는 결과가 아님 |
| MLEvolver: MLE-Bench Lite medal rate 72.7% | 해당 subset과 지표에 한정 |
| MLEvolver: KernelBench Level 3 `fast₁` score 94% | 일반 성공률로 해석하지 않음 |

**근거 범위:** 제공된 abstract·서지 정보의 dossier를 정리했다. 원문 본문·코드·통계적 유의성·세부 실행 설정을 확인한 재현 보고서가 아니다. Learning과 Projects는 실습 제안이다.

## Learning Path

- [ ] [[tech/ai/autoresearch-harness-design/README|학습 지도 (현재 노트)]]
- [ ] [[tech/ai/autoresearch-harness-design/01-overview|Overview]]
- [ ] [[tech/ai/autoresearch-harness-design/02-ecosystem|Ecosystem]]
- [ ] [[tech/ai/autoresearch-harness-design/03-references|References]]
- [ ] [[tech/ai/autoresearch-harness-design/04-learning/01-getting-started|시작하기]]
- [ ] [[tech/ai/autoresearch-harness-design/04-learning/02-deep-dive|심화 학습]]
- [ ] [[tech/ai/autoresearch-harness-design/05-projects|Projects]]
- [ ] [[tech/ai/autoresearch-harness-design/cheatsheet|Cheatsheet]]

## When To Use

- 장기 autoresearch에서 실패 이력과 실험 조건을 다시 조회해야 할 때.
- lessons가 누적되어 어떤 지침을 유지·통합·삭제할지 평가할 때.
- 기반 모델을 고정하고 harness 정책의 기여를 분리해서 비교할 때.

## When Not To Use

- 제공 자료만으로 MLEvolver의 정확한 구현이나 성능 재현을 해야 할 때.
- 단발성 작업에 장기 memory 관리가 필요한지 검토하지 않은 채 적용할 때.
- 서로 다른 benchmark 지표를 하나의 성공률로 비교하려 할 때.

## Related Notes

- [[MOCs/Index]]
- [[MOCs/AI]]
- [[tech/ai/thin-harness-fat-skills|Thin Harness, Fat Skills]] — harness와 skill 역할 분리의 관련 관점. 이 논문 결과를 입증하는 자료로 사용하지 않는다.

## Sources

- https://arxiv.org/abs/2611.28244
- https://doi.org/10.48550/arXiv.2611.28244
