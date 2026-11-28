---
date: 2026-11-26
tags: [tech]
type: tech-tool-study
status: draft
---

# Lean 4의 증명 시스템과 프로그래밍 아키텍처

> **한 줄 정의**: Lean 4는 dependent type theory를 바탕으로 수학적 명제와 프로그램의 성질을 형식화하고 증명을 기계적으로 검사하는 interactive theorem prover이자 함수형 프로그래밍 언어다. **[확인 필요]**

## Overview

> **근거 범위:** 제공된 dossier를 재구성한 노트다. 수집 출처가 없고 외부 검증을 수행하지 않았으므로 기술 설명·비교·적용 가능성은 **확인 필요**다. 현재 버전·지원 현황·성능·채택 규모는 판단하지 않는다.

테스트는 선택한 입력의 동작을 확인한다. Formal verification은 명시한 가정과 모델 아래에서 성질이 성립함을 증명하는 것을 목표로 한다. Lean 4 학습의 핵심은 자연어 요구사항을 정의·명세·증명으로 바꾸고, 검사 결과가 보장하는 범위를 이해하는 것이다. **[확인 필요]**

개념적 흐름은 `정의·정리·tactic → elaboration 및 증명 구성 → kernel 검사`다. 함수 실행, type checking, 정확성 정리의 증명, 실제 배포 환경의 가정 충족은 각각 구분해야 한다. **[확인 필요]**

## Learning Path

- [ ] [[tech/devtools/lean-four-formal-verification/01-overview|Overview]] — 명제·type·증명과 검사 구조 이해
- [ ] [[tech/devtools/lean-four-formal-verification/02-ecosystem|Ecosystem 비교]] — 대안과 library 선택 기준 정리
- [ ] [[tech/devtools/lean-four-formal-verification/03-references|References]] — 근거 공백과 검증할 자료 목록 확인
- [ ] [[tech/devtools/lean-four-formal-verification/04-learning/01-getting-started|시작하기]] — 함수, term proof, tactic proof 실습
- [ ] [[tech/devtools/lean-four-formal-verification/04-learning/02-deep-dive|심화 학습]] — rewriting, induction, 신뢰 범위 점검
- [ ] [[tech/devtools/lean-four-formal-verification/05-projects|Projects]] — 작은 명세로 검증 프로젝트 수행
- [ ] [[tech/devtools/lean-four-formal-verification/cheatsheet|Cheatsheet]] — goal과 가정 중심의 복습

## When To Use

- 수학 증명의 전제와 보조정리 의존 관계를 명시적으로 관리하고 싶을 때.
- 순수 함수의 입력 전반에 적용되는 성질이나 자료구조 invariant를 명세할 때.
- AI가 만든 증명 후보를 기계적으로 검사하는 실험을 할 때.
- 위 적용 가능성은 모두 **확인 필요**이며, 필요한 library와 유지보수 비용을 먼저 검토한다.

## When Not To Use

- 요구사항 자체가 불명확하고 형식화 범위를 합의하지 못했을 때.
- 빠른 반례 탐색만으로 목적을 달성할 수 있고 증명 비용을 감당하기 어려울 때.
- 외부 I/O와 운영 환경까지 자동으로 정확성이 보장된다고 기대할 때.

## Related Notes

- [[MOCs/Index]]
- [[MOCs/Devtools]]
- 관련 tech 주제: Property-based testing — 기존 노트의 존재와 경로를 확인할 수 없어 링크를 만들지 않았다.

## Sources

- 사용자 제공 Lean 4 dossier: 기존 지식 기반 분석이며 출처 URL은 제공되지 않았다.
- 외부 자료를 검색하거나 URL을 열지 않았다. 추정 URL은 기재하지 않는다. 공식 문서와 구현을 통한 후속 검증이 필요하다.
