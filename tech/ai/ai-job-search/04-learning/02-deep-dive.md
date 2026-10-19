---
date: 2026-10-19
tags: [tech]
type: tech-tool-study
status: draft
---

# AI Job Search — 심화

> [[../README|목차로 돌아가기]] | [[01-getting-started|이전: 시작하기]]

## 1. Design the Ranking Function

`must-have` 조건은 ranking 이전에 필터링하고, 남은 후보에만 soft score를 적용한다.

```text
final_score = 0.35 * keyword_score
            + 0.35 * vector_score
            + 0.15 * skill_overlap
            + 0.10 * recency_score
            + 0.05 * preference_score
```

위 가중치는 예시일 뿐이다. query별 결과, 직무별 차이, 사용자 피드백으로 조정하며 경쟁도처럼 수집 불완전성이 큰 신호는 과신하지 않는다.

## 2. Make Every Recommendation Inspectable

추천 카드에는 점수뿐 아니라 requirement와 profile evidence를 나란히 보여 준다.

| JD requirement | Profile evidence | 상태 | 사용자 행동 |
|---|---|---|---|
| Go 서비스 경험 | “Go API 운영” resume 문장 | 확인됨 | 원문 링크 열기 |
| Kubernetes | 프로젝트 배포 기록 | 부분 충족 | 범위 정확성 확인 |
| 특정 cloud certification | evidence 없음 | 부족 | 허위 추가 대신 학습 계획 선택 |

이 형식은 모델의 매칭 설명을 검증 가능한 주장으로 제한하고, skill gap을 지원 배제 사유가 아니라 학습·보완 항목으로 다루게 한다.

## 3. Grounded Document Generation

LLM prompt에는 허용된 evidence만 제공하고 다음 규칙을 둔다.

```text
- evidence에 없는 회사, 기간, 성과 수치, 자격증, skill을 만들지 않는다.
- 각 문장은 대응하는 evidence ID를 반환한다.
- 충족하지 않는 requirement는 "근거 없음"으로 표시한다.
- 출력은 원본 Resume와 비교 가능한 diff 초안으로 낸다.
```

생성 결과는 채용 담당자에게 보내기 전 사람이 문장, 수치, 회사명, URL, 개인정보 노출을 확인한다.

## 4. Evaluate Quality and Risk

| 영역 | 지표 또는 질문 |
|---|---|
| Retrieval | Recall@K, Precision@K, hard-filter 위반률 |
| Explanation | evidence citation 정확도, 근거 누락률, 검토자 동의율 |
| Generation | 사실 오류율, 수정률, unsupported claim 비율 |
| Operations | 중복 공고율, stale posting 비율, alert latency |
| Fairness/privacy | 집단별 추천 격차, 민감정보 노출, 삭제 요청 처리 시간 |

NIST AI RMF가 제시하는 validity/reliability, transparency, explainability, privacy, fairness 관점으로 risk register를 유지한다. 고용 관련 시스템은 접근성과 차별 위험도 함께 검토한다.

## 5. Approval Gate

```text
추천/초안 생성 → evidence 검토 → 공고 유효성 확인
      → 개인정보·문서 확인 → 사용자 승인 → 공식 지원 경로
```

approval gate는 우회 가능한 UI가 아니라 write action과 분리된 권한 경계여야 한다. third-party bot을 통한 자동 지원이 금지된 서비스에서는 제출 자동화를 연결하지 않는다.

## Sources

- https://www.linkedin.com/help/linkedin/answer/a5338456
- https://www.nist.gov/itl/ai-risk-management-framework/ai-risk-management-framework-faqs
- https://www.eeoc.gov/sites/default/files/2022-07/ADA%20and%20AI%20Worker%20Tip%20Sheet.pdf
- https://www.indeed.com/help/job-seekers/articles/360028540531-indeed-job-seeker-guidelines?co=US&hl=en
