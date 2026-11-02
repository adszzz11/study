---
date: 2026-11-03
tags: [tech]
type: tech-tool-study
status: draft
---

# Atticus 시작하기

## 목표

도구를 열기 전에 “무엇을 검증해야 하는가”를 정의한다. 작은 annual-report section 또는 investor presentation 10쪽 내외를 pilot 범위로 잡으면 owner·evidence·versioning 흐름을 빠르게 검증할 수 있다.

## 1. Materiality 기준 만들기

다음 중 하나에 해당하면 verification unit 후보로 분류한다.

- 재무 수치, KPI, forward-looking statement
- 법적·규제상 정확성이 필요한 서술
- ESG metric과 그 산출 방식
- 투자자 의사결정에 영향을 줄 수 있는 claim

단순 문체 수정이나 반복 문구는 별도 교정 흐름으로 분리한다.

## 2. Verification matrix 설계

| 필드 | 예시 |
|---|---|
| Statement | “FY2025 매출은 전년 대비 12% 증가했다.” |
| Owner | Finance FP&A |
| Reviewer | Controller / Legal |
| Source-of-truth | 승인된 ERP export, board pack |
| Evidence | 매출 reconciliation workbook, signed report |
| Due date | 2026-11-14 |
| Status | Not started → In review → Verified / Needs revision |

이 matrix의 행을 Atticus의 annotation과 assignment로 옮긴다는 관점으로 시작한다.

## 3. 첫 검증 cycle

1. 대상 PDF와 근거 문서를 준비하고 접근 권한을 확인한다.
2. claim을 boxing 또는 highlighting하고 owner·reviewer를 배정한다.
3. owner가 evidence를 연결하고 설명을 남긴다.
4. reviewer가 evidence의 적합성과 문장 일치를 확인해 상태를 결정한다.
5. release 전 미해결·기한 초과·evidence 누락 항목을 report로 점검한다.

다음 단계에서는 [[tech/ai/atticus-document-verification/04-learning/02-deep-dive|Deep Dive]]로 versioning과 Glide 평가를 진행한다.

## Sources

- https://www.atticus.tech/au/verifying
- https://www.atticus.tech/frequently-asked-questions
