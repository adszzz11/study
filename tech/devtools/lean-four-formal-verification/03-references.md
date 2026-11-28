---
date: 2026-11-26
tags: [tech]
type: tech-tool-study
status: draft
---

# Lean 4 References와 검증 계획

> **근거 범위:** 제공된 dossier를 재구성한 노트다. 수집 출처가 없고 외부 검증을 수행하지 않았으므로 기술 설명·비교·적용 가능성은 **확인 필요**다. 현재 버전·지원 현황·성능·채택 규모는 판단하지 않는다.

## 현재 자료 상태

제공된 외부 자료와 URL은 없다. 이 노트 모음은 공식 문서나 구현을 확인한 조사 결과가 아니다. 아래 자료명은 후속 확인 대상이며, 확인한 출처나 링크로 취급하지 않는다.

## 후속 확인 대상

| 자료 유형 | 확인할 질문 | 상태 |
|---|---|---|
| Lean 공식 언어 문서 | `Prop`, dependent types, elaboration, kernel의 정확한 의미는? | 미확인 |
| Lean 공식 학습 자료 | term/tactic proof와 induction의 권장 학습 순서는? | 미확인 |
| Lake / elan 문서 | 설치, toolchain 고정, build 절차는? | 미확인 |
| mathlib 문서 | 예제에 필요한 정리·import·의존성은? | 미확인 |
| 신뢰 모델 관련 문서 | axiom, `sorry`, 실행과 증명 경로의 신뢰 범위는? | 미확인 |

## 검증 기록 양식

```text
검증한 주장:
실제로 열어 본 출처 URL:
확인 날짜:
사용 toolchain / library revision:
재현 코드와 실행 결과:
남은 불확실성:
```

출처 URL을 확보하면 관련 주장 옆에 연결하고, 실제 검증 범위에 한해서만 **확인 필요** 표시를 갱신한다.

## Related Notes

- [[tech/devtools/lean-four-formal-verification/README|학습 진입점]]

## Sources

- 사용자 제공 Lean 4 dossier: 기존 지식 기반 분석이며 출처 URL은 제공되지 않았다.
- 외부 자료를 검색하거나 URL을 열지 않았다. 추정 URL은 기재하지 않는다. 공식 문서와 구현을 통한 후속 검증이 필요하다.
