---
date: 2026-10-19
tags: [tech]
type: tech-tool-study
status: draft
---

# AI Job Search — Ecosystem

> [[README|목차로 돌아가기]]

## Options at a Glance

| 선택지 | 강점 | 적합한 경우 | 주의점 |
|---|---|---|---|
| LinkedIn AI-powered job search | professional graph, 자연어 검색, Job Match | 네트워크·white-collar 직무 탐색 | profile 완성도와 플랫폼 내 공고 범위에 영향 |
| Indeed Career Scout | 대화형 career guidance, resume 개선, 지원 추적 | 폭넓은 공고 탐색과 구직 workflow | 기능·국가별 제공 범위 확인 필요 |
| ChatGPT agent / 범용 LLM | 공고 조사, 비교표, 맞춤 문서 초안, research 자동화 | 개인화된 job-search copilot | 로그인·지원 제출은 사람 승인과 서비스 약관 준수 필요 |
| ATS/회사 Careers 직접 지원 | 원본 공고·최신 상태·정식 지원 경로 | 선호 회사가 명확할 때 | 사이트별 form·정책이 달라 통합이 어려움 |
| 자체 구축 Job Search Copilot | 데이터 모델·ranking·privacy 통제 | 커뮤니티, 대학, recruiting product | 공고 수집 권한, 평가 데이터, 법무·운영 비용 필요 |

## Selection Guide

- **지금 구직 중인 개인**: LinkedIn·Indeed로 discovery를 시작하고, 관심 회사는 공식 career site에서 공고 상태와 지원 경로를 재확인한다.
- **문서 작업이 병목인 개인**: 범용 LLM으로 requirement-to-evidence 표와 문서 diff를 만들되, 모든 수치와 경력 사실을 원문에서 확인한다.
- **조직/서비스 제작자**: search quality뿐 아니라 데이터 권한, deletion workflow, bias 평가, human escalation을 제품 요구사항으로 둔다.

## Implementation Pattern

LinkedIn Recruiter의 AI Search처럼 LLM은 자유형 요청을 structured filter와 query로 변환하고, 기존 retrieval 시스템이 후보를 반환하는 패턴이 유용하다. LLM이 공고 데이터의 진실성이나 지원 자격을 단독 판단하게 하지 않는다.

```text
User intent → LLM query planner → filters + search terms
                                      │
                         keyword / vector retrieval
                                      │
                         rank + evidence explanation
                                      │
                              user review
```

## Sources

- https://www.linkedin.com/help/linkedin/answer/a6889044/
- https://www.linkedin.com/help/linkedin/answer/a7120158
- https://www.linkedin.com/help/recruiter/answer/a1673877
- https://www.indeed.com/news/releases/indeed-introduces-new-suite-of-hiring-products-career-scout-talent-scout-premium-sponsored-jobs-and-indeed-connect
- https://help.openai.com/en/articles/11794368-chatgpt-agent-release-notes
