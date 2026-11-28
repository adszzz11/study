---
date: 2026-11-26
tags: [tech]
type: tech-tool-study
status: draft
---

# Lean 4 Cheatsheet

> **근거 범위:** 제공된 dossier를 재구성한 노트다. 수집 출처가 없고 외부 검증을 수행하지 않았으므로 기술 설명·비교·적용 가능성은 **확인 필요**다. 현재 버전·지원 현황·성능·채택 규모는 판단하지 않는다.

## 개념 빠른 참조

| 표현·요소 | 읽는 방법 | 확인할 점 |
|---|---|---|
| `P → Q` | P의 증거에서 Q의 증거로 | 필요한 가정이 정확한가? |
| `P ∧ Q` | 두 증거를 함께 제공 | 두 성질을 모두 보였는가? |
| `∃ x, R x` | witness와 그 성질 | witness가 명세에 맞는가? |
| Dependent type | 값에 의존하는 type | 복잡도를 감수할 제약인가? |
| Elaboration | 생략 정보 추론과 term 구성 | 의도한 해석인가? |
| Kernel | 구성된 term 검사 | 추가 가정은 무엇인가? |

모든 기술 설명은 **확인 필요**다.

## 작은 증명 읽기

```lean
-- 미검증 예시
example (P : Prop) : P → P := by
  intro h
  exact h
```

| 수단 | 개념적 목적 |
|---|---|
| `intro` | 가정을 도입하거나 함수 인자를 받음 |
| `exact` | 현재 goal에 맞는 term 제공 |
| Rewriting | 등식을 이용해 표현 변경 |
| Simplification | 정의·정리를 이용해 표현 단순화 |
| Induction | 재귀 구조의 기저와 귀납 단계로 분해 |

Tactic의 정확한 문법·적용 조건은 환경에서 확인한다.

## 막혔을 때

1. 현재 goal과 가정을 자연어로 읽는다.
2. 정의를 계산할 문제인지 정리가 필요한 문제인지 구분한다.
3. 필요한 보조정리와 induction hypothesis의 형태를 비교한다.
4. 명제 일반화가 필요한지 살핀다.
5. 자동화 성공 뒤에도 정리 문장과 가정을 검토한다.

## 제출 전 점검

- [ ] `sorry` 등 미완성 증명을 확인했다.
- [ ] 사용한 axiom과 외부 가정을 기록했다.
- [ ] 실행 확인과 정확성 증명을 구분했다.
- [ ] 실제 요구사항보다 약한 정리를 증명하지 않았는지 검토했다.
- [ ] toolchain과 의존성을 기록했다.

## Related Notes

- [[tech/devtools/lean-four-formal-verification/README|학습 진입점]]

## Sources

- 사용자 제공 Lean 4 dossier: 기존 지식 기반 분석이며 출처 URL은 제공되지 않았다.
- 외부 자료를 검색하거나 URL을 열지 않았다. 추정 URL은 기재하지 않는다. 공식 문서와 구현을 통한 후속 검증이 필요하다.
