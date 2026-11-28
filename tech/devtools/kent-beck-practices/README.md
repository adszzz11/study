---
date: 2026-11-26
tags: [tech]
type: tech-tool-study
status: draft
---

# Kent Beck — TDD·XP·작은 변경의 설계 철학

> **한 줄 정의**: Kent Beck은 TDD·XP·점진적 소프트웨어 설계와 밀접하게 연결되는 개발자이자 저자로 알려져 있다. 인물과 방법론의 정확한 관계는 **확인 필요**다.

## Overview

> **근거 범위:** 제공된 dossier는 수집 자료 없이 일반 지식으로 작성된 잠정 정리다. 인물의 기여·저술·개념의 정확한 표현은 확인 필요하다. 해석과 실습 제안은 Kent Beck의 직접적인 발언이나 권고가 아니다.

이 study는 제품 사용법 대신 **작은 변경 → 빠른 검증 → 구조 개선**을 개발 작업에 적용하는 법을 다룬다. 불확실한 요구와 설계를 처음부터 확정하기보다, 가정이 틀렸을 때 수정하기 쉬운 상태를 유지한다는 관점이다. 이는 본 문서의 해석이다.

- **TDD:** 구현 전에 기대 동작을 구체화하고 짧은 주기로 검증한다.
- **Refactoring:** 외부 동작을 유지하며 내부 구조를 개선한다.
- **XP:** 테스트·설계를 협업·통합·전달의 반복과 연결한다.
- **적용 구성:** 언어별 test framework, CI, version control, 필요한 integration test.
- **평가 기준:** 테스트 수보다 변경 안전성, 실패 진단 시간, 전달 대기 시간을 관찰한다.

## Learning Path

- [ ] [[tech/devtools/kent-beck-practices/01-overview|Overview]] — What/Why와 핵심 작업 구조 이해
- [ ] [[tech/devtools/kent-beck-practices/02-ecosystem|Ecosystem]] — 접근별로 줄이는 불확실성 비교
- [ ] [[tech/devtools/kent-beck-practices/03-references|References]] — 근거의 한계와 확인할 자료 정리
- [ ] [[tech/devtools/kent-beck-practices/04-learning/01-getting-started|시작하기]] — 작은 순수 함수로 Red–Green–Refactor 실습
- [ ] [[tech/devtools/kent-beck-practices/04-learning/02-deep-dive|심화 학습]] — 의존성·설계·팀 피드백 탐색
- [ ] [[tech/devtools/kent-beck-practices/05-projects|Projects]] — 실제 변경과 팀 병목에 적용
- [ ] [[tech/devtools/kent-beck-practices/cheatsheet|Cheatsheet]] — 작업 중 판단 기준 재확인

## When To Use

- 정책 로직의 경계 조건을 작은 사례로 구체화할 때
- Legacy 코드에 보호 테스트를 추가하고 변경 범위를 줄일 때
- 테스트·통합·review 대기의 병목을 함께 개선할 때

## When Not To Use

- 테스트 통과만으로 보안·성능·운영 안정성을 보증하려는 경우
- 공개 API, 데이터 migration, 보안 경계의 설계 검토를 대체하려는 경우
- 실험 목적이 불분명한 일회성 spike에 엄격한 절차만 강제하려는 경우: 먼저 학습 목표와 폐기 기준을 정한다.

## Related Notes

- [[MOCs/Index]]
- [[MOCs/Devtools]]
- 관련 tech 주제: Refactoring, Continuous Integration, Property-based Testing. 현재 빈 작업 폴더에서는 기존 노트 경로를 확인할 수 없어 링크하지 않았다.
- [[tech/devtools/kent-beck-practices/02-ecosystem|관련 개발 접근 비교]]

## Sources

- 제공된 dossier: URL 없음. 일반 지식 기반 잠정 정리이며 인용 가능한 수집 자료는 제공되지 않았다.
- 확인할 자료 후보: https://www.kentbeck.com/ — 인물·저술 확인용. 이 노트 작성 시 원문 미검증.
- 확인할 자료 후보: https://martinfowler.com/bliki/TestDrivenDevelopment.html — TDD 개념 확인용. 이 노트 작성 시 원문 미검증.
- 확인할 자료 후보: https://refactoring.com/ — Refactoring 개념 확인용. 이 노트 작성 시 원문 미검증.
