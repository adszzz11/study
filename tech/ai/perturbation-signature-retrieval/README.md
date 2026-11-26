---
date: 2026-11-27
tags: [tech]
type: tech-tool-study
status: draft
---

# 세포 수준 Perturbation Signatures 기반 표적·화합물 검색

> **한 줄 정의**: 세포에 가해진 perturbation 이후의 변화 패턴인 **perturbation signature**를 검색 단서로 삼아 관련 표적(target)과 화합물(compound)을 찾는 연구 주제다.

## Overview

세포 반응을 검색 가능한 표현으로 바꾸어 개입 후보를 좁히는 문제를 공부한다. 특정 제품의 사용법이나 논문 재현 가이드가 아니라 **문제 정의·검색 설계·평가를 위한 tool-study**다.

제공 자료에서 확인되는 것은 영상 **00:47에 해당 주제의 논문 제목이 표시되었다는 설명**뿐이다. 원 영상이나 논문을 직접 확인하지 않았으며 모델, 데이터셋, 측정 방식, 성능 및 URL은 알 수 없다. 이후의 아키텍처와 실습은 학습용 제안이다.

- 데이터: 관측 특징, perturbation identity, 실험 context, target·compound 연결 정보.
- 처리: 품질 관리 → signature 생성 → 벡터 또는 embedding 검색 → 후보 순위화.
- 검증: Top-K relevance, 누수, 조건별 일반화, 순위 안정성.
- 해석: **검색상 유사성 ≠ 생물학적 관련성 ≠ 인과적 작용 관계**.

## Learning Path

- [ ] [[tech/ai/perturbation-signature-retrieval/01-overview|Overview]]
- [ ] [[tech/ai/perturbation-signature-retrieval/02-ecosystem|설계 대안 비교]]
- [ ] [[tech/ai/perturbation-signature-retrieval/03-references|References]]
- [ ] [[tech/ai/perturbation-signature-retrieval/04-learning/01-getting-started|시작하기]]
- [ ] [[tech/ai/perturbation-signature-retrieval/04-learning/02-deep-dive|심화 학습]]
- [ ] [[tech/ai/perturbation-signature-retrieval/05-projects|Projects]]
- [ ] [[tech/ai/perturbation-signature-retrieval/cheatsheet|Cheatsheet]]

## When To Use

- 관찰 또는 원하는 세포 반응으로부터 후속 검증할 후보를 탐색할 때.
- signature 검색의 query·candidate·relevance 계약을 설계할 때.
- 데이터 분할과 context가 검색 평가에 미치는 영향을 공부할 때.

## When Not To Use

- 제목만으로 원 논문의 모델·성능을 설명하거나 재현하려 할 때.
- 유사도만으로 target identification, 약효 또는 치료 효과를 확정하려 할 때.
- 실험 조건이나 relevance 정의 없이 검색 점수를 비교하려 할 때.

## Related Notes

- [[MOCs/Index]]
- [[MOCs/AI]]
- [[tech/ai/perturbation-signature-retrieval/02-ecosystem|관련 tech 노트: Signature retrieval 설계 대안]]
- 기존 vault의 관련 tech 노트는 현재 작업 공간에서 확인할 수 없어 추가 링크를 만들지 않았다.

## Sources

- 사용자 제공 dossier: 영상 00:47에 주제의 논문 제목이 표시되었다는 설명. 영상 및 논문 URL은 제공되지 않아 기재할 수 없다.
- 아래 설계·실습은 dossier를 바탕으로 만든 학습용 제안이며, 원 논문의 구현 또는 검증 결과가 아니다.
