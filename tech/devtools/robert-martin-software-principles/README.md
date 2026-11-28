---
date: 2026-11-26
tags: [tech]
type: tech-tool-study
status: draft
---

# Robert C. Martin의 소프트웨어 설계 철학과 실무 적용

> **한 줄 정의**: Robert C. Martin(Uncle Bob)은 Clean Code, SOLID, Clean Architecture, TDD를 중심으로 소프트웨어의 변경 용이성과 개발자의 전문성을 강조해 온 소프트웨어 개발자이자 저자다.

## Overview

이 study는 특정 도구의 설치법이 아니라 소프트웨어 설계 철학을 코드와 변경 실험으로 학습하는 tool-study다. 핵심 질문은 **어떤 변경이 어디까지 전파되며, 얼마나 안전하게 검증할 수 있는가?**다.

| 범위 | 개념 | 학습 목표 |
|---|---|---|
| 코드 | Clean Code | 이름·책임·제어 흐름의 이해 비용 낮추기 |
| 모듈 | SOLID | 변경 이유, 행동 계약, 의존성 판단하기 |
| 시스템 | Clean Architecture | business policy를 외부 기술에서 보호하기 |
| 과정 | TDD, refactoring | 짧은 feedback으로 행동을 유지하며 개선하기 |
| 태도 | Professionalism | 품질과 검증을 개발자의 책임으로 다루기 |

수집 자료가 없어 제공 dossier의 개념 분석을 정리했다. 인용·최신 동향·실증적 효과는 검증하지 않았으며 **확인 필요**다.

## Learning Path

- [ ] [[tech/devtools/robert-martin-software-principles/01-overview|Overview]] — What/Why와 핵심 개념을 정리한다.
- [ ] [[tech/devtools/robert-martin-software-principles/02-ecosystem|Ecosystem 비교]] — 대안의 관심사와 적용 비용을 비교한다.
- [ ] [[tech/devtools/robert-martin-software-principles/04-learning/01-getting-started|시작하기]] — 단순 주문 프로그램에서 변경 비용을 기록한다.
- [ ] [[tech/devtools/robert-martin-software-principles/04-learning/02-deep-dive|심화 학습]] — dependency inversion과 test boundary를 실습한다.
- [ ] [[tech/devtools/robert-martin-software-principles/05-projects|Projects]] — 주문·환불 또는 기존 service에 적용한다.
- [ ] [[tech/devtools/robert-martin-software-principles/03-references|References]] — 자료 검증 상태와 후속 조사 항목을 확인한다.
- [ ] [[tech/devtools/robert-martin-software-principles/cheatsheet|Cheatsheet]] — 설계 검토 질문으로 복습한다.

## When To Use

- 장기간 유지보수하며 business rule과 외부 기술의 변경 주기가 다를 때.
- 정책 변경이 무관한 모듈로 전파되거나 테스트에 database·network 준비가 항상 필요할 때.
- 기존 service를 작은 단계로 refactoring하고 변경 영향을 비교할 때.

## When Not To Use

- 일회성 script나 단순 CRUD에 관성적으로 모든 계층과 interface를 적용하려 할 때.
- 제품 탐색 중 경계가 아직 불명확하고 abstraction의 유지 비용이 더 클 때.
- 지연시간에 민감한 시스템에서 측정 없이 변환·간접 호출을 늘리려 할 때.

원칙 자체를 배제한다는 뜻은 아니다. 현재 변경 패턴에 도움이 되는 만큼 적용한다.

## Related Notes

- [[MOCs/Index]]
- [[MOCs/Devtools]]
- [[tech/devtools/robert-martin-software-principles/01-overview|설계 철학 개요]] — 관련 tech 개념 노트.
- [[tech/devtools/robert-martin-software-principles/02-ecosystem|설계 접근 비교]] — Hexagonal Architecture, DDD, Vertical Slice와의 관계.

## Sources

- 근거: 사용자 제공 dossier(공개 URL 미제공), 기존 지식에 기반한 개념 분석.
- 출처 URL: 제공된 URL 없음. 웹 검색 및 URL 열기를 수행하지 않았으며 URL을 임의로 생성하지 않았다.
- 직접 인용, 최신 동향, 정량적 생산성 효과, 프로젝트별 적용 성과는 검증하지 않았다. 해당 주장은 **확인 필요**다.
