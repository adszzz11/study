---
date: 2026-09-29
tags: [tech]
type: tech-tool-study
status: draft
---

# 이력서 작성 Skills

> **한 줄 정의**: 이력서 작성 Skill은 후보자의 사실 기반 경력 데이터와 채용공고를 분석해, ATS-friendly·직무 맞춤형 Resume/CV·Cover Letter를 반복 가능하게 생성·검증하는 Agent Skill 워크플로다.

## Overview

좋은 이력서 작성 Skill은 문장을 그럴듯하게 만드는 도구가 아니라 품질 시스템이다. `candidate source → JD 분석 → evidence mapping → tailoring → QA → rendering` 순서를 강제해 공고별 결과물과 검토 근거를 남긴다.

```text
Candidate fact base + Job Description
             ↓
 requirement / keyword / evidence map
             ↓
 Resume · Cover Letter · Interview STAR
             ↓
 truth · ATS · readability · privacy QA
             ↓
      render → applicant approval
```

AI는 초안 파트너이고, 사실 확인과 최종 제출 결정은 지원자가 맡는다. 숫자, 직책, 기간, 회사명, 기술은 source에 있는 것만 쓴다.

## Learning Path

- [ ] [[01-overview|1. Overview — What, Why, architecture]]
- [ ] [[02-ecosystem|2. Ecosystem — 대안과 선택 기준]]
- [ ] [[03-references|3. References — 공식 문서와 공개 구현]]
- [ ] [[04-learning/01-getting-started|4. Getting Started — fact base부터 첫 tailored draft까지]]
- [ ] [[04-learning/02-deep-dive|5. Deep Dive — evidence gate, QA, rendering]]
- [ ] [[05-projects|6. Projects — 재현 가능한 지원 workflow]]
- [ ] [[cheatsheet|7. Cheatsheet — 규칙, schema, 검토 목록]]

## When To Use

- 여러 공고에 지원하며 동일 경력의 tailored version을 추적할 때
- career coach나 팀이 같은 사실성·privacy 기준을 재사용할 때
- Markdown/YAML과 Git diff로 source와 PDF 산출물을 분리할 때
- ATS plain-text version과 사람이 읽는 styled version을 함께 점검할 때

## When Not To Use

- 지원자가 경력 사실·성과를 검토하고 승인할 수 없을 때
- 민감 개인정보를 외부 LLM에 입력해야만 workflow가 성립할 때
- 단 한 번의 비공식 초안만 급히 필요하고 버전 관리·검증 비용이 과도할 때
- ATS score를 객관적 채용 가능성 또는 공식 benchmark처럼 해석하려 할 때

## Related Notes

- [[MOCs/Index]]
- [[MOCs/AI]]
- [[tech/ai/agent-garden|Agent Garden]]

## Sources

- https://learn.chatgpt.com/docs/build-skills
- https://developers.openai.com/api/docs/guides/tools-skills
- https://academy.openai.com/public/resources/helping-job-seekers-with-chatgpt-2025-12-03
- https://docs.rendercv.com/user_guide/index.html
