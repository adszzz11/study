---
date: 2026-11-26
tags: [tech]
type: tech-tool-study
status: draft
---

# 시작하기 — 작은 할인 계산으로 TDD 체험

> **근거 범위:** 제공된 dossier는 수집 자료 없이 일반 지식으로 작성된 잠정 정리다. 인물의 기여·저술·개념의 정확한 표현은 확인 필요하다. 해석과 실습 제안은 Kent Beck의 직접적인 발언이나 권고가 아니다.

## 준비와 규칙

Python 3와 표준 라이브러리 unittest를 사용한다. 아래 파일은 학습자가 별도 실습 디렉터리에 만드는 예시이며 vault에 추가할 파일 목록은 아니다.

- 입력은 0 이상의 정수 금액, 할인율은 0~100 사이 정수로 제한한다.
- 할인액은 정수 나눗셈으로 버리고, 최종 금액을 반환한다.
- 범위 밖 정수는 ValueError로 처리한다. 정수 외 타입 검증은 이번 실습 범위에서 제외한다.

## Red → Green

먼저 `test_discount.py`만 작성한다.

```python
import unittest
from discount import final_price

class DiscountTest(unittest.TestCase):
    def test_ten_percent(self):
        self.assertEqual(final_price(1000, 10), 900)
```

```sh
python3 -m unittest -v
```

처음 모듈이 없으면 import 오류가 발생한다. 빈 `discount.py`에 `def final_price(amount, percent): return amount`를 추가하고 다시 실행해 **900 대신 1000을 반환하는 assertion 실패**를 확인한다. 환경 오류와 동작 실패를 구분한다.

이후 다음 최소 구현으로 정상 사례를 통과시킨다.

```python
def final_price(amount, percent):
    return amount - amount * percent // 100
```

## 경계값을 한 번에 하나씩 추가

| 입력 | 기대 결과 | 목적 |
|---|---|---|
| (0, 10) | 0 | 금액 하한 |
| (1000, 0) | 1000 | 할인 없음 |
| (1000, 100) | 0 | 전액 할인 |
| (999, 10) | 900 | 할인액 소수 버림 |
| (-1, 10) | ValueError | 잘못된 금액 |
| (1000, 101) | ValueError | 할인율 상한 |
| (1000, -1) | ValueError | 할인율 하한 |

예외 사례는 `with self.assertRaises(ValueError):`로 작성한다. 실패를 본 다음 구현에 다음 검증을 추가한다.

```python
if amount < 0 or not 0 <= percent <= 100:
    raise ValueError("amount or percent out of range")
```

## Refactor와 요구 변경

- Green 상태에서 할인액을 `discount_amount` 변수로 추출하고 다시 테스트한다.
- 새 요구로 할인액 상한 200을 추가한다. `(5000, 10)`의 결과가 4800이 되는 실패 테스트부터 시작한다.
- 새 요구가 생기기 전에 만든 abstraction이 도움이 되었는지 기록한다.

완료 기준: 의도한 assertion 실패, 전체 테스트 통과, 동작을 유지한 구조 변경을 각각 설명할 수 있다. 테스트 수보다 피드백이 다음 결정을 어떻게 바꾸었는지 적는다.

## 다음 학습

[[tech/devtools/kent-beck-practices/04-learning/02-deep-dive|외부 의존성과 팀 피드백]] · [[tech/devtools/kent-beck-practices/README|학습 경로]]

## Sources

- 제공된 dossier: URL 없음. 일반 지식 기반 잠정 정리이며 인용 가능한 수집 자료는 제공되지 않았다.
- 확인할 자료 후보: https://www.kentbeck.com/ — 인물·저술 확인용. 이 노트 작성 시 원문 미검증.
- 확인할 자료 후보: https://martinfowler.com/bliki/TestDrivenDevelopment.html — TDD 개념 확인용. 이 노트 작성 시 원문 미검증.
- 확인할 자료 후보: https://refactoring.com/ — Refactoring 개념 확인용. 이 노트 작성 시 원문 미검증.
