---
date: 2026-11-26
tags: [tech]
type: tech-tool-study
status: draft
---

# Ecosystem: 설계 접근 비교

이들은 직접 경쟁하는 제품이 아니라 관심사가 겹치거나 보완되는 설계 방식이다.

| 접근 | 주된 관심사 | Martin 철학과의 관계 | 적용 비용·주의점 |
|---|---|---|---|
| Clean Architecture | 정책 보호와 의존성 방향 | 시스템 설계 접근을 대표 | 계층과 변환 코드가 늘 수 있음 |
| Hexagonal Architecture | Ports & Adapters | 외부 기술에서 내부를 보호하는 목표 공유 | 모든 I/O에 복잡한 abstraction을 둘 필요는 없음 |
| Domain-Driven Design | domain model, 언어, 경계 | business rule 구체화에 보완적 | Clean Architecture가 domain modeling을 대신하지 않음 |
| Functional Core, Imperative Shell | 순수 계산과 side effect 분리 | business logic을 I/O에서 분리 | 함수·데이터로도 경계를 만들 수 있음 |
| Vertical Slice Architecture | 기능별 변경의 응집성 | 계층과 다른 조직화 기준 | slice 내부의 책임·의존성 판단은 여전히 필요 |
| 단순 layered CRUD | 적은 구조로 빠른 구현 | domain 복잡도가 낮을 때 실용적 | 복잡해지면 service·ORM에 책임 집중 가능 |

## 선택 기준

- 기능 하나를 바꿀 때 여러 계층에 같은 상용구 수정이 반복된다면 구조를 줄이거나 기능별 응집성을 검토한다.
- database나 framework 변경이 business rule까지 흔든다면 경계를 강화한다.
- 계산과 I/O 분리만으로 충분하다면 먼저 순수 함수를 추출한다.
- 복잡한 domain의 용어와 규칙이 불명확하다면 DDD 관점을 함께 학습한다.

예: 할인 계산은 순수 함수, 주문 접수는 Use Case, 저장은 adapter로 분리할 수 있다. 기능별 slice와 내부 의존성 규칙도 함께 사용할 수 있다. 명칭보다 실제 변경 비용으로 판단한다.

## Navigation

[[tech/devtools/robert-martin-software-principles/README|학습 경로로 돌아가기]]

## Sources

- 근거: 사용자 제공 dossier(공개 URL 미제공), 기존 지식에 기반한 개념 분석.
- 출처 URL: 제공된 URL 없음. 웹 검색 및 URL 열기를 수행하지 않았으며 URL을 임의로 생성하지 않았다.
- 직접 인용, 최신 동향, 정량적 생산성 효과, 프로젝트별 적용 성과는 검증하지 않았다. 해당 주장은 **확인 필요**다.
