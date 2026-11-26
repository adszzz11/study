---
date: 2026-11-26
tags: [tech]
type: tech-tool-study
status: draft
---

# Lean 4 개요: What / Why / Architecture

> **근거 범위:** 제공된 dossier를 재구성한 노트다. 수집 출처가 없고 외부 검증을 수행하지 않았으므로 기술 설명·비교·적용 가능성은 **확인 필요**다. 현재 버전·지원 현황·성능·채택 규모는 판단하지 않는다.

## What

Lean 4는 interactive theorem prover와 함수형 프로그래밍 언어를 함께 이해하는 것이 출발점이다. 명제와 프로그램의 성질을 언어 안에서 표현하고 증명 객체를 검사하는 모델이다. **[확인 필요]**

## Why

“자명하다”, “이 상태는 발생하지 않는다” 같은 설명을 명시적인 가정과 추론으로 바꾸면 생략된 조건을 드러낼 수 있다. 대신 형식화와 보조정리 작성 비용이 발생한다. **증명의 타당성과 명세의 적절성은 별도 문제**다.

## 핵심 특징

| 개념 | 이해할 내용 | 비용·주의점 |
|---|---|---|
| Propositions as Types | 명제는 type, 증명은 그 type의 term | 의도한 명제를 정확히 표현해야 함 |
| Dependent types | type이 값에 의존 | 제약을 type으로 옮길수록 증명 의무가 복잡해질 수 있음 |
| Term proof | 증명 객체를 직접 구성 | 함수와 논리의 대응 이해 필요 |
| Tactic proof | goal을 변환하며 증명 구성 | 자동화 실패 시 goal과 보조정리 분석 필요 |

위 설명은 모두 **확인 필요**다. `P → Q`의 증명은 개념적으로 `P`의 증거를 받아 `Q`의 증거를 만드는 함수로 읽는다(Curry–Howard correspondence).

## 검사 아키텍처

```text
사용자 정의·정리·tactic
        ↓
Elaboration: 표기 해석, implicit argument 추론, typeclass 처리
        ↓
구성된 term
        ↓
Kernel: term의 적합성 검사
```

개념적 구분이며 정확한 구현은 **확인 필요**다. Tactic은 증명을 구성하는 수단이고 결과는 검사를 통과해야 한다. 전체 신뢰 범위에는 axiom, 사용한 증명 경로, 실행 환경도 포함해 검토한다.

## 실행과 증명

1. 함수 실행은 관찰한 실행 결과를 보여 준다.
2. Type checking 통과는 작성한 정확성 명세 전체의 증명을 뜻하지 않는다.
3. 정확성 정리를 증명해도 배포 시스템이 그 가정을 만족하는지는 별도 검토한다.
4. 외부 I/O와 다른 언어 연동은 모델 밖의 가정을 추가할 수 있다.

구체적인 Lean 동작은 **확인 필요**다.

## Related Notes

- [[tech/devtools/lean-four-formal-verification/README|학습 진입점]]

## Sources

- 사용자 제공 Lean 4 dossier: 기존 지식 기반 분석이며 출처 URL은 제공되지 않았다.
- 외부 자료를 검색하거나 URL을 열지 않았다. 추정 URL은 기재하지 않는다. 공식 문서와 구현을 통한 후속 검증이 필요하다.
