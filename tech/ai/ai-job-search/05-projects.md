---
date: 2026-10-19
tags: [tech]
type: tech-tool-study
status: draft
---

# AI Job Search — Projects

> [[README|목차로 돌아가기]]

## 1. Personal Job Search Copilot

saved search, 허가된 이메일 alert, 공고 deduplication, match score, Kanban(`application` / `interview` / `offer`), weekly review를 제공한다.

**완료 조건**: 공고마다 source URL·확인 시점·중복 근거가 있고, 지원 상태 변경과 제출은 사용자가 직접 승인한다.

**지표**: stale posting 비율, duplicate rate, alert latency, weekly review 완료율.

## 2. Resume-to-Job Evidence Mapper

JD의 requirement를 Resume 문장과 연결하고, 근거가 없는 requirement는 부족 skill로 표시한다. 수정 후보는 새 사실을 만들지 않고 `diff`와 evidence ID를 함께 보여 준다.

**완료 조건**: 검토자가 모든 생성 문장을 원문 evidence 또는 “근거 없음”으로 추적할 수 있다.

**지표**: evidence citation 정확도, unsupported claim 비율, 검토자 수정률.

## 3. Career Transition Explorer

현재 skill과 인접 역할을 연결해 skill gap, 학습 순서, portfolio project 후보를 제안한다. 유사도 점수와 함께 어떤 skill·경험 때문에 인접하다고 보았는지 설명한다.

**완료 조건**: 희망 지역·근무 형태·work authorization 필터를 통과한 결과만 제시하고, 역할 추천을 고용 가능성 보장처럼 표현하지 않는다.

## 4. University/Community Opportunity Hub

허가된 공고 feed와 회사 career page를 수집해 학생·구성원 profile에 맞춘 추천과 설명 가능한 ranking을 제공한다.

**필수 설계**: source attribution, opt-in profile, data retention/deletion, accessibility, bias audit, 관리자 escalation.

## 5. Recruiting QA Console

운영자가 query, hard filter, ranking feature, explanation, data freshness를 점검하는 콘솔을 만든다.

```text
Test profile + labeled jobs
            │
            ▼
retrieval regression suite → ranking/explanation report
            │                         │
            └──── privacy/bias checks ┘
                                      ▼
                           release approval
```

**완료 조건**: release 전에 retrieval regression, hard-filter 위반, explanation 오류, privacy/bias 점검 결과를 검토할 수 있다.

## Sources

- https://www.nist.gov/itl/ai-risk-management-framework
- https://www.linkedin.com/help/linkedin/answer/a7120158
- https://www.indeed.com/career-advice/finding-a-job/how-indeed-uses-ai-to-help-job-search
