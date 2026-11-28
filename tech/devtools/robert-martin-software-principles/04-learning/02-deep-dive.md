---
date: 2026-11-26
tags: [tech]
type: tech-tool-study
status: draft
---

# 심화: 의존성 방향과 검증 경계

## Runtime과 source dependency 구분

```text
Runtime call:
Controller -> CreateOrder -> SqlOrderRepository -> Database

Source dependency:
Controller -> CreateOrder -> OrderRepository (내부 계약)
SqlOrderRepository -> OrderRepository (내부 계약)
Composition root -> CreateOrder + SqlOrderRepository (연결)
```

내부 계약은 Use Case가 필요로 하는 최소 기능을 표현한다. 외부 adapter가 이를 구현하고 composition root에서 연결한다. Use Case의 입력·출력에 ORM model이나 HTTP request type이 노출되는지도 확인한다.

## TDD 실습: 취소된 주문은 결제할 수 없다

1. **Red:** 취소된 주문의 결제 요청이 명시적인 오류 결과를 내는 테스트를 쓴다.
2. **Green:** 상태를 검사하는 최소 구현을 추가한다.
3. **Refactor:** 상태 전이와 결제 I/O 책임을 정리하고 같은 테스트를 실행한다.
4. 정상 주문의 성공과 결제 adapter의 실패 행동도 추가한다.

행동 예시:

```text
Given: status = CANCELLED
When: pay(order)
Then: OrderNotPayable 오류가 반환되고 결제는 발생하지 않는다
```

실제 결제가 발생하지 않는 것은 business requirement다. 이 경계의 관찰은 유용하지만 내부 helper 호출 순서까지 테스트에 고정하지 않는다.

## Test boundary

| 테스트 | 확인 대상 | 보장하지 못하는 것 |
|---|---|---|
| Domain unit | 상태 전이, 금액 invariant | SQL·network |
| Use Case + fake adapter | 흐름과 오류 결과 | 실제 adapter 동작 |
| Repository integration | SQL, mapping, transaction 동작 | 외부 결제 서비스 |
| Payment integration | 요청·응답 mapping, 실패 처리 | 전체 배포 환경 |
| Wiring / end-to-end | 실제 연결과 주요 사용자 흐름 | 모든 실패 조합 |

## 실패 상황을 설계에 포함하기

- 결제 성공 후 저장 실패 시 재시도·보상·상태 복구 전략을 정의한다.
- 중복 결제 요청에는 idempotency 요구와 키의 수명을 명시한다.
- transaction 범위와 외부 API 호출의 경계를 구분한다.
- interface만으로 원자성이 생기지 않는다. 실패를 주입해 실제 복구 행동을 검증한다.

이 항목들은 dossier의 실패 처리 문제를 구체화한 실습 제안이며 검증된 운영 처방이 아니다.

## 완료 기준

내부 정책의 import를 검사해 framework 의존이 없는지 확인한다. 두 저장 adapter에 같은 행동 계약 테스트를 적용하고, 대체 시 반환값·오류·정렬 등 호출자 가정이 유지되는지 검증한다.

## Navigation

[[tech/devtools/robert-martin-software-principles/README|학습 경로로 돌아가기]]

## Sources

- 근거: 사용자 제공 dossier(공개 URL 미제공), 기존 지식에 기반한 개념 분석.
- 출처 URL: 제공된 URL 없음. 웹 검색 및 URL 열기를 수행하지 않았으며 URL을 임의로 생성하지 않았다.
- 직접 인용, 최신 동향, 정량적 생산성 효과, 프로젝트별 적용 성과는 검증하지 않았다. 해당 주장은 **확인 필요**다.
