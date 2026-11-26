---
date: 2026-11-26
tags: [tech]
type: tech-tool-study
status: draft
---

# Overview: What / Why / 특징

## What

Martin의 철학은 읽기 쉬운 코드, 변경 이유에 따른 책임 분리, 정책을 향하는 의존성, 짧은 검증 feedback을 연결한다. “작은 함수와 많은 interface”만으로 요약할 수 없다.

## Why

기능이 늘면서 책임과 의존성이 뒤엉키면 작은 수정도 여러 모듈에 영향을 준다. 변경 전에 시스템 전체를 이해해야 하므로 불확실성이 커진다. 설계의 목적은 이 영향을 제한하고 검증 가능하게 만드는 것이다. 모든 프로젝트에서 비용이 줄어든다는 정량적 주장은 **확인 필요**다.

## Clean Code

- 의도가 드러나는 이름, 집중된 책임, 명확한 제어 흐름을 지향한다.
- business rule과 I/O를 구분하고 함께 바뀌는 코드는 가까이 둔다.
- 작은 함수는 이해를 돕는 수단이다. 파일 이동과 간접 호출만 늘어난다면 다시 응집성을 검토한다.

## SOLID

Martin은 SOLID를 설명하고 대중화한 주요 인물이다. 다섯 원칙을 모두 단독 발명했다고 보는 것은 부정확하며, 개별 기원과 명칭 형성 과정은 **확인 필요**다.

| 원칙 | 의미 | 검토 질문 |
|---|---|---|
| SRP — Single Responsibility Principle | 서로 다른 변경 이유 분리 | 다른 이해관계자의 요구가 같은 모듈을 바꾸는가? |
| OCP — Open/Closed Principle | 예상되는 변화에 대한 확장 지점 | 반복되는 분기가 안정된 확장 지점을 요구하는가? |
| LSP — Liskov Substitution Principle | 하위 타입의 행동 계약 준수 | 대체 구현이 호출자의 가정을 깨는가? |
| ISP — Interface Segregation Principle | 쓰지 않는 기능에 대한 의존 축소 | client가 불필요한 메서드에 묶이는가? |
| DIP — Dependency Inversion Principle | 상위 정책을 구체 구현에서 분리 | business rule 실행에 특정 ORM이 필수인가? |

SRP는 클래스당 메서드 하나를 뜻하지 않는다. DIP도 모든 클래스에 interface를 만들라는 뜻이 아니다.

## Clean Architecture

**Dependency Rule:** source-code dependency는 외부 세부사항에서 내부 정책을 향한다.

| 영역 | 책임 | 예시 |
|---|---|---|
| Entities | 핵심 business rule | 주문 상태 전이, 가격 계산 |
| Use Cases | 애플리케이션 작업 흐름 | 주문 접수, 환불 처리 |
| Interface Adapters | 외부 표현과 내부 모델 변환 | controller, presenter, repository 구현 |
| Frameworks & Drivers | 실행 환경·외부 기술 | web framework, database, API client |

Use Case가 내부 저장 계약을 사용하고 외부 adapter가 이를 구현하면 실행 중에는 adapter를 호출하면서도 source dependency는 내부를 향할 수 있다. 네 개 폴더를 만들어도 내부가 ORM model이나 framework type을 import하면 경계가 약하다.

## TDD와 전문성

Red → Green → Refactor로 원하는 행동을 먼저 표현하고, 구현 후 행동을 유지하며 구조를 개선한다. 내부 호출 횟수보다 관찰 가능한 결과와 invariant를 검증한다. Unit test만으로 SQL, transaction, network, framework wiring을 보장하지 못하므로 integration test도 필요하다. 품질과 검증을 개발 책임의 일부로 다룬다.

## Navigation

[[tech/devtools/robert-martin-software-principles/README|학습 경로로 돌아가기]]

## Sources

- 근거: 사용자 제공 dossier(공개 URL 미제공), 기존 지식에 기반한 개념 분석.
- 출처 URL: 제공된 URL 없음. 웹 검색 및 URL 열기를 수행하지 않았으며 URL을 임의로 생성하지 않았다.
- 직접 인용, 최신 동향, 정량적 생산성 효과, 프로젝트별 적용 성과는 검증하지 않았다. 해당 주장은 **확인 필요**다.
