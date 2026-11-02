---
date: 2026-11-03
tags: [tech]
type: tech-tool-study
status: draft
---

# Atticus deep dive

## Version-control 재검증

새 문서 버전을 올린 뒤 전체를 다시 검토하지 말고, 변경된 statement를 중심으로 queue를 만든다. 기존 evidence를 가져올 수 있어도 다음은 반드시 다시 판단한다.

- 변경이 의미·수치·scope를 바꾸었는가?
- evidence의 reporting period와 entity가 새 문장에 맞는가?
- 기존 verified status가 여전히 유효한가?

`변경 탐지 → 영향 claim 분류 → evidence 재사용 여부 판단 → reviewer 승인 → report`의 sequence를 release checklist에 넣는다.

## Glide pilot 설계

Glide의 value는 자동 승인률이 아니라 reviewer의 유효 작업을 얼마나 줄이는지로 측정한다. 이미 검증 완료된 문서를 gold set으로 사용하고, suggestion과 사람이 확정한 결과를 비교한다.

| KPI | 확인 질문 |
|---|---|
| Annotation precision / recall | 중요한 claim을 정확히 잡았으며 누락은 얼마나 되는가? |
| Evidence suggestion acceptance | 후보 evidence가 실제로 채택되는 비율은 얼마인가? |
| False positive | 불필요한 검토 queue를 얼마나 만드는가? |
| Review time | statement당 검토 시간이 기준선보다 줄었는가? |
| Approval trace | suggestion·수정·최종 승인자가 구분되어 남는가? |

## 통제와 보안 checklist

- workspace activation과 최소 권한을 적용한다.
- 민감한 prospectus·non-public information의 data residency와 계약상 처리 조건을 확인한다.
- AI/search output은 evidence 후보이지 사실의 증명이 아님을 reviewer 교육에 명시한다.
- pilot 종료 시 미해결 claim, suggestion error, exception disposition을 보존한다.

프로젝트 단위 적용은 [[tech/ai/atticus-document-verification/05-projects|Projects]], 용어 요약은 [[tech/ai/atticus-document-verification/cheatsheet|Cheatsheet]]를 참고한다.

## Sources

- https://www.atticus.tech/glide
- https://www.atticus.tech/blog/atticus-launches-glide-agentic-ai-for-verifying-annual-reports-and-prospectuses
- https://www.atticus.tech/general-terms-uk-eu
