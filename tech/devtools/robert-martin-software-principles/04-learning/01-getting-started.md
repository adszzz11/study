---
date: 2026-11-26
tags: [tech]
type: tech-tool-study
status: draft
---

# 시작하기: 작은 주문 프로그램

## 목표와 준비

익숙한 언어와 test runner로 시작한다. 필수 framework나 설치 패키지는 없다. 정수 단위 금액을 쓰는 작은 주문 프로그램에서 변경 전후를 관찰한다.

## 실습 순서

1. 주문 합계, 할인, 메모리 저장 기능을 단순하게 구현한다. 처음부터 interface를 늘리지 않는다.
2. 정상 주문과 잘못된 수량에 대한 행동 테스트를 작성한다.
3. 할인 정책 추가, 저장소 교체, HTTP 외 CLI 실행을 한 번에 하나씩 시도한다.
4. business rule까지 영향이 전파되는 위치를 기록한다.
5. 가격 계산을 I/O에서 분리하고, 실제 교체 필요가 드러난 저장 경계에만 계약을 둔다.
6. 같은 변경을 다시 수행하고 수정 범위와 읽기 흐름을 비교한다.

```python
# 최소 계산 예시. 실제 통화의 반올림·세금 정책은 별도 정의한다.
def total(items, discount=0):
    if discount < 0:
        raise ValueError("negative discount")
    if any(price < 0 or qty <= 0 for price, qty in items):
        raise ValueError("invalid item")
    return max(0, sum(price * qty for price, qty in items) - discount)

assert total([(1000, 2), (500, 1)], discount=300) == 2200
```

## 관찰 기록

| 시나리오 | 수정 파일 수 | 테스트 준비 비용 | 추가 코드량 | 읽기 흐름·정책 영향 |
|---|---|---|---|---|
| 할인 정책 추가 | 직접 기록 | 직접 기록 | 직접 기록 | 직접 기록 |
| 저장소 교체 | 직접 기록 | 직접 기록 | 직접 기록 | 직접 기록 |
| CLI 추가 | 직접 기록 | 직접 기록 | 직접 기록 | 직접 기록 |

## 완료 기준

- [ ] 계산을 database·network 연결 없이 실행할 수 있다.
- [ ] 추가한 abstraction을 구체적인 변경 시나리오로 설명할 수 있다.
- [ ] 분리가 오히려 복잡해진 부분도 기록했다.
- [ ] 한 지표로 설계 우열을 단정하지 않았다.

## Navigation

[[tech/devtools/robert-martin-software-principles/README|학습 경로로 돌아가기]]

## Sources

- 근거: 사용자 제공 dossier(공개 URL 미제공), 기존 지식에 기반한 개념 분석.
- 출처 URL: 제공된 URL 없음. 웹 검색 및 URL 열기를 수행하지 않았으며 URL을 임의로 생성하지 않았다.
- 직접 인용, 최신 동향, 정량적 생산성 효과, 프로젝트별 적용 성과는 검증하지 않았다. 해당 주장은 **확인 필요**다.
