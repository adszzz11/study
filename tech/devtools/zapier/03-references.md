---
date: 2026-08-24
tags: [tech]
type: tech-tool-study
status: draft
---

# Zapier — References

> [[02-ecosystem|이전: Ecosystem]] · [[README|목차로 돌아가기]] · [[04-learning/01-getting-started|다음: Getting Started]]

## 공식 입문 문서

- [What is Zapier?](https://help.zapier.com/hc/en-us/articles/37518970271245-What-is-Zapier) — 제품 범위와 핵심 개념
- [What is a Zap?](https://help.zapier.com/hc/en-us/articles/8496309697421-What-is-a-Zap) — Trigger, Action, Zap 구조
- [How Zap triggers work](https://help.zapier.com/hc/en-us/articles/8496244568589-How-Zap-triggers-work) — instant/polling과 interval
- [Introduction to apps](https://help.zapier.com/hc/en-us/articles/21996626006541-Introduction-to-apps-on-Zapier) — app, event, account 연결
- [App Directory](https://zapier.com/apps) — connector와 지원 action 확인

## Logic, data, human interaction

- [Create forms in Zapier Forms](https://help.zapier.com/hc/en-us/articles/15927500577037-Create-forms-in-Zapier-Forms)
- [Create a canvas](https://help.zapier.com/hc/en-us/articles/19880280846221-Create-a-canvas-to-visualize-your-automated-system)
- [Zapier Tables](https://help.zapier.com/hc/en-us/categories/9505357429389-Zapier-Tables)
- [Human in the Loop](https://help.zapier.com/hc/en-us/articles/38737614362005-Add-a-human-review-step-to-your-Zap-with-Human-in-the-Loop)

## Developer와 AI

- [Developer Platform CLI tutorial](https://docs.zapier.com/integrations/quickstart/cli-tutorial)
- [Zapier SDK documentation](https://docs.zapier.com/sdk)
- [Zapier MCP guide](https://zapier.com/blog/zapier-mcp-guide/)
- [MCP vs SDK vs CLI](https://zapier.com/blog/zapier-mcp-vs-sdk/)
- [Data safety with Zapier Agents](https://help.zapier.com/hc/en-us/articles/24687564925453-Data-safety-with-Zapier-Agents)
- [AI Guardrails](https://help.zapier.com/hc/en-us/articles/38205001625101-Use-AI-Guardrails-by-Zapier)

## Pricing과 운영

- [Zapier task usage rates](https://zapier.com/pricing/rates) — step별 task 계산
- [Zapier pricing](https://zapier.com/pricing) — plan과 entitlement
- [Zap History](https://help.zapier.com/hc/en-us/articles/8496291146637-View-and-manage-your-Zap-history) — 실행 확인과 replay

## 읽는 순서

| 단계 | 자료 | 확인할 질문 |
|---|---|---|
| 1 | What is Zapier / What is a Zap | 무엇을 Trigger와 Action으로 모델링하는가? |
| 2 | Trigger 동작 | webhook인가 polling인가? latency와 dedup은? |
| 3 | App Directory | 필요한 operation과 field가 실제로 제공되는가? |
| 4 | Task rates | 정상·retry·fan-out에서 task가 몇 개인가? |
| 5 | History / Agents safety | 실패와 비결정성을 어떻게 관찰·통제하는가? |
| 6 | CLI / SDK / MCP | no-code step을 넘어 어떤 확장 경로가 필요한가? |

## 조사 메모

- 조사 기준일: **2026-08-24**
- 가격, app/action 수, Beta 표기, plan entitlement는 변동 가능하다.
- 실제 도입 전에는 App Directory의 이름만 보지 말고 필요한 Trigger/Action, field, authentication scope를 test account로 확인한다.

## Sources

- [Zapier Help Center](https://help.zapier.com/)
- [Zapier Developer Platform](https://docs.zapier.com/platform/home)
- [Zapier SDK](https://docs.zapier.com/sdk)
- [Zapier pricing](https://zapier.com/pricing)

