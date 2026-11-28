---
date: 2026-11-25
tags: [tech]
type: tech-tool-study
status: draft
---

# Projects — 변경 영향과 테스트 공백 실습

아래는 dossier의 checkout 예시를 응용한 학습 과제다. 실제 repository 분석·테스트 실행 결과를 주장하지 않는다.

## 1. Checkout 영향 지도

**목표:** Guest checkout 변경과 함께 바뀌는 정책을 사용자 flow로 설명한다.

1. 학습용 Git repository에서 guest checkout 변경과 비교 revision을 준비한다.
2. `map`과 `review`를 생성하고 checkout entry point를 실제 코드와 대조한다.
3. 다음 표를 코드 줄 인용·test verdict로 채운다.

| 변경 후보 | 위험 가설 | 확인할 테스트 |
|---|---|---|
| Payment retry | 중복 결제 | timeout 후 재시도·중복 요청 |
| 재고 확보 시점 | 마지막 재고 중복 판매 | 동시 구매·재고 수량 assertion |
| 무료배송 기준 | 가격 정책 변화 | $34.99·$35.00·$35.01 경계값 |

**완료 기준:** 각 가설에 코드 근거, 반대 근거, verdict, 남은 불확실성이 있다. `summary.md`의 partial 여부를 확인하고 추가할 테스트 한 개를 구체화한다.

## 2. 테스트 검출력 개선

**목표:** `reached only`와 `covered`의 차이를 검증한다.

- 코드는 실행하지만 동작을 확인하지 않는 테스트를 선택한다.
- 바뀐 동작을 관찰하는 assertion을 추가한다.
- 학습용 변경으로 해당 동작을 의도적으로 깨뜨려 테스트가 실패하는지 확인하고 원복한다.
- 테스트 실행 결과와 Genesis 판정을 따로 기록한다. 판정이 일치하지 않으면 인용·fixture·assertion을 다시 읽는다.

**완료 기준:** 정상 동작의 통과와 의도적 오류의 실패를 모두 기록한다. 이는 학습자가 수행하는 검증이며 Genesis가 테스트를 실행한다는 뜻은 아니다.

## 3. Agent 단독 리뷰와 비교

같은 작은 변경에 agent 단독 리뷰와 Genesis 보조 리뷰를 적용한다. Entry point의 정답 목록과 위험 근거를 먼저 기록한 뒤 비교한다.

| 기록 항목 | 비교 목적 |
|---|---|
| 올바른 entry point / 제시한 entry point | 정확성 |
| 찾은 entry point / 확인된 전체 entry point | 누락 정도 |
| 근거가 확인된 위험 / 전체 경고 | False alarm 점검 |
| 검출력 부족 테스트 식별 | 단순 coverage 판정과 구분 |

**완료 기준:** 사람이 확인한 근거로 차이를 설명하고 소규모 실습을 일반적인 성능 주장으로 확대하지 않는다.

## 연결

[[tech/devtools/genesis-agent-change-map/04-learning/02-deep-dive|검증 개념]] · [[tech/devtools/genesis-agent-change-map/03-references|근거 범위]] · [[tech/devtools/genesis-agent-change-map/README|학습 경로]]

## Sources

- https://github.com/GenesisAgentInfra/genesis — 제공된 dossier의 GitHub 수집 본문 근거.
- https://raw.githubusercontent.com/GenesisAgentInfra/genesis/main/docs/install.md — 본문에서 안내한 설치 가이드. 내용은 별도 열람하지 않음.
