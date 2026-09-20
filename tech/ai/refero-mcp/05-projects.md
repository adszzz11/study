---
date: 2026-09-20
tags: [tech]
type: tech-tool-study
status: draft
---

# Refero MCP — Projects

> [[04-learning/02-deep-dive|이전: Deep Dive]] · [[README|목차]] · [[cheatsheet|다음: Cheatsheet]]

## 1. SaaS Onboarding Redesign

competitor onboarding flow를 조사해 activation milestone, permission/request state, error recovery를 설계한다.

- Deliverable: flow coverage matrix, reference lock, state별 wireframe, QA screenshots
- Success: happy path뿐 아니라 denied permission·retry·completion handoff가 정의됨

## 2. Design-system Seed

marketing-site style을 조사해 typography scale, color role, spacing/radius/elevation token 초안을 만든다.

- Deliverable: semantic token proposal과 근거 reference
- Guardrail: raw 값을 복사하지 않고 자사 brand token, contrast, existing components로 재검토

## 3. Product UI Audit

“우리 empty state가 generic한가?”라는 질문으로 동종 product screen을 비교한다.

- Deliverable: hierarchy, CTA, helper copy, recoverability에 대한 before/after recommendation
- Success: aesthetics 의견이 아니라 user goal과 관찰된 trait로 제안이 설명됨

## 4. AI Coding Agent Guardrail

다음 ritual을 PRD와 implementation 사이에 둔다.

```text
PRD → Refero research note → reference lock → implementation → visual QA
```

- Deliverable: brief template, research report template, visual review checklist
- Guardrail: agent가 search result를 product copy 또는 final design으로 자동 승격하지 않음

## 5. Benchmark Research Assistant

PM/Designer가 자연어로 screen·flow 사례를 찾고, agent가 evidence와 implementation recommendation을 분리해 report를 만든다.

| Report section | 포함할 것 |
|---|---|
| Evidence | reference와 관찰 가능한 trait |
| Inference | 해당 trait가 brief에 맞는 이유 |
| Recommendation | 자사 token·component에 맞춘 제안 |
| Open questions | brand, legal, accessibility, platform 확인 항목 |

## Sources

- https://refero.design/mcp
- https://github.com/referodesign/refero_skill/blob/master/skills/refero-design/SKILL.md
