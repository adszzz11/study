---
date: 2026-11-29
tags: [tech]
type: tech-tool-study
status: draft
---

# CodeWiki — 코드베이스 지식화와 문서 탐색

> **한 줄 정의**: CodeWiki는 코드베이스의 구조·동작·설계 지식을 Wiki로 탐색하는 접근 또는 도구를 가리키는 명칭으로 해석할 수 있으며, 이 노트가 다루는 특정 제품의 정체는 **확인 필요**다.

## Overview

코드, 테스트, README, ADR, PR에 흩어진 정보를 연결해 “어디서 시작하고, 무엇에 의존하며, 왜 이렇게 구현했는가”를 이해하는 방법을 공부한다. 핵심은 문서량보다 **설명의 정확성·근거·변경 추적 가능성**이다.

이 노트는 제공된 dossier를 바탕으로 한 개념 분석이다. 운영 주체, 지원 언어, 가격, 라이선스, 실제 구현 스택은 확인되지 않았다. 아키텍처와 실습은 특정 제품의 기능 설명이 아닌 설계·평가 제안이다.

## Learning Path

- [ ] [[tech/devtools/codewiki-analysis/README|학습 진입점]] — 범위와 학습 순서 확인
- [ ] [[tech/devtools/codewiki-analysis/01-overview|Overview]] — 문제와 reference architecture 이해
- [ ] [[tech/devtools/codewiki-analysis/02-ecosystem|Ecosystem]] — 대안의 역할과 한계 비교
- [ ] [[tech/devtools/codewiki-analysis/03-references|References]] — 제품 식별과 출처의 증거 수준 확인
- [ ] [[tech/devtools/codewiki-analysis/04-learning/01-getting-started|시작하기]] — 고정 commit에서 수동 기준 답안 만들기
- [ ] [[tech/devtools/codewiki-analysis/04-learning/02-deep-dive|심화 학습]] — 검색 누락·변경 영향·권한 검증
- [ ] [[tech/devtools/codewiki-analysis/05-projects|Projects]] — 좁은 범위의 평가 프로젝트 수행
- [ ] [[tech/devtools/codewiki-analysis/cheatsheet|Cheatsheet]] — 검토 항목을 반복 적용

## When To Use

- 신규 개발자의 onboarding과 repository atlas를 만들 때.
- module 간 흐름을 파악하고 원본 코드까지 추적해야 할 때.
- 코드 설명의 근거와 최신성을 평가하는 체계를 설계할 때.

## When Not To Use

- 특정 CodeWiki의 설치법·가격·지원 언어에 대한 확정 정보가 필요할 때: 먼저 제품 식별이 필요하다.
- 운영 장애나 보안 판단을 생성된 설명만으로 확정하려 할 때: 코드·테스트·runtime 근거를 직접 확인한다.
- 원본 접근 권한과 파생 문서의 권한을 보존할 수 없을 때.

## Related Notes

- [[MOCs/Index]]
- [[MOCs/Devtools]]
- [[tech/devtools/codewiki-analysis/01-overview|코드 지식화의 구조·동작·설계 의도]]

## Sources

- 사용자 제공 dossier: 제품을 식별할 URL과 수집 자료 없음.
- 아래 URL은 일반 개념의 추가 참고자료이며, 특정 CodeWiki의 사양을 입증하지 않는다. 이번 작성에서는 웹 페이지를 열어 검증하지 않았다.
- Git revision 지정: https://git-scm.com/docs/gitrevisions
- Tree-sitter 소개: https://tree-sitter.github.io/tree-sitter/
- Retrieval-Augmented Generation 논문: https://arxiv.org/abs/2005.11401
- ADR 개념: https://adr.github.io/
