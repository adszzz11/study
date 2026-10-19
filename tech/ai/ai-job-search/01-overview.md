---
date: 2026-10-19
tags: [tech]
type: tech-tool-study
status: draft
---

# AI Job Search — Overview

> [[README|목차로 돌아가기]]

## What

AI job search는 구직자의 Resume, profile, 선호 조건과 채용공고를 구조화한 뒤, keyword와 의미 기반 검색으로 매칭하는 workflow다. LLM은 공고 요약, requirement 추출, 맞춤 문서의 **검토용 초안**과 면접 준비를 보조한다.

## Why

직무명·키워드만으로 검색하면 career transition, 비전형 경력, 복수 기술의 조합을 놓치기 쉽다. 자연어 의도와 skill 유사성을 함께 쓰면 탐색 폭을 넓힐 수 있지만, 관련성이 곧 지원 자격이나 합격 가능성을 뜻하지는 않는다.

LinkedIn은 AI-powered job search에서 자연어 검색 의도를 공고와 매칭한다고 설명하고, Job Match는 profile 또는 resume와 공고의 required·preferred qualification을 비교한다. Indeed의 Career Scout는 대화형 탐색, resume 개선, 지원 관리 흐름을 제시한다.

## Core Characteristics

| 특징 | 역할 | 반드시 지킬 제약 |
|---|---|---|
| Natural-language retrieval | 자연어 의도를 직무·skill·경험 수준 후보로 확장 | location, visa, employment type은 명시적 filter로 확인 |
| Profile-first matching | Resume와 선호를 정규화해 비교 | 원문과 evidence link를 보존 |
| Hybrid ranking | BM25/keyword와 vector score를 결합 | 점수 근거와 최신성을 함께 표시 |
| Evidence-grounded generation | JD 요구사항별로 경력 근거를 연결 | 입력에 없는 성과·skill·수치를 생성하지 않음 |
| Human-in-the-loop | 추천과 초안을 사람이 승인 | 제출 전 공고 유효성·개인정보·문서 확인 |

## Reference Architecture

```text
Resume / Profile / Preferences
            │
            ▼
   Profile normalization + skill taxonomy
            │                         Job board / company careers / alerts
            └──────────────┬───────────────────────────────┘
                           ▼
             Hybrid retrieval (keyword + vector)
                           ▼
       Match scoring + evidence / skill-gap explanation
                           ▼
LLM copilot: resume bullet · cover letter · interview prep
                           ▼
Human approval → official application → CRM/analytics
```

## Trust Boundaries

- **Hard filter**: 지역, work authorization/visa, seniority, 고용 형태처럼 틀리면 안 되는 조건이다.
- **Soft ranking**: 기술, 도메인, 성과, 유사 역할, 공고 최신성·경쟁도는 점수화하되 사용자가 조정할 수 있어야 한다.
- **Generation**: LLM은 evidence store 밖의 사실을 추가할 수 없고, 초안과 원문 차이를 검토 가능하게 제공해야 한다.
- **Privacy and fairness**: 민감정보를 최소화하고, 보관기간·삭제 요청·접근 권한을 정의하며, ranking의 불리한 편향을 측정한다.

## Sources

- https://www.linkedin.com/help/linkedin/answer/a6889044/
- https://www.linkedin.com/help/linkedin/answer/a7120158
- https://www.linkedin.com/help/linkedin/answer/a5338456
- https://www.nist.gov/itl/ai-risk-management-framework/ai-risk-management-framework-faqs
