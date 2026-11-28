---
date: 2026-11-26
tags: [tech]
type: tech-tool-study
status: draft
---

# Lean 4 시작하기

> **근거 범위:** 제공된 dossier를 재구성한 노트다. 수집 출처가 없고 외부 검증을 수행하지 않았으므로 기술 설명·비교·적용 가능성은 **확인 필요**다. 현재 버전·지원 현황·성능·채택 규모는 판단하지 않는다.

## 실습 준비

설치 명령과 버전별 문법은 확인되지 않았다. 공식 설치 절차를 확인한 뒤 toolchain과 library 의존성을 기록하고, editor에서 goal과 오류를 볼 수 있는 상태를 만든다. 이 노트는 검증된 설치 안내가 아닌 권장 실습안이다.

## 1. 함수와 실행

아래 코드는 **실행·컴파일 검증을 하지 않은 학습 예시**다. 필요 import와 문법을 실제 환경에서 확인한다.

```lean
def twice (n : Nat) : Nat := n + n
#eval twice 3
```

- 자연수와 리스트를 다루는 재귀 함수를 작성한다.
- Pattern matching과 종료 조건을 살펴본다.
- 실행 결과 확인과 모든 입력에 대한 정확성 증명을 구분한다.

## 2. 같은 명제를 두 방식으로 증명

```lean
-- Term proof 예시 (미검증)
example (P : Prop) : P → P := fun h => h

-- Tactic proof 예시 (미검증)
example (P : Prop) : P → P := by
  intro h
  exact h
```

개념적으로 `intro h` 이후에는 가정 `h : P` 아래에서 goal `P`를 해결한다. `exact h`는 그 증거를 제공한다. 세부 동작은 **확인 필요**다.

## 3. 다음 연습

- [ ] `P ∧ Q`에서 `P`를 얻는 증명을 작성한다.
- [ ] 구체적인 witness를 제공해 existential proposition을 증명한다.
- [ ] 각 tactic 전후의 가정과 goal을 기록한다.
- [ ] 자연어 요구사항, 정리 문장, 증명 객체의 역할을 구별해 설명한다.

## 완료 기준

코드가 검사된다는 사실 외에, 명제가 무엇을 보장하는지와 무엇을 가정하는지 설명할 수 있어야 한다. 실습 결과와 toolchain을 기록하고 `sorry`가 남아 있는지 확인한다.

다음: [[tech/devtools/lean-four-formal-verification/04-learning/02-deep-dive|심화 학습]]

## Related Notes

- [[tech/devtools/lean-four-formal-verification/README|학습 진입점]]

## Sources

- 사용자 제공 Lean 4 dossier: 기존 지식 기반 분석이며 출처 URL은 제공되지 않았다.
- 외부 자료를 검색하거나 URL을 열지 않았다. 추정 URL은 기재하지 않는다. 공식 문서와 구현을 통한 후속 검증이 필요하다.
