---
date: 2026-11-28
tags: [tech]
type: tech-tool-study
status: draft
---

# P-FedSkill: Task Heterogeneity를 고려한 개인화 Federated Skill Learning

> **한 줄 정의**: P-FedSkill은 agent trajectory에서 추출한 skill을 client별 task 성과와 적용 조건에 따라 개인화하고, 실행 시 task에 맞게 선택하는 Personalized Federated Skill Learning framework다.

## Overview

Agent의 실행 경험을 재사용하려면 유용한 지식을 추출해야 한다. 여러 client가 협업할 때 원본 trajectory에는 민감 정보가 포함될 수 있고, client마다 task 구성이 달라 같은 skill의 유용성도 달라진다.

P-FedSkill은 **LSE → PSS → TASR**로 이 문제를 다룬다. LSE는 적용 조건과 실행 전략으로 된 skill patch 및 별도의 실행 결과를 추출한다. PSS는 client별 후보군을 구성하고, TASR은 현재 task에 맞는 subset을 고른다.

**자료 범위:** 제공된 arXiv 서지 정보와 초록 설명만 사용했다. 저자들은 theoretical guarantee와 extensive experiments를 제시한다고 밝히지만, 보장 조건·benchmark·개선 폭·공식 구현은 확인되지 않았다. 아래 실습은 개념 학습용 제안이다.

## Learning Path

- [ ] [[tech/ai/personalized-federated-skill-learning/README|학습 지도]] — 자료 범위와 활용 조건 파악
- [ ] [[tech/ai/personalized-federated-skill-learning/01-overview|Overview]] — What/Why와 LSE·PSS·TASR 구분
- [ ] [[tech/ai/personalized-federated-skill-learning/02-ecosystem|Ecosystem]] — similarity 기반 FSL 및 설계 대안 비교
- [ ] [[tech/ai/personalized-federated-skill-learning/03-references|References]] — 확인된 근거와 미확인 항목 확인
- [ ] [[tech/ai/personalized-federated-skill-learning/04-learning/01-getting-started|시작하기]] — 합성 trajectory로 skill patch 작성
- [ ] [[tech/ai/personalized-federated-skill-learning/04-learning/02-deep-dive|심화 학습]] — selection·routing 분리 및 ablation 설계
- [ ] [[tech/ai/personalized-federated-skill-learning/05-projects|Projects]] — 작은 실험과 평가 산출물 설계
- [ ] [[tech/ai/personalized-federated-skill-learning/cheatsheet|Cheatsheet]] — 용어와 해석 주의점 복습

## When To Use

- 여러 client의 agent 경험을 공유하되 task 분포 차이에 따른 skill 유용성을 연구할 때.
- Skill library에서 client별 후보군 선택과 실행 시 routing을 분리해 설계할 때.
- 원본 trajectory 대신 추출된 지식을 공유하는 구조의 비용·유출 위험을 검토할 때.

## When Not To Use

- 검증된 설치 명령, 운영 SDK 또는 논문의 정확한 재현 절차가 바로 필요할 때: 제공 자료에는 없다.
- 명시적인 privacy 보장이나 정량적 성능 우위를 근거로 도입을 결정해야 할 때: 이 자료만으로 판단할 수 없다.
- 단일 client의 단순한 task만 있어 협업·개인화 비용의 필요성이 불분명할 때.

## Related Notes

- [[MOCs/Index]]
- [[MOCs/AI]]
- [[tech/ai/agentic-design-patterns/README|Agentic Design Patterns]] — agent 실행 구조와 경험 재사용 설계를 함께 살펴볼 기존 노트.

## Sources

- https://arxiv.org/abs/2611.33707 — 제공된 dossier의 서지 정보·초록 설명을 근거로 정리. 전문·코드·실험 수치는 확인하지 않음.
