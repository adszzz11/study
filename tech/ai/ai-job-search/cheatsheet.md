---
date: 2026-10-19
tags: [tech]
type: tech-tool-study
status: draft
---

# AI Job Search — Cheatsheet

> [[README|목차로 돌아가기]]

## Workflow

```text
Profile facts → normalize → retrieve → rank → explain
                                  │              │
                                  └── hard filters┘
                                                ↓
                                     draft → human approval → official apply
```

## Minimum Data Model

| 객체 | 최소 필드 |
|---|---|
| Profile | experience, skills, achievements, preferences, evidence IDs |
| Job | title, company, source URL, checked_at, location, type, requirements |
| Match | job ID, profile ID, filter result, component scores, evidence links |
| Application | status, official URL, user approval time, next action |

## Retrieval Rules

- `hard filter`: location, work authorization/visa, seniority, employment type
- `keyword`: 직무명, 기술명, 약어, 회사명
- `vector`: 유사 경험, career transition, 표현이 다른 skill
- `hybrid`: 같은 평가 세트에서 Recall@K와 수동 품질을 비교
- `freshness`: `checked_at`이 오래된 공고는 재확인 또는 낮은 우선순위 처리

## Generation Guardrails

- 입력 evidence 밖의 skill, 기간, 성과 수치, 자격증을 생성하지 않는다.
- requirement마다 evidence ID 또는 `근거 없음`을 반환한다.
- Resume/cover letter는 diff 초안으로 제공한다.
- 사람은 회사명, 날짜, 수치, 개인정보, 공고 상태를 확인한다.

## Pre-application Checklist

- [ ] 공식 URL에서 공고가 아직 유효한지 확인했다.
- [ ] location, work authorization, employment type을 확인했다.
- [ ] 생성 문장마다 Resume 또는 portfolio 근거가 있다.
- [ ] 민감한 개인정보가 불필요하게 문서·로그에 포함되지 않았다.
- [ ] 플랫폼 정책을 준수하며, 사용자가 직접 최종 제출한다.

## Metrics

| 목표 | 지표 |
|---|---|
| 발견 품질 | Recall@K, Precision@K, saved-job rate |
| 설명 품질 | citation accuracy, reviewer agreement |
| 문서 안전성 | unsupported claim rate, reviewer edit rate |
| 운영 품질 | duplicate rate, stale posting rate, alert latency |
| 신뢰성 | hard-filter 위반, privacy incident, deletion SLA |

## Sources

- https://www.indeed.com/help/job-seekers/articles/360028540531-indeed-job-seeker-guidelines?co=US&hl=en
- https://www.nist.gov/itl/ai-risk-management-framework/ai-risk-management-framework-faqs
