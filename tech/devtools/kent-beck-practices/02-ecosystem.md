---
date: 2026-11-26
tags: [tech]
type: tech-tool-study
status: draft
---

# Ecosystem — 관련 개발 접근 비교

> **근거 범위:** 제공된 dossier는 수집 자료 없이 일반 지식으로 작성된 잠정 정리다. 인물의 기여·저술·개념의 정확한 표현은 확인 필요하다. 해석과 실습 제안은 Kent Beck의 직접적인 발언이나 권고가 아니다.

## 비교 관점

인물이므로 제품 간 경쟁 대신 개발 접근을 비교한다. 아래 표는 일반적인 개념 비교이며 Beck 자신의 평가가 아니다.

| 접근 | 주된 관심 | TDD·XP와의 관계 | 주의점 |
|---|---|---|---|
| TDD | 구현·설계의 빠른 피드백 | 개인 개발의 짧은 반복 | 사례 밖의 문제는 별도 검증 |
| Test-after | 구현 후 정확성 검증 | 기존 코드의 보호를 보강하는 경로 | 구현 전 interface 탐색 효과는 적음 |
| BDD | 예시를 통한 공동 이해 | acceptance 기준과 해석 보완 | 문법·도구만으로 합의가 생기지 않음 |
| XP | 개발·협업·전달 실천 | TDD를 팀 맥락에 배치 | 일부 실천의 효과를 따로 평가 |
| Scrum | 계획·검토·적응 | 기술 실천과 함께 사용 가능 | 테스트·코드 품질 방식을 자체 해결하지 않음 |
| 사전 설계 중심 접근 | 구현 전 구조·제약 검토 | 되돌리기 어려운 결정 검토에 보완적 | 불확실한 부분의 조기 확정 주의 |
| Property-based Testing | 넓은 입력 공간의 성질 | 예시 기반 테스트 보완 | property·generator 설계 필요 |

## 선택 예시

- **요구가 모호함:** 이해관계자와 구체적인 예시·acceptance 기준을 합의한다.
- **정책 계산 오류:** 빠른 unit test와 경계값, 필요하면 property를 추가한다.
- **DB transaction의 불확실성:** 실제 저장소에서 integration test를 실행한다.
- **외부 API 호환성:** mock만 신뢰하지 않고 계약·실제 연동을 확인한다.
- **통합 대기:** CI와 변경 크기, review 흐름을 함께 관찰한다.

한 접근의 승패보다 **어떤 불확실성을 어떤 피드백으로 줄이는가**를 판단한다. [[tech/devtools/kent-beck-practices/04-learning/02-deep-dive|심화 학습]]과 [[tech/devtools/kent-beck-practices/05-projects|적용 프로젝트]]로 연결한다.

## Sources

- 제공된 dossier: URL 없음. 일반 지식 기반 잠정 정리이며 인용 가능한 수집 자료는 제공되지 않았다.
- 확인할 자료 후보: https://www.kentbeck.com/ — 인물·저술 확인용. 이 노트 작성 시 원문 미검증.
- 확인할 자료 후보: https://martinfowler.com/bliki/TestDrivenDevelopment.html — TDD 개념 확인용. 이 노트 작성 시 원문 미검증.
- 확인할 자료 후보: https://refactoring.com/ — Refactoring 개념 확인용. 이 노트 작성 시 원문 미검증.
