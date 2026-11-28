---
date: 2026-11-28
tags: [tech]
type: tech-tool-study
status: draft
---

# Projects: 검토 가능한 Onboarding 설계

아래는 학습용 설계 과제이며 실제 Convex 수정이나 검증 완료를 뜻하지 않는다. Dummy 데이터와 로컬 fixture만 사용한다.

## 1. 데이터 전송 미리보기

- **산출물:** 목적·수신처·전송 필드를 보여주는 안내 초안.
- **설계:** 전송 전에 payload를 미리 보여주고, 사용자가 동의하지 않아도 기본 로컬 runbook을 제공한다.
- **완료 기준:** `idea`와 `template`을 명시하고, 서버 보관 정책은 미확인으로 표시한다. 동의 전에는 요청하지 않는 흐름을 문서화한다.

## 2. Script manifest와 검토 기록

- **산출물:** 로컬 dummy script, 기대 SHA-256을 담은 manifest, 검토 기록.
- **설계:** 배포물에 코드를 포함하거나 신뢰한 버전에 digest를 묶는다. 변경된 bytes는 실행 대상으로 승인하지 않는다.
- **완료 기준:** fixture 한 글자 변경으로 digest가 달라지는 것을 확인한다. Hash 일치가 코드 안전성까지 보증하지 않는다고 적는다.

```text
승인된 배포물/manifest
 → 로컬 fixture bytes와 digest 비교
 → 내용·필요 권한 검토
 → 불일치 또는 미승인: 중단
```

## 3. Harness 친화적인 실행 계획

- **산출물:** 다운로드부터 실행까지 한눈에 보이는 계획과 거절 처리 흐름.
- **설계:** 각 tool call의 출처와 최종 실행 의도를 연결한다. 거절 시 call 모양을 바꾸는 재시도를 제거한다.
- **완료 기준:** 리뷰어가 전체 원격 실행 효과와 요구 권한을 파악하고, 수동 대안 또는 중단 경로를 찾을 수 있다.

## 리뷰 질문

- 사용자가 무엇을 선택했고 어떤 데이터가 나가는가?
- 검토한 코드와 실행 대상이 같은지 확인할 수 있는가?
- 정책 거절을 존중하는가?
- 확인된 사실과 설계 제안을 구분했는가?

[[tech/devtools/convex-skill-trust-boundary/cheatsheet|검토 Cheatsheet]] · [[tech/devtools/convex-skill-trust-boundary/README|학습 경로]]

## Sources

- https://github.com/convex/convex-backend-skill/issues/64 — 문제와 대안의 근거; 과제는 학습용 재구성
