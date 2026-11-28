---
date: 2026-11-25
tags: [tech]
type: tech-tool-study
status: draft
---

# Genesis Overview

## What / Why

Genesis는 coding agent 리뷰를 business flow와 코드 인용으로 구조화하는 도구다. 단순 diff는 바뀐 줄을 알려주지만, 리뷰어는 사용자 행동의 변화, 영향을 받는 entry point, 테스트의 실제 검출력을 알아야 한다.

Checkout 테스트가 재고 코드를 통과하더라도 마지막 재고를 두 번 구매하는 상황을 검증하지 않는다면 재고 경쟁을 방어한다고 할 수 없다. 이것이 execution coverage와 behavior verification의 차이다.

## 주요 특징

| 기능 | 역할 | 경계 |
|---|---|---|
| `map` | 현재 business flow 표현 | 완전한 아키텍처 명세라는 보장은 없음 |
| `review <revision>` | 변경과 테스트 검증 수준 표시 | 의미·위험 설명은 agent 해석 |
| 코드 줄 인용 | 설명을 실제 코드에 연결 | 인용 일치가 의미 정확성을 보장하지 않음 |
| frozen snapshot 대조 | 잘못된 인용이 있으면 전체 설명 거부·재시도 | 실행 검증을 대체하지 않음 |
| Python parsing | 누락 branch가 있으면 `partial` 표시 가능 | 다른 언어에 같은 보장 없음 |

Flow step을 클릭하면 변경, test verdict와 설명, 관련 코드를 확인할 수 있다. CLI는 model 호출·외부 데이터 전송·프로젝트 코드 실행·테스트 실행을 하지 않으며 risk rule engine도 없다. 함께 쓰는 Claude Code·Codex의 model 호출과 데이터 처리까지 local이라는 뜻은 아니다.

## 네 단계의 테스트 판정

| 화면 | summary 값 | 의미 | 예시 |
|---|---|---|---|
| 🔴 No coverage found | `not reached` | 변경에 도달하는 테스트를 찾지 못함 | Payment timeout 유발 테스트 없음 |
| 🟡 Behavior not checked | `reached only` | 코드는 실행하지만 해당 동작 미검증 | 마지막 재고 두 번 구매 미검증 |
| ⚪ Coverage unclear | `unknown` | 읽은 코드만으로 판단 불가 | 테스트 case가 외부 package에 있음 |
| ✅ Behavior checked | `covered` | 변경 동작의 검증 근거 존재 | 배송 기준 $34.99·$35.00·$35.01 검증 |

## 프로젝트 측 benchmark

5개 open-source Python 프로젝트의 최근 commit 10개를 사용했다. 각 agent는 commit마다 단독 3회, Genesis와 함께 3회 답했다. Reference answer는 실행 전 코드와 테스트를 바탕으로 작성했고, 답변은 사람이 아닌 language-model reader가 평가했다.

| 지표 | Claude Code | + Genesis | Codex | + Genesis |
|---|---:|---:|---:|---:|
| 올바른 test-coverage verdict | 79% | 88% | 76% | 80% |
| 실행되지만 오류를 잡지 못하는 변경 식별 | 8% | 38% | 4% | 23% |
| 위 변경을 잘못 covered로 판정 | 47% | 34% | 43% | 30% |
| 영향을 받는 entry point 식별 | 32% | 47% | 15% | 24% |
| 제시한 entry point의 정확성 | 67% | 68% | 71% | 54% |
| 제기한 위험 중 실제 위험 비율 | 44% | 64% | 54% | 72% |
| 리뷰당 false alarm 수 | 2.1 | 0.7 | 1.4 | 0.5 |

검출력이 부족한 테스트의 식별 증가와 false alarm 감소가 중요한 신호다. 리뷰당 실제 위험 수는 Claude Code 2.9→2.8, Codex 2.4→2.4로 거의 같아, 위험을 더 많이 발견했다기보다 코드로 배제 가능한 경고를 줄인 것으로 해석할 수 있다.

다만 모두 covered라고 답해도 정확도가 82%인 표본이다. Genesis를 써도 검출력이 부족한 변경의 약 3분의 1을 covered로 오판했다. Codex는 entry point를 더 많이 찾았지만 정확성은 71%→54%로 하락했다. Python commit 10개로 다른 언어·대규모 저장소·실제 장애 예방 효과를 일반화할 수 없다. 독립적인 사람 평가와 통계적 유의성은 확인되지 않았다.

## 다음 학습

[[tech/devtools/genesis-agent-change-map/04-learning/02-deep-dive|인용과 verdict의 검증 경계]] · [[tech/devtools/genesis-agent-change-map/README|학습 경로]]

## Sources

- https://github.com/GenesisAgentInfra/genesis — 제공된 dossier의 GitHub 수집 본문 근거.
- https://raw.githubusercontent.com/GenesisAgentInfra/genesis/main/docs/install.md — 본문에서 안내한 설치 가이드. 내용은 별도 열람하지 않음.
