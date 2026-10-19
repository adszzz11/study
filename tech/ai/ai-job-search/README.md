---
date: 2026-10-19
tags: [tech]
type: tech-tool-study
status: draft
---

# AI Job Search

> **한 줄 정의**: AI job search는 이력서·경력·선호·공고 데이터를 Semantic Search와 LLM으로 연결해, 적합한 채용공고 탐색부터 지원서 맞춤화·추적까지 지원하는 인간 검토형 구직 시스템이다.

## Overview

AI job search의 목적은 사람을 대신해 대량 지원하는 것이 아니라, 구직자가 더 적합한 기회를 찾고 근거를 바탕으로 지원 문서를 검토하도록 돕는 것이다. keyword 검색, vector retrieval, ranking, evidence-grounded generation, human approval을 하나의 workflow로 연결한다.

핵심 원칙은 간단하다. **검색·정리·초안은 AI, 사실 확인·최종 지원은 사람**이다. 플랫폼의 자동화 정책과 각 회사의 공식 지원 경로도 함께 지켜야 한다.

## Learning Path

- [ ] [[01-overview|개요]] — 문제, 구성 요소, 안전 원칙 이해
- [ ] [[02-ecosystem|생태계]] — LinkedIn, Indeed, 범용 LLM, ATS, 자체 구축 비교
- [ ] [[03-references|참고자료]] — 제품 정책·Responsible AI·공공 가이드 원문 확인
- [ ] [[04-learning/01-getting-started|시작하기]] — profile과 공고를 구조화하고 retrieval baseline 만들기
- [ ] [[04-learning/02-deep-dive|심화]] — hybrid ranking, explanation, 평가와 approval gate 설계
- [ ] [[05-projects|프로젝트]] — Copilot, Evidence Mapper, Opportunity Hub 구현 과제
- [ ] [[cheatsheet|치트시트]] — 데이터 모델, 지표, 안전 체크 빠른 참조

## When To Use

- 비전형 경력, career transition, 복합 skill 조합에 맞는 공고를 넓게 탐색할 때
- Resume와 JD(Job Description)를 requirement-to-evidence 형태로 비교할 때
- saved search, alert, 중복 제거, application Kanban을 한 흐름으로 관리할 때
- 추천 품질·설명 가능성·privacy를 통제하는 커뮤니티 또는 교육용 서비스를 만들 때

## When Not To Use

- 검증 없이 resume의 skill, 성과, 자격증을 만들어 내는 문서 생성에 사용할 때
- bot으로 지원 form을 제출하거나 플랫폼 정책을 우회하는 대량 자동지원에 사용할 때
- 추천 점수만으로 고용·채용 관련 결정을 자동화할 때
- 민감한 profile 데이터를 보관·공유하는데 동의, 삭제 경로, 접근 제어가 없을 때

## Related Notes

- [[MOCs/Index]]
- [[MOCs/AI]]
- [[tech/ai/model-context-protocol-mcp/README|Model Context Protocol (MCP)]] — 외부 도구와 human approval 경계 설계

## Sources

- https://www.linkedin.com/help/linkedin/answer/a6889044/
- https://www.linkedin.com/help/linkedin/answer/a7120158
- https://www.indeed.com/news/releases/indeed-introduces-new-suite-of-hiring-products-career-scout-talent-scout-premium-sponsored-jobs-and-indeed-connect
- https://www.indeed.com/career-advice/finding-a-job/how-indeed-uses-ai-to-help-job-search
- https://www.indeed.com/help/job-seekers/articles/360028540531-indeed-job-seeker-guidelines?co=US&hl=en
