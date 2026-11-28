---
date: 2026-11-25
tags: [tech]
type: tech-tool-study
status: draft
---

# Deep Dive — 근거 검증과 테스트 검출력

## 처리 구조

```text
Git repository / 비교 revision
  → 두 버전의 코드 비교로 변경 식별
  → Agent: business flow·변경 의미·테스트·위험 해석
  → 각 step에 코드 줄 인용 첨부
  → CLI: frozen snapshot과 인용 대조
       + 제한적인 verdict 검증
       + Python parsing으로 누락 경로 점검
  → view.html / summary.md
```

변경 목록은 Genesis가 두 버전의 코드를 비교해 찾는다. 변경 의미, test verdict, 위험 설명은 agent의 해석이다. 모든 step의 인용은 frozen snapshot과 대조하며 하나라도 맞지 않으면 전체 설명을 거부하고 agent가 재시도한다. 이는 잘못 옮긴 코드나 존재하지 않는 코드를 걸러내지만 인용의 의미 해석까지 증명하지 않는다.

## CLI가 verdict를 거부하는 제한적 조건

- `covered`인데 assertion이 있는 인용 테스트가 없는 경우.
- Python에서 테스트가 변경 함수를 직접 호출하는데 `not reached`라고 한 경우.

다른 언어의 인용 테스트에 assertion이 있는지는 agent 판단에 의존한다. Assertion 존재와 변경 오류 검출력도 별개다. `covered`는 안전 인증이 아니라 검증 근거를 확인해야 하는 판정이다.

## 언어별 분석 경계

자료에는 Python·TypeScript·JavaScript·Go·Java·Rust 등 일반적인 여러 언어 지원이 설명돼 있다. Python은 직접 parsing해 agent가 빠뜨린 branch를 `partial`로 표시할 수 있다. 다른 언어는 agent의 코드 읽기와 source 인용 검증을 사용하지만 같은 누락 경로 표시를 기대할 수 없다.

`map` 화면의 상단 “Partial” 표시와 달리 `review` 화면은 해당 표시가 없으므로 `summary.md`를 읽어야 한다.

## Assertion을 읽는 실습

아래는 학습용 의사코드이며 저장소의 실제 테스트 인용이 아니다.

```python
# 실행 도달만 확인할 수 있는 약한 예
result = checkout(cart)
assert result is not None

# 배송 기준 변경을 검증하려는 경계값 예
assert shipping_fee(subtotal=34.99) > 0
assert shipping_fee(subtotal=35.00) == 0
assert shipping_fee(subtotal=35.01) == 0
```

첫 assertion은 무료배송 기준이 잘못 바뀌어도 통과할 수 있다. 두 번째 묶음은 특정 가격 정책을 가정한 경계값 예시다. 실제 정책과 fixture가 맞는지 확인하고 실행해야 검증 의미가 생긴다.

| 리뷰 질문 | 확인할 근거 |
|---|---|
| 변경 함수까지 도달하는가? | 호출 경로, 테스트 setup |
| 오류가 나면 테스트가 실패하는가? | 해당 동작을 관찰하는 assertion |
| 빠진 경우가 있는가? | timeout, retry, 경계값, 동시성 |
| 근거를 읽을 수 있는가? | 외부 fixture·package이면 `unknown` 고려 |

## 실습 기록

- [ ] Payment retry가 같은 요청을 두 번 결제할 수 있는지 코드로 대조.
- [ ] 마지막 재고를 둘이 구매하는 상황을 assertion이 검증하는지 확인.
- [ ] 각 위험에 반대 근거도 찾아 false alarm 여부 판단.
- [ ] 읽을 수 없는 근거와 미검증 동작을 구분해 기록.

## 연결

[[tech/devtools/genesis-agent-change-map/05-projects|프로젝트 실습]] · [[tech/devtools/genesis-agent-change-map/01-overview|네 단계 판정]] · [[tech/devtools/genesis-agent-change-map/README|학습 경로]]

## Sources

- https://github.com/GenesisAgentInfra/genesis — 제공된 dossier의 GitHub 수집 본문 근거.
- https://raw.githubusercontent.com/GenesisAgentInfra/genesis/main/docs/install.md — 본문에서 안내한 설치 가이드. 내용은 별도 열람하지 않음.
