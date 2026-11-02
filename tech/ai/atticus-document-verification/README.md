---
date: 2026-11-03
tags: [tech]
type: tech-tool-study
status: draft
---

# Atticus — Agent-Assisted Critical Document Verification Platform

> **한 줄 정의**: Atticus는 상장사와 로펌이 critical document의 주장·수치·문장을 증빙자료와 연결해 검증하고 감사 추적을 남기도록 돕는 SaaS 플랫폼이다.

## Overview

Atticus는 annual report, prospectus, investor presentation처럼 오류 비용이 큰 문서의 **최종 검증**에 초점을 둔다. 문서 속 statement를 verification unit으로 만들고, 담당자·evidence·승인 상태·변경 이력을 한 화면에서 연결한다. 2026년 공개된 Atticus Glide는 annotation, materiality, evidence 후보 탐색을 first pass로 보조하지만 최종 판단과 승인은 사람이 수행한다.

- 데이터 흐름: `document → statement → owner → evidence → verification status → audit trail`
- 주요 사용 부서: Legal, Finance, Investor Relations, ESG, 외부 counsel·auditor
- 자세한 맥락: [[tech/ai/atticus-document-verification/01-overview|Overview]]

## Learning Path

- [ ] [[tech/ai/atticus-document-verification/01-overview|Overview]] — 문제와 핵심 데이터 모델을 이해한다.
- [ ] [[tech/ai/atticus-document-verification/04-learning/01-getting-started|시작하기]] — materiality 기준과 verification matrix를 설계한다.
- [ ] [[tech/ai/atticus-document-verification/02-ecosystem|Ecosystem]] — Workiva, filing provider, 수작업 흐름과 역할을 비교한다.
- [ ] [[tech/ai/atticus-document-verification/04-learning/02-deep-dive|Deep Dive]] — versioning, Glide pilot, 통제 설계를 검토한다.
- [ ] [[tech/ai/atticus-document-verification/05-projects|Projects]] — 공시 검증 workspace 또는 pilot을 설계한다.
- [ ] [[tech/ai/atticus-document-verification/03-references|References]] — 공식 문서와 사례를 확인한다.
- [ ] [[tech/ai/atticus-document-verification/cheatsheet|Cheatsheet]] — 실무 용어와 release gate를 빠르게 복습한다.

## When To Use

- 여러 팀·외부 자문사가 공시 문서의 사실·수치·서술을 함께 검증할 때
- 주장별 evidence와 reviewer의 책임, 승인 이력을 audit-ready하게 남겨야 할 때
- 새 문서 버전에서 변경된 statement만 우선 재검토하고 싶을 때
- Glide의 suggestion을 사람의 검토 절차 안에서 pilot하고 싶을 때

## When Not To Use

- SEC/EDGAR 제출 파일 생성, XBRL tagging, 배포 자체가 주된 문제일 때는 filing production provider를 우선 검토한다.
- 공동 작성, linked data, ESG/GRC를 포괄하는 reporting platform이 필요할 때는 Workiva 같은 broader suite를 비교한다.
- 비중요 문서 한두 건의 단순 교정처럼 role-based evidence trail의 가치가 낮을 때는 도입 비용이 과할 수 있다.

## Related Notes

- [[MOCs/Index]]
- [[MOCs/AI]]
- [[tech/ai/docling/README|Docling]]

## Sources

- https://www.atticus.tech/
- https://www.atticus.tech/au/verifying
- https://www.atticus.tech/glide
- https://www.atticus.tech/blog/atticus-launches-glide-agentic-ai-for-verifying-annual-reports-and-prospectuses
- https://www.atticus.tech/frequently-asked-questions
